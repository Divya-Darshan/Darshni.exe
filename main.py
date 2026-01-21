from PIL import Image
import os
import piexif
from datetime import datetime

input_folder = "./img"
output_folder = "./img_jpg"

os.makedirs(output_folder, exist_ok=True)

def get_creation_date(path):
    stat = os.stat(path)
    try:
        return stat.st_birthtime   # macOS or some Linux
    except AttributeError:
        return stat.st_ctime       # Windows fallback

def format_exif_date(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y:%m:%d %H:%M:%S")  # EXIF format

# Correct EXIF tag IDs (works on ALL versions)
TAG_DATETIME = 306                  # ImageIFD DateTimedfsdfsdfsdfsdf
TAG_DATETIME_ORIGINAL = 36867       # ExifIFD DateTimeOriginal
TAG_DATETIME_DIGITIZED = 36868      # ExifIFD DateTimeDigitized (CreateDate)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".png"):
        png_path = os.path.join(input_folder, filename)

        jpg_name = filename.rsplit(".", 1)[0] + ".jpg"
        jpg_path = os.path.join(output_folder, jpg_name)

        print(f"Converting {filename} → {jpg_name}")

        # Convert PNG → JPG
        with Image.open(png_path) as img:
            rgb_img = img.convert("RGB")
            rgb_img.save(jpg_path, "JPEG", quality=95)

        # Get file creation date
        creation_timestamp = get_creation_date(png_path)
        creation_str = format_exif_date(creation_timestamp)

        # Build EXIF dictionary manually
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

        exif_dict["0th"][TAG_DATETIME] = creation_str
        exif_dict["Exif"][TAG_DATETIME_ORIGINAL] = creation_str
        exif_dict["Exif"][TAG_DATETIME_DIGITIZED] = creation_str

        exif_bytes = piexif.dump(exif_dict)

        # Insert metadata into JPG
        piexif.insert(exif_bytes, jpg_path)

print("\n✓ All PNG files converted and EXIF dates inserted successfully.")
