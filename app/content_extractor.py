import requests
from bs4 import BeautifulSoup


def fetch_text_simple(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        print("Status:", response.status_code)
    except Exception as e:
        print("Error:", e)
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")

    texts = [p.get_text(strip=True) for p in paragraphs]

    return "\n".join(texts)


if __name__ == "__main__":
    urls = [
        "https://forbes.kz",
        "https://www.bbc.com",
        "https://www.reuters.com",
    ]

    for url in urls:
        print(f"\n--- {url} ---\n")
        text = fetch_text_simple(url)
        print(text[:1500])