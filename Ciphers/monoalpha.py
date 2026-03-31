def monoaplha(plaintext,substitution):
    cipher = ""
    plaintext = plaintext.upper()
    for i in plaintext:
        if i.isalpha():
            cipher += substitution[ord(i)-ord('A')]
        else:
            cipher += i
    return cipher

# print(monoaplha("abzy","QWERTYUIOPASDFGHJKLZXCVBNM"))