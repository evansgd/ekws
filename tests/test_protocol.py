import unittest
import protocol

class TestProtocol(unittest.TestCase):
    def setUp(self):
        kl = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
        self.protocol = protocol.Protocol(kl)
  
    def test_extraction(self):
        cipher_text_with_embed_key = self.protocol.send("Star Trek")
        retrieved_key, retrieved_message = self.protocol.receive(cipher_text_with_embed_key)
        self.assertEqual(len(retrieved_key), 48)
        self.assertEqual(retrieved_message, "Star Trek")
