def transposition(plaintext = "shivam", key = "LEMON"):
    keylen = len(key)
    ptlen = len(plaintext)

    # create columns
    columns = {i: [] for i in range(keylen)}

    # fill row-wise
    counter = 0
    for i in range(ptlen):
        columns[counter].append(plaintext[i])
        counter += 1
        if counter >= keylen:
            counter = 0

    # padding 
    if counter < keylen:
        while counter != keylen:
            columns[counter].append(" ")
            counter += 1

    # sort key order
    key_order = sorted(range(keylen), key=lambda x: key[x])

    # read column-wise
    cipher_list = []
    for i in key_order:
        cipher_list.extend(columns[i])

    return "".join(cipher_list)

if __name__ == "__main__":
    print(transposition())