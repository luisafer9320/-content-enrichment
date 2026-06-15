import logging
from dataclasses import dataclass
from typing import Optional, Tuple
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup


@dataclass
class WikipediaArticle:
    """Representa los datos minimos que necesitamos de un articulo."""

    title: str
    content: str


class WikipediaScraper:
    """Se encarga solo de buscar y extraer contenido desde Wikipedia."""

    def __init__(self, base_url: str = "https://es.wikipedia.org/wiki", http_client=requests):
        # Guardamos la URL base y el cliente HTTP para poder probar esta clase sin internet.
        self.base_url = base_url.rstrip("/")
        self.http_client = http_client

    def search(self, topic: str) -> Optional[WikipediaArticle]:
        """Busca un tema y devuelve el titulo y los primeros cinco parrafos utiles."""
        clean_topic = topic.strip()
        if not clean_topic:
            logging.warning("WikipediaScraper recibio un tema vacio.")
            return None

        url = self._build_url(clean_topic)
        logging.info("Consultando Wikipedia para el tema: %s", clean_topic)

        try:
            response = self.http_client.get(url, headers=self._headers(), timeout=10)
            if response.status_code == 404:
                logging.error("Articulo no encontrado en Wikipedia: %s", clean_topic)
                return None

            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            logging.error("Error de red consultando Wikipedia: %s", error)
            return None

        return self._parse_article(response.text)

    def _build_url(self, topic: str) -> str:
        # quote evita problemas con espacios, tildes u otros caracteres especiales en la URL.
        safe_topic = quote(topic.replace(" ", "_"))
        return f"{self.base_url}/{safe_topic}"

    def _headers(self) -> dict:
        # Wikipedia recomienda identificar la aplicacion con un User-Agent.
        return {"User-Agent": "ContentEnricher/1.0 (student project)"}

    def _parse_article(self, html: str) -> Optional[WikipediaArticle]:
        # BeautifulSoup convierte el HTML en un arbol facil de consultar.
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("h1", id="firstHeading")
        title = title_tag.get_text(strip=True) if title_tag else "Articulo de Wikipedia"

        paragraphs = []
        for paragraph in soup.find_all("p"):
            text = paragraph.get_text(" ", strip=True)
            if len(text) > 60:
                paragraphs.append(text)
            if len(paragraphs) == 5:
                break

        if not paragraphs:
            logging.error("Wikipedia no devolvio parrafos utiles para el articulo.")
            return None

        logging.info("Wikipedia devolvio %s parrafos utiles.", len(paragraphs))
        return WikipediaArticle(title=title, content="\n\n".join(paragraphs))


def scraping_wikipedia(tema: str) -> Tuple[Optional[str], Optional[str]]:
    """Funcion de compatibilidad usada por versiones anteriores del proyecto."""
    article = WikipediaScraper().search(tema)
    if article is None:
        return None, None
    return article.title, article.content
