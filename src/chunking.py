import re

ARTICLE_PATTERN = r"(Article\s+\d+|ARTICLE\s+\d+|Art\.\s*\d+)"

def clean_text(text: str) -> str:
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def split_by_articles(text: str):
    parts = re.split(ARTICLE_PATTERN, text)

    chunks = []
    for i in range(1, len(parts), 2):
        article = parts[i].strip()
        content = parts[i + 1].strip()

        if len(content) < 50:
            continue  # ignore bruit

        chunks.append({
            "article": article,
            "text": content
        })

    return chunks
