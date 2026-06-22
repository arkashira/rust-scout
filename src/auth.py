import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class User:
    email: str
    password: str

class AuthManager:
    def __init__(self):
        self.users: Dict[str, User] = {}

    def create_account(self, email: str, password: str) -> bool:
        if email in self.users:
            return False
        self.users[email] = User(email, password)
        return True

    def log_in(self, email: str, password: str) -> bool:
        if email not in self.users:
            return False
        return self.users[email].password == password

    def get_premium_features(self, email: str) -> str:
        if email not in self.users:
            return "Access denied"
        return "Premium features"

    def save_to_file(self, filename: str) -> None:
        data = {email: user.__dict__ for email, user in self.users.items()}
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_from_file(self, filename: str) -> None:
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.users = {email: User(**user) for email, user in data.items()}
        except FileNotFoundError:
            pass
