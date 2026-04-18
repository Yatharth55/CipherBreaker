import math
from collections import defaultdict

def clean_text(text):
    return "".join([c.upper() for c in text if c.isalpha()])


def kasiski_test(text):
    text = clean_text(text)
    n = len(text)

    # Step 1: collect trigram positions
    trigram_pos = defaultdict(list)
    for i in range(n - 2):
        trigram = text[i:i+3]
        trigram_pos[trigram].append(i)

    # Step 2: compute distances
    distances = []
    for positions in trigram_pos.values():
        if len(positions) > 1:
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    distances.append(positions[j] - positions[i])

    if not distances:
        return None  # no useful repeats

    # Step 3: compute GCD of all distances
    gcd_value = distances[0]
    for d in distances[1:]:
        gcd_value = math.gcd(gcd_value, d)

    return gcd_value