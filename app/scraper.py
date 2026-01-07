import requests
import os
from bs4 import BeautifulSoup
from markdownify import markdownify as md

BASE_URL = "https://support.optisigns.com/api/v2/help_center/en-us/articles.json"
OUTPUT_DIR = "articles"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_articles(page=1):
    url = f"{BASE_URL}?page={page}&per_page=100"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def clean_html_to_markdown(html):
    soup = BeautifulSoup(html, "html.parser")

    # remove nav, footer, ads, script, style
    for tag in soup(["nav", "footer", "aside", "script", "style"]):
        tag.decompose()

    return md(str(soup))

def scrape_articles(limit=30):
    count = 0
    page = 1

    while count < limit:
        data = get_articles(page)
        articles = data.get("articles", [])

        if not articles:
            break

        for art in articles:
            if count >= limit:
                break

            title = art["title"]
            slug = art["html_url"].split("/")[-1]
            body_html = art["body"]

            article_url = art["html_url"]
            markdown = (
                    f"# {title}\n\n"
                    f"Article URL: {article_url}\n\n"
                    + clean_html_to_markdown(body_html)
            )

            file_path = os.path.join(OUTPUT_DIR, f"{slug}.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(markdown)

            print(f"Saved: {file_path}")
            count += 1

        page += 1

if __name__ == "__main__":
    scrape_articles(limit=30)
