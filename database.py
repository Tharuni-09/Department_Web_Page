from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

    with app.app_context():
        # Enable WAL mode for faster concurrent reads (ideal for 500+ users)
        @event.listens_for(db.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.execute("PRAGMA cache_size=-64000")  # 64MB cache
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        from models import user_model, notes_model, papers_model
        from models import outreach_model, placement_model, resume_model
        from models import notification_model
        db.create_all()
        print("[OK] Database initialized with WAL mode")