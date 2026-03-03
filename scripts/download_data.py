#!/usr/bin/env python3
import httpx
import zipfile
import os
from pathlib import Path

DATA_DIR = Path("data")
URLS = {
    "small": "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip",
    "1m": "https://files.grouplens.org/datasets/movielens/ml-1m.zip",
}

def download_dataset(size="small"):
    os.makedirs(DATA_DIR, exist_ok=True)
    
    url = URLS[size]
    zip_path = DATA_DIR / f"ml-latest-{size}.zip"
    
    if not zip_path.exists():
        print(f"Downloading {size} dataset...")
        with httpx.Client(follow_redirects=True) as client:
            with client.stream("GET", url) as resp:
                resp.raise_for_status()
                with open(zip_path, "wb") as f:
                    for chunk in resp.iter_bytes(chunk_size=8192):
                        f.write(chunk)
    else:
        print(f"{zip_path} already exists")
    
    # Extract
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(DATA_DIR)
    
    print(f"Dataset ready in {DATA_DIR}")

if __name__ == "__main__":
    download_dataset("small")
