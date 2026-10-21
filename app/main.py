"""A simple Flask API for the DevSecOps CI/CD pipeline."""

import os
import sqlite3
from pathlib import Path

from flask import Flask, g, jsonify, request


def create_app(db_path=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Store the database in the project directory by default.
    project_root = Path(__file__).resolve().parent.parent
    default_db_path = project_root / "items.db"

    app.config["DB_PATH"] = str(
        db_path or os.environ.get("DB_PATH", str(default_db_path))
    )

    # Create the parent directory if it does not exist.
    Path(app.config["DB_PATH"]).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    def get_db():
        """Create or reuse the database connection for this request."""
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DB_PATH"])
            g.db.row_factory = sqlite3.Row

        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        """Close the database connection after each request."""
        db = g.pop("db", None)

        if db is not None:
            db.close()

    # Initialize the database table.
    with sqlite3.connect(app.config["DB_PATH"]) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            """
        )

    @app.after_request
    def security_headers(response):
        """Add security headers to every response."""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; frame-ancestors 'none'"
        )
        response.headers["Cache-Control"] = "no-store"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        return response

    @app.get("/")
    def home():
        """Return basic application information."""
        return jsonify(
            project="DevSecOps CI/CD Pipeline",
            message="DevSecOps CI/CD Pipeline Application",
            status="running",
        ), 200

    @app.get("/health")
    def health():
        """Health check endpoint."""
        return jsonify(status="ok"), 200

    @app.get("/api/items")
    def list_items():
        """Return all stored items."""
        rows = get_db().execute(
            "SELECT id, name FROM items ORDER BY id"
        ).fetchall()

        return jsonify([dict(row) for row in rows]), 200

    @app.post("/api/items")
    def add_item():
        """Validate and add a new item."""
        data = request.get_json(silent=True) or {}
        name = data.get("name")

        if not isinstance(name, str) or not 1 <= len(name.strip()) <= 100:
            return jsonify(
                error="name must be a string of 1-100 characters"
            ), 400

        cleaned_name = name.strip()
        db = get_db()

        # Parameterized SQL helps prevent SQL injection.
        cursor = db.execute(
            "INSERT INTO items (name) VALUES (?)",
            (cleaned_name,),
        )
        db.commit()

        return jsonify(
            id=cursor.lastrowid,
            name=cleaned_name,
        ), 201

    @app.get("/api/items/search")
    def search_items():
        """Search items by name."""
        query = request.args.get("q", "")[:100]

        rows = get_db().execute(
            "SELECT id, name FROM items WHERE name LIKE ? ORDER BY id",
            (f"%{query}%",),
        ).fetchall()

        return jsonify([dict(row) for row in rows]), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False,
    )