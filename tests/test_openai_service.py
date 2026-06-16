from services.openai_service import OpenAIService, enriquecer_con_ai, generar_resumen


class FakeMessage:
    content = "Respuesta generada por OpenAI"


class FakeChoice:
    message = FakeMessage()


class FakeCompletions:
    def create(self, **kwargs):
        self.kwargs = kwargs
        return type("FakeResponse", (), {"choices": [FakeChoice()]})()


class FakeChat:
    def __init__(self):
        self.completions = FakeCompletions()


class FakeClient:
    def __init__(self):
        self.chat = FakeChat()


class BrokenCompletions:
    def create(self, **kwargs):
        raise RuntimeError("fallo API")


class BrokenChat:
    def __init__(self):
        self.completions = BrokenCompletions()


class BrokenClient:
    def __init__(self):
        self.chat = BrokenChat()


def test_enrich_text_uses_openai_client_when_available():
    service = OpenAIService(client=FakeClient())

    result = service.enrich_text("Texto original")

    assert result == "Respuesta generada por OpenAI"


def test_enrich_text_falls_back_when_openai_client_fails():
    service = OpenAIService(client=BrokenClient())

    result = service.enrich_text("Texto original")

    assert "CONTENIDO ENRIQUECIDO LOCALMENTE" in result


def test_enrich_text_returns_empty_string_for_empty_text():
    service = OpenAIService(client=FakeClient())

    result = service.enrich_text("")

    assert result == ""


def test_summarize_text_uses_openai_client_when_available():
    service = OpenAIService(client=FakeClient())

    result = service.summarize_text("Texto enriquecido")

    assert result == "Respuesta generada por OpenAI"


def test_summarize_text_falls_back_when_openai_client_fails():
    service = OpenAIService(client=BrokenClient())

    result = service.summarize_text("Texto enriquecido.")

    assert result == "- Texto enriquecido."


def test_summarize_text_returns_empty_string_for_empty_text():
    service = OpenAIService(client=FakeClient())

    result = service.summarize_text("")

    assert result == ""


def test_enrich_text_uses_local_fallback_without_client(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    service = OpenAIService(api_key=None, client=None)

    result = service.enrich_text("Texto original")

    assert "Texto original" in result
    assert "CONTENIDO ENRIQUECIDO LOCALMENTE" in result


def test_summarize_text_uses_local_fallback_without_client(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    service = OpenAIService(api_key=None, client=None)

    result = service.summarize_text("Primera idea. Segunda idea.")

    assert "- Primera idea." in result


def test_summarize_text_local_fallback_handles_empty_sentences(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    service = OpenAIService(api_key=None, client=None)

    result = service._fallback_summary("...")

    assert result == "- No hay contenido suficiente para resumir."


def test_compatibility_functions_use_service(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    enriched = enriquecer_con_ai("Texto")
    summary = generar_resumen("Texto enriquecido.")

    assert "CONTENIDO ENRIQUECIDO LOCALMENTE" in enriched
    assert "- Texto enriquecido." == summary
