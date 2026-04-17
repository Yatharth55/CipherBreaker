def clean_text(text):
    te = ""
    for i in text:
        if i.isalpha():
            te += i.upper()
    return te

def kasiski(text):
    text = clean_text(text)
    