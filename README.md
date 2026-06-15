# Content Enricher

Content Enricher es una herramienta de consola creada en Python. El programa busca un tema en Wikipedia, extrae el titulo y los primeros cinco parrafos, enriquece el contenido con OpenAI, permite generar un resumen, traduce el resultado y ofrece guardar el informe final en formato TXT o PDF.

El proyecto tambien incluye una entrada web compatible con Vercel (`app`, `application` y `handler` en `main.py`). Esta entrada existe porque Vercel no puede ejecutar aplicaciones interactivas de consola con `input()`.

## Objetivo del proyecto

El objetivo es facilitar la investigacion de temas usando una fuente inicial como Wikipedia y agregando procesamiento automatico para enriquecer, resumir, traducir y exportar la informacion.

## Requisitos principales cumplidos

| Requisito | Estado | Donde se cumple |
| --- | --- | --- |
| Backend en Python | Cumplido | `main.py` y modulos internos |
| Scraping de Wikipedia | Cumplido | `scraper/wiki_scraper.py` |
| Extraccion de titulo y 5 parrafos | Cumplido | `WikipediaScraper._parse_article()` |
| Interaccion por terminal | Cumplido | `ContentEnricherApp.run()` |
| Mostrar resultado antes de acciones extra | Cumplido | Se imprime la seccion `RESULTADO DE WIKIPEDIA` antes del resumen/exportacion |
| OpenAI para enriquecer | Cumplido | `services/openai_service.py` |
| Resumen con ChatGPT | Cumplido | `OpenAIService.summarize_text()` |
| Traduccion con DeepTranslate | Cumplido | `services/translator/TranslatorService.py` |
| Exportacion TXT/PDF | Cumplido | `exporters/file_exporter.py` |
| Logs | Cumplido | `app_logging.log` |
| Pruebas y cobertura 100% | Cumplido | Carpeta `tests/` y `.coveragerc` |

## Criterios de rendimiento

### Calidad del codigo

El codigo esta separado por responsabilidades:

- `main.py`: coordina la aplicacion de consola.
- `scraper/wiki_scraper.py`: consulta y procesa Wikipedia.
- `services/openai_service.py`: enriquece y resume contenido.
- `services/translator/TranslatorService.py`: traduce contenido.
- `exporters/file_exporter.py`: genera archivos TXT y PDF.

Las clases tienen nombres descriptivos y los metodos explican su accion principal. Tambien se agregaron comentarios cortos para estudiar el flujo sin saturar el codigo.

### Funcionalidad

La aplicacion realiza el flujo completo:

1. Pide el tema.
2. Pide el idioma destino.
3. Busca el articulo en Wikipedia.
4. Muestra titulo y contenido original.
5. Enriquece el texto.
6. Permite generar resumen.
7. Traduce el contenido.
8. Permite guardar TXT o PDF.

### Interfaz de usuario

La terminal muestra secciones separadas con titulos claros:

- `RESULTADO DE WIKIPEDIA`
- `CONTENIDO ENRIQUECIDO CON IA`
- `RESUMEN EJECUTIVO`
- `CONTENIDO TRADUCIDO`

Las entradas indican ejemplos, como idiomas `en`, `fr`, `it`, `de`.

### Manejo de errores

El sistema maneja errores comunes:

- Tema o idioma vacio.
- Articulo no encontrado en Wikipedia.
- Error de red consultando Wikipedia.
- Falta de `OPENAI_API_KEY`.
- Fallos de OpenAI durante enriquecimiento o resumen.
- Fallos del traductor externo.
- Formato de archivo no soportado.
- Error de escritura en disco.

Cuando una API externa falla, el programa evita perder el flujo y muestra o guarda el mejor resultado disponible.

### Documentacion

Este README explica instalacion, ejecucion, dependencias, pruebas, cobertura, estructura y criterios de evaluacion. Tambien se incluye una guia de gestion agil en `docs/gestion_agil.md`.

### Ejecucion del proyecto

El proyecto fue verificado con pruebas automatizadas y cobertura total:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=. --cov-report=term-missing
```

Resultado esperado:

```text
44 passed
TOTAL 100%
```

### Colaboracion y gestion

La propuesta de gestion agil esta documentada en `docs/gestion_agil.md`. Incluye columnas sugeridas de Trello, roles, ceremonias y ejemplos de tarjetas para evidenciar avance del equipo.

### Innovacion

Ademas de los requisitos minimos, el proyecto incluye:

- Resumen opcional del contenido enriquecido.
- Exportacion en dos formatos.
- Logs de proceso.
- Respaldo local cuando OpenAI no esta configurado.
- Pruebas automatizadas sin depender de internet.
- Validacion de nombres de archivo para evitar errores en Windows.

## Instalacion

Desde la carpeta del proyecto, instala las dependencias dentro del entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Configurar OpenAI

Para usar OpenAI real, configura la variable de entorno `OPENAI_API_KEY`:

```powershell
$env:OPENAI_API_KEY="tu_api_key"
```

Si no configuras la API key, la aplicacion usa un enriquecimiento local de respaldo. Esto permite ejecutar y revisar el proyecto aunque no tengas credenciales.

## Ejecutar la aplicacion

```powershell
.\.venv\Scripts\python.exe main.py
```

Ejemplo de uso:

```text
1. Ingrese el tema a investigar en Wikipedia: Python
2. Ingrese el idioma destino para la traduccion (ej: en, fr, it, de): en
Desea generar un resumen con ChatGPT? (s/n): s
Desea guardar el resultado en un archivo? (s/n): s
Nombre del archivo sin extension: reporte_python
Formato de salida (txt/pdf): pdf
```

## Ejecutar en Vercel

Vercel necesita que el archivo Python exporte una variable o funcion llamada `app`, `application` o `handler`. Por eso `main.py` incluye una entrada WSGI llamada `app`.

Despues de desplegar, puedes probar:

```text
https://TU-DOMINIO.vercel.app/
```

Para ejecutar el enriquecimiento desde Vercel, usa el endpoint:

```text
https://TU-DOMINIO.vercel.app/api/enrich?topic=Python&language=en&summary=true
```

Parametros:

- `topic`: tema que se buscara en Wikipedia.
- `language`: idioma destino, por ejemplo `en`, `fr`, `it`, `de`, `es`.
- `summary`: opcional. Usa `true` para generar resumen.

Importante: en Vercel no se genera una conversacion por terminal ni se puede usar `input()`. La version de Vercel responde en JSON para que el backend sea ejecutable en web.

## Ejecutar pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Ejecutar pruebas con cobertura

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=. --cov-report=term-missing
```

## Dependencias principales

- `requests`: realiza peticiones HTTP a Wikipedia.
- `beautifulsoup4`: procesa el HTML de Wikipedia.
- `openai`: conecta con la API de OpenAI.
- `deep-translator`: traduce el contenido.
- `reportlab`: crea archivos PDF.
- `pytest`: ejecuta pruebas.
- `pytest-cov`: mide cobertura de pruebas.

## Estructura del proyecto

```text
.
|-- main.py
|-- requirements.txt
|-- README.md
|-- .coveragerc
|-- scraper/
|   `-- wiki_scraper.py
|-- services/
|   |-- openai_service.py
|   `-- translator/
|       `-- TranslatorService.py
|-- exporters/
|   `-- file_exporter.py
|-- tests/
|   |-- test_file_exporter.py
|   |-- test_main_integration.py
|   |-- test_openai_service.py
|   |-- test_translator_service.py
|   `-- test_wiki_scraper.py
`-- docs/
    `-- gestion_agil.md
```

## Notas para PyCharm

1. Abre la carpeta completa del proyecto.
2. Selecciona el interprete `.venv`.
3. Ejecuta `main.py` para usar la aplicacion.
4. Ejecuta la carpeta `tests/` para correr pruebas.

## Gitflow sugerido

Ramas recomendadas:

- `main`: version estable para entrega.
- `develop`: integracion del trabajo.
- `feature/scraper-wikipedia`: scraping.
- `feature/openai-service`: enriquecimiento y resumen.
- `feature/translator-service`: traduccion.
- `feature/exporter`: TXT/PDF.
- `feature/tests`: pruebas y cobertura.
