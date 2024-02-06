class VigenereCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        key_length = len(self.key)
        key_as_int = [ord(i) for i in self.key]
        plaintext_int = [ord(i) for i in plaintext]
        ciphertext = ''
        for i in range(len(plaintext_int)):
            value = (plaintext_int[i] + key_as_int[i % key_length]) % 256
            ciphertext += chr(value)
        return ciphertext

    def decrypt(self, ciphertext):
        key_length = len(self.key)
        key_as_int = [ord(i) for i in self.key]
        ciphertext_int = [ord(i) for i in ciphertext]
        plaintext = ''
        for i in range(len(ciphertext_int)):
            value = (ciphertext_int[i] - key_as_int[i % key_length]) % 256
            plaintext += chr(value)
        return plaintext
