#auto cor-relation is a feautre to detect periodic ciphers like vigenere cipher that get their 
#maxima at keylength

#we will be using auto-correlation of 1-10

def auto_correlation(text):
    clean = clean_text(text)
    length = len(clean)
    dic = {i:0 for i in range(1,11)}
    for i in range(2,shifts+1):
        matches = 0
        if i>=length:
            continue
        for j in range(length-i):
            if clean[j] == clean[i+j]:
                matches +=1
        #normalising
        dic[i] = matches/(length-i)
    ls = []
    for i in range(1,11):
        ls.append(dic[i])
    return ls

# print(auto_correlation("AAAAAAAAAA",10))