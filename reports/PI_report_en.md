# Reporte de Proyecto Individual M1

A continuación, el reporte solicitado para esta entrega.

Autor: [Cristobal Herreros](https://github.com/Sapo-san)

## Arquitectura

Para el desarrollo de este proyecto decidí como arquitectura una única clase `class Agent` que tiene los siguientes métodos:

...

## Técnica de prompting

Como técnica de prompting decidí utilizar *Chain of Thought* ya que el problema propuesto no me pareció lo suficientemente complejo como para utilizar *ReAct* pero tampoco lo suficientemente sencillo para usar una instrucción directa, y para fines de este reporte decidí utilizar tres versiones del system prompt para comparar, una *zero shot* (v1) y las otras dos *few shots* con uno (v2) y cuatro ejemplos (v3) respectivamente.

La estructura de todos los prompts incluye los principios clave expuestos en el curso:

- **Definir el Rol: Establece la perspectiva del modelo.** En este caso indiqué *"experto en asistencia de soporte al cliente de una empresa chilena líder en telecomunicaciones."*
- **Proporcionar Contexto: datos de entrada relevantes.** En este caso tambien especifiqué que los datos de entrada vienen en JSON. Los campos de entrada del prompt son:
  - `nombre`: nombre del cliente.
  - `perfil`: Perfil/contexto adicional del cliente
  - `solicitud`: solicitud textual del cliente
- **Especificar la Tarea: Indicar claramente lo que el modelo debe hacer.** En todas las versiones del prompt esta sección es identica: Idioma en que se comunica (Español chileno formal), formato de entrada (JSON tres campos), especificación del CoT y que debe generar una salida. La salida es *una sugerencia de mensaje y estrategia a seguir la conversación, dirigida ejecutivos de atención al cliente*.
- **Definir el Formato de Salida: Asegurar que la respuesta sea legible por máquina.** Se le indicó el formato exacto del JSON a responder y un formato alternativo en caso de error. El formato de salida es:
  - `chain_of_thought`: tres pasos Puntos clave, Estrategia identificada a seguir y sugerencia.
  - `opener`: Mensaje para iniciar la conversación.
  - `confianza`: float entre 0 y 1 que indica la confianza del modelo en su respuesta.

Respecto al formato de salida, para asegurar el formato JSON tambien implementé parseo por código con la libreria `json` de python para verificar el formato correcto y verifiqué manualmente la existencia de los campos pedidos. Opté por una validación más casera por que aun no estoy del todo familiarizado con Pydantic todavía y prioricé hacer la entrega antes que explorar Pydantic para el parseo de datos.

## Métricas de ejemplo

Se capturaron las métricas: tokens_prompt, tokens_completion, total_tokens, latency_ms, estimated_cost_usd

Por cada combinación de `prompt+modelo` se hicieron las mismas seis llamadas con inputs distintos (ver `main.ipynb`). En todos los casos los tokens estimados con la librería `tiktoken` coinciden con enviados registrados por la API. Las metricas que "incluyen errores" estan contando las respuestas cortas (ejemplo: `{"error": "lo siento, no puedo ayudarte con eso"}`) que el prompt induce al modelo a dar.

### Métricas recolectadas

A modo de resumen para cada versión del prompt:

- **main_prompt v1 | modelo: gpt-o4-mini**
  - latencia (ms) minima, promedio y máxima: 797, 2344, 4415
  - tokens promedio por respuesta
    - sin errores: 136.2
    - incluyendo errores: 91.875
  - costo promedio por llamada
    - sin errores: 0.00013752 USD
    - incluyendo errores: 0.00011025 USD
  - costo máximo por error (tres llamadas sin éxito): 0.0001944 USD

- **main_prompt v2 | modelo: gpt-o4-mini**
  - latencia (ms) minima, promedio y máxima: 810, 1699.1, 3705
  - tokens promedio por respuesta
    - sin errores: 134.25
    - incluyendo errores: 64.5
  - costo promedio por llamada
    - sin errores: 0.0001707 USD
    - incluyendo errores: 0.0012804 USD
  - costo máximo por error (tres llamadas sin éxito): 0.0003006 USD

- **main_prompt v3 | modelo: gpt-o4-mini**
  - latencia (ms) minima, promedio y máxima: 742, 1837.1, 4033
  - tokens promedio por respuesta
    - sin errores: 146
    - incluyendo errores: 69.2
  - costo promedio por llamada
    - sin errores: 0.00027975 USD
    - incluyendo errores: 0.00023286 USD
  - costo máximo por error (tres llamadas sin éxito): 0.0006066 USD

Adicionalmente, para el prompt v3, se probó con dos modelos mas para contrastar:

- **main_prompt v3 | modelo: gpt-5o-mini**
  - latencia (ms) minima, promedio y máxima: 6231, 8538.33, 10245
  - tokens promedio por respuesta: 1117.83
  - costo promedio por llamada: 0,002554917 USD
  NOTA: este modelo respondió sin errores en todos los casos testeados.

- **main_prompt v3 | modelo: gpt-o4**
  - latencia (ms) minima, promedio y máxima: 708, 3444.7, 16655
  - tokens promedio por respuesta
    - sin errores: 146
    - incluyendo errores: 69.2
  - costo promedio por llamada
    - sin errores: 0.0046625 USD
    - incluyendo errores: 0.003881 USD
  - costo máximo por error (tres llamadas sin éxito): 0.01011 USD

## Trade-offs

...