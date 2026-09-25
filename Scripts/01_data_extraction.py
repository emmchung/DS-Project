import tarfile
import os

tar_path = r"C:\Users\bryso\Downloads\Yelp-Json.tar"
extract_to = r"C:\Users\bryso\Downloads\Yelp-JSON"

os.makedirs(extract_to, exist_ok=True)

with tarfile.open(tar_path, "r") as tar:
    tar.extractall(path=extract_to)

print("Extracted to:", extract_to)
