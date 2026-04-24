import random
import string

from Ciphers.caeser import caesar
from Ciphers.monoalpha import monoalpha
from Ciphers.transposition import transposition
from Ciphers.vigenere import vigenere

from clean_text.clean_text import clean_text


def get_sample(plaintext):
    encryption = ["caesar", "monoalpha", "transposition", "vigenere"]

    cipher = random.choice(encryption)

    #plaintext
    #plaintext = "HI there my name is yatharth and i am from jalalabad and i study in nit jalandhar"
    plaintext = clean_text(plaintext)

    # generate key + choose function
    if cipher == "caesar":
        key = random.randint(0, 25)
        encrypt_func = caesar

    elif cipher == "monoalpha":
        letters = list(string.ascii_uppercase)
        random.shuffle(letters)
        key = ''.join(letters)
        encrypt_func = monoalpha

    elif cipher == "transposition":
        key_length = random.randint(3, 8)
        key = ''.join(random.choice(string.ascii_uppercase) for _ in range(key_length))
        encrypt_func = transposition

    elif cipher == "vigenere":
        length = random.randint(3, 8)
        key = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
        encrypt_func = vigenere

    # encrypt
    ciphertext = encrypt_func(plaintext, key)

    return ciphertext, cipher, key , plaintext


# test
if __name__ == "__main__":
    ct, label, key = get_sample()
    print("Cipher:", label)
    print("Key:", key)
    print("Ciphertext:", ct)