def vigenere(plaintext, key):
    result = ""
    keysize = len(key)

    for i in range(len(plaintext)):
        p = ord(plaintext[i]) - ord('A')
        k = ord(key[i % keysize]) - ord('A')

        c = (p + k) % 26

        result += chr(c + ord('A'))

    return result

# print(vigenere("hello","hi"))