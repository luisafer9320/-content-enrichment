import logging

from exporters.file_exporter import FileExporter
from scraper.wiki_scraper import WikipediaScraper
from services.openai_service import OpenAIService
from services.translator.TranslatorService import TranslatorService


def configure_logging() -> None:
    """Configura el archivo de logs solicitado en los requisitos tecnicos."""
    logging.basicConfig(
        filename="app_logging.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )


class ContentEnricherApp:
    """Coordina el flujo completo de la aplicacion de consola."""

    def __init__(self, scraper=None, ai_service=None, translator=None, exporter=None):
        # Cada dependencia tiene una sola responsabilidad y puede probarse por separado.
        self.scraper = scraper or WikipediaScraper()
        self.ai_service = ai_service or OpenAIService()
        self.translator = translator or TranslatorService()
        self.exporter = exporter or FileExporter()

    def run(self) -> None:
        """Ejecuta el flujo principal pedido en el proyecto."""
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
        # Este requisito es extra, por eso se pregunta al usuario si desea usarlo.
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


def ejecutar_sistema() -> None:
    """Funcion de entrada para mantener compatibilidad con el proyecto original."""
    configure_logging()
    ContentEnricherApp().run()


if __name__ == "__main__":  # pragma: no cover
    try:
        ejecutar_sistema()
    except Exception as error:
        logging.exception("Error critico en el sistema principal.")
        print(f"\n[Error Critico] Ocurrio un fallo inesperado: {error}")
