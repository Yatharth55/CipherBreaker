from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from joblib import load
from pydantic import BaseModel, Field

from Ciphers.caeser import caesar
from Ciphers.monoalpha import monoalpha
from Ciphers.transposition import transposition
from Ciphers.vigenere import vigenere
from Features.autocorrelation import auto_correlation
from Features.chi_squared import chi_sqaured
from Features.entropy import ngram, shanon_entropy
from Features.frequency import frequency
from Features.indexofcoincidence import ioc
from Features.kasiski import kasiski_test
from clean_text.clean_text import clean_text


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "Models" / "cipher_classifier.joblib"

app = FastAPI(title="CipherBreaker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextRequest(BaseModel):
    text: str


class CipherPredictRequest(BaseModel):
    ciphertext: str


class CaesarRequest(BaseModel):
    plaintext: str
    shift: int = Field(ge=0, le=25)


class MonoalphaRequest(BaseModel):
    plaintext: str
    substitution: str


class TranspositionRequest(BaseModel):
    plaintext: str
    key: str


class VigenereRequest(BaseModel):
    plaintext: str
    key: str


class NgramRequest(BaseModel):
    text: str
    n: int = Field(ge=1)


class EntropyRequest(BaseModel):
    text: str
    n: int = Field(ge=1)


class AutoCorrelationRequest(BaseModel):
    text: str
    shifts: int = Field(ge=1, le=10)


def load_artifact():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. Train the classifier first."
        )
    return load(MODEL_PATH)


def extract_feature_list(ciphertext):
    cleaned = clean_text(ciphertext)
    features = []

    features.extend(frequency(cleaned))
    features.append(ioc(cleaned))
    features.append(shanon_entropy(cleaned, 2))
    features.append(shanon_entropy(cleaned, 3))
    features.append(chi_sqaured(cleaned))
    features.extend(auto_correlation(cleaned, 10))

    kasiski_value = kasiski_test(cleaned)
    features.append(kasiski_value if kasiski_value is not None else 0)

    return cleaned, features


def validate_substitution_key(substitution):
    key = substitution.upper()
    if len(key) != 26 or len(set(key)) != 26 or not key.isalpha():
        raise ValueError(
            "substitution must be a 26-character alphabetic permutation."
        )
    return key


def validate_alpha_key(key, field_name):
    cleaned_key = clean_text(key)
    if not cleaned_key:
        raise ValueError(f"{field_name} must contain at least one alphabetic character.")
    return cleaned_key


@app.get("/")
def root():
    return {
        "name": "CipherBreaker API",
        "status": "ok",
        "endpoints": {
            "health": "/health",
            "clean_text": "/clean-text",
            "classify_cipher": "/predict/cipher-type",
            "encrypt_caesar": "/cipher/caesar",
            "encrypt_monoalpha": "/cipher/monoalpha",
            "encrypt_transposition": "/cipher/transposition",
            "encrypt_vigenere": "/cipher/vigenere",
            "features_all": "/features/all",
            "features_frequency": "/features/frequency",
            "features_ioc": "/features/ioc",
            "features_entropy": "/features/entropy",
            "features_ngram": "/features/ngram",
            "features_chi_squared": "/features/chi-squared",
            "features_autocorrelation": "/features/autocorrelation",
            "features_kasiski": "/features/kasiski",
        },
    }


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/clean-text")
def clean_text_api(request: TextRequest):
    return {"cleaned_text": clean_text(request.text)}


@app.post("/predict/cipher-type")
def predict_cipher_type(request: CipherPredictRequest):
    try:
        artifact = load_artifact()
        model = artifact["model"]
        label_encoder = artifact["label_encoder"]

        cleaned_ciphertext, features = extract_feature_list(request.ciphertext)
        prediction = model.predict([features])[0]
        cipher_type = label_encoder.inverse_transform([prediction])[0]
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "ciphertext": request.ciphertext,
        "cleaned_ciphertext": cleaned_ciphertext,
        "cipher_type": cipher_type,
        "features": features,
    }


@app.post("/cipher/caesar")
def caesar_api(request: CaesarRequest):
    return {
        "cipher": "caesar",
        "ciphertext": caesar(request.plaintext, request.shift),
        "shift": request.shift,
    }


@app.post("/cipher/monoalpha")
def monoalpha_api(request: MonoalphaRequest):
    try:
        substitution = validate_substitution_key(request.substitution)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "cipher": "monoalpha",
        "ciphertext": monoalpha(request.plaintext, substitution),
        "substitution": substitution,
    }


@app.post("/cipher/transposition")
def transposition_api(request: TranspositionRequest):
    try:
        key = validate_alpha_key(request.key, "key")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "cipher": "transposition",
        "ciphertext": transposition(request.plaintext, key),
        "key": key,
    }


@app.post("/cipher/vigenere")
def vigenere_api(request: VigenereRequest):
    try:
        key = validate_alpha_key(request.key, "key")
        plaintext = clean_text(request.plaintext)
        if not plaintext:
            raise ValueError("plaintext must contain at least one alphabetic character.")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "cipher": "vigenere",
        "ciphertext": vigenere(plaintext, key),
        "plaintext": plaintext,
        "key": key,
    }


@app.post("/features/all")
def all_features_api(request: TextRequest):
    cleaned_text, features = extract_feature_list(request.text)
    return {
        "cleaned_text": cleaned_text,
        "features": features,
    }


@app.post("/features/frequency")
def frequency_api(request: TextRequest):
    cleaned = clean_text(request.text)
    if not cleaned:
        raise HTTPException(status_code=400, detail="text must contain alphabetic characters.")
    return {"cleaned_text": cleaned, "frequency": frequency(cleaned)}


@app.post("/features/ioc")
def ioc_api(request: TextRequest):
    cleaned = clean_text(request.text)
    if len(cleaned) < 2:
        raise HTTPException(status_code=400, detail="text must contain at least two alphabetic characters.")
    return {"cleaned_text": cleaned, "ioc": ioc(cleaned)}


@app.post("/features/ngram")
def ngram_api(request: NgramRequest):
    cleaned = clean_text(request.text)
    if len(cleaned) < request.n:
        raise HTTPException(status_code=400, detail="text length must be at least n after cleaning.")
    return {"cleaned_text": cleaned, "n": request.n, "ngram": ngram(cleaned, request.n)}


@app.post("/features/entropy")
def entropy_api(request: EntropyRequest):
    cleaned = clean_text(request.text)
    return {
        "cleaned_text": cleaned,
        "n": request.n,
        "entropy": shanon_entropy(cleaned, request.n),
    }


@app.post("/features/chi-squared")
def chi_squared_api(request: TextRequest):
    cleaned = clean_text(request.text)
    if not cleaned:
        raise HTTPException(status_code=400, detail="text must contain alphabetic characters.")
    return {"cleaned_text": cleaned, "chi_squared": chi_sqaured(cleaned)}


@app.post("/features/autocorrelation")
def autocorrelation_api(request: AutoCorrelationRequest):
    cleaned = clean_text(request.text)
    if len(cleaned) < 2:
        raise HTTPException(status_code=400, detail="text must contain at least two alphabetic characters.")
    return {
        "cleaned_text": cleaned,
        "shifts": request.shifts,
        "autocorrelation": auto_correlation(cleaned, request.shifts),
    }


@app.post("/features/kasiski")
def kasiski_api(request: TextRequest):
    cleaned = clean_text(request.text)
    if len(cleaned) < 3:
        raise HTTPException(status_code=400, detail="text must contain at least three alphabetic characters.")
    return {
        "cleaned_text": cleaned,
        "kasiski": kasiski_test(cleaned),
    }
