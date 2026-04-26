from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from joblib import load
from pydantic import BaseModel

from pipeline.extract_features import extract_features


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


class PredictRequest(BaseModel):
    ciphertext: str


def load_artifact():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. Train the classifier first."
        )
    return load(MODEL_PATH)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/predict/cipher-type")
def predict_cipher_type(request: PredictRequest):
    try:
        artifact = load_artifact()
        model = artifact["model"]
        label_encoder = artifact["label_encoder"]

        features = extract_features(request.ciphertext)
        prediction = model.predict([features])[0]
        cipher_type = label_encoder.inverse_transform([prediction])[0]
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "ciphertext": request.ciphertext,
        "cipher_type": cipher_type,
    }
