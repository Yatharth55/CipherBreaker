import math 

def ngram(text,n):
    text = clean_text(text)
    fre = {}
    totalngram = len(text)-n+1
    for i in range(0,totalngram):
        gram = text[i:i+n]
        if gram in fre:
            fre[gram] += 1
        else:
            fre[gram] = 1
    for i in fre:
        fre[i] = fre[i]/totalngram#converts into probabilty of n-gram
    return fre

def shanon_entropy(text,n):
    if len(text)<n:
        return 0
    prob = ngram(text,n)
    sum = 0
    for i in prob:
        sum += prob[i]*math.log2(prob[i])
    entropy = -sum
    return entropy

# print(shanon_entropy("aaaaaaa",1))
# print(shanon_entropy("abcdefg",1))