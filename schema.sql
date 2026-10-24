-- =====================================================================
-- Smart Lost & Found System (CampusFind)
-- MySQL Database Schema
-- Author: Individual BTech CSE Project
-- Target Database: MySQL 8.0+ / MariaDB 10.4+
-- =====================================================================

CREATE DATABASE IF NOT EXISTS campusfind
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE campusfind;

-- ---------------------------------------------------------------------
-- 1. Table: users
-- Stores registered students, staff members, and administrators.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    student_id VARCHAR(50) DEFAULT NULL,
    phone VARCHAR(30) DEFAULT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'staff', 'admin') NOT NULL DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (email),
    INDEX idx_user_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 2. Table: items
-- Stores reports for both 'lost' and 'found' items.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type ENUM('lost', 'found') NOT NULL,
    title VARCHAR(180) NOT NULL,
    category VARCHAR(60) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(150) NOT NULL,
    item_date DATE NOT NULL,
    image_filename VARCHAR(255) DEFAULT NULL,
    storage_location VARCHAR(150) DEFAULT NULL COMMENT 'For found items: where the item is physically kept (e.g. Security Desk)',
    secret_hint VARCHAR(255) DEFAULT NULL COMMENT 'For lost items: an ownership test hint (e.g. laptop wallpaper, unique engraving)',
    status ENUM('open', 'claimed', 'returned', 'resolved', 'closed') NOT NULL DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_items_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    INDEX idx_items_type (type),
    INDEX idx_items_category (category),
    INDEX idx_items_status (status),
    INDEX idx_items_date (item_date),
    INDEX idx_items_location (location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 3. Table: claims
-- Tracks ownership verification requests submitted by students/users.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    claimant_id INT NOT NULL,
    proof_details TEXT NOT NULL COMMENT 'Detailed explanation or proof confirming ownership',
    secret_answer VARCHAR(255) DEFAULT NULL COMMENT 'Answer to the secret verification hint',
    contact_phone VARCHAR(30) NOT NULL,
    status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    admin_notes TEXT DEFAULT NULL COMMENT 'Remarks entered by campus administrator upon review',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_claims_item FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE,
    CONSTRAINT fk_claims_claimant FOREIGN KEY (claimant_id) REFERENCES users (id) ON DELETE CASCADE,
    INDEX idx_claims_status (status),
    INDEX idx_claims_item (item_id),
    INDEX idx_claims_claimant (claimant_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 4. Table: matches
-- Persists computed similarity links between lost and found items.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lost_item_id INT NOT NULL,
    found_item_id INT NOT NULL,
    similarity_score DECIMAL(5, 2) NOT NULL COMMENT 'Score percentage from 0.00 to 100.00',
    match_details JSON DEFAULT NULL COMMENT 'Detailed factor-by-factor scoring breakdown',
    status ENUM('potential', 'verified', 'dismissed') NOT NULL DEFAULT 'potential',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_matches_lost FOREIGN KEY (lost_item_id) REFERENCES items (id) ON DELETE CASCADE,
    CONSTRAINT fk_matches_found FOREIGN KEY (found_item_id) REFERENCES items (id) ON DELETE CASCADE,
    INDEX idx_matches_score (similarity_score),
    INDEX idx_matches_pair (lost_item_id, found_item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 5. Table: activity_logs
-- Audit log recording administrative and important system events.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT NULL,
    action VARCHAR(80) NOT NULL,
    details TEXT DEFAULT NULL,
    ip_address VARCHAR(45) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_logs_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
    INDEX idx_logs_action (action),
    INDEX idx_logs_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
