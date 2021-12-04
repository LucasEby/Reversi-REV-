import unittest

from client.model.password_crypter import PasswordCrypter


class TestPasswordCrypter(unittest.TestCase):
    def test_crypter_right_password(self):
        password: bytes = PasswordCrypter.encrypt("This class...")
        correct: bool = PasswordCrypter.is_match(
            plaintext_password="This class...", stored_password=password
        )
        self.assertTrue(correct)

    def test_crypter_wrong_password(self):
        password: bytes = PasswordCrypter.encrypt("This class...")
        incorrect: bool = PasswordCrypter.is_match(
            plaintext_password="Dis class...", stored_password=password
        )
        self.assertFalse(incorrect)


if __name__ == "__main__":
    unittest.main()
