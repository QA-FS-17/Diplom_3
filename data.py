# data.py

import random

class TestUser:
    @property
    def email(self):
        return f"test{random.randint(10000, 99999)}@example.com"

    @property
    def password(self):
        return f"Pass{random.randint(1000, 9999)}"

    @property
    def name(self):
        return f"User{random.randint(100, 999)}"