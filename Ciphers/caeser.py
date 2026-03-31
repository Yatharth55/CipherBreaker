def caeser(plaintext,shift):
    plaintext = plaintext.upper()
    cipher = ""
    for i in plaintext:
        if i.isalpha():
            en = (ord(i)-ord('A')+shift)%26

            cipher += chr(en+ord('A'))
        else:
            cipher+=i

    return cipher
print(caeser("hello3world",1))