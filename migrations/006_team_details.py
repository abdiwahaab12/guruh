"""Migration 006 — team_details table."""

MIGRATION_ID = "006_team_details"

SQLITE_CREATE = """
CREATE TABLE IF NOT EXISTS team_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_member_id INTEGER NOT NULL UNIQUE REFERENCES team_members(id) ON DELETE CASCADE,
    slug VARCHAR(150) NOT NULL UNIQUE,
    department VARCHAR(150) DEFAULT '',
    member_type VARCHAR(50) DEFAULT 'staff',
    years_experience VARCHAR(50) DEFAULT '',
    education VARCHAR(255) DEFAULT '',
    experience_summary TEXT DEFAULT '',
    is_featured BOOLEAN NOT NULL DEFAULT 0,
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    social_links_json TEXT DEFAULT '[]',
    gallery_paths_json TEXT DEFAULT '[]',
    related_project_ids_json TEXT DEFAULT '[]',
    related_service_slugs_json TEXT DEFAULT '[]',
    related_equipment_ids_json TEXT DEFAULT '[]',
    deleted_at DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_team_details_team_member_id ON team_details (team_member_id);
CREATE INDEX IF NOT EXISTS ix_team_details_slug ON team_details (slug);
"""

MYSQL_CREATE = """
CREATE TABLE IF NOT EXISTS team_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_member_id INT NOT NULL,
    slug VARCHAR(150) NOT NULL,
    department VARCHAR(150) DEFAULT '',
    member_type VARCHAR(50) DEFAULT 'staff',
    years_experience VARCHAR(50) DEFAULT '',
    education VARCHAR(255) DEFAULT '',
    experience_summary TEXT,
    is_featured TINYINT(1) NOT NULL DEFAULT 0,
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    social_links_json TEXT,
    gallery_paths_json TEXT,
    related_project_ids_json TEXT,
    related_service_slugs_json TEXT,
    related_equipment_ids_json TEXT,
    deleted_at DATETIME NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE KEY uq_team_details_team_member_id (team_member_id),
    UNIQUE KEY uq_team_details_slug (slug),
    KEY ix_team_details_team_member_id (team_member_id),
    KEY ix_team_details_slug (slug),
    CONSTRAINT fk_team_details_member FOREIGN KEY (team_member_id) REFERENCES team_members(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
