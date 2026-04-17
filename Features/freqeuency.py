def frequency(et):
    et = et.upper()
    freq = {i:0 for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for i in et:
        if i.isalpha():
            freq[i] += 1
    return freq

