import os
import hashlib
import requests
from urllib.parse import urlparse


IMAGE_DIR = "output/images"


def download_image(url):

    try:

        os.makedirs(
            IMAGE_DIR,
            exist_ok=True
        )

        ext = os.path.splitext(
            urlparse(url).path
        )[1]

        if ext.lower() not in [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        ]:
            ext = ".jpg"


        filename = (
            hashlib.md5(
                url.encode()
            ).hexdigest()
            + ext
        )

        path = os.path.join(
            IMAGE_DIR,
            filename
        )


        if os.path.exists(path):
            return path


        r = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        if r.status_code != 200:
            return None


        with open(
            path,
            "wb"
        ) as f:
            f.write(r.content)


        return path


    except Exception:

        return None
    
    from PIL import Image


def prepare_image(path):

    try:

        img = Image.open(path)

        # Convert to grayscale
        img = img.convert("L")


        # Resize for Kindle
        max_width = 758

        if img.width > max_width:

            ratio = max_width / img.width

            height = int(
                img.height * ratio
            )

            img = img.resize(
                (max_width, height),
                Image.LANCZOS
            )


        output = path.rsplit(".", 1)[0] + ".jpg"


        img.save(
            output,
            "JPEG",
            quality=75,
            optimize=True
        )


        return output


    except Exception as e:

        print(
            "Image processing failed:",
            e
        )

        return None