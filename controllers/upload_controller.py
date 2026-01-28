from fastapi import APIRouter, UploadFile, File, HTTPException, status
import cloudinary.uploader
from config.cloudinary_config import logger

class UploadController:
    def __init__(self):
        self.router = APIRouter(tags=["Uploads"])
        self.register_routes()

    def register_routes(self):
        self.router.add_api_route("/upload/image", self.upload_image, methods=["POST"], status_code=status.HTTP_201_CREATED)

    async def upload_image(self, file: UploadFile = File(...)):
        """
        Upload an image to Cloudinary and return the secure URL.
        """
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        try:
            # Upload file directly from stream
            result = cloudinary.uploader.upload(file.file, folder="ferreteria-products")
            
            return {
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "format": result.get("format")
            }
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")
