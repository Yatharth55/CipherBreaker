def monoalpha(plaintext = "yatharth",substitution = "QWERTYUIOPASDFGHJKLZXCVBNM"):
    cipher = ""
    plaintext = plaintext.upper()
    for i in plaintext:
        if i.isalpha():
            cipher += substitution[ord(i)-ord('A')]
        else:
            cipher += i
    return cipher

# print(monoaplha("abzy","QWERTYUIOPASDFGHJKLZXCVBNM"))

if __name__ == "__main__":
    print(monoalpha())