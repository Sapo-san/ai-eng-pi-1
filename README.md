# Projecto individual M1 - Curso AI Engineering

## Setup

El entorno de desarrollo donde se creó y desarrolló este repositorio es WSL (Ubuntu) dentro de Windows 11 con `uv` y Python 3.12 instalado.

**Configurar variables de entorno:**

```bash
cp .env.example .env
```

Nota: Completar variable `OPENAI_API_KEY` en `.env` y borrar comentarios.

---

**Para instalar dependencias** detalladas en uv.lock

```bash
# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias
uv sync
```

---

**Ejecutar tests**: 

Correr `tests/test_core.py` con el comando:

```bash
uv run pytest
```

## Ejecución

**Para correr el agente**: Interactuar con el notebook ubicado en `src/main.ipynb`

Aparte de las librerías, El notebook importa dos archivos `.py`:

- `agent.py`: Archivo con la la clase `Agent` que instancia el agente.
- `log_gen.py`: Archivo con la función custom de logging.

## Consideraciones y otros

Para el desarrollo de este PI seguí lo indicado en `instrucciones.md` que es un copiar-pegar de lo ubicado en la lecture [M1PI | Proyecto](https://www.app.soyhenry.com/my-cohort/c1be21ab-e806-4e47-9052-446e5dcff8f8/lecture/3451b37f-9151-418e-84f3-79785d904786)

El reporte solicitado se encuentra en `reports/PI_report_en.md`.

Decidí utilizar un notebook antes que un `run_query` o `endpoint.py` para poder desarrollar más rápido y de manera iterativa.

Los tests con pytest es bastante sencillo, se verifican las configuraciones por defecto y se hace un conteo de tokens tomando en cuenta el `system_prompt`.

El agente implementado utiliza el contenido del archivo `main_prompt.md` como `system_prompt`. Los otros archivos con sufijos `v<numero>` son las distintas versiones del mismo prompt utilizadas para el reporte. Para mayor legibilidad decidí que el archivo del system prompt esté en formato markdown antes texto plano.

Los logs se generan en texto plano en la carpeta `logs/` como un archivo con nombre de la forma `logs-{fecha-hoy}.txt`, loggean la información solicitada ademas de la que consideré relevante. Incluiré en repositorio los logs generados por las ejecuciones hechas para el reporte.

Las metricas se generan dentro de `metrics/` como archivos `.csv`

Dentro de las instrucciones del prompt incluí un manejo de seguridad mínimo al restringir el tipo de consultas sobre las que puede responder el modelo, no se si será suficiente para para contar con el bonus de seguridad/moderación pero al menos con la llamada de ejemplo final que se supone que debe gatillar el error, la medida minima logró evitar salidas inseguras.
