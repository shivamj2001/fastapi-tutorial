# Import the Minio library, which provides the tools to talk to the MinIO server.
from minio import Minio
# Import your app's settings (usually from an .env file) to keep passwords secret.
from app.core.config import settings

# Initialize the Minio client. This is the "driver" you will use to 
# upload, download, or delete files.
minio_client = Minio(
    # The URL where MinIO is running (e.g., "localhost:9000").
    endpoint=settings.minio_endpoint,
    
    # Your "Username" for MinIO.
    access_key=settings.minio_access_key,
    
    # Your "Password" for MinIO.
    secret_key=settings.minio_secret_key,
    
    # Set to 'False' because you are likely running this locally without 
    # SSL/HTTPS certificates. Set to 'True' in a real production site.
    secure=False
)

# The name of the 'folder' (called a Bucket) where all files will be stored.
# In MinIO/S3, you can't upload a file unless it belongs to a bucket.
BUCKET_NAME = "user-files"