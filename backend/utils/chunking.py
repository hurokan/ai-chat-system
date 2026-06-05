def chunk_text(text: str, size: int = 500):
    text = text.replace("\x00", "")  # IMPORTANT FIX (your error)
    return [text[i:i+size] for i in range(0, len(text), size)]
