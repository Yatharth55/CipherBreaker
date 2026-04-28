def vigenere(plaintext = "yatharth pujani", key="jjjj"):
    result = ""
    keysize = len(key)

    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            p = ord(plaintext[i]) - ord('A')
            k = ord(key[i % keysize]) - ord('A')

            c = (p + k) % 26

            result += chr(c + ord('A'))
        else:
            result += plaintext[i]
    return result

if __name__ == "__main__":
    print(vigenere())