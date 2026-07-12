import sqlite3
import json
from flask import g
import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_id INTEGER NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    model TEXT NOT NULL,
    price INTEGER,
    description TEXT DEFAULT '',
    specs TEXT DEFAULT '{}',
    image_url TEXT,
    in_stock INTEGER DEFAULT 1,
    is_promo INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_state (
    chat_id INTEGER PRIMARY KEY,
    awaiting_search INTEGER DEFAULT 0
);
"""

SEED = """
INSERT INTO categories (name, sort_order)
SELECT 'Muzlatgichlar', 1 WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = 'Muzlatgichlar');
INSERT INTO categories (name, sort_order)
SELECT 'Kir yuvish mashinalari', 2 WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = 'Kir yuvish mashinalari');
INSERT INTO categories (name, sort_order)
SELECT 'Konditsionerlar', 3 WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = 'Konditsionerlar');
INSERT INTO categories (name, sort_order)
SELECT 'Televizorlar', 4 WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = 'Televizorlar');
"""


def get_db():
    """So'rov davomida bitta ulanishni qayta ishlatadi (Flask 'g' orqali)."""
    if "db" not in g:
        g.db = sqlite3.connect(config.DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(config.DB_PATH)
    conn.executescript(SCHEMA)
    conn.executescript(SEED)
    conn.commit()
    conn.close()


def query(sql, params=()):
    db = get_db()
    cur = db.execute(sql, params)
    rows = cur.fetchall()
    return rows


def execute(sql, params=()):
    db = get_db()
    cur = db.execute(sql, params)
    db.commit()
    return cur.lastrowid


def row_to_dict(row):
    return dict(row) if row else None


def parse_specs(specs_json):
    try:
        return json.loads(specs_json) if specs_json else {}
    except (json.JSONDecodeError, TypeError):
        return {}
