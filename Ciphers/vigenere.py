def alphtonum(character):
    

def vigenere(plaintext,key):
    keysize = len(key)
    encrypted = ""
    j = 0
    for i in range(len(plaintext)):
        if plaintext[i] == " ":
            continue
        else:
            en = (int(plaintext[i]) - "a" + int(key[j%keysize])-"a")%26
            j = j+1
            encrypted += (en+int("a"))
    return encrypted

print(vigenere("hello","hi"))