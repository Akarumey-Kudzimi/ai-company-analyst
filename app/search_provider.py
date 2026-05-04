from dataclasses import dataclass

from ddgs import DDGS


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    source_type: str = "web_search"


class SearchProviderError(Exception):
    pass


class DuckDuckGoSearchProvider:
    def search_company_sources(self, company_name: str) -> list[SearchResult]:
        query = (
            f'"{company_name}" компания отзывы сотрудников работа '
            f'карьера вакансии культура условия'
        )

        results: list[SearchResult] = []

        try:
            with DDGS(timeout=20) as ddgs:
                for item in ddgs.text(query, max_results=10):
                    results.append(
                        SearchResult(
                            title=item.get("title", ""),
                            url=item.get("href", ""),
                            snippet=item.get("body", ""),
                        )
                    )
        except Exception as error:
            raise SearchProviderError(
                f"Search provider failed: {error}"
            ) from error

        return results


if __name__ == "__main__":
    provider = DuckDuckGoSearchProvider()

    try:
        results = provider.search_company_sources("Kaspi.kz")
    except SearchProviderError as error:
        print(error)
    else:
        for result in results:
            print("\n---")
            print("TITLE:", result.title)
            print("URL:", result.url)
            print("SNIPPET:", result.snippet[:300])