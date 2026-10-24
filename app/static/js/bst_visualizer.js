/**
 * CampusFind - Interactive BST Visualizer Engine
 * Translates the Python Binary Search Tree into dynamic SVG graphics
 * and animates algorithmic traversals and searches.
 */

class BSTVisualizer {
    constructor(svgId) {
        this.svg = document.getElementById(svgId);
        this.logContainer = document.getElementById('visualizer-log');
        this.treeData = null;
        this.nodeRadius = 22;
        this.levelHeight = 70;
        this.nodeCoordinates = new Map(); // key -> {x, y, node}
    }

    log(message, type = 'info') {
        if (!this.logContainer) return;
        const line = document.createElement('div');
        line.className = 'log-line';
        const now = new Date().toLocaleTimeString();
        line.innerHTML = `<span class="log-time">[${now}]</span> ${message}`;
        this.logContainer.appendChild(line);
        this.logContainer.scrollTop = this.logContainer.scrollHeight;
    }

    clearLog() {
        if (this.logContainer) this.logContainer.innerHTML = '';
    }

    async loadTree() {
        try {
            const res = await fetch('/dsa/api/tree');
            const data = await res.json();
            if (data.success) {
                this.treeData = data.tree;
                this.updateMetrics(data.size, data.height);
                this.render();
            }
        } catch (err) {
            this.log(`Error loading tree: ${err.message}`, 'error');
        }
    }

    updateMetrics(size, height) {
        const sizeEl = document.getElementById('metric-size');
        const heightEl = document.getElementById('metric-height');
        const compEl = document.getElementById('metric-optimal-comps');

        if (sizeEl) sizeEl.innerText = size;
        if (heightEl) heightEl.innerText = height;
        if (compEl) {
            const optimal = size > 0 ? Math.floor(Math.log2(size)) + 1 : 0;
            compEl.innerText = optimal;
        }
    }

    /**
     * Compute node coordinates using in-order numbering for X
     * and tree depth for Y to eliminate overlapping.
     */
    computeCoordinates(root, svgWidth, svgHeight) {
        this.nodeCoordinates.clear();
        if (!root) return;

        // Adapt node dimensions based on available viewport width
        this.nodeRadius = svgWidth < 600 ? 18 : 22;
        this.levelHeight = svgWidth < 600 ? 60 : 70;

        // 1. Assign in-order indices for non-overlapping X
        let inorderIndex = 0;
        const assignInorder = (node, depth) => {
            if (!node) return;
            assignInorder(node.left, depth + 1);
            node._inorderIdx = inorderIndex++;
            node._depth = depth;
            assignInorder(node.right, depth + 1);
        };
        assignInorder(root, 0);

        const totalNodes = Math.max(1, inorderIndex);
        const marginX = svgWidth < 600 ? 25 : 40;
        const usableWidth = svgWidth - (marginX * 2);
        const xStep = usableWidth / (totalNodes + 1);

        const assignPositions = (node) => {
            if (!node) return;
            const x = marginX + (node._inorderIdx + 1) * xStep;
            const y = 45 + (node._depth * this.levelHeight);
            this.nodeCoordinates.set(node.key, { x, y, node });
            assignPositions(node.left);
            assignPositions(node.right);
        };
        assignPositions(root);
    }

    render() {
        if (!this.svg) return;
        this.svg.innerHTML = '';

        if (!this.treeData) {
            this.svg.innerHTML = `
                <text x="50%" y="50%" text-anchor="middle" fill="#94a3b8" font-size="16">
                    Tree is currently empty. Use the controls above to insert keys!
                </text>
            `;
            return;
        }

        const width = this.svg.clientWidth || 900;
        const height = this.svg.clientHeight || 520;
        this.computeCoordinates(this.treeData, width, height);

        // Group for branches (drawn behind nodes)
        const branchGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        branchGroup.setAttribute('id', 'branch-group');
        this.svg.appendChild(branchGroup);

        // Group for nodes
        const nodeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        nodeGroup.setAttribute('id', 'node-group');
        this.svg.appendChild(nodeGroup);

        // Render branches
        for (const [key, item] of this.nodeCoordinates.entries()) {
            const { x, y, node } = item;

            if (node.left && this.nodeCoordinates.has(node.left.key)) {
                const childPos = this.nodeCoordinates.get(node.left.key);
                this.renderBranch(branchGroup, x, y, childPos.x, childPos.y, `branch-${key}-${node.left.key}`);
            }

            if (node.right && this.nodeCoordinates.has(node.right.key)) {
                const childPos = this.nodeCoordinates.get(node.right.key);
                this.renderBranch(branchGroup, x, y, childPos.x, childPos.y, `branch-${key}-${node.right.key}`);
            }
        }

        // Render nodes
        for (const [key, item] of this.nodeCoordinates.entries()) {
            this.renderNode(nodeGroup, item.x, item.y, key, item.node.data);
        }
    }

    renderBranch(parent, x1, y1, x2, y2, id) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('id', id);
        line.setAttribute('class', 'bst-branch');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        parent.appendChild(line);
    }

    renderNode(parent, x, y, key, data) {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'bst-node');
        g.setAttribute('id', `node-g-${key}`);
        g.setAttribute('transform', `translate(${x}, ${y})`);
        g.setAttribute('tabindex', '0');
        g.setAttribute('role', 'button');
        g.setAttribute('aria-label', `Tree Node ${key}${data && data.title ? ': ' + data.title : ''}`);

        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('class', 'node-circle');
        circle.setAttribute('id', `node-circle-${key}`);
        circle.setAttribute('r', this.nodeRadius);

        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('class', 'node-text');
        text.textContent = key;

        g.appendChild(circle);
        g.appendChild(text);

        // Accessible tooltip
        if (data && data.title) {
            const titleEl = document.createElementNS('http://www.w3.org/2000/svg', 'title');
            titleEl.textContent = `Key: ${key}\nItem: ${data.title}\n(Click or press Enter to search)`;
            g.appendChild(titleEl);
        }

        g.addEventListener('click', () => {
            this.searchKey(key);
        });

        g.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.searchKey(key);
            }
        });

        parent.appendChild(g);
    }

    clearHighlights() {
        document.querySelectorAll('.node-circle').forEach(c => {
            c.classList.remove('state-visited', 'state-found', 'state-delete');
        });
        document.querySelectorAll('.bst-branch').forEach(b => {
            b.classList.remove('branch-active');
        });
    }

    async insertKey(key, title) {
        this.clearHighlights();
        this.log(`Initiating BST Insert for Key: ${key}...`);

        try {
            const res = await fetch('/dsa/api/insert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key, title })
            });
            const data = await res.json();
            if (data.success) {
                this.treeData = data.tree;
                this.updateMetrics(data.size, data.height);
                this.render();
                this.log(`Key ${key} inserted. Preserving BST invariant (left < ${key} <= right).`);
                // Briefly highlight newly inserted node
                const newCircle = document.getElementById(`node-circle-${key}`);
                if (newCircle) {
                    newCircle.classList.add('state-found');
                    setTimeout(() => newCircle.classList.remove('state-found'), 1200);
                }
            } else {
                this.log(`Failed to insert key ${key}: ${data.error}`, 'error');
            }
        } catch (err) {
            this.log(`Error during insert: ${err.message}`, 'error');
        }
    }

    async searchKey(key) {
        this.clearHighlights();
        this.log(`Searching for Key ${key} (Logarithmic traversal O(log n))...`);

        try {
            const res = await fetch('/dsa/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key })
            });
            const data = await res.json();
            if (!data.success) {
                this.log(`Search error: ${data.error}`, 'error');
                return;
            }

            const path = data.path || [];
            for (let i = 0; i < path.length; i++) {
                const stepKey = path[i];
                await new Promise(r => setTimeout(r, 450));

                const circle = document.getElementById(`node-circle-${stepKey}`);
                if (circle) {
                    if (stepKey === key && data.found) {
                        circle.classList.add('state-found');
                        this.log(`Target Key ${key} FOUND at depth ${i}! Comparisons required: ${i + 1}.`);
                    } else {
                        circle.classList.add('state-visited');
                        const direction = key < stepKey ? 'LEFT (< ' + stepKey + ')' : 'RIGHT (> ' + stepKey + ')';
                        this.log(`Step ${i + 1}: Visited ${stepKey}. Target ${key} is ${key < stepKey ? 'smaller' : 'larger'} -> Branching ${direction}`);
                    }
                }
            }

            if (!data.found) {
                this.log(`Search concluded: Key ${key} is NOT present in the tree after ${path.length} comparisons.`, 'warn');
            }
        } catch (err) {
            this.log(`Error during search: ${err.message}`, 'error');
        }
    }

    async deleteKey(key) {
        this.clearHighlights();
        this.log(`Initiating BST deletion for Key ${key}...`);

        const targetCircle = document.getElementById(`node-circle-${key}`);
        if (targetCircle) {
            targetCircle.classList.add('state-delete');
            await new Promise(r => setTimeout(r, 400));
        }

        try {
            const res = await fetch('/dsa/api/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key })
            });
            const data = await res.json();
            if (data.success) {
                this.treeData = data.tree;
                this.updateMetrics(data.size, data.height);
                this.render();
                this.log(data.message);
            } else {
                this.log(`Deletion failed: ${data.error}`, 'error');
            }
        } catch (err) {
            this.log(`Error during delete: ${err.message}`, 'error');
        }
    }

    async animateTraversal(order) {
        this.clearHighlights();
        this.log(`Running ${order.toUpperCase()} Traversal...`);

        try {
            const res = await fetch(`/dsa/api/traverse?order=${order}`);
            const data = await res.json();
            if (!data.success) {
                this.log(`Traversal error: ${data.error}`, 'error');
                return;
            }

            const keys = data.keys || [];
            this.log(`${order.toUpperCase()} Sequence: [${keys.join(' -> ')}]`);

            for (let i = 0; i < keys.length; i++) {
                const k = keys[i];
                const circle = document.getElementById(`node-circle-${k}`);
                if (circle) {
                    circle.classList.add('state-visited');
                    await new Promise(r => setTimeout(r, 350));
                }
            }
            this.log(`Traversal complete. Visited all ${keys.length} nodes.`);
        } catch (err) {
            this.log(`Error during traversal: ${err.message}`, 'error');
        }
    }

    async resetTree() {
        this.clearHighlights();
        this.clearLog();
        this.log("Resetting BST to initial balanced campus dataset...");
        try {
            const res = await fetch('/dsa/api/reset', { method: 'POST' });
            const data = await res.json();
            if (data.success) {
                this.treeData = data.tree;
                this.updateMetrics(data.size, data.height);
                this.render();
                this.log("BST successfully reset.");
            }
        } catch (err) {
            this.log(`Reset error: ${err.message}`, 'error');
        }
    }
}

// Global initialization
window.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('bst-svg')) {
        const visualizer = new BSTVisualizer('bst-svg');
        window.bstViz = visualizer;
        visualizer.loadTree();

        // Control buttons
        const insertBtn = document.getElementById('btn-insert');
        if (insertBtn) {
            insertBtn.addEventListener('click', () => {
                const keyInput = document.getElementById('input-key');
                const titleInput = document.getElementById('input-title');
                const key = parseInt(keyInput.value, 10);
                if (isNaN(key)) {
                    alert('Please enter a valid numeric key.');
                    return;
                }
                const title = titleInput.value.trim() || `Item #${key}`;
                visualizer.insertKey(key, title);
                keyInput.value = '';
                titleInput.value = '';
            });
        }

        const searchBtn = document.getElementById('btn-search');
        if (searchBtn) {
            searchBtn.addEventListener('click', () => {
                const keyInput = document.getElementById('input-key');
                const key = parseInt(keyInput.value, 10);
                if (isNaN(key)) {
                    alert('Please enter a valid numeric key to search.');
                    return;
                }
                visualizer.searchKey(key);
            });
        }

        const deleteBtn = document.getElementById('btn-delete');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => {
                const keyInput = document.getElementById('input-key');
                const key = parseInt(keyInput.value, 10);
                if (isNaN(key)) {
                    alert('Please enter a valid numeric key to delete.');
                    return;
                }
                visualizer.deleteKey(key);
                keyInput.value = '';
            });
        }

        const inorderBtn = document.getElementById('btn-inorder');
        if (inorderBtn) inorderBtn.addEventListener('click', () => visualizer.animateTraversal('inorder'));

        const preorderBtn = document.getElementById('btn-preorder');
        if (preorderBtn) preorderBtn.addEventListener('click', () => visualizer.animateTraversal('preorder'));

        const postorderBtn = document.getElementById('btn-postorder');
        if (postorderBtn) postorderBtn.addEventListener('click', () => visualizer.animateTraversal('postorder'));

        const resetBtn = document.getElementById('btn-reset');
        if (resetBtn) resetBtn.addEventListener('click', () => visualizer.resetTree());

        // Responsive resize listener with debouncing
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                if (visualizer && visualizer.treeData) {
                    visualizer.render();
                }
            }, 150);
        });
    }
});
