# data.py

TEST_INGREDIENTS = {
    "bun": "61c0c5a71d1f82001bdaaa6d",  # Флюоресцентная булка
    "sauce": "61c0c5a71d1f82001bdaaa72"  # Биокотлета
}


class TestUser:
    @staticmethod
    def generate_test_email():
        import uuid
        return f"test_{uuid.uuid4().hex[:8]}@example.com"

    @property
    def valid_credentials(self):
        return {
            "email": self.generate_test_email(),
            "password": "Password123",
            "name": "Test User"
        }