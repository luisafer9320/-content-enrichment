import logging
import json
from urllib.parse import parse_qs

from exporters.file_exporter import FileExporter
from scraper.wiki_scraper import WikipediaScraper
from services.openai_service import OpenAIService
from services.translator.TranslatorService import TranslatorService


def configure_logging() -> None:
    logging.basicConfig(
        filename="app_logging.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )


class ContentEnricherApp:
    def __init__(self, scraper=None, ai_service=None, translator=None, exporter=None):
        self.scraper = scraper or WikipediaScraper()
        self.ai_service = ai_service or OpenAIService()
        self.translator = translator or TranslatorService()
        self.exporter = exporter or FileExporter()

    def run(self) -> None:
        self._print_header()
        logging.info("El usuario inicio el sistema.")

        topic = input("1. Ingrese el tema a investigar en Wikipedia: ").strip()
        language = input("2. Ingrese el idioma destino para la traduccion (ej: en, fr, it, de): ").strip()

        if not topic or not language:
            print("[Error] El tema y el idioma destino son obligatorios.")
            logging.warning("Ejecucion cancelada por campos vacios.")
            return

        article = self._search_wikipedia(topic)
        if article is None:
            print("[Error] No se pudo obtener informacion de Wikipedia. Intente con otro tema.")
            return

        self._print_section("RESULTADO DE WIKIPEDIA")
        print(f"Titulo: {article.title}\n")
        print(article.content)

        enriched = self._enrich(article.content)
        self._print_section("CONTENIDO ENRIQUECIDO CON IA")
        print(enriched)

        summary = self._ask_for_summary(enriched)
        translated = self._translate(enriched, language)
        self._print_section("CONTENIDO TRADUCIDO")
        print(translated)

        self._ask_for_export(article.title, article.content, enriched, translated, summary)
        print("\nProceso finalizado. Revise app_logging.log para ver el historial.")
        logging.info("Flujo completado correctamente.")

    def _print_header(self) -> None:
        print("=" * 70)
        print(" SISTEMA DE INVESTIGACION, ENRIQUECIMIENTO Y TRADUCCION")
        print("=" * 70)

    def _print_section(self, title: str) -> None:
        print("\n" + "-" * 70)
        print(f"--- {title} ---")
        print("-" * 70)

    def _search_wikipedia(self, topic: str):
        print(f"\n[Procesando] Buscando '{topic}' en Wikipedia...")
        return self.scraper.search(topic)

    def _enrich(self, original_content: str) -> str:
        print("\n[Procesando] Enviando contenido a OpenAI para enriquecimiento...")
        return self.ai_service.enrich_text(original_content)

    def _ask_for_summary(self, enriched_content: str) -> str:
        wants_summary = input("\nDesea generar un resumen con ChatGPT? (s/n): ").strip().lower()
        if wants_summary != "s":
            return ""

        print("[Procesando] Generando resumen...")
        summary = self.ai_service.summarize_text(enriched_content)
        self._print_section("RESUMEN EJECUTIVO")
        print(summary)
        return summary

    def _translate(self, enriched_content: str, language: str) -> str:
        print(f"\n[Procesando] Traduciendo contenido al idioma '{language}'...")
        return self.translator.translate(enriched_content, language)

    def _ask_for_export(self, title: str, original: str, enriched: str, translated: str, summary: str) -> None:
        wants_export = input("\nDesea guardar el resultado en un archivo? (s/n): ").strip().lower()
        if wants_export != "s":
            logging.info("El usuario decidio no exportar archivo.")
            return

        filename = input("Nombre del archivo sin extension: ").strip()
        file_format = input("Formato de salida (txt/pdf): ").strip().lower()

        try:
            output_path = self.exporter.export(filename, file_format, title, original, enriched, translated, summary)
            print(f"Archivo guardado correctamente: {output_path}")
        except ValueError as error:
            print(f"[Error] {error}")
            logging.error("No se pudo exportar archivo: %s", error)
        except OSError as error:
            print(f"[Error] No se pudo guardar el archivo en el disco: {error}")
            logging.error("Error de sistema al exportar archivo: %s", error)


def build_web_report(topic: str, language: str, include_summary: bool = False) -> tuple[dict, int]:
    if not topic or not language:
        return {"error": "Los parametros 'topic' y 'language' son obligatorios."}, 400

    scraper = WikipediaScraper()
    ai_service = OpenAIService()
    translator = TranslatorService()

    article = scraper.search(topic)
    if article is None:
        return {"error": "No se pudo obtener informacion de Wikipedia para el tema solicitado."}, 404

    enriched = ai_service.enrich_text(article.content)
    summary = ai_service.summarize_text(enriched) if include_summary else ""
    translated = translator.translate(enriched, language)

    return {
        "topic": topic,
        "language": language,
        "title": article.title,
        "original": article.content,
        "enriched": enriched,
        "summary": summary,
        "translated": translated,
    }, 200


def _json_response(start_response, data: dict, status_code: int = 200):
    status_text = "OK" if status_code < 400 else "ERROR"
    body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    headers = [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(body))),
    ]
    start_response(f"{status_code} {status_text}", headers)
    return [body]


def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    query = parse_qs(environ.get("QUERY_STRING", ""))

    if path == "/api/enrich":
        topic = query.get("topic", [""])[0].strip()
        language = query.get("language", [""])[0].strip()
        include_summary = query.get("summary", ["false"])[0].lower() in {"1", "true", "s", "si", "yes"}
        data, status_code = build_web_report(topic, language, include_summary)
        return _json_response(start_response, data, status_code)

    return _json_response(
        start_response,
        {
            "name": "Content Enricher",
            "status": "ok",
            "message": "Proyecto desplegado correctamente en Vercel.",
            "usage": "/api/enrich?topic=Python&language=en&summary=true",
        },
    )


application = app
handler = app


def ejecutar_sistema() -> None:
    configure_logging()
    ContentEnricherApp().run()


if __name__ == "__main__":
    try:
        ejecutar_sistema()
    except Exception as error:
        logging.exception("Error critico en el sistema principal.")
        print(f"\n[Error Critico] Ocurrio un fallo inesperado: {error}")
