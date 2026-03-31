def transposition(plaintext, key):
    keylen = len(key)
    ptlen = len(plaintext)
    dic = {i: [] for i in range(keylen)}#initiailsing
    counter = 0
    for i in range(ptlen):
        dic[counter].append(plaintext[i])
        counter += 1

        if counter >= keylen:
            counter = 0
    if counter < keylen:#padding
        while counter != keylen:
            dic[counter].append(" ")
            counter += 1
    # print(dic)
    # Sort key with index (VERY IMPORTANT)
    key_order = sorted(range(keylen), key=lambda x: key[x])
    cipher = ""
    for i in key_order:
        for ch in dic[i]:
            cipher += ch
    return cipher
