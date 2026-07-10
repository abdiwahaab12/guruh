"""Migration 008 — job_listing_details table."""

MIGRATION_ID = "008_job_listing_details"

SQLITE_CREATE = """
CREATE TABLE IF NOT EXISTS job_listing_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_listing_id INTEGER NOT NULL UNIQUE REFERENCES job_listings(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    short_description VARCHAR(500) DEFAULT '',
    experience_required VARCHAR(100) DEFAULT '',
    image VARCHAR(255) DEFAULT '',
    responsibilities_json TEXT DEFAULT '[]',
    qualifications_json TEXT DEFAULT '[]',
    skills_json TEXT DEFAULT '[]',
    benefits_json TEXT DEFAULT '[]',
    is_featured BOOLEAN NOT NULL DEFAULT 0,
    accept_applications BOOLEAN NOT NULL DEFAULT 1,
    notify_email VARCHAR(120) DEFAULT '',
    auto_reply_enabled BOOLEAN NOT NULL DEFAULT 0,
    auto_reply_message TEXT DEFAULT '',
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    deleted_at DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_job_listing_details_job_listing_id ON job_listing_details (job_listing_id);
"""

MYSQL_CREATE = """
CREATE TABLE IF NOT EXISTS job_listing_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_listing_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    short_description VARCHAR(500) DEFAULT '',
    experience_required VARCHAR(100) DEFAULT '',
    image VARCHAR(255) DEFAULT '',
    responsibilities_json TEXT,
    qualifications_json TEXT,
    skills_json TEXT,
    benefits_json TEXT,
    is_featured TINYINT(1) NOT NULL DEFAULT 0,
    accept_applications TINYINT(1) NOT NULL DEFAULT 1,
    notify_email VARCHAR(120) DEFAULT '',
    auto_reply_enabled TINYINT(1) NOT NULL DEFAULT 0,
    auto_reply_message TEXT,
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    deleted_at DATETIME NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE KEY uq_job_listing_details_job_listing_id (job_listing_id),
    KEY ix_job_listing_details_job_listing_id (job_listing_id),
    CONSTRAINT fk_job_listing_details_job FOREIGN KEY (job_listing_id) REFERENCES job_listings(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
