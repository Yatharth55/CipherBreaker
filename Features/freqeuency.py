def frequency(et):
    et = et.upper()
    freq = {i:0 for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for i in et:
        if i.isalpha():
            freq[i] += 1
    ls = []
    a = ord('A')
    for i in range(26):
        ls.append(freq[chr(a+i)])
    return ls

