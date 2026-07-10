"""
Migration 002 — media_assets table (Enterprise Media Manager).

Fresh installs: python init_db.py
Existing databases: python scripts/apply_media_migration.py
"""

MIGRATION_ID = "002_media_assets"

SQLITE_CREATE = """
CREATE TABLE IF NOT EXISTS media_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    storage_path VARCHAR(500) NOT NULL UNIQUE,
    folder VARCHAR(50) NOT NULL DEFAULT 'general',
    media_type VARCHAR(20) NOT NULL,
    mime_type VARCHAR(120) NOT NULL,
    file_size BIGINT NOT NULL DEFAULT 0,
    title VARCHAR(200) NOT NULL DEFAULT '',
    alt_text VARCHAR(255) DEFAULT '',
    caption VARCHAR(500) DEFAULT '',
    description TEXT DEFAULT '',
    tags VARCHAR(500) DEFAULT '',
    category VARCHAR(100) DEFAULT '',
    seo_title VARCHAR(200) DEFAULT '',
    seo_description VARCHAR(500) DEFAULT '',
    width INTEGER,
    height INTEGER,
    uploaded_by_id INTEGER REFERENCES users(id),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    deleted_at DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_media_assets_storage_path ON media_assets (storage_path);
CREATE INDEX IF NOT EXISTS ix_media_assets_folder ON media_assets (folder);
CREATE INDEX IF NOT EXISTS ix_media_assets_media_type ON media_assets (media_type);
"""

MYSQL_CREATE = """
CREATE TABLE IF NOT EXISTS media_assets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    folder VARCHAR(50) NOT NULL DEFAULT 'general',
    media_type VARCHAR(20) NOT NULL,
    mime_type VARCHAR(120) NOT NULL,
    file_size BIGINT NOT NULL DEFAULT 0,
    title VARCHAR(200) NOT NULL DEFAULT '',
    alt_text VARCHAR(255) DEFAULT '',
    caption VARCHAR(500) DEFAULT '',
    description TEXT,
    tags VARCHAR(500) DEFAULT '',
    category VARCHAR(100) DEFAULT '',
    seo_title VARCHAR(200) DEFAULT '',
    seo_description VARCHAR(500) DEFAULT '',
    width INT NULL,
    height INT NULL,
    uploaded_by_id INT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    deleted_at DATETIME NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE KEY uq_media_assets_storage_path (storage_path),
    KEY ix_media_assets_folder (folder),
    KEY ix_media_assets_media_type (media_type),
    CONSTRAINT fk_media_assets_uploaded_by FOREIGN KEY (uploaded_by_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
