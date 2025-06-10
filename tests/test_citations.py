import pytest

from utils.citations import to_apa, to_mla, to_chicago

ARTICLE = {
    "author": "Jane Doe",
    "title": "Amazing News",
    "source": "Example Times",
    "published": "2024-05-01",
    "url": "https://example.com/amazing-news",
}


def test_to_apa():
    citation = to_apa(ARTICLE)
    assert "Jane Doe." in citation
    assert "(2024)." in citation
    assert "Amazing News." in citation
    assert "Example Times." in citation
    assert ARTICLE["url"] in citation


def test_to_mla():
    citation = to_mla(ARTICLE)
    assert citation.startswith("Jane Doe.")
    assert '"Amazing News."' in citation
    assert "Example Times," in citation
    assert ARTICLE["url"] in citation


def test_to_chicago():
    citation = to_chicago(ARTICLE)
    assert citation.startswith("Jane Doe.")
    assert '"Amazing News."' in citation
    assert "Example Times." in citation
    assert ARTICLE["url"] in citation
