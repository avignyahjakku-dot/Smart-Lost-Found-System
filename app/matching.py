"""
Smart Matching Engine
=====================
CampusFind Heuristic Multi-Factor Similarity System

Evaluates candidate matches between Lost and Found reports using:
1. Category compatibility (Weight: 30%)
2. Textual overlap on Title & Description (Weight: 35%)
3. Campus Location proximity (Weight: 20%)
4. Chronological sequence plausibility (Weight: 15%)

Produces an explainable score between 0 and 100%, with confidence tiers:
- High (>= 75%)
- Moderate (50% - 74%)
- Plausible (30% - 49%)
"""

import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
    'by', 'my', 'is', 'it', 'was', 'i', 'lost', 'found', 'please', 'help',
    'item', 'items', 'this', 'that', 'there', 'from', 'near', 'around', 'none', 'null'
}

def clean_tokens(text: str) -> set:
    """Normalize and tokenize text into informative word tokens."""
    if not text:
        return set()
    words = re.findall(r'\b[a-zA-Z0-9]{2,}\b', text.lower())
    return {w for w in words if w not in STOP_WORDS}

def calculate_jaccard_similarity(tokens_a: set, tokens_b: set) -> float:
    """Compute Jaccard similarity between two sets of tokens."""
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = len(tokens_a.intersection(tokens_b))
    union = len(tokens_a.union(tokens_b))
    return intersection / union if union > 0 else 0.0

def evaluate_match(lost_item: Dict[str, Any], found_item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare a single lost item against a single found item.
    Returns an evaluation dictionary with score, tier, and transparent factor breakdown.
    """
    breakdown = {}

    # --- 1. Category Matching (Weight: 30) ---
    lost_cat = (lost_item.get('category') or '').strip().lower()
    found_cat = (found_item.get('category') or '').strip().lower()

    if lost_cat and found_cat:
        if lost_cat == found_cat:
            cat_score = 30.0
            cat_reason = f"Exact category match ({lost_item.get('category')})"
        else:
            cat_score = 0.0
            cat_reason = f"Category mismatch ({lost_item.get('category')} vs {found_item.get('category')})"
    else:
        cat_score = 10.0
        cat_reason = "Unspecified category"

    breakdown['category'] = {
        'weight': 30.0,
        'earned': cat_score,
        'reason': cat_reason
    }

    # --- 2. Title and Description Text Overlap (Weight: 35) ---
    lost_title = lost_item.get('title') or ''
    lost_desc = lost_item.get('description') or ''
    found_title = found_item.get('title') or ''
    found_desc = found_item.get('description') or ''

    lost_text = f"{lost_title} {lost_desc}"
    found_text = f"{found_title} {found_desc}"

    lost_tokens = clean_tokens(lost_text)
    found_tokens = clean_tokens(found_text)

    overlap = lost_tokens.intersection(found_tokens)
    jaccard = calculate_jaccard_similarity(lost_tokens, found_tokens)

    # Title-specific substring boost
    lost_title_tokens = clean_tokens(lost_title)
    found_title_tokens = clean_tokens(found_title)
    title_overlap = lost_title_tokens.intersection(found_title_tokens)

    text_score = min(35.0, (jaccard * 25.0) + (len(title_overlap) * 5.0) + (len(overlap) * 1.5))
    if overlap:
        matched_sample = ', '.join(sorted(list(overlap))[:5])
        text_reason = f"Shared keywords: [{matched_sample}]"
    else:
        text_reason = "No significant textual overlap found"

    breakdown['text'] = {
        'weight': 35.0,
        'earned': round(text_score, 1),
        'reason': text_reason
    }

    # --- 3. Location Proximity (Weight: 20) ---
    lost_loc = (lost_item.get('location') or '').strip().lower()
    found_loc = (found_item.get('location') or '').strip().lower()

    lost_loc_tokens = clean_tokens(lost_loc)
    found_loc_tokens = clean_tokens(found_loc)
    loc_overlap = lost_loc_tokens.intersection(found_loc_tokens)

    if lost_loc == found_loc and lost_loc != '':
        loc_score = 20.0
        loc_reason = f"Exact campus location match ({lost_item.get('location')})"
    elif loc_overlap:
        loc_score = 15.0
        loc_reason = f"Shared campus landmark: [{', '.join(loc_overlap)}]"
    elif any(tok in found_loc for tok in lost_loc_tokens) or any(tok in lost_loc for tok in found_loc_tokens):
        loc_score = 10.0
        loc_reason = "Partial landmark/zone similarity"
    else:
        loc_score = 3.0
        loc_reason = f"Different campus zones reported ({lost_item.get('location')} vs {found_item.get('location')})"

    breakdown['location'] = {
        'weight': 20.0,
        'earned': round(loc_score, 1),
        'reason': loc_reason
    }

    # --- 4. Date Chronological Plausibility (Weight: 15) ---
    lost_date_str = str(lost_item.get('item_date', ''))[:10]
    found_date_str = str(found_item.get('item_date', ''))[:10]

    date_score = 8.0
    date_reason = "Dates could not be chronologically compared"

    try:
        lost_dt = datetime.strptime(lost_date_str, "%Y-%m-%d").date()
        found_dt = datetime.strptime(found_date_str, "%Y-%m-%d").date()
        delta_days = (found_dt - lost_dt).days

        if delta_days >= 0:
            # Chronologically consistent: lost first, then found
            if delta_days == 0:
                date_score = 15.0
                date_reason = "Identical calendar day"
            elif delta_days <= 3:
                date_score = 14.0
                date_reason = f"Found within {delta_days} day(s) of reported loss"
            elif delta_days <= 14:
                date_score = 11.0
                date_reason = f"Found within {delta_days} days of reported loss"
            elif delta_days <= 30:
                date_score = 8.0
                date_reason = f"Found within a month ({delta_days} days)"
            else:
                date_score = 4.0
                date_reason = f"Long time gap ({delta_days} days)"
        else:
            # Item was reported found before it was reported lost!
            if abs(delta_days) == 1:
                # Slight human reporting inaccuracy tolerance (1 day difference)
                date_score = 5.0
                date_reason = "Found date slightly precedes lost date (~1 day reporting skew)"
            else:
                date_score = 0.0
                date_reason = f"Chronologically implausible (found {abs(delta_days)} days before reported lost date)"
    except Exception:
        pass

    breakdown['date'] = {
        'weight': 15.0,
        'earned': round(date_score, 1),
        'reason': date_reason
    }

    # Compute Total Score
    total_score = round(cat_score + text_score + loc_score + date_score, 1)

    # Classify confidence tier
    if total_score >= 75.0:
        tier = "High"
        summary = "Strong candidate match. Primary attributes and chronological timeline align closely."
    elif total_score >= 50.0:
        tier = "Moderate"
        summary = "Plausible candidate match. Multiple key attributes correspond."
    elif total_score >= 30.0:
        tier = "Plausible"
        summary = "Weak / speculative match. Verify identifying marks before claiming."
    else:
        tier = "Low"
        summary = "Unlikely to be the same item based on significant attribute divergence."

    return {
        'lost_item_id': lost_item.get('id'),
        'found_item_id': found_item.get('id'),
        'total_score': total_score,
        'tier': tier,
        'summary': summary,
        'breakdown': breakdown
    }

def find_matches_for_item(item: Dict[str, Any], candidate_items: List[Dict[str, Any]], min_score: float = 30.0) -> List[Dict[str, Any]]:
    """
    Search candidate items of opposite type (e.g. found items for a lost item)
    and return ranked matches exceeding the minimum score threshold.
    """
    matches = []
    item_type = item.get('type')

    for candidate in candidate_items:
        # Ignore same item or items of same type
        if candidate.get('id') == item.get('id') or candidate.get('type') == item_type:
            continue

        if item_type == 'lost':
            eval_result = evaluate_match(lost_item=item, found_item=candidate)
            eval_result['candidate'] = candidate
        else:
            eval_result = evaluate_match(lost_item=candidate, found_item=item)
            eval_result['candidate'] = candidate

        if eval_result['total_score'] >= min_score:
            matches.append(eval_result)

    # Sort descending by total score
    matches.sort(key=lambda m: m['total_score'], reverse=True)
    return matches
