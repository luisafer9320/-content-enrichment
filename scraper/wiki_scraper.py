import logging
import requests
from bs4 import BeautifulSoup


def scraping_wikipedia(tema):
    """
    Realiza una búsqueda en Wikipedia en español, extrae el título
    y exactamente los primeros 5 párrafos de contenido.
    """
    # Reemplazamos los espacios por guiones bajos para formar la URL de Wikipedia
    url = f"https://es.wikipedia.org/wiki/{tema.replace(' ', '_')}"

    try:
        logging.info(f"Iniciando scraping en Wikipedia para el tema: '{tema}'")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        # Realizamos la petición a la web
        respuesta = requests.get(url, headers=headers, timeout=10)

        if respuesta.status_code == 404:
            logging.error(f"Artículo no encontrado (404) para el tema: {tema}")
            print("[Error] No se encontró el artículo exacto en Wikipedia.")
            return None, None

        respuesta.raise_for_status()
        soup = BeautifulSoup(respuesta.text, 'html.parser')

        # Extraemos el título principal de la página
        titulo = soup.find('h1', id='firstHeading').text

        # Buscamos todos los párrafos (<p>)
        parrafos = soup.find_all('p')
        parrafos_limpios = []

        for p in parrafos:
            texto = p.text.strip()
            # Filtramos textos muy cortos o vacíos para asegurar que sean párrafos reales
            if len(texto) > 60:
                parrafos_limpios.append(texto)
            # Nos detenemos estrictamente al llegar a 5 párrafos
            if len(parrafos_limpios) == 5:
                break

        contenido_completo = "\n\n".join(parrafos_limpios)
        logging.info(f"Scraping exitoso. 5 párrafos obtenidos.")
        return titulo, contenido_completo

    except requests.exceptions.RequestException as e:
        logging.error(f"Error de red al conectar a Wikipedia: {str(e)}")
        print(f"[Error de Red] No se pudo conectar a Wikipedia: {e}")
        return None, None