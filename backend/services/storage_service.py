import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class StorageService:
    def __init__(self):
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.supabase: Client = create_client(url, key)
        self.bucket_name = "student-documents"

    def upload_file(self, remote_path: str, local_file_bytes: bytes, file_mime: str) -> str:
        """Uploads raw binary streams into specific file path keys inside secure buckets."""
        response = self.supabase.storage.from_(self.bucket_name).upload(
            path=remote_path,
            file=local_file_bytes,
            file_options={"content-type": file_mime, "x-upsert": "true"}
        )
        return remote_path

    def get_download_url(self, remote_path: str) -> str:
        """Generates temporary signing keys to download sensitive documents securely."""
        res = self.supabase.storage.from_(self.bucket_name).create_signed_url(remote_path, expires_in=3600)
        return res.get("signedURL", "")
