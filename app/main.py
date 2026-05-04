from pipeline import collect_company_data
from llm_analyzer import analyze_company_data


def main():
    company_name = input("Введите название компании: ").strip()

    if not company_name:
        print("Название компании не может быть пустым")
        return

    print(f"\n🔎 Анализируем: {company_name}\n")

    data = collect_company_data(company_name)

    if not data["source_texts"] and not data["review_snippets"]:
        print("\n⚠️ Не удалось найти информацию по компании.")
        print("Попробуй указать более точное название (например: Kaspi.kz, Google, Yandex)")
        return

    print("\n=== RESULT SUMMARY ===")
    print("Company:", data["company_name"])
    print("Text sources:", len(data["source_texts"]))
    print("Review snippets:", len(data["review_snippets"]))

    # 🔥 пока просто заглушка
    analysis = analyze_company_data(data)

    print("\n=== ANALYSIS ===")
    print(analysis)


if __name__ == "__main__":
    main()