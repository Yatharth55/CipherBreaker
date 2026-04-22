from clean_text.clean_text import clean_text as c_t
from Features.autocorrelation import auto_correlation
from Features.chi_squared import chi_sqaured
from Features.entropy import shanon_entropy
from Features.entropy import ngram
from Features.frequency import frequency
from Features.indexofcoincidence import ioc
from Features.kasiski import kasiski_test

def extract_features(ciphertext):
    ciphertext = c_t(ciphertext)

    feat = []

    # 1. frequency (26 values)
    feat.extend(frequency(ciphertext))

    # 2. IC
    feat.append(ioc(ciphertext))

    # 3. entropy (2 values)
    feat.append(shanon_entropy(ciphertext, 2))
    feat.append(shanon_entropy(ciphertext, 3))

    # 4. chi-square
    feat.append(chi_sqaured(ciphertext))

    # 5. autocorrelation (10 values)
    feat.extend(auto_correlation(ciphertext, 10))

    # 6. kasiski (1 value)
    k = kasiski_test(ciphertext)
    feat.append(k if k is not None else 0)

    return feat

if __name__ == "__main__":
    features = extract_features("HELLOWORLDTHISISATESTSTRING")
    print(len(features))
    print(features)