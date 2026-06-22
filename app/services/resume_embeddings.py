import re

from app.services.vector_store import load_vector_store

# Common software job abbreviations
ABBREVIATIONS = {
    "SDE": "Software Development Engineer",
    "SWE": "Software Engineer",
    "DA": "Data Analyst",
    "DS": "Data Scientist",
    "DE": "Data Engineer",
    "MLE": "Machine Learning Engineer",
    "ML": "Machine Learning",
    "AI": "Artificial Intelligence",
    "QA": "Quality Assurance",
    "FE": "Frontend",
    "BE": "Backend",
    "FS": "Full Stack",
    "PM": "Product Manager",
}


def normalize_query(text: str) -> str:
    """
    Expand common abbreviations and normalize experience phrases
    before semantic search.
    """

    # Expand abbreviations
    for short, full in ABBREVIATIONS.items():
        pattern = rf"\b{re.escape(short)}\b"
        text = re.sub(
            pattern,
            f"{short} {full}",
            text,
            flags=re.IGNORECASE,
        )

    # Freshers / entry level
    text = re.sub(
        r"\bfresher(s)?\b",
        "0 years experience",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\bentry[\s-]?level\b",
        "0 years experience",
        text,
        flags=re.IGNORECASE,
    )

    # Internship
    text = re.sub(
        r"\bintern(ship)?\b",
        "Intern 0 years experience",
        text,
        flags=re.IGNORECASE,
    )

    # Normalize "3 yrs" -> "3 years"
    text = re.sub(
        r"(\d+)\s*\+?\s*(yrs?|years?)",
        r"\1 years",
        text,
        flags=re.IGNORECASE,
    )

    return text


def search_jobs_for_resume_text(raw_text: str, k: int = 10):
    """
    Take resume summary, normalize it,
    and retrieve the most relevant jobs.
    """

    query = normalize_query(raw_text)

    store = load_vector_store()

    retriever = store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )

    docs = retriever.invoke(query)

    return docs
