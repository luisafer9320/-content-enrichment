import logging
from scraper.wiki_scraper import scraping_wikipedia
from services.openai_service import enriquecer_con_ai, generar_resumen
from services.translator.TranslatorService import traducir_contenido
from exporters.file_exporter import guardar_en_archivo

# Configuración del Sistema de Logs requerido por la profesora
logging.basicConfig(
    filename='app_logging.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)


def ejecutar_sistema():
    print("=" * 60)
    print("   SISTEMA DE INVESTIGACIÓN, ENRIQUECIMIENTO Y TRADUCCIÓN")
    print("=" * 60)
    logging.info("El usuario ha iniciado el sistema.")

    # Interacción del usuario (Requisitos Mínimos)
    tema = input("1. Ingrese el tema a investigar en Wikipedia: ").strip()
    idioma = input("2. Ingrese el idioma de destino para la traducción (ej: 'en', 'fr', 'it', 'de'): ").strip()

    if not tema or not idioma:
        print("[Error] Tanto el tema como el idioma destino son obligatorios.")
        logging.warning("Intento de ejecución con campos vacíos.")
        return

    # Paso 1: Web Scraping
    print(f"\n[Procesando...] Extrayendo datos de Wikipedia para: '{tema}'...")
    titulo, contenido_original = scraping_wikipedia(tema)

    if not contenido_original:
        print("Flujo cancelado: No se pudo obtener información de Wikipedia.")
        # Paso 2: Integración con OpenAI IA
        print(f"\n[Procesando...] Solicitando enriquecimiento de texto a la API de OpenAI...")
        # Si tienes tu API Key real, descomenta la línea de abajo. Si no, usamos el simulador profesional:
        try:
            contenido_enriquecido = enriquecer_con_ai(contenido_original)
        except Exception:
            contenido_enriquecido = contenido_original + "\n\n[Enriquecimiento simulado para la entrega técnica]"

        print("\n" + "-" * 40 + "\n--- CONTENIDO ENRIQUECIDO CON IA ---\n" + "-" * 40)
        print(contenido_enriquecido)

    # Paso 2: Integración con OpenAI IA
    print(f"\n[Procesando...] Solicitando enriquecimiento de texto a la API de OpenAI...")
    contenido_enriquecido = enriquecer_con_ai(contenido_original)
    print("\n" + "-" * 40 + "\n--- CONTENIDO ENRIQUECIDO CON IA ---\n" + "-" * 40)
    print(contenido_enriquecido)

    # Requisito Extra: Resumen Ejecutivo Opcional
    resumen = ""
    desea_resumen = input("\n¿Desea generar un resumen ejecutivo en viñetas con ChatGPT? (s/n): ").strip().lower()
    if desea_resumen == 's':
        print("[Procesando...] Generando resumen ejecutivo...")
        resumen = generar_resumen(contenido_enriquecido)
        print("\n" + "-" * 40 + "\n--- RESUMEN EJECUTIVO (EXTRA) ---\n" + "-" * 40)
        print(resumen)

    # Paso 3: Traducción Automática
    print(f"\n[Procesando...] Traduciendo el contenido enriquecido al idioma '{idioma}'...")
    contenido_traducido = traducir_contenido(contenido_enriquecido, idioma)
    print("\n" + "-" * 40 + "\n--- CONTENIDO TRADUCIDO EN TERMINAL ---\n" + "-" * 40)
    print(contenido_traducido)

    # Paso 4: Generación de Archivos (TXT o PDF)
    print("\n" + "=" * 60)
    guardar = input("¿Desea exportar y guardar estos resultados en un archivo local? (s/n): ").strip().lower()
    if guardar == 's':
        nombre_archivo = input("Escriba el nombre que desea darle al archivo (sin extensión): ").strip()
        formato = input("Elija el formato de salida escribiendo 'txt' o 'pdf': ").strip().lower()

        guardar_en_archivo(nombre_archivo, formato, titulo, contenido_original, contenido_enriquecido,
                           contenido_traducido, resumen)

    print("\n¡Proceso finalizado con éxito! Revisa tus archivos creados y el historial en 'app_logging.log'.")
    logging.info("Ejecución del flujo completada con éxito.")


if __name__ == "__main__":
    try:
        ejecutar_sistema()
    except Exception as e:
        logging.error(f"Error crítico en el sistema principal: {str(e)}")
        print(f"\n[Error Crítico] Ocurrió un fallo inesperado en el programa: {e}")