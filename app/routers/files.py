# This file contains routes related to file operations, such as generating upload URLs, 
from fastapi import APIRouter, Depends, HTTPException
# timedelta is used to set expiration times for the presigned URLs.
from datetime import timedelta
# Import the MinIO client and bucket name from your storage module.
from app.core.storage import minio_client, BUCKET_NAME
# Import the dependency that gets the current logged-in user.
from app.core.dependencies import get_current_user
# user model to type hint the current user.
from app.models.user import User

# Group these routes under "/files" and label them "Files" in the Swagger docs.
router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload-url")
def generate_upload_url(
    filename: str, 
    # Ensure the person requesting a link is a logged-in user.
    current_user: User = Depends(get_current_user)
):
    # Organizes files in the bucket by User ID (e.g., "user123/my_photo.png").
    # This prevents users from overwriting each other's files.
    object_name = f"{current_user.id}/{filename}"

    # Generate a 'Presigned URL'. This is a special URL that allows
    # someone to perform a 'PUT' (upload) without needing the secret keys.
    url = minio_client.presigned_put_object(
        BUCKET_NAME,
        object_name,
        # The link is only valid for 10 minutes. If they don't use it, it dies.
        expires=timedelta(minutes=10)
    )

    # Return the temporary link to the frontend.
    return {
        "upload_url": url,
        "object_name": object_name
    }






# Route to generate a presigned download URL for a file.
@router.get("/download-url")
def generate_download_url(
    object_name: str, 
    # Only logged-in users can request a download link.
    current_user: User = Depends(get_current_user)
):
    # SECURITY CHECK: This is the most important part!
    # It ensures the user is only requesting a file from THEIR OWN "folder".
    # If User #5 tries to download "4/private_document.pdf", they get blocked.
    if not object_name.startswith(f"{current_user.id}/"):
        raise HTTPException(status_code=403, detail="Access denied")

    # Generate a 'Presigned GET' URL. 
    # This turns a private file into a temporary public link.
    url = minio_client.presigned_get_object(
        BUCKET_NAME,
        object_name,
        # The link expires in 10 minutes. 
        # After that, the link is useless, which keeps the file secure.
        expires=timedelta(minutes=10)
    )

    # Return the secure link to the user's browser or app.
    return {"download_url": url}
