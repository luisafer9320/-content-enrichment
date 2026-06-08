"""""
from deep_translator import GoogleTranslator
from pip._internal.index import sources

translated_text = GoogleTranslator(sources="es", targets="fr").translate("amor mio, te amo")
print(translated_text)
"""

import logging
from deep_translator import GoogleTranslator


def traducir_contenido(texto, idioma_destino):
    """
    Traduce un texto desde cualquier idioma (detectado automáticamente)
    al idioma de destino seleccionado por el usuario.
    """
    try:
        logging.info(f"Iniciando proceso de traducción al idioma: {idioma_destino}")

        # 'auto' detecta si el texto original está en español, inglés, etc.
        traductor = GoogleTranslator(source='auto', target=idioma_destino)
        resultado = traductor.translate(texto)

        logging.info("Traducción completada con éxito.")
        return resultado

    except Exception as e:
        logging.error(f"Error en el servicio de traducción: {str(e)}")
        print(f"[Aviso] No se pudo traducir el contenido. Error: {e}")
        return texto  # Si falla, devuelve el texto original como respaldo


# --- PRUEBA LOCAL ---
# Esto solo se ejecuta si corres este archivo suelto para probar que funcione
if __name__ == "__main__":
    test_traduccion = traducir_contenido("amor mio, te amo", "fr")
    print("Resultado de la prueba en francés:", test_traduccion)



