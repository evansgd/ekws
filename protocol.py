"""Encryption Key Distribution Applying Steganographic Techniques
   POC implementation of the article:
   https://www.researchgate.net/publication/265209062_Encryption_Key_Distribution_Applying_Steganographic_Techniques
"""
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class Protocol:
    """Protocol that allows to embed a cryptographic key into a cipher text"""
    def __init__(self, key_locations):
        """Takes key_locations (kl)
           :param key_locations: array of integers
        """
        self.key_locations = key_locations

    def pad_right_if_needed(self, plain_text_bytes):
        """Adds padding bytes according to cipher block size.
           ref: https://gist.github.com/btoueg/f71b62f456550da42ea9f4a4bd907d21#file-main-py-L15
           :param plain_text_bytes: array of bytes representing the plain text.
           :return: array of bytes from plain text with padding if applicable.
        """
        block_size_in_bytes = 16
        plain_text_size = len(plain_text_bytes)
        length_with_padding = (
            plain_text_size + (block_size_in_bytes - plain_text_size) % block_size_in_bytes
        )
        return plain_text_bytes.ljust(length_with_padding, '\x00')

    def send(self, message):
        """Creates a cipher text with an embeded cryptographic key (48 bytes)
           from a plain text message.
           :param message: string message in utf-8 format.
           :return: array of bytes of cipher text with an embeded key.
        """
        key = os.urandom(32)
        initialization_vector = os.urandom(16)
        embed_key = bytearray(key + initialization_vector)
        b_message = bytes(self.pad_right_if_needed(message), "utf-8")
        cipher = Cipher(algorithms.AES(key), modes.CBC(initialization_vector))
        encryptor = cipher.encryptor()
        cipher_text = bytearray((encryptor.update(b_message) + encryptor.finalize()))

        cipher_text_with_embed_key = bytearray()
        for index in range(0, len(cipher_text) + len(embed_key)):
            if index in self.key_locations:
                cipher_text_with_embed_key.append(embed_key[0])
                embed_key.pop(0)
            elif len(cipher_text) > 0:
                cipher_text_with_embed_key.append(cipher_text[0])
                cipher_text.pop(0)
        return cipher_text_with_embed_key

    def receive(self, cipher_text_with_embed_key):
        """Retrieves a plain text message from a cipher text with an embeded key.
           :param cipher_text_with_embed_key: bytes of cipher text with an embeded key.
           :return: (key, plain text message).
        """
        new_key = bytearray()
        original_cipher_text = bytearray()
        for index, cipher_text_byte in enumerate(cipher_text_with_embed_key):
            if index in self.key_locations:
                new_key.append(cipher_text_byte)
            else:
                original_cipher_text.append(cipher_text_byte)

        cipher = Cipher(algorithms.AES(new_key[0:-16]), modes.CBC(new_key[-16:]))
        decryptor = cipher.decryptor()
        encoded_original_text_with_padding = decryptor.update(original_cipher_text) \
            + decryptor.finalize()
        recovered_message = encoded_original_text_with_padding.decode("utf-8").rstrip('\x00')
        return new_key, recovered_message
