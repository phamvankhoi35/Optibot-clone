import os
from openai import OpenAI
from dotenv import load_dotenv
from app.hash_utils import file_hash
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VECTOR_STORE_NAME = "optibot-knowledge"
ARTICLES_DIR = "articles"
HASH_FILE = "data/file_hashes.json"

def load_old_hashes():
    if not os.path.exists(HASH_FILE):
        return {}

    try:
        with open(HASH_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except Exception as e:
        print("Warning: Could not read file_hashes.json, starting fresh.")
        return {}

def save_hashes(hashes):
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=2)

def create_vector_store():
    vs = client.vector_stores.create(name=VECTOR_STORE_NAME)
    print("Created Vector Store:", vs.id)
    return vs.id

def upload_files_to_vector_store(vector_store_id):
    old_hashes = load_old_hashes()
    new_hashes = {}

    added = 0
    updated = 0
    skipped = 0
    files_to_upload = []

    for fname in os.listdir(ARTICLES_DIR):
        if not fname.endswith(".md"):
            continue

        path = os.path.join(ARTICLES_DIR, fname)
        h = file_hash(path)
        new_hashes[fname] = h

        if fname not in old_hashes:
            files_to_upload.append(open(path, "rb"))
            added += 1
        elif old_hashes[fname] != h:
            files_to_upload.append(open(path, "rb"))
            updated += 1
        else:
            skipped += 1

    if files_to_upload:
        batch = client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id,
            files=files_to_upload
        )
        print("Upload status:", batch.status)

    save_hashes(new_hashes)

    print(f"Added: {added}, Updated: {updated}, Skipped: {skipped}")
    return added, updated, skipped
