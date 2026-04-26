import csv
import random
from pathlib import Path

from clean_text.clean_text import clean_text
from pipeline.extract_features import extract_features
from pipeline.get_sample import get_sample


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "Data"
BOOK_PATH = DATA_DIR / "book.txt"
DATASET_PATH = DATA_DIR / "dataset.csv"


def load_text(file_path):
    return Path(file_path).read_text(encoding="utf-8")


def load_book_text(file_path=BOOK_PATH):
    book_text = clean_text(load_text(file_path))

    if not book_text:
        raise ValueError(
            f"No alphabetic text found in {file_path}. Add content to book.txt before generating the dataset."
        )

    return book_text


def get_random_chunk(text, min_len=150, max_len=200):
    if not text:
        raise ValueError("Cannot sample from empty text.")

    if min_len <= 0 or max_len <= 0:
        raise ValueError("Chunk lengths must be positive integers.")

    if min_len > max_len:
        raise ValueError("min_len cannot be greater than max_len.")

    chunk_length = min(random.randint(min_len, max_len), len(text))

    if chunk_length == len(text):
        return text

    start = random.randint(0, len(text) - chunk_length)
    return text[start:start + chunk_length]


def generate_dataset(
    num_samples=1000,
    filename=DATASET_PATH,
    book_path=BOOK_PATH,
    min_len=150,
    max_len=200,
):
    if num_samples <= 0:
        raise ValueError("num_samples must be greater than 0.")

    source_text = load_book_text(book_path)
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        feature_count = None

        for i in range(num_samples):
            plaintext = get_random_chunk(source_text, min_len=min_len, max_len=max_len)
            ciphertext, cipher_type, _, plaintext = get_sample(plaintext)
            features = extract_features(ciphertext)

            if feature_count is None:
                feature_count = len(features)
                header = ["ciphertext", "plaintext", "cipher_type"] + [
                    f"f{i}" for i in range(feature_count)
                ]
                writer.writerow(header)

            writer.writerow([ciphertext, plaintext, cipher_type] + features)

            if (i + 1) % 100 == 0 or i == num_samples - 1:
                print(f"{i + 1}/{num_samples} samples generated...")

    print(f"\nDataset saved to {output_path}")
    return output_path


if __name__ == "__main__":
    generate_dataset(num_samples=50000)
