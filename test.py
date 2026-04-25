from joblib import load
from pipeline.get_sample import get_sample
from pipeline.extract_features import extract_features

artifact = load("Models/cipher_classifier.joblib")
model = artifact["model"]
label_encoder = artifact["label_encoder"]

plaintext = "The children racing past the fountain treated the day as if it belonged entirely to them"
ciphertext, true_label, key, cleaned_plaintext = get_sample(plaintext)
features = extract_features(ciphertext)

pred = model.predict([features])[0]
pred_label = label_encoder.inverse_transform([pred])[0]

print("plaintext   :", cleaned_plaintext)
print("ciphertext  :", ciphertext)
print("true label  :", true_label)
print("predicted   :", pred_label)
print("key         :", key)
