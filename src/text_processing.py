import re


def normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, max_words: int = 120, overlap: int = 25) -> list[str]:
    normalized = normalize_text(text)
    sections = [section.strip() for section in normalized.splitlines() if section.strip()]
    if not sections:
        return []

    chunks = []
    for section in sections:
        words = section.split()
        if len(words) <= max_words:
            chunks.append(section)
            continue

        start = 0
        while start < len(words):
            end = min(start + max_words, len(words))
            chunks.append(" ".join(words[start:end]))
            if end == len(words):
                break
            start = max(end - overlap, start + 1)

    return chunks
