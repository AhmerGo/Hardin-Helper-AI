import os
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse, unquote


def scrape_and_clean(url, headers, session):
    try:
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}: Status code {response.status_code}")
            return None, None

        soup = BeautifulSoup(response.content, 'html.parser')

        for inline_tag in soup.find_all(['b', 'strong', 'i', 'em', 'span']):
            if inline_tag.string:
                inline_tag.string.replace_with(f" {inline_tag.string} ")

        title = soup.title.string if soup.title else urlparse(url).path.split('/')[-1]  # Fallback to URL path if title is missing
        title = title.replace('/', '_').replace(' ', '_')  # Replace slashes and spaces with underscores

        paragraphs = soup.find_all('p')
        text = ' '.join(p.get_text(" ", strip=True) for p in paragraphs)

        cleaned_text = ' '.join(text.split()).replace('\u200B', '')
        return cleaned_text, title

    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None, None


def save_to_text_file(text, title, url, base_dir='./Dataset'):
    filename = f"{title}.txt"
    filepath = os.path.join(base_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"URL: {url}\n\n{text}\n")  # Include URL at the beginning

    print(f"Saved text to {filepath}")


def main():
    urls_file = "Website_URLS/website_urls.txt"

    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }

    session = requests.Session()

    for url in urls:
        print(f"Scraping {url}")
        text, title = scrape_and_clean(url, headers, session)
        if text and title:
            save_to_text_file(text, title, url)
        else:
            print(f"Failed to scrape text from {url}")

        time.sleep(1)


if __name__ == "__main__":
    main()
