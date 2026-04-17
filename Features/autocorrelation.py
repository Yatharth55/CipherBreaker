#auto cor-relation is a feautre to detect periodic ciphers like vigenere cipher that get their 
#maxima at keylength

#we will be using auto-correlation of 1-10

def clean_text(text):
    te = ""
    for i in text:
        if i.isalpha():
            te += i.upper()
    return te

def auto_correlation(text,shifts):
    clean = clean_text(text)
    length = len(clean)
    dic = {i:0 for i in range(1,shifts+1)}
    for i in range(2,shifts+1):
        matches = 0
        if i>=length:
            continue
        for j in range(length-i):
            if clean[j] == clean[i+j]:
                matches +=1
        #normalising
        dic[i] = matches/(length-i)
    return dic

# print(auto_correlation("AAAAAAAAAA",10))