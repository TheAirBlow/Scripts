#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
import hashlib
import signal
import sys
import os

def term(signum, frame):
    print("Exiting...")
    sys.exit(-1)

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(1048576), b""):
            hasher.update(block)
    return hasher.hexdigest()

hashes = list()
deleted = 0
unique = 0
def check_file(file_path):
    global hashes, deleted, unique
    file_hash = hash_file(file_path)
    if file_hash in hashes:
        print("[-]", file_path)
        os.remove(file_path)
        deleted += 1
    else:
        print("[+]", file_path)
        hashes.append(file_hash)
        unique += 1

signal.signal(signal.SIGINT, term)
with ThreadPoolExecutor(max_workers = 8) as executor:
    print("This will recursively DELETE duplicate files.")
    choice = input("Do you want to continue? [y/N] ").strip().lower()
    if choice != 'y':
        print("Cancelled by user")
        sys.exit(-1)

    hashes = list()
    for root, dirs, files in os.walk('.'):
        for name in files:
            file_path = os.path.join(root, name)
            executor.submit(check_file, file_path)

    executor.shutdown(wait=True)
print(f"{deleted} duplicates of {unique} unique files deleted")
