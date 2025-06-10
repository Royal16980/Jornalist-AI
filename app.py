from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import openai
import os
import json

app = FastAPI()

class Article(BaseModel):
    title: str
    url: str
    source: str
    published_at: str

class BriefRequest(BaseModel):
    articles: list[Article]

@app.post("/brief")
async def brief(req: BriefRequest = Body(...)):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    prompt = (
        """
Summarise the following articles in \u2264150 words bullet-point form, rate overall relevance to the query on 0-100, extract up to 3 direct quotes with attribution.
ARTICLES_JSON = {articles}
""".strip()
    ).format(articles=json.dumps([a.dict() for a in req.articles]))

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    async def streamer():
        for chunk in response:
            delta = chunk["choices"][0].get("delta", {})
            content = delta.get("content")
            if content:
                yield content

    return StreamingResponse(streamer(), media_type="application/json")
