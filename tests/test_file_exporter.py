from pathlib import Path

import pytest

from exporters.file_exporter import FileExporter, guardar_en_archivo


def test_export_txt_creates_report_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    exporter = FileExporter()

    output_path = exporter.export("mi_reporte", "txt", "Titulo", "Original", "Enriquecido", "Traducido", "Resumen")

    assert output_path == Path("mi_reporte.txt")
    assert output_path.exists()
    assert "REPORTE DE INVESTIGACION: Titulo" in output_path.read_text(encoding="utf-8")
    assert "Resumen" in output_path.read_text(encoding="utf-8")


def test_export_pdf_creates_report_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    exporter = FileExporter()

    output_path = exporter.export("mi_reporte", "pdf", "Titulo", "Original", "Enriquecido", "Traducido")

    assert output_path == Path("mi_reporte.pdf")
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_export_pdf_with_summary_creates_report_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    exporter = FileExporter()

    output_path = exporter.export("mi_reporte", "pdf", "Titulo", "Original", "Enriquecido", "Traducido", "Resumen")

    assert output_path.exists()


def test_export_rejects_unsupported_format(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    exporter = FileExporter()

    with pytest.raises(ValueError):
        exporter.export("mi_reporte", "docx", "Titulo", "Original", "Enriquecido", "Traducido")


def test_export_sanitizes_windows_invalid_filename_characters(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    exporter = FileExporter()

    output_path = exporter.export("reporte:final", "txt", "Titulo", "Original", "Enriquecido", "Traducido")

    assert output_path == Path("reporte_final.txt")


def test_export_uses_default_values_and_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    exporter = FileExporter()

    output_path = exporter.export("", "txt", "", "", "", "")

    assert output_path == Path("reporte_content_enricher.txt")
    text = output_path.read_text(encoding="utf-8")
    assert "Reporte sin titulo" in text
    assert "No se obtuvo contenido original" in text


def test_compatibility_function_exports_txt(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    output_path = guardar_en_archivo("compat", "txt", "Titulo", "Original", "Enriquecido", "Traducido")

    assert output_path == Path("compat.txt")
    assert output_path.exists()
