"""Migration 005 — equipment and equipment_details tables."""

MIGRATION_ID = "005_equipment"

SQLITE_CREATE = """
CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(150) NOT NULL UNIQUE,
    category VARCHAR(150) NOT NULL,
    short_description VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(255),
    capacity VARCHAR(150),
    condition VARCHAR(50) NOT NULL DEFAULT 'Operational',
    maintenance_status VARCHAR(255),
    usage TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_featured BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_equipment_slug ON equipment (slug);
CREATE TABLE IF NOT EXISTS equipment_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER NOT NULL UNIQUE REFERENCES equipment(id) ON DELETE CASCADE,
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    specifications_json TEXT DEFAULT '[]',
    gallery_paths_json TEXT DEFAULT '[]',
    related_project_ids_json TEXT DEFAULT '[]',
    related_service_slugs_json TEXT DEFAULT '[]',
    team_member_ids_json TEXT DEFAULT '[]',
    deleted_at DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_equipment_details_equipment_id ON equipment_details (equipment_id);
"""

MYSQL_CREATE = """
CREATE TABLE IF NOT EXISTS equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(150) NOT NULL,
    category VARCHAR(150) NOT NULL,
    short_description VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(255) NULL,
    capacity VARCHAR(150) NULL,
    `condition` VARCHAR(50) NOT NULL DEFAULT 'Operational',
    maintenance_status VARCHAR(255) NULL,
    `usage` TEXT NULL,
    sort_order INT NOT NULL DEFAULT 0,
    is_featured TINYINT(1) NOT NULL DEFAULT 0,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE KEY uq_equipment_slug (slug),
    KEY ix_equipment_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE IF NOT EXISTS equipment_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT NOT NULL,
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    specifications_json TEXT,
    gallery_paths_json TEXT,
    related_project_ids_json TEXT,
    related_service_slugs_json TEXT,
    team_member_ids_json TEXT,
    deleted_at DATETIME NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE KEY uq_equipment_details_equipment_id (equipment_id),
    KEY ix_equipment_details_equipment_id (equipment_id),
    CONSTRAINT fk_equipment_details_equipment FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
