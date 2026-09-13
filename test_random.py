import random
import string
from joblib import load
from api import extract_feature_list
from Ciphers.caeser import caesar
from Ciphers.monoalpha import monoalpha
from Ciphers.transposition import transposition
from Ciphers.vigenere import vigenere
from clean_text.clean_text import clean_text

try:
    with open("Data/book.txt", "r", encoding="utf-8") as f:
        book_data = f.read()
except:
    book_data = "kuchh bhi " * 1000

def get_real_text(l):
    idx = random.randint(0, max(0, len(book_data) - l - 1))
    return book_data[idx:idx+l]

print("loading model...")
artifact = load("Models/cipher_classifier.joblib")
m = artifact["model"]
encoder = artifact["label_encoder"]

print("running tests with text from book.txt")
for x in range(2):
    plain = get_real_text(random.randint(100, 300))
    cleaned_plain = clean_text(plain)
    
    if not cleaned_plain:
        cleaned_plain = "EHEHEHHEHEHEH"
        
    ctype = random.choice(['caesar', 'monoalpha', 'transposition', 'vigenere'])
    
    if ctype == 'caesar':
        ctext = caesar(cleaned_plain, random.randint(1, 25))
    elif ctype == 'monoalpha':
        shuffled = list(string.ascii_uppercase)
        random.shuffle(shuffled)
        ctext = monoalpha(cleaned_plain, "".join(shuffled))
    elif ctype == 'transposition':
        ctext = transposition(cleaned_plain, "RANDOMKEY")
    elif ctype == 'vigenere':
        ctext = vigenere(cleaned_plain, "SECRET")
        
    cleaned, f = extract_feature_list(ctext)
    
    p = m.predict([f])[0]
    res = encoder.inverse_transform([p])[0]
    
    print(f"test {x+1} - length {len(ctext)}")
    print(f"actual used : {ctype}")
    print(f"predicted   : {res}")
    print(f"snippet     : {ctext[:40]}...")
    print("-" * 30)

