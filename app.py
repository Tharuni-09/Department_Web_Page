from flask import Flask, send_from_directory
from config import Config
from database import init_db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Create upload directories
    upload_dirs = [
        Config.UPLOAD_FOLDER, Config.NOTES_FOLDER, Config.PAPERS_FOLDER,
        Config.OUTREACH_FOLDER, Config.RESUME_FOLDER, Config.PROFILE_FOLDER,
        Config.PPT_FOLDER
    ]
    for d in upload_dirs:
        os.makedirs(d, exist_ok=True)

    # Initialize database
    init_db(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.hod import hod_bp
    from routes.faculty import faculty_bp
    from routes.student import student_bp
    from routes.resume import resume_bp
    from routes.notes import notes_bp
    from routes.papers import papers_bp
    from routes.outreach import outreach_bp
    from routes.placements import placements_bp
    from routes.chatbot import chatbot_bp
    from routes.ppt import ppt_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(hod_bp, url_prefix="/hod")
    app.register_blueprint(faculty_bp, url_prefix="/faculty")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(resume_bp, url_prefix="/resume")
    app.register_blueprint(notes_bp, url_prefix="/notes")
    app.register_blueprint(papers_bp, url_prefix="/papers")
    app.register_blueprint(outreach_bp, url_prefix="/outreach")
    app.register_blueprint(placements_bp, url_prefix="/placements")
    app.register_blueprint(chatbot_bp, url_prefix="/chatbot")
    app.register_blueprint(ppt_bp, url_prefix="/ppt")

    # Serve uploaded files
    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return "<h1 style='text-align:center;margin-top:100px;font-family:Inter,sans-serif;color:#64748b;'>404 — Page Not Found</h1>", 404

    @app.errorhandler(500)
    def server_error(e):
        return "<h1 style='text-align:center;margin-top:100px;font-family:Inter,sans-serif;color:#ef4444;'>500 — Server Error</h1>", 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)