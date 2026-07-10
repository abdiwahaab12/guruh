"""Migration 007 — gallery_details table."""

MIGRATION_ID = "007_gallery_details"

SQLITE_CREATE = """
CREATE TABLE IF NOT EXISTS gallery_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gallery_image_id INTEGER NOT NULL UNIQUE REFERENCES gallery_images(id) ON DELETE CASCADE,
    slug VARCHAR(150) NOT NULL UNIQUE,
    media_type VARCHAR(20) NOT NULL DEFAULT 'image',
    album VARCHAR(100) DEFAULT '',
    caption TEXT DEFAULT '',
    location VARCHAR(150) DEFAULT '',
    county VARCHAR(100) DEFAULT '',
    country VARCHAR(100) DEFAULT 'Somalia',
    media_date VARCHAR(50) DEFAULT '',
    year VARCHAR(10) DEFAULT '',
    is_featured BOOLEAN NOT NULL DEFAULT 0,
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    service_slug VARCHAR(150) DEFAULT '',
    equipment_slug VARCHAR(150) DEFAULT '',
    team_member_ids_json TEXT DEFAULT '[]',
    video_provider VARCHAR(50) DEFAULT '',
    video_id VARCHAR(100) DEFAULT '',
    embed_url VARCHAR(500) DEFAULT '',
    deleted_at DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_gallery_details_gallery_image_id ON gallery_details (gallery_image_id);
CREATE INDEX IF NOT EXISTS ix_gallery_details_slug ON gallery_details (slug);
"""

MYSQL_CREATE = """
CREATE TABLE IF NOT EXISTS gallery_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gallery_image_id INT NOT NULL,
    slug VARCHAR(150) NOT NULL,
    media_type VARCHAR(20) NOT NULL DEFAULT 'image',
    album VARCHAR(100) DEFAULT '',
    caption TEXT,
    location VARCHAR(150) DEFAULT '',
    county VARCHAR(100) DEFAULT '',
    country VARCHAR(100) DEFAULT 'Somalia',
    media_date VARCHAR(50) DEFAULT '',
    year VARCHAR(10) DEFAULT '',
    is_featured TINYINT(1) NOT NULL DEFAULT 0,
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    service_slug VARCHAR(150) DEFAULT '',
    equipment_slug VARCHAR(150) DEFAULT '',
    team_member_ids_json TEXT,
    video_provider VARCHAR(50) DEFAULT '',
    video_id VARCHAR(100) DEFAULT '',
    embed_url VARCHAR(500) DEFAULT '',
    deleted_at DATETIME NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE KEY uq_gallery_details_gallery_image_id (gallery_image_id),
    UNIQUE KEY uq_gallery_details_slug (slug),
    KEY ix_gallery_details_gallery_image_id (gallery_image_id),
    KEY ix_gallery_details_slug (slug),
    CONSTRAINT fk_gallery_details_image FOREIGN KEY (gallery_image_id) REFERENCES gallery_images(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
