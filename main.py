from app.scraper import scrape_articles
from app.uploader import create_vector_store, upload_files_to_vector_store

def main():
    print("Scraping articles...")
    scrape_articles(limit=30)

    print("Creating vector store...")
    vs_id = create_vector_store()

    print("Uploading to vector store...")
    upload_files_to_vector_store(vs_id)

    print("Done.")

if __name__ == "__main__":
    main()
