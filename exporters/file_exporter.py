import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def guardar_en_archivo(nombre, formato, titulo, original, enriquecido, traducido, resumen=""):
    """
    Permite al usuario guardar el contenido en formato .txt o .pdf profesional,
    asegurando que si algún campo está vacío (None), se maneje correctamente.
    """
    # Validamos que si algún contenido llegó vacío, no rompa el programa
    titulo = titulo if titulo else "Reporte sin título"
    original = original if original else "No se obtuvo contenido original de Wikipedia."
    enriquecido = enriquecido if enriquecido else "No se obtuvo contenido enriquecido."
    traducido = traducido if traducido else "No se obtuvo contenido traducido."
    resumen = resumen if resumen else ""

    nombre_completo = f"{nombre}.{formato}"
    try:
        if formato == 'txt':
            with open(nombre_completo, 'w', encoding='utf-8') as file:
                file.write(f"REPORTE DE INVESTIGACIÓN: {titulo}\n")
                file.write("=" * 60 + "\n\n")
                file.write(f"--- CONTENIDO ORIGINAL WIKIPEDIA ---\n{original}\n\n")
                file.write(f"--- CONTENIDO ENRIQUECIDO POR IA ---\n{enriquecido}\n\n")
                if resumen:
                    file.write(f"--- RESUMEN EJECUTIVO CHATGPT ---\n{resumen}\n\n")
                file.write(f"--- CONTENIDO TRADUCIDO ---\n{traducido}\n\n")
            print(f"¡Éxito! Archivo de texto guardado como: '{nombre_completo}'")

        elif formato == 'pdf':
            doc = SimpleDocTemplate(nombre_completo, pagesize=letter)
            estilos = getSampleStyleSheet()

            estilo_titulo = ParagraphStyle('DocTitle', parent=estilos['Heading1'], fontSize=18, spaceAfter=12,
                                           textColor='#1a202c')
            estilo_sub = ParagraphStyle('DocSub', parent=estilos['Heading2'], fontSize=12, spaceBefore=14, spaceAfter=6,
                                        textColor='#2b6cb0')
            estilo_cuerpo = ParagraphStyle('DocBody', parent=estilos['Normal'], fontSize=10, leading=14, spaceAfter=10)

            historia = []
            historia.append(Paragraph(f"Reporte de Investigación: {titulo}", estilo_titulo))
            historia.append(Spacer(1, 10))

            historia.append(Paragraph("1. Contenido Original (Wikipedia)", estilo_sub))
            historia.append(Paragraph(original.replace('\n', '<br/>'), estilo_cuerpo))

            historia.append(Paragraph("2. Contenido Enriquecido (OpenAI GPT-4)", estilo_sub))
            historia.append(Paragraph(enriquecido.replace('\n', '<br/>'), estilo_cuerpo))

            if resumen:
                historia.append(Paragraph("3. Resumen Ejecutivo (ChatGPT)", estilo_sub))
                historia.append(Paragraph(resumen.replace('\n', '<br/>'), estilo_cuerpo))

            historia.append(Paragraph("4. Contenido Traducido", estilo_sub))
            historia.append(Paragraph(traducido.replace('\n', '<br/>'), estilo_cuerpo))

            doc.build(historia)
            print(f"¡Éxito! Reporte PDF profesional guardado como: '{nombre_completo}'")

        else:
            print("[Error] Formato no soportado. Elige 'txt' o 'pdf'.")
            return

        logging.info(f"Archivo exportado correctamente con nombre: {nombre_completo}")
    except Exception as e:
        logging.error(f"Error al guardar el archivo en disco: {str(e)}")
        print(f"[Error de Escritura] No se pudo guardar el archivo: {e}")