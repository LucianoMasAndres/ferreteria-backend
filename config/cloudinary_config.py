import os
import logging
import cloudinary
import cloudinary.uploader
import cloudinary.api

logger = logging.getLogger(__name__)

# Configure Cloudinary
def setup_cloudinary():
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        logger.warning("⚠️  Cloudinary credentials missing. Image uploads will fail.")
        return

    try:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
        logger.info("✅ Cloudinary configured successfully")
    except Exception as e:
        logger.error(f"❌ Error configuring Cloudinary: {e}")
