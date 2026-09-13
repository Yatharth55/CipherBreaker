from clean_text.clean_text import clean_text 

from Features.chi_squared import chi_sqaured

def caesar_recovery(ciphertext="WYRFYPRF"):
    ls = []
    for shift in range(26):
        ciphertext = ciphertext.upper()
        plain = ""
        for i in ciphertext:
            if i.isalpha():
                en = (ord(i)-ord('A')-shift)%26

                plain += chr(en+ord('A'))
            else:
                plain+=i
        ls.append(plain)
    chi_ls = []
    mini =1000 
    mni = 10000
    for i in ls:
        # ioc_ls.append(ioc(clean_text(i)))
        chi_ls.append(chi_sqaured(clean_text(i)))
        # print(i)
        # print()
    for i in range(len(ls)):
        if chi_ls[i]<mini:
            mini = chi_ls[i]
            mni = i
    # print(ioc_ls)
    # print(ls)
    # print(chi_ls)
    return ls[mni]

if __name__ == "__main__":
    #print(caeser_recovery())

    ls = caesar_recovery()
    # ioc_ls = []
    chi_ls = []
    mini =1000 
    mni = 10000
    for i in ls:
        # ioc_ls.append(ioc(clean_text(i)))
        chi_ls.append(chi_sqaured(clean_text(i)))
        # print(i)
        # print()
    for i in range(len(ls)):
        if chi_ls[i]<mini:
            mini = chi_ls[i]
            mni = i
    # print(ioc_ls)
    # print(ls)
    # print(chi_ls)
    print(ls[mni])