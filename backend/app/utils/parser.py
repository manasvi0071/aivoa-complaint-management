import pdfplumber
import io


def extract_text_from_file(filename: str, file_bytes: bytes) -> str:
    """Extract raw text from PDF, email (.txt/.eml), or fallback to plain decode."""
    lower = filename.lower()

    if lower.endswith(".pdf"):
        text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()

    # .txt, .eml, or anything else — treat as plain text
    try:
        return file_bytes.decode("utf-8", errors="ignore").strip()
    except Exception:
        return ""