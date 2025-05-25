# data.py

import random


class TestUser:
    @staticmethod
    def get_random_email():
        return f"test_user_{random.randint(1000, 9999)}@example.com"

    @staticmethod
    def get_random_password():
        return f"Password{random.randint(100, 999)}"

    @property
    def email(self):
        return self.get_random_email()

    @property
    def password(self):
        return self.get_random_password()

    @property
    def name(self):
        return "Test User"