import json
import main
from scraper.wiki_scraper import WikipediaArticle
from main import ContentEnricherApp, app, build_web_report, configure_logging, ejecutar_sistema


class FakeScraper:
    def search(self, topic):
        return WikipediaArticle(title="Python", content="Contenido original")


class FakeAIService:
    def enrich_text(self, original_content):
        return f"{original_content} enriquecido"

    def summarize_text(self, enriched_content):
        return f"Resumen de {enriched_content}"


class FakeTranslator:
    def translate(self, enriched_content, language):
        return f"{enriched_content} traducido a {language}"


class FakeExporter:
    def __init__(self):
        self.calls = []

    def export(self, filename, file_format, title, original, enriched, translated, summary):
        self.calls.append((filename, file_format, title, original, enriched, translated, summary))
        return "salida.txt"


def test_full_console_flow_exports_report(monkeypatch, capsys):
    exporter = FakeExporter()
    app = ContentEnricherApp(
        scraper=FakeScraper(),
        ai_service=FakeAIService(),
        translator=FakeTranslator(),
        exporter=exporter,
    )
    answers = iter(["Python", "en", "s", "s", "salida", "txt"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))

    app.run()

    output = capsys.readouterr().out
    assert "RESULTADO DE WIKIPEDIA" in output
    assert "CONTENIDO ENRIQUECIDO CON IA" in output
    assert "CONTENIDO TRADUCIDO" in output
    assert exporter.calls == [
        (
            "salida",
            "txt",
            "Python",
            "Contenido original",
            "Contenido original enriquecido",
            "Contenido original enriquecido traducido a en",
            "Resumen de Contenido original enriquecido",
        )
    ]


def test_console_flow_stops_when_wikipedia_has_no_result(monkeypatch, capsys):
    class EmptyScraper:
        def search(self, topic):
            return None

    app = ContentEnricherApp(scraper=EmptyScraper(), ai_service=FakeAIService())
    answers = iter(["Tema raro", "en"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))

    app.run()

    output = capsys.readouterr().out
    assert "No se pudo obtener informacion de Wikipedia" in output


def test_console_flow_stops_when_required_fields_are_empty(monkeypatch, capsys):
    app = ContentEnricherApp()
    answers = iter(["", "en"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))

    app.run()

    output = capsys.readouterr().out
    assert "El tema y el idioma destino son obligatorios" in output


def test_console_flow_can_skip_summary_and_export(monkeypatch, capsys):
    app = ContentEnricherApp(
        scraper=FakeScraper(),
        ai_service=FakeAIService(),
        translator=FakeTranslator(),
        exporter=FakeExporter(),
    )
    answers = iter(["Python", "en", "n", "n"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))

    app.run()

    output = capsys.readouterr().out
    assert "Proceso finalizado" in output


def test_console_flow_prints_export_error(monkeypatch, capsys):
    class ErrorExporter:
        def export(self, filename, file_format, title, original, enriched, translated, summary):
            raise ValueError("Formato no soportado")

    app = ContentEnricherApp(
        scraper=FakeScraper(),
        ai_service=FakeAIService(),
        translator=FakeTranslator(),
        exporter=ErrorExporter(),
    )
    answers = iter(["Python", "en", "n", "s", "salida", "docx"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))

    app.run()

    output = capsys.readouterr().out
    assert "Formato no soportado" in output


def test_console_flow_prints_disk_export_error(monkeypatch, capsys):
    class DiskErrorExporter:
        def export(self, filename, file_format, title, original, enriched, translated, summary):
            raise OSError("permiso denegado")

    app = ContentEnricherApp(
        scraper=FakeScraper(),
        ai_service=FakeAIService(),
        translator=FakeTranslator(),
        exporter=DiskErrorExporter(),
    )
    answers = iter(["Python", "en", "n", "s", "salida", "txt"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))

    app.run()

    output = capsys.readouterr().out
    assert "No se pudo guardar el archivo en el disco" in output


def test_configure_logging_calls_basic_config(monkeypatch):
    called = {}

    def fake_basic_config(**kwargs):
        called.update(kwargs)

    monkeypatch.setattr("logging.basicConfig", fake_basic_config)

    configure_logging()

    assert called["filename"] == "app_logging.log"
    assert called["encoding"] == "utf-8"


def test_ejecutar_sistema_configures_and_runs_app(monkeypatch):
    called = {"logging": False, "run": False}

    class FakeApp:
        def run(self):
            called["run"] = True

    monkeypatch.setattr(main, "configure_logging", lambda: called.update({"logging": True}))
    monkeypatch.setattr(main, "ContentEnricherApp", lambda: FakeApp())

    ejecutar_sistema()

    assert called == {"logging": True, "run": True}


def test_build_web_report_validates_required_parameters():
    data, status_code = build_web_report("", "en")

    assert status_code == 400
    assert "obligatorios" in data["error"]


def test_build_web_report_returns_404_when_wikipedia_fails(monkeypatch):
    class EmptyScraper:
        def search(self, topic):
            return None

    monkeypatch.setattr(main, "WikipediaScraper", lambda: EmptyScraper())

    data, status_code = build_web_report("Nada", "en")

    assert status_code == 404
    assert "Wikipedia" in data["error"]


def test_build_web_report_returns_complete_data(monkeypatch):
    monkeypatch.setattr(main, "WikipediaScraper", lambda: FakeScraper())
    monkeypatch.setattr(main, "OpenAIService", lambda: FakeAIService())
    monkeypatch.setattr(main, "TranslatorService", lambda: FakeTranslator())

    data, status_code = build_web_report("Python", "en", include_summary=True)

    assert status_code == 200
    assert data["title"] == "Python"
    assert data["summary"] == "Resumen de Contenido original enriquecido"
    assert data["translated"] == "Contenido original enriquecido traducido a en"


def test_vercel_app_root_returns_status_json():
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = headers

    response = app({"PATH_INFO": "/", "QUERY_STRING": ""}, start_response)
    data = json.loads(response[0].decode("utf-8"))

    assert captured["status"] == "200 OK"
    assert data["status"] == "ok"


def test_vercel_app_api_returns_report(monkeypatch):
    captured = {}

    def fake_build_web_report(topic, language, include_summary):
        return {"topic": topic, "language": language, "summary": include_summary}, 200

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = headers

    monkeypatch.setattr(main, "build_web_report", fake_build_web_report)

    response = app({"PATH_INFO": "/api/enrich", "QUERY_STRING": "topic=Python&language=en&summary=true"}, start_response)
    data = json.loads(response[0].decode("utf-8"))

    assert captured["status"] == "200 OK"
    assert data == {"topic": "Python", "language": "en", "summary": True}
