"""Migration 004 — service_details table."""

MIGRATION_ID = "004_service_details"

SQLITE_CREATE = """
CREATE TABLE IF NOT EXISTS service_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_id INTEGER NOT NULL UNIQUE REFERENCES services(id) ON DELETE CASCADE,
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    scope_of_work_json TEXT DEFAULT '[]',
    benefits_json TEXT DEFAULT '[]',
    equipment_json TEXT DEFAULT '[]',
    gallery_paths_json TEXT DEFAULT '[]',
    related_project_ids_json TEXT DEFAULT '[]',
    related_service_slugs_json TEXT DEFAULT '[]',
    team_member_ids_json TEXT DEFAULT '[]',
    deleted_at DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_service_details_service_id ON service_details (service_id);
"""

MYSQL_CREATE = """
CREATE TABLE IF NOT EXISTS service_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_id INT NOT NULL,
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    scope_of_work_json TEXT,
    benefits_json TEXT,
    equipment_json TEXT,
    gallery_paths_json TEXT,
    related_project_ids_json TEXT,
    related_service_slugs_json TEXT,
    team_member_ids_json TEXT,
    deleted_at DATETIME NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE KEY uq_service_details_service_id (service_id),
    KEY ix_service_details_service_id (service_id),
    CONSTRAINT fk_service_details_service FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
