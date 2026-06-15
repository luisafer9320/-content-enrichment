# Gestion agil y colaboracion

Este documento sirve como evidencia de la forma recomendada de organizar el trabajo del equipo. Puede copiarse a Trello o usarse como guia para explicar la metodologia aplicada.

## Metodologia

Se propone trabajar con una metodologia agil tipo Kanban/Scrum ligero. El objetivo es dividir el proyecto en tareas pequenas, revisar avances frecuentemente y entregar incrementos funcionales.

## Tablero Trello sugerido

Columnas recomendadas:

- `Backlog`: ideas y tareas pendientes.
- `Por hacer`: tareas priorizadas para el sprint actual.
- `En progreso`: tareas que alguien esta desarrollando.
- `En revision`: tareas terminadas que necesitan pruebas o revision del equipo.
- `Hecho`: tareas completadas y verificadas.

## Tarjetas sugeridas

- Crear estructura base del proyecto Python.
- Implementar scraping de Wikipedia.
- Extraer titulo y primeros cinco parrafos.
- Implementar servicio de OpenAI para enriquecimiento.
- Implementar resumen opcional.
- Implementar traduccion con deep-translator.
- Implementar exportacion TXT.
- Implementar exportacion PDF.
- Configurar logs.
- Agregar manejo de errores.
- Crear pruebas unitarias.
- Crear prueba de integracion.
- Verificar cobertura 100%.
- Documentar README.
- Preparar demostracion final.

## Roles sugeridos

- `Backend`: implementa scraper, servicios y exportacion.
- `QA`: ejecuta pruebas, revisa cobertura y valida errores.
- `Documentacion`: mantiene README, criterios y guia de uso.
- `Scrum master`: revisa tablero, desbloquea tareas y coordina avances.

Si el proyecto fue realizado por una sola persona, la misma persona puede asumir todos los roles y documentarlo asi durante la entrega.

## Sprint sugerido

Duracion sugerida: 1 semana.

Objetivo del sprint:

- Tener una herramienta funcional de consola que consulte Wikipedia, procese el contenido y genere un archivo final.

Definicion de terminado:

- El flujo principal se ejecuta sin errores.
- Los errores comunes muestran mensajes claros.
- El proyecto tiene pruebas automatizadas.
- La cobertura reporta 100%.
- El README explica instalacion, uso y dependencias.

## Reuniones sugeridas

- `Planning`: elegir tareas del sprint.
- `Daily`: revisar que se hizo, que se hara y bloqueos.
- `Review`: mostrar el flujo funcionando.
- `Retrospective`: identificar mejoras para el siguiente proyecto.

## Evidencia para la entrega

Capturas recomendadas:

- Tablero Trello con columnas y tarjetas.
- Terminal ejecutando `python main.py`.
- Archivo TXT o PDF generado.
- Terminal ejecutando `pytest --cov`.
- Fragmento de `app_logging.log` mostrando el proceso.
