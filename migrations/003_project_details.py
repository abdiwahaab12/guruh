"""Migration 003 — project_details table."""

MIGRATION_ID = "003_project_details"

SQLITE_CREATE = """
CREATE TABLE IF NOT EXISTS project_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL UNIQUE REFERENCES projects(id) ON DELETE CASCADE,
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    overview TEXT DEFAULT '',
    consultant VARCHAR(150) DEFAULT '',
    duration VARCHAR(100) DEFAULT '',
    completion_year VARCHAR(10) DEFAULT '',
    challenges_json TEXT DEFAULT '[]',
    solutions_json TEXT DEFAULT '[]',
    scope_of_work_json TEXT DEFAULT '[]',
    timeline_json TEXT DEFAULT '[]',
    service_slugs_json TEXT DEFAULT '[]',
    equipment_json TEXT DEFAULT '[]',
    team_member_ids_json TEXT DEFAULT '[]',
    related_project_ids_json TEXT DEFAULT '[]',
    related_service_slugs_json TEXT DEFAULT '[]',
    document_paths_json TEXT DEFAULT '[]',
    deleted_at DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_project_details_project_id ON project_details (project_id);
"""

MYSQL_CREATE = """
CREATE TABLE IF NOT EXISTS project_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    meta_title VARCHAR(200) DEFAULT '',
    meta_description VARCHAR(500) DEFAULT '',
    og_image VARCHAR(255) DEFAULT '',
    canonical_url VARCHAR(500) DEFAULT '',
    overview TEXT,
    consultant VARCHAR(150) DEFAULT '',
    duration VARCHAR(100) DEFAULT '',
    completion_year VARCHAR(10) DEFAULT '',
    challenges_json TEXT,
    solutions_json TEXT,
    scope_of_work_json TEXT,
    timeline_json TEXT,
    service_slugs_json TEXT,
    equipment_json TEXT,
    team_member_ids_json TEXT,
    related_project_ids_json TEXT,
    related_service_slugs_json TEXT,
    document_paths_json TEXT,
    deleted_at DATETIME NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    UNIQUE KEY uq_project_details_project_id (project_id),
    KEY ix_project_details_project_id (project_id),
    CONSTRAINT fk_project_details_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
