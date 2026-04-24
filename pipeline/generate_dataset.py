import csv
import random
from pipeline.get_sample import get_sample
from pipeline.extract_features import extract_features

def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_random_chunk(text = load_text("Data/book.txt"), min_len=150, max_len=200):
    length = random.randint(min_len, max_len)

    if len(text) < length:
        return text

    start = random.randint(0, len(text) - length)
    return text[start:start + length]

def generate_dataset(num_samples=1000, filename="Data/dataset.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        # header
        header = [f"f{i}" for i in range(41)] + ["label"]
        writer.writerow(header)

        for i in range(num_samples):
            ciphertext, label, key = get_sample(get_random_chunk())

            # extract features here
            features = extract_features(ciphertext)

            writer.writerow(features + [label])

            if i % 100 == 0:
                print(f"{i} samples generated...")

    print(f"\nDataset saved to {filename}")


if __name__ == "__main__":
    generate_dataset(num_samples=5000)