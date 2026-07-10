"""Migration 009 — messages inbox extension tables and job applications."""

MIGRATION_ID = "009_messages_inbox"

SQLITE_CREATE = """
CREATE TABLE IF NOT EXISTS contact_submission_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_submission_id INTEGER NOT NULL UNIQUE REFERENCES contact_submissions(id) ON DELETE CASCADE,
    is_starred BOOLEAN NOT NULL DEFAULT 0,
    is_archived BOOLEAN NOT NULL DEFAULT 0,
    deleted_at DATETIME,
    admin_notes TEXT DEFAULT '',
    reply_subject VARCHAR(200) DEFAULT '',
    reply_body TEXT DEFAULT '',
    replied_at DATETIME,
    replied_by_user_id INTEGER REFERENCES users(id),
    extra_json TEXT DEFAULT '{}',
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_contact_submission_details_contact_submission_id ON contact_submission_details (contact_submission_id);

CREATE TABLE IF NOT EXISTS quote_request_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote_request_id INTEGER NOT NULL UNIQUE REFERENCES quote_requests(id) ON DELETE CASCADE,
    is_starred BOOLEAN NOT NULL DEFAULT 0,
    is_archived BOOLEAN NOT NULL DEFAULT 0,
    deleted_at DATETIME,
    admin_notes TEXT DEFAULT '',
    reply_subject VARCHAR(200) DEFAULT '',
    reply_body TEXT DEFAULT '',
    replied_at DATETIME,
    replied_by_user_id INTEGER REFERENCES users(id),
    extra_json TEXT DEFAULT '{}',
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_quote_request_details_quote_request_id ON quote_request_details (quote_request_id);

CREATE TABLE IF NOT EXISTS job_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_listing_id INTEGER REFERENCES job_listings(id),
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(50),
    position VARCHAR(200),
    years_experience VARCHAR(50),
    education VARCHAR(200),
    cover_letter TEXT,
    is_read BOOLEAN NOT NULL DEFAULT 0,
    is_starred BOOLEAN NOT NULL DEFAULT 0,
    is_archived BOOLEAN NOT NULL DEFAULT 0,
    deleted_at DATETIME,
    admin_notes TEXT DEFAULT '',
    reply_subject VARCHAR(200) DEFAULT '',
    reply_body TEXT DEFAULT '',
    replied_at DATETIME,
    replied_by_user_id INTEGER REFERENCES users(id),
    extra_json TEXT DEFAULT '{}',
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_job_applications_job_listing_id ON job_applications (job_listing_id);
CREATE INDEX IF NOT EXISTS ix_job_applications_email ON job_applications (email);
CREATE INDEX IF NOT EXISTS ix_job_applications_is_read_created_at ON job_applications (is_read, created_at);
CREATE INDEX IF NOT EXISTS ix_job_applications_archived_created_at ON job_applications (is_archived, created_at);
"""

MYSQL_CREATE = """
CREATE TABLE IF NOT EXISTS contact_submission_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contact_submission_id INT NOT NULL,
    is_starred TINYINT(1) NOT NULL DEFAULT 0,
    is_archived TINYINT(1) NOT NULL DEFAULT 0,
    deleted_at DATETIME NULL,
    admin_notes TEXT,
    reply_subject VARCHAR(200) DEFAULT '',
    reply_body TEXT,
    replied_at DATETIME NULL,
    replied_by_user_id INT NULL,
    extra_json TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE KEY uq_contact_submission_details_submission_id (contact_submission_id),
    KEY ix_contact_submission_details_contact_submission_id (contact_submission_id),
    CONSTRAINT fk_contact_submission_details_submission FOREIGN KEY (contact_submission_id) REFERENCES contact_submissions(id) ON DELETE CASCADE,
    CONSTRAINT fk_contact_submission_details_user FOREIGN KEY (replied_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS quote_request_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quote_request_id INT NOT NULL,
    is_starred TINYINT(1) NOT NULL DEFAULT 0,
    is_archived TINYINT(1) NOT NULL DEFAULT 0,
    deleted_at DATETIME NULL,
    admin_notes TEXT,
    reply_subject VARCHAR(200) DEFAULT '',
    reply_body TEXT,
    replied_at DATETIME NULL,
    replied_by_user_id INT NULL,
    extra_json TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE KEY uq_quote_request_details_request_id (quote_request_id),
    KEY ix_quote_request_details_quote_request_id (quote_request_id),
    CONSTRAINT fk_quote_request_details_request FOREIGN KEY (quote_request_id) REFERENCES quote_requests(id) ON DELETE CASCADE,
    CONSTRAINT fk_quote_request_details_user FOREIGN KEY (replied_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS job_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_listing_id INT NULL,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(50) NULL,
    position VARCHAR(200) NULL,
    years_experience VARCHAR(50) NULL,
    education VARCHAR(200) NULL,
    cover_letter TEXT NULL,
    is_read TINYINT(1) NOT NULL DEFAULT 0,
    is_starred TINYINT(1) NOT NULL DEFAULT 0,
    is_archived TINYINT(1) NOT NULL DEFAULT 0,
    deleted_at DATETIME NULL,
    admin_notes TEXT,
    reply_subject VARCHAR(200) DEFAULT '',
    reply_body TEXT,
    replied_at DATETIME NULL,
    replied_by_user_id INT NULL,
    extra_json TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    KEY ix_job_applications_job_listing_id (job_listing_id),
    KEY ix_job_applications_email (email),
    KEY ix_job_applications_is_read_created_at (is_read, created_at),
    KEY ix_job_applications_archived_created_at (is_archived, created_at),
    CONSTRAINT fk_job_applications_listing FOREIGN KEY (job_listing_id) REFERENCES job_listings(id) ON DELETE SET NULL,
    CONSTRAINT fk_job_applications_user FOREIGN KEY (replied_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
