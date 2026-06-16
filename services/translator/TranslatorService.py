import logging

from deep_translator import GoogleTranslator


class TranslatorService:
    def __init__(self, translator_class=GoogleTranslator):
        self.translator_class = translator_class

    def translate(self, text: str, target_language: str) -> str:
        clean_language = target_language.strip().lower()
        if not text:
            return ""
        if not clean_language:
            logging.warning("No se recibio idioma destino para traduccion.")
            return text

        try:
            logging.info("Traduciendo contenido al idioma: %s", clean_language)
            translator = self.translator_class(source="auto", target=clean_language)
            return translator.translate(text)
        except Exception as error:
            logging.error("Error en traduccion: %s", error)
            return text


def traducir_contenido(texto: str, idioma_destino: str) -> str:
    return TranslatorService().translate(texto, idioma_destino)
