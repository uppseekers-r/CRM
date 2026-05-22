import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class AuthenticationManager:
    def __init__(self):
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_ANON_KEY")
        self.client: Client = create_client(url, key)

    def login_user(self, email: str, password: str):
        try:
            auth_response = self.client.auth.sign_in_with_password({"email": email, "password": password})
            return auth_response
        except Exception:
            return None

    def sign_out(self):
        self.client.auth.sign_out()
