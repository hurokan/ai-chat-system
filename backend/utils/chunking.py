def chunk_text(text: str, size: int = 1000, overlap: int = 200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap

    return chunks

