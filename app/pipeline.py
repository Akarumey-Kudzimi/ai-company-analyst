from urllib.parse import urlparse

from search_provider import DuckDuckGoSearchProvider
from content_extractor import fetch_text_simple


ALLOWED_TEXT_DOMAINS = [
    "wikipedia.org",
    "ruwiki.ru",
    "forbes.kz",
    "yahoo.com",
    "finance.yahoo.com",
    "marketscreener.com",
    "prnewswire.com",
    "globenewswire.com",
    "kase.kz",
    "kaspi.kz",
    "ir.kaspi.kz",
    "pk.uchet.kz",
    "ba.prg.kz",
    "kontakt.kz",
    "emis.com",
    "hh.kz",
    "almaty.hh.kz",
    "small.kz",
]

REVIEW_DOMAINS = [
    "glassdoor.",
    "indeed.",
    "teamblind.",
    "hh.kz",
    "almaty.hh.kz",
]


def get_domain(url: str) -> str:
    return urlparse(url).netloc.lower()


def is_allowed_text_source(url: str) -> bool:
    return any(domain in url.lower() for domain in ALLOWED_TEXT_DOMAINS)


def is_review_source(url: str) -> bool:
    return any(domain in url.lower() for domain in REVIEW_DOMAINS)


def collect_company_data(company_name: str) -> dict:
    provider = DuckDuckGoSearchProvider()
    search_results = provider.search_company_sources(company_name)

    source_texts = []
    review_snippets = []

    for result in search_results:
        domain = get_domain(result.url)

        if is_review_source(result.url):
            print(f"Review snippet found: {result.url}")

            review_snippets.append({
                "title": result.title,
                "url": result.url,
                "domain": domain,
                "snippet": result.snippet,
            })

            continue

        if not is_allowed_text_source(result.url):
            print(f"Skipping: {result.url}")
            continue

        print(f"\nFetching text source: {result.url}")

        text = fetch_text_simple(result.url)

        if not text:
            print("No text extracted")
            continue

        source_texts.append({
            "title": result.title,
            "url": result.url,
            "domain": domain,
            "text": text[:5000],
        })

        if len(source_texts) >= 3:
            break

    if not source_texts and review_snippets:
        print("\n⚠️ Using review snippets as fallback data")

        for item in review_snippets[:3]:
            source_texts.append({
                "title": item["title"],
                "url": item["url"],
                "domain": item["domain"],
                "text": item["snippet"],
            })

    return {
        "company_name": company_name,
        "source_texts": source_texts,
        "review_snippets": review_snippets,
    }
