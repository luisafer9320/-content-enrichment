# Content Enricher

Herramienta de consola en Python que busca un tema en Wikipedia, extrae el titulo y los primeros cinco parrafos, enriquece el contenido con OpenAI, lo traduce con `deep-translator` y permite guardar el resultado en TXT o PDF.

## Requisitos cubiertos

- Backend en Python.
- Scraping con `requests` y `BeautifulSoup`.
- Integracion con OpenAI mediante el SDK oficial.
- Traduccion con `deep-translator`.
- Exportacion a `.txt` y `.pdf`.
- Logs en `app_logging.log`.
- Codigo orientado a objetos y separado por responsabilidad.
- Pruebas unitarias e integracion con `pytest`.
- Cobertura verificada al 100%.

## Configuracion

Instala las dependencias dentro del entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Para usar OpenAI real, configura la variable `OPENAI_API_KEY`. Si no existe, el proyecto usa un respaldo local para que la aplicacion siga funcionando durante la revision.

```powershell
$env:OPENAI_API_KEY="tu_api_key"
```

## Ejecucion

```powershell
.\.venv\Scripts\python.exe main.py
```

## Pruebas y cobertura

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=. --cov-report=term-missing
```

## Estructura

- `main.py`: coordina el flujo de consola.
- `scraper/wiki_scraper.py`: busca y extrae contenido de Wikipedia.
- `services/openai_service.py`: enriquece y resume contenido.
- `services/translator/TranslatorService.py`: traduce contenido.
- `exporters/file_exporter.py`: guarda reportes TXT o PDF.
- `tests/`: contiene pruebas unitarias e integracion.
