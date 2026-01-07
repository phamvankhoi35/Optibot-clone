import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VECTOR_STORE_NAME = "optibot-knowledge"
ARTICLES_DIR = "articles"

def create_vector_store():
    vs = client.vector_stores.create(name=VECTOR_STORE_NAME)
    print("Created Vector Store:", vs.id)
    return vs.id

def upload_files_to_vector_store(vector_store_id):
    files = []
    for fname in os.listdir(ARTICLES_DIR):
        if fname.endswith(".md"):
            path = os.path.join(ARTICLES_DIR, fname)
            files.append(open(path, "rb"))

    print("Uploading", len(files), "files...")

    file_batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id,
        files=files
    )

    print("Upload status:", file_batch.status)
    print("File counts:", file_batch.file_counts)
    return file_batch.file_counts

if __name__ == "__main__":
    vs_id = create_vector_store()
    upload_files_to_vector_store(vs_id)
