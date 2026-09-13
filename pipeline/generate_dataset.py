import csv
import random
from pathlib import Path
from multiprocessing import Pool, cpu_count

from clean_text.clean_text import clean_text
from pipeline.extract_features import extract_features
from pipeline.get_sample import get_sample


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "Data"
BOOK_PATH = DATA_DIR / "book.txt"
DATASET_PATH = DATA_DIR / "dataset.csv"


# -------------------------------
# LOAD TEXT ONCE (GLOBAL)
# -------------------------------
def load_text(file_path):
    return Path(file_path).read_text(encoding="utf-8")


def load_book_text(file_path=BOOK_PATH):
    book_text = clean_text(load_text(file_path))
    if not book_text:
        raise ValueError("Empty cleaned text.")
    return book_text


TEXT = load_book_text()  # shared across processes (fork on Linux/mac)


# -------------------------------
# FAST RANDOM CHUNK
# -------------------------------
def get_random_chunk(text, min_len=150, max_len=200):
    chunk_length = random.randint(min_len, max_len)
    start = random.randint(0, len(text) - chunk_length)
    return text[start:start + chunk_length]


# -------------------------------
# WORKER FUNCTION (BATCH)
# -------------------------------
def generate_batch(batch_size):
    rows = []

    for _ in range(batch_size):
        plaintext = get_random_chunk(TEXT)
        ciphertext, cipher_type, _, plaintext = get_sample(plaintext)
        features = extract_features(ciphertext)

        rows.append([ciphertext, plaintext, cipher_type] + features)

    return rows


# -------------------------------
# MAIN GENERATOR
# -------------------------------
def generate_dataset(
    num_samples=200000,
    batch_size=10_000,
    filename=DATASET_PATH,
):
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    num_workers = cpu_count()
    num_batches = num_samples // batch_size

    print(f"Using {num_workers} cores ⚡")

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        with Pool(num_workers) as pool:
            for i, batch in enumerate(pool.imap_unordered(generate_batch, [batch_size] * num_batches)):

                # Write header once
                if i == 0:
                    feature_count = len(batch[0]) - 3
                    header = ["ciphertext", "plaintext", "cipher_type"] + [
                        f"f{i}" for i in range(feature_count)
                    ]
                    writer.writerow(header)

                writer.writerows(batch)

                if (i + 1) % 10 == 0:
                    print(f"{(i + 1) * batch_size:,} samples done")

    print(f"\nDataset saved to {output_path}")

if __name__ == "__main__":
    generate_dataset()