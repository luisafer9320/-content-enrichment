import requests
import pytest

from scraper.wiki_scraper import WikipediaScraper, scraping_wikipedia


class FakeResponse:
    """Respuesta falsa que simula lo que devuelve requests.get."""

    def __init__(self, text="", status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP error")


class FakeHttpClient:
    """Cliente HTTP falso para probar sin conectarnos a Wikipedia."""

    def __init__(self, response):
        self.response = response
        self.last_url = None

    def get(self, url, headers=None, timeout=10):
        self.last_url = url
        return self.response


def test_fake_response_can_raise_http_error():
    response = FakeResponse(status_code=500)

    with pytest.raises(Exception):
        response.raise_for_status()


def test_search_extracts_title_and_first_five_paragraphs():
    paragraphs = "".join(f"<p>Parrafo largo numero {index} con contenido suficiente para pasar el filtro de longitud del scraper.</p>" for index in range(1, 7))
    html = f"<html><h1 id='firstHeading'>Python</h1>{paragraphs}</html>"
    scraper = WikipediaScraper(http_client=FakeHttpClient(FakeResponse(html)))

    article = scraper.search("Python")

    assert article.title == "Python"
    assert article.content.count("Parrafo largo numero") == 5


def test_search_returns_none_when_article_does_not_exist():
    scraper = WikipediaScraper(http_client=FakeHttpClient(FakeResponse(status_code=404)))

    article = scraper.search("Tema inexistente")

    assert article is None


def test_search_builds_safe_url_for_spaces():
    fake_client = FakeHttpClient(FakeResponse("<h1 id='firstHeading'>Test</h1><p>Este parrafo largo contiene texto suficiente para ser aceptado por el scraper.</p>"))
    scraper = WikipediaScraper(http_client=fake_client)

    scraper.search("Lenguaje Python")

    assert fake_client.last_url.endswith("/Lenguaje_Python")


def test_search_returns_none_for_empty_topic():
    scraper = WikipediaScraper()

    article = scraper.search("  ")

    assert article is None


def test_search_returns_none_when_network_fails():
    class BrokenHttpClient:
        def get(self, url, headers=None, timeout=10):
            raise requests.exceptions.Timeout("sin respuesta")

    scraper = WikipediaScraper(http_client=BrokenHttpClient())

    article = scraper.search("Python")

    assert article is None


def test_search_returns_none_when_html_has_no_useful_paragraphs():
    html = "<html><h1 id='firstHeading'>Python</h1><p>Corto.</p></html>"
    scraper = WikipediaScraper(http_client=FakeHttpClient(FakeResponse(html)))

    article = scraper.search("Python")

    assert article is None


def test_compatibility_function_returns_none_tuple(monkeypatch):
    class EmptyScraper:
        def search(self, topic):
            return None

    monkeypatch.setattr("scraper.wiki_scraper.WikipediaScraper", lambda: EmptyScraper())

    title, content = scraping_wikipedia("Nada")

    assert title is None
    assert content is None


def test_compatibility_function_returns_title_and_content(monkeypatch):
    class SuccessfulScraper:
        def search(self, topic):
            return type("Article", (), {"title": "Titulo", "content": "Contenido"})()

    monkeypatch.setattr("scraper.wiki_scraper.WikipediaScraper", lambda: SuccessfulScraper())

    title, content = scraping_wikipedia("Algo")

    assert title == "Titulo"
    assert content == "Contenido"
