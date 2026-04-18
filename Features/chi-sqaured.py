
def chi_sqaured(text):

    alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    c_e = clean_text(text)
    total_letters = len(c_e)
    if total_letters == 0:
        return 0
    expected_prob = {
    'A': 0.08167,
    'B': 0.01492,
    'C': 0.02782,
    'D': 0.04253,
    'E': 0.12702,
    'F': 0.02228,
    'G': 0.02015,
    'H': 0.06094,
    'I': 0.06966,
    'J': 0.00153,
    'K': 0.00772,
    'L': 0.04025,
    'M': 0.02406,
    'N': 0.06749,
    'O': 0.07507,
    'P': 0.01929,
    'Q': 0.00095,
    'R': 0.05987,
    'S': 0.06327,
    'T': 0.09056,
    'U': 0.02758,
    'V': 0.00978,
    'W': 0.02360,
    'X': 0.00150,
    'Y': 0.01974,
    'Z': 0.00074
    }
    observed_frequency = {i:0 for i in alphabets}
    for i in c_e:
        observed_frequency[i] += 1
    chi = 0
    for i in alphabets:
        expected_frequency = expected_prob[i]*total_letters
        chi += ((observed_frequency[i]-expected_frequency)**2)/expected_frequency
    return chi/total_letters

# print(chi_sqaured("HI there i am yatharth ho hiohco rhce oho hclugc ibfiufvbf iubvriu bvuie pbiub fbvlib vif bvubv if bv ui vipu bviviuhvrnvioerbveruibvibvieubviub iubv iubcfilubub vpb ivb iu bvuphcuc"))