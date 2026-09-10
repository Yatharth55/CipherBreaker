# CipherBreaker 🔐

> **Machine-learning-assisted classical cipher identification and cryptanalysis**

CipherBreaker is a Python project that combines **classical cryptanalysis**, **statistical text analysis**, and **machine learning** to identify the likely cipher used to produce a ciphertext.

The project generates a training dataset from real English text, encrypts samples using different classical ciphers and randomly selected keys, extracts statistical features from the resulting ciphertext, and trains a classifier to recognize the cipher family.

It also contains implementations of several classical ciphers and attack/recovery techniques, exposed through a FastAPI backend.

---

## ✨ Features

### Cipher implementations

CipherBreaker currently includes:

- **Caesar cipher**
- **Monoalphabetic substitution cipher**
- **Transposition cipher**
- **Vigenère cipher**

The implementations are located in `Ciphers/`.

### Statistical cryptanalysis

The project extracts features that are useful for distinguishing classical ciphers:

- Letter-frequency distribution
- **Index of Coincidence (IoC)**
- **Shannon entropy**
- N-gram statistics
- **Chi-squared statistic**
- **Autocorrelation**
- **Kasiski examination**

These features are implemented in `Features/`.

### Machine-learning classifier

The classification pipeline is designed around the following workflow:

```text
English plaintext
       │
       ▼
Random cipher + random key
       │
       ▼
Generated ciphertext
       │
       ▼
Feature extraction
       │
       ├── Frequency
       ├── IoC
       ├── Entropy
       ├── N-grams
       ├── Chi-squared
       ├── Autocorrelation
       └── Kasiski
       │
       ▼
ML classifier
       │
       ▼
Predicted cipher type
```

The trained model is stored as:

```text
Models/cipher_classifier.joblib
```

The artifact contains the trained model and its label encoder.

### Cryptanalytic attacks

The `Attacks/` package currently contains:

- Caesar key recovery
- Hill-climbing based cryptanalysis

The attack layer is intended to grow alongside the classifier so that cipher identification can eventually be followed by automated key recovery.

### API

CipherBreaker includes a **FastAPI** backend providing endpoints for:

- Cipher-type prediction
- Text cleaning
- Cipher encryption
- Feature extraction
- Individual statistical tests
- Health checking

---

## 🧠 How the classifier works

CipherBreaker does not attempt to learn plaintext/ciphertext mappings directly.

Instead, it treats cipher identification as a **supervised classification problem**.

For every training sample:

1. An English sentence is selected from the project dataset.
2. The plaintext is cleaned.
3. A cipher is selected.
4. A random key/parameter is generated.
5. The plaintext is encrypted.
6. Statistical properties of the ciphertext are calculated.
7. The resulting feature vector is stored with the cipher label.
8. A machine-learning model is trained on the generated dataset.

For inference, the same feature-extraction process is applied to an unknown ciphertext and the trained classifier predicts its most likely cipher type.

This makes the project a useful experiment in applying **feature engineering + classical cryptanalysis + ML** rather than relying purely on hard-coded rules.

---

## 📁 Project structure

```text
CipherBreaker/
│
├── Attacks/
│   ├── __init__.py
│   ├── caeser_recovery.py
│   └── hillclimbing.py
│
├── Ciphers/
│   ├── __init__.py
│   ├── caeser.py
│   ├── monoalpha.py
│   ├── transposition.py
│   └── vigenere.py
│
├── Data/
│   └── book.txt
│
├── Features/
│   ├── __init__.py
│   ├── autocorrelation.py
│   ├── chi_squared.py
│   ├── entropy.py
│   ├── frequency.py
│   ├── indexofcoincidence.py
│   └── kasiski.py
│
├── clean_text/
│   ├── __init__.py
│   └── clean_text.py
│
├── pipeline/
│   ├── extract_features.py
│   ├── generate_dataset.py
│   ├── get_sample.py
│   └── train_model.py
│
├── api.py
├── test.py
├── requirements.txt
└── readme.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Yatharth55/CipherBreaker.git
cd CipherBreaker
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Generate training data

The dataset-generation pipeline uses `Data/book.txt` as the source of English text.

Run:

```bash
python -m pipeline.generate_dataset
```

This generates encrypted samples and their corresponding feature information for model training.

> The exact output depends on the current implementation of the pipeline and its configuration.

---

## 🤖 Train the classifier

After generating the dataset:

```bash
python -m pipeline.train_model
```

The trained artifact is expected at:

```text
Models/cipher_classifier.joblib
```

The API loads this artifact when a cipher-type prediction is requested.

---

## 🚀 Run the API

Start the FastAPI server with:

```bash
uvicorn api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 🔌 API endpoints

### Health

```http
GET /health
```

Returns:

```json
{
  "ok": true
}
```

### Predict cipher type

```http
POST /predict/cipher-type
```

Request:

```json
{
  "ciphertext": "KHOORZRUOG"
}
```

The response contains the cleaned ciphertext, extracted features, and predicted cipher type.

### Clean text

```http
POST /clean-text
```

### Encrypt with Caesar

```http
POST /cipher/caesar
```

Example:

```json
{
  "plaintext": "HELLO WORLD",
  "shift": 3
}
```

### Encrypt with monoalphabetic substitution

```http
POST /cipher/monoalpha
```

### Encrypt with transposition

```http
POST /cipher/transposition
```

### Encrypt with Vigenère

```http
POST /cipher/vigenere
```

### Extract all features

```http
POST /features/all
```

Individual feature endpoints are also available:

```text
/features/frequency
/features/ioc
/features/entropy
/features/ngram
/features/chi-squared
/features/autocorrelation
/features/kasiski
```

---

## 🔬 Feature engineering

The classifier uses several properties of ciphertext.

### Frequency analysis

Measures the distribution of letters in the ciphertext.

This is particularly useful because classical substitution-based ciphers often preserve some statistical properties of the underlying language.

### Index of Coincidence

IoC measures the probability that two randomly selected characters from a text are identical.

It is useful for distinguishing different cipher families and is especially relevant to polyalphabetic-cipher analysis.

### Shannon entropy

Entropy measures the uncertainty/disorder of the character distribution.

```text
Higher entropy → more uniform distribution
Lower entropy  → more uneven distribution
```

### Chi-squared statistic

Compares the observed character-frequency distribution against an expected distribution.

### Autocorrelation

Measures similarity between a sequence and shifted versions of itself. It can expose periodic structures in ciphertext.

### Kasiski examination

Looks for repeated sequences and distances between them. This is particularly useful when analyzing periodic polyalphabetic ciphers such as Vigenère.

---

## 🧩 Example workflow

A typical prediction workflow looks like:

```python
from pathlib import Path
from joblib import load

from pipeline.get_sample import get_sample
from pipeline.extract_features import extract_features

artifact = load("Models/cipher_classifier.joblib")

model = artifact["model"]
label_encoder = artifact["label_encoder"]

plaintext = "The children racing past the fountain treated the day as if it belonged entirely to them"

ciphertext, true_label, key, cleaned_plaintext = get_sample(plaintext)

features = extract_features(ciphertext)

prediction = model.predict([features])[0]
predicted_label = label_encoder.inverse_transform([prediction])[0]

print("Plaintext :", cleaned_plaintext)
print("Ciphertext:", ciphertext)
print("True label:", true_label)
print("Predicted :", predicted_label)
print("Key       :", key)
```

---

## 🛠️ Technology stack

- **Python**
- **NumPy**
- **scikit-learn**
- **XGBoost**
- **Joblib**
- **FastAPI**
- **Pydantic**
- **Uvicorn**

---

## 🎯 Project goals

CipherBreaker is being developed as an exploration of the intersection between:

- Classical cryptography
- Cryptanalysis
- Statistical inference
- Feature engineering
- Machine learning
- Automated key recovery

The long-term goal is to move beyond simply answering:

> **"Which cipher is this?"**

towards:

> **"Which cipher is this, what key/parameters were probably used, and can the ciphertext be recovered automatically?"**

---

## 🚧 Roadmap

Planned/improvable areas include:

- [ ] Improve training-data generation and class balance
- [ ] Add more classical cipher families
- [ ] Add confidence/probability scores to predictions
- [ ] Improve automated key recovery
- [ ] Connect cipher identification directly to the appropriate attack
- [ ] Benchmark different ML classifiers
- [ ] Add proper train/validation/test splits
- [ ] Add model evaluation metrics and confusion matrices
- [ ] Add automated cryptanalysis pipelines
- [ ] Add a dedicated web interface
- [ ] Add unit and integration tests
- [ ] Improve API documentation

---

## ⚠️ Limitations

CipherBreaker is focused on **classical ciphers and statistical cryptanalysis**.

It should not be interpreted as a tool capable of breaking modern cryptographic primitives such as AES, RSA, or properly implemented public-key cryptography.

Machine-learning predictions are also dependent on the training distribution. Ciphertexts that differ significantly from the generated training data may be classified incorrectly.

---

## 📚 Educational purpose

This project is primarily intended for:

- Learning classical cryptanalysis
- Understanding statistical properties of ciphertext
- Experimenting with feature engineering
- Studying ML classification
- Exploring automated cryptanalysis

Use it only on data and systems you are authorized to analyze.

---

## 👨‍💻 Author

**Yatharth Pujani**

GitHub: [@Yatharth55](https://github.com/Yatharth55)

Project: [CipherBreaker](https://github.com/Yatharth55/CipherBreaker)

---

## ⭐ Contributing

Contributions, experiments, improvements, and new cryptanalytic techniques are welcome.

If you find a bug or have an idea for improving the classifier or attack pipeline, open an issue or submit a pull request.

---

## 📄 License

See the repository's `LICENSE` file for licensing information.
