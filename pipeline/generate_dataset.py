import csv
from pipeline.get_sample import get_sample


def generate_dataset(num_samples=1000, filename="dataset.csv"):
    data = []

    # Generate data
    for i in range(num_samples):
        features, label = get_sample()
        data.append(features + [label])

        if i % 100 == 0:
            print(f"{i} samples generated...")

    # Write to CSV
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        # Optional header
        num_features = len(data[0]) - 1
        header = [f"f{i}" for i in range(num_features)] + ["label"]
        writer.writerow(header)

        writer.writerows(data)

    print(f"\nDataset saved to {filename}")


if __name__ == "__main__":
    generate_dataset(num_samples=5000)