from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from urllib.parse import unquote

from utils.citations import to_apa, to_mla, to_chicago

app = FastAPI()


# Placeholder article fetcher
async def fetch_article(url: str) -> dict:
    """Fetch article metadata. This is a placeholder that simply returns
    minimal data based on the URL. In a real application this would search
    providers or a database."""
    # For demonstration, only use the URL's hostname as source and the path as title.
    from urllib.parse import urlparse

    parsed = urlparse(url)
    title = parsed.path.rsplit('/', 1)[-1] or parsed.netloc
    return {
        "author": "Unknown",
        "title": title.replace('-', ' ').title(),
        "source": parsed.netloc,
        "published": "",
        "url": url,
    }


@app.get("/citation")
async def get_citation(style: str = Query("apa"), url: str = Query(...)):
    article_url = unquote(url)
    article = await fetch_article(article_url)

    if style.lower() == "apa":
        citation = to_apa(article)
    elif style.lower() == "mla":
        citation = to_mla(article)
    elif style.lower() == "chicago":
        citation = to_chicago(article)
    else:
        raise HTTPException(status_code=400, detail="Unknown style")

    return JSONResponse({"citation": citation})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
