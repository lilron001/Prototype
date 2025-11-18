# database.py
"""Database operations manager"""

from supabase import create_client, Client
import hashlib
from config import SUPABASE_URL, SUPABASE_KEY


class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def get_user_by_username(self, username: str):
        """Retrieve user by username"""
        response = self.supabase.table('users').select('*').eq('username', username).execute()
        return response.data[0] if response.data else None
    
    def get_user_by_id(self, user_id: int):
        """Retrieve user by ID"""
        response = self.supabase.table('users').select('*').eq('id', user_id).execute()
        return response.data[0] if response.data else None
    
    def check_username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        response = self.supabase.table('users').select('username').eq('username', username).execute()
        return len(response.data) > 0
    
    def check_email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        response = self.supabase.table('users').select('email').eq('email', email).execute()
        return len(response.data) > 0
    
    def create_user(self, username: str, email: str, password: str):
        """Create a new user"""
        response = self.supabase.table('users').insert({
            'username': username,
            'email': email,
            'password': self.hash_password(password)
        }).execute()
        return response.data[0] if response.data else None
    
    def update_user_profile(self, user_id: int, full_name: str, email: str, phone: str, age: int):
        """Update user profile information"""
        response = self.supabase.table('users').update({
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'age': age
        }).eq('id', user_id).execute()
        return response.data[0] if response.data else None
    
    def update_user_password(self, user_id: int, new_password: str):
        """Update user password"""
        response = self.supabase.table('users').update({
            'password': self.hash_password(new_password)
        }).eq('id', user_id).execute()
        return response.data[0] if response.data else None
    
    def verify_password(self, user_id: int, password: str) -> bool:
        """Verify user password"""
        user = self.get_user_by_id(user_id)
        if user:
            return user['password'] == self.hash_password(password)
        return False