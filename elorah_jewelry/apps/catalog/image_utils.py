import os
import magic
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from apps.core.utils import generate_safe_filename

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_DIMENSIONS = (4096, 4096)
THUMBNAIL_SIZE = (300, 300)

def validate_extension(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Unsupported file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

def validate_file_size(size: int):
    if size > MAX_FILE_SIZE:
        raise ValidationError("File size exceeds the 5MB limit.")

def validate_mime_type(file):
    file.seek(0)
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)
    if not mime.startswith('image/'):
        raise ValidationError("Invalid MIME type. Only images are allowed.")

def validate_dimensions(size: tuple):
    if size[0] > MAX_DIMENSIONS[0] or size[1] > MAX_DIMENSIONS[1]:
        raise ValidationError(f"Image dimensions exceed maximum allowed ({MAX_DIMENSIONS[0]}x{MAX_DIMENSIONS[1]}).")

def convert_to_django_file(img: Image, filename: str, format="JPEG", content_type="image/jpeg"):
    output = BytesIO()
    img.save(output, format=format, quality=85)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField', filename, content_type, output.getbuffer().nbytes, None)

def process_product_image(uploaded_file):
    """
    Validates and processes an uploaded image.
    Returns a dict with 'original', 'thumbnail', 'webp'.
    """
    validate_extension(uploaded_file.name)
    validate_file_size(uploaded_file.size)
    validate_mime_type(uploaded_file)
    
    try:
        img = Image.open(uploaded_file)
        img.verify() # check for corruption
        
        # re-open after verify()
        uploaded_file.seek(0)
        img = Image.open(uploaded_file)
    except Exception:
        raise ValidationError("Invalid or corrupted image file.")
        
    validate_dimensions(img.size)
    
    # Strip EXIF and convert to RGB
    if img.mode != "RGB":
        img = img.convert("RGB")
        
    safe_name = generate_safe_filename(uploaded_file.name)
    base_name = os.path.splitext(safe_name)[0]
    
    # Re-encode original as JPEG
    original_file = convert_to_django_file(img, f"{base_name}.jpg", "JPEG", "image/jpeg")
    
    # Generate thumbnail
    thumb_img = img.copy()
    thumb_img.thumbnail(THUMBNAIL_SIZE)
    thumb_file = convert_to_django_file(thumb_img, f"{base_name}_thumb.jpg", "JPEG", "image/jpeg")
    
    # Generate WebP
    webp_file = convert_to_django_file(img, f"{base_name}.webp", "WEBP", "image/webp")
    
    return {
        "original": original_file,
        "thumbnail": thumb_file,
        "webp": webp_file
    }
