from datetime import datetime


def _get_year(date_str: str) -> str:
    """Extract year from ISO date string."""
    try:
        return str(datetime.fromisoformat(date_str).year)
    except Exception:
        return "n.d."


def to_apa(article: dict) -> str:
    """Return article citation in APA style."""
    author = article.get("author", "").strip()
    year = _get_year(article.get("published", ""))
    title = article.get("title", "").strip()
    source = article.get("source", "").strip()
    url = article.get("url", "").strip()

    parts = []
    if author:
        parts.append(f"{author}.")
    if year:
        parts.append(f"({year}).")
    if title:
        parts.append(f"{title}.")
    if source:
        parts.append(f"{source}.")
    if url:
        parts.append(url)

    return " ".join(parts)


def to_mla(article: dict) -> str:
    """Return article citation in MLA style."""
    author = article.get("author", "").strip()
    title = article.get("title", "").strip()
    source = article.get("source", "").strip()
    date = article.get("published", "").strip()
    url = article.get("url", "").strip()

    parts = []
    if author:
        parts.append(f"{author}.")
    if title:
        parts.append(f'"{title}."')
    if source:
        parts.append(f"{source},")
    if date:
        parts.append(date + ",")
    if url:
        parts.append(url)

    return " ".join(parts)


def to_chicago(article: dict) -> str:
    """Return article citation in Chicago style."""
    author = article.get("author", "").strip()
    title = article.get("title", "").strip()
    source = article.get("source", "").strip()
    date = article.get("published", "").strip()
    url = article.get("url", "").strip()

    parts = []
    if author:
        parts.append(f"{author}.")
    if title:
        parts.append(f'"{title}."')
    if source:
        parts.append(f"{source}.")
    if date:
        parts.append(date + ".")
    if url:
        parts.append(url)

    return " ".join(parts)
