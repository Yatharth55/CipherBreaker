def ioc(et):
    alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    su = 0
    et = et.upper()
    count = 0
    for i in alphabets:
        fre = et.count(i)
        su += fre*(fre-1)
        count += fre
    ioc = su/(count*(count-1))
    return ioc

