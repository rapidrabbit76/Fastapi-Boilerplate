import io
from PIL import Image as PILImage
import PIL
from fastapi import File, UploadFile


async def ImageFile(
    image: UploadFile = File(media_type="image/*"),
) -> bytes:
    try:
        image_bytes = await image.read()
        buf = io.BytesIO(image_bytes)
        image_ = PILImage.open(buf)
        w, h = image_.size
        if w > 1000 or h > 1000:
            image_.thumbnail((1000, 1000))
            resized_buf = io.BytesIO()
            image_.save(resized_buf, format="WEBP", quality=80)
            return resized_buf.getvalue()
    except PIL.UnidentifiedImageError as e:
        raise e
    return image_bytes
