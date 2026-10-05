import io
import re
from pypdf import PdfReader
import docx
from rapidfuzz import fuzz

from skills_data import SKILL_LIST, SKILL_ALIASES


def extract_text(filename: str, content: bytes) -> str:
    """Pull raw text out of a PDF, DOCX, or TXT resume file."""
    name = filename.lower()

    if name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages)
        if not text.strip():
            raise ValueError(
                "No readable text found — this PDF may be a scanned image. "
                "Try a text-based PDF, or paste the resume text manually."
            )
        return text

    if name.endswith(".docx"):
        d = docx.Document(io.BytesIO(content))
        return "\n".join(p.text for p in d.paragraphs)

    if name.endswith(".doc"):
        raise ValueError("Old .doc format isn't supported — please save as .docx or .pdf and re-upload.")

    if name.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")


def _word_boundary_match(phrase: str, text_low: str) -> bool:
    """True whole-word/phrase match, so 'c' doesn't match inside 'css' or 'react'."""
    pattern = r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])"
    return re.search(pattern, text_low) is not None


def extract_skills(text: str):
    """
    Keyword + alias matching on whole words/phrases, with a tight fuzzy fallback
    for near-misses (e.g. 'spring-boot' vs 'spring boot', or minor typos).
    This is the baseline approach — swap in sentence-transformers embeddings
    here for the semantic-matching upgrade described in the project report.
    """
    text_low = text.lower()
    # normalise punctuation so "spring-boot" / "node.js" style variants still line up
    text_norm = re.sub(r"[^a-z0-9\s]", " ", text_low)
    words = text_norm.split()
    tokens = set(words)

    found = set()
    for skill in SKILL_LIST:
        if _word_boundary_match(skill, text_low):
            found.add(skill)
            continue
        if any(_word_boundary_match(alias, text_low) for alias in SKILL_ALIASES.get(skill, [])):
            found.add(skill)
            continue
        # fuzzy fallback: only for skills of a reasonable length, compared word-by-word,
        # so we catch typos/formatting quirks without matching unrelated short strings
        if len(skill) >= 4 and " " not in skill:
            if any(fuzz.ratio(skill, tok) >= 90 for tok in tokens if abs(len(tok) - len(skill)) <= 2):
                found.add(skill)

    return sorted(found)
