import hashlib
import os


class PasswordCrypter:

    SALT_LENGTH = 27

    @classmethod
    def encrypt(cls, password: str) -> bytes:
        """
        Encrypts a password
        :param password: Plaintext password
        :return: Encrypted password
        """
        # Salt and hash the password
        salt: bytes = os.urandom(cls.SALT_LENGTH)
        key: bytes = cls.__generate_key(password=password, salt=salt)
        # Set the encrypted password to contain the salt and the key together
        return salt + key

    @classmethod
    def is_match(cls, plaintext_password: str, stored_password: bytes) -> bool:
        """
        Checks whether a given plaintext password, when encrypted, matches the encrypted password
        :param plaintext_password: Password that needs validation
        :param stored_password: Password that has already been encrypted to check against
        :return: True if passwords match, False if they don't
        """
        # Split encrypted password into salt and key
        stored_salt: bytes = stored_password[: cls.SALT_LENGTH]
        stored_key: bytes = stored_password[cls.SALT_LENGTH :]
        # Generate a test key from the plaintext password
        test_key: bytes = cls.__generate_key(
            password=plaintext_password, salt=stored_salt
        )
        # Return whether test key and stored key are equivalent
        return stored_key == test_key

    @classmethod
    def __generate_key(cls, password: str, salt: bytes) -> bytes:
        """
        Generates a key from a password and a salt
        :param password: Plaintext password
        :param salt: Salt to use when generating the key
        :return: key as bytes
        """
        return hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=salt,
            iterations=50000,
        )
