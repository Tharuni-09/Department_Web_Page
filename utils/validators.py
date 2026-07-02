import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_DOC_EXTENSIONS = {"pdf", "docx", "doc"}
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = ALLOWED_DOC_EXTENSIONS | ALLOWED_IMAGE_EXTENSIONS
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

def save_file(file, upload_folder, allowed_extensions=None):
    """Save uploaded file with unique name. Returns filename or None."""
    if file and file.filename and allowed_file(file.filename, allowed_extensions):
        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filename
    return None

def delete_file(filename, upload_folder):
    """Delete a file from upload folder."""
    if filename:
        filepath = os.path.join(upload_folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)