from services.translator.TranslatorService import TranslatorService, traducir_contenido


class FakeTranslator:
    """Traductor falso que evita llamar al servicio externo en las pruebas."""

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def translate(self, text):
        return f"{text} traducido a {self.target}"


class BrokenTranslator:
    """Traductor falso que simula un error del proveedor externo."""

    def __init__(self, source, target):
        raise RuntimeError("servicio caido")


def test_translate_returns_translated_text():
    service = TranslatorService(translator_class=FakeTranslator)

    result = service.translate("Hola", "en")

    assert result == "Hola traducido a en"


def test_translate_returns_original_text_when_provider_fails():
    service = TranslatorService(translator_class=BrokenTranslator)

    result = service.translate("Hola", "en")

    assert result == "Hola"


def test_translate_returns_empty_string_for_empty_text():
    service = TranslatorService(translator_class=FakeTranslator)

    result = service.translate("", "en")

    assert result == ""


def test_translate_returns_original_text_for_empty_language():
    service = TranslatorService(translator_class=FakeTranslator)

    result = service.translate("Hola", " ")

    assert result == "Hola"


def test_compatibility_function_handles_empty_text():
    result = traducir_contenido("", "en")

    assert result == ""
