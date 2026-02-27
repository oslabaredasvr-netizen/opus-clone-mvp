import requests
from app.core.config import settings

class SupabaseRESTClient:
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    def insert(self, table: str, payload: dict):
        url = f"{self.url}/rest/v1/{table}"
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def select_eq(self, table: str, column: str, value: str):
        url = f"{self.url}/rest/v1/{table}?{column}=eq.{value}&select=*"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def select_all_desc(self, table: str, order_col: str, limit: int = 10):
        url = f"{self.url}/rest/v1/{table}?order={order_col}.desc&limit={limit}&select=*"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_eq(self, table: str, payload: dict, column: str, value: str):
        url = f"{self.url}/rest/v1/{table}?{column}=eq.{value}"
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def delete_eq(self, table: str, column: str, value: str):
        url = f"{self.url}/rest/v1/{table}?{column}=eq.{value}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return True

if settings.supabase_url and settings.supabase_key:
    supabase = SupabaseRESTClient(settings.supabase_url, settings.supabase_key)
else:
    supabase = None
