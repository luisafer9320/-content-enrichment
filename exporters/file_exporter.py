import html
import logging
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


class FileExporter:
    SUPPORTED_FORMATS = {"txt", "pdf"}

    def export(self, filename: str, file_format: str, title: str, original: str, enriched: str, translated: str, summary: str = "") -> Path:
        clean_format = file_format.strip().lower()
        if clean_format not in self.SUPPORTED_FORMATS:
            raise ValueError("Formato no soportado. Usa 'txt' o 'pdf'.")

        output_path = Path(f"{self._safe_filename(filename)}.{clean_format}")
        report_data = self._normalize_report_data(title, original, enriched, translated, summary)

        if clean_format == "txt":
            self._write_txt(output_path, report_data)
        else:
            self._write_pdf(output_path, report_data)

        logging.info("Archivo exportado correctamente: %s", output_path)
        return output_path

    def _safe_filename(self, filename: str) -> str:
        clean_name = filename.strip() or "reporte_content_enricher"
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            clean_name = clean_name.replace(char, "_")
        return clean_name

    def _normalize_report_data(self, title: str, original: str, enriched: str, translated: str, summary: str) -> dict:
        return {
            "title": title or "Reporte sin titulo",
            "original": original or "No se obtuvo contenido original de Wikipedia.",
            "enriched": enriched or "No se obtuvo contenido enriquecido.",
            "translated": translated or "No se obtuvo contenido traducido.",
            "summary": summary or "",
        }

    def _write_txt(self, output_path: Path, data: dict) -> None:
        content = [
            f"REPORTE DE INVESTIGACION: {data['title']}",
            "=" * 60,
            "",
            "--- CONTENIDO ORIGINAL WIKIPEDIA ---",
            data["original"],
            "",
            "--- CONTENIDO ENRIQUECIDO POR IA ---",
            data["enriched"],
            "",
        ]

        if data["summary"]:
            content.extend(["--- RESUMEN EJECUTIVO CHATGPT ---", data["summary"], ""])

        content.extend(["--- CONTENIDO TRADUCIDO ---", data["translated"], ""])
        output_path.write_text("\n".join(content), encoding="utf-8")

    def _write_pdf(self, output_path: Path, data: dict) -> None:
        document = SimpleDocTemplate(str(output_path), pagesize=letter)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("DocTitle", parent=styles["Heading1"], fontSize=18, spaceAfter=12)
        subtitle_style = ParagraphStyle("DocSub", parent=styles["Heading2"], fontSize=12, spaceBefore=14, spaceAfter=6)
        body_style = ParagraphStyle("DocBody", parent=styles["Normal"], fontSize=10, leading=14, spaceAfter=10)

        story = [
            Paragraph(f"Reporte de Investigacion: {self._pdf_text(data['title'])}", title_style),
            Spacer(1, 10),
            Paragraph("1. Contenido Original (Wikipedia)", subtitle_style),
            Paragraph(self._pdf_text(data["original"]), body_style),
            Paragraph("2. Contenido Enriquecido (OpenAI)", subtitle_style),
            Paragraph(self._pdf_text(data["enriched"]), body_style),
        ]

        if data["summary"]:
            story.extend([
                Paragraph("3. Resumen Ejecutivo (ChatGPT)", subtitle_style),
                Paragraph(self._pdf_text(data["summary"]), body_style),
            ])

        story.extend([
            Paragraph("4. Contenido Traducido", subtitle_style),
            Paragraph(self._pdf_text(data["translated"]), body_style),
        ])
        document.build(story)

    def _pdf_text(self, value: str) -> str:
        return html.escape(value).replace("\n", "<br/>")


def guardar_en_archivo(nombre: str, formato: str, titulo: str, original: str, enriquecido: str, traducido: str, resumen: str = "") -> Path:
    return FileExporter().export(nombre, formato, titulo, original, enriquecido, traducido, resumen)
