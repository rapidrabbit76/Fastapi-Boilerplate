from dataclasses import dataclass, field
from dependency_injector.wiring import inject, Provide
import os
from typing import Any
from uuid import uuid4
from PIL import Image as PILImage
from tempfile import NamedTemporaryFile


@dataclass(init=True, kw_only=True)
class S3Client:
    bucket_name: str
    cdn_url: str
    s3_client: Any = field(init=False)

    @inject
    def __post_init__(self, s3_clinet=Provide["s3_client"]):
        self.s3_client = s3_clinet

    def upload_file(self, file_path, key):
        self.s3_client.upload_file(file_path, self.bucket_name, key)
        return os.path.join(self.cdn_url, key)

    def upload_image(self, image: PILImage.Image) -> str:
        with NamedTemporaryFile() as temp_file:
            image.save(temp_file.name, format="webp", quality=70)
            image_url = self.upload_file(temp_file.name, f"{uuid4()}.webp")
        return image_url

    def upload_images(self, images: list[PILImage.Image]) -> list[str]:
        return [self.upload_image(image) for image in images]
