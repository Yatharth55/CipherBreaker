from clean_text.clean_text import clean_text 

from Features.chi_squared import chi_sqaured

def caeser_recovery(ciphertext="Uxvvldq Dpedvvdgru-dw-Odujh Dqguhb Ehorxvry, khdg ri lwv ghohjdwlrq wr wkh frqihuhqfh, remhfwhg wr vlqjolqj rxw Ludq dqg hasuhvvhg krsh wkdw wkh fulwlflvp dqg “srolwlflvdwlrq” vwduwlqj rq gdb rqh zloo qrw diihfw wkh rxwfrph, zklfk kh hasuhvvhg krsh zloo eh vxffhvvixo"):
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

    return ls

if __name__ == "__main__":
    #print(caeser_recovery())

    ls = caeser_recovery()
    # ioc_ls = []
    chi_ls = []
    mini =1000 
    mni = 10000
    for i in ls:
        # ioc_ls.append(ioc(clean_text(i)))
        chi_ls.append(chi_sqaured(clean_text(i)))
        print(i)
        print()
    for i in range(len(ls)):
        if chi_ls[i]<mini:
            mini = chi_ls[i]
            mni = i
    # print(ioc_ls)
    # print(ls)
    # print(chi_ls)
    print(ls[mni])