import logging
import os
from typing import Optional

from openai import OpenAI


class OpenAIService:
    def __init__(self, api_key: Optional[str] = None, client=None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = client or (OpenAI(api_key=self.api_key) if self.api_key else None)
        self.model = model

    def enrich_text(self, original_text: str) -> str:
        if not original_text:
            return ""

        if self.client is None:
            logging.warning("OPENAI_API_KEY no esta configurada. Se usa enriquecimiento local.")
            return self._fallback_enrichment(original_text)

        prompt = (
            "Enriquece el siguiente texto de Wikipedia para un informe educativo. "
            "Agrega contexto, ejemplos claros y una conclusion breve. "
            "No inventes datos especificos que no puedas justificar.\n\n"
            f"{original_text}"
        )
        logging.info("Enviando contenido a OpenAI para enriquecimiento.")
        try:
            return self._ask_openai(prompt)
        except Exception as error:
            logging.error("OpenAI fallo durante el enriquecimiento: %s", error)
            return self._fallback_enrichment(original_text)

    def summarize_text(self, enriched_text: str) -> str:
        if not enriched_text:
            return ""

        if self.client is None:
            logging.warning("OPENAI_API_KEY no esta configurada. Se usa resumen local.")
            return self._fallback_summary(enriched_text)

        prompt = (
            "Resume el siguiente contenido enriquecido en 5 vinetas claras para una estudiante principiante:\n\n"
            f"{enriched_text}"
        )
        logging.info("Enviando contenido a OpenAI para resumen.")
        try:
            return self._ask_openai(prompt)
        except Exception as error:
            logging.error("OpenAI fallo durante el resumen: %s", error)
            return self._fallback_summary(enriched_text)

    def _ask_openai(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Eres un asistente educativo claro y preciso."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()

    def _fallback_enrichment(self, original_text: str) -> str:
        return (
            f"{original_text}\n\n"
            "CONTENIDO ENRIQUECIDO LOCALMENTE:\n"
            "- Contexto: el tema se puede analizar desde su origen, evolucion e impacto actual.\n"
            "- Relevancia: conocer sus conceptos principales ayuda a entender mejor el articulo base.\n"
            "- Ejemplo de uso: este contenido puede servir como punto de partida para una investigacion.\n"
            "- Conclusion: la informacion extraida de Wikipedia fue ampliada para facilitar el aprendizaje."
        )

    def _fallback_summary(self, enriched_text: str) -> str:
        sentences = [part.strip() for part in enriched_text.replace("\n", " ").split(".") if part.strip()]
        selected = sentences[:5] or ["No hay contenido suficiente para resumir"]
        return "\n".join(f"- {sentence}." for sentence in selected)


def enriquecer_con_ai(texto_original: str) -> str:
    return OpenAIService().enrich_text(texto_original)


def generar_resumen(texto_enriquecido: str) -> str:
    return OpenAIService().summarize_text(texto_enriquecido)
