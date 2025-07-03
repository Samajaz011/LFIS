import os
import secrets
from werkzeug.utils import secure_filename
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, folder):
    """Save uploaded file and return filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add random string to avoid filename conflicts
        random_hex = secrets.token_hex(8)
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{random_hex}{ext}"

        # Create directory if it doesn't exist
        upload_path = os.path.join('static', 'uploads', folder)
        os.makedirs(upload_path, exist_ok=True)

        # Also create in uploads directory for compatibility
        alt_upload_path = os.path.join('uploads', folder)
        os.makedirs(alt_upload_path, exist_ok=True)

        # Save file to both locations
        file_path = os.path.join(upload_path, filename)
        alt_file_path = os.path.join(alt_upload_path, filename)

        file.save(file_path)

        # Copy to alternative location
        import shutil
        shutil.copy2(file_path, alt_file_path)

        return filename
    return None

def resize_image(image_path, max_size=(800, 600)):
    """Resize image to max_size while maintaining aspect ratio"""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(image_path, optimize=True, quality=85)
    except Exception as e:
        print(f"Error resizing image: {e}")

def get_file_size(file_path):
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except:
        return 0

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"