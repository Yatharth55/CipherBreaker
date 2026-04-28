def caesar(plaintext= "yatharth",shift = 24):
    plaintext = plaintext.upper()
    cipher = ""
    for i in plaintext:
        if i.isalpha():
            en = (ord(i)-ord('A')+shift)%26

            cipher += chr(en+ord('A'))
        else:
            cipher+=i

    return cipher

if __name__ == "__main__":
    cipher = caesar()
    print(cipher)