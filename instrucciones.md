# Proyecto Individual 1

Instrucciones a seguir para completar el proyecto individual del M1

## Contexto y Objetivos

Eres ingeniero/a en un equipo pequeño de producto que está construyendo un asistente para agentes de soporte al cliente. El asistente debe devolver, para cualquier pregunta entrante, una respuesta concisa en JSON para que los sistemas downstream puedan mostrar: una respuesta, una estimación de confianza y acciones recomendadas. El equipo también necesita métricas por consulta (tokens, latencia y costo estimado en USD) para monitorear el uso.

### **🎯Objetivos (qué vas a entregar y por qué importa):**

- Implementar un script ejecutable o un endpoint mínimo que reciba una pregunta del usuario y devuelva JSON válido con campos nombrados (por ejemplo: answer, confidence, actions, etc.). Esto crea un contrato estable para integraciones posteriores.
- Registrar métricas por ejecución: tokens (prompt/completion/total), latency_ms y estimated_cost_usd. Esto habilita el monitoreo de costo y performance.
- Aplicar al menos una técnica explícita de prompt engineering (few-shot, chain-of-thought, o self-consistency) y documentar por qué se eligió.
- Entregar un reporte breve (1–2 páginas) que describa: arquitectura, técnica de prompting, métricas de ejemplo y trade-offs.
- Incluir al menos un test automatizado (por ejemplo, validación de JSON o conteo de tokens).
- Opcional: implementar un fallback de seguridad/moderación para entradas adversariales.

    ¿Por qué esto es importante? Outputs estructurados + métricas + decisiones de prompting documentadas son habilidades clave para construir sistemas de IA confiables y sirven como base para enfoques RAG (Retrieval-Augmented Generation).

---

### 📢Consigna

Desarrolla una aplicación de “Multitasking Text Utility” que reciba una pregunta del usuario y devuelva una salida en formato JSON. Utiliza la API de OpenAI aplicando al menos una técnica de prompt engineering aprendida en clase. Registra y reporta al menos tres métricas, como costo, tokens utilizados y latencia.

Bonus: incluye soporte para manejar prompts adversariales y así evaluar la seguridad.

---

## Entregables del proyecto y requisitos de entrega

Enviar mediante un enlace público al repositorio en Git. Asegurarse de que el repositorio sea autocontenido y que se pueda ejecutar sin depender de elementos externos no documentados.

### 📂Estructura de repositorio esperada

| Entregable | Archivo/Formato | Contenido mínimo |
| :---: | :---: | --- |
| Aplicación o script ejecutable | src/run_query.py or app/endpoint.py (or notebook .ipynb) | src/run_query.py or app/endpoint.py (or notebook .ipynb) |
| Plantilla(s) de prompt | prompts/main_prompt.txt (or .md) | Prompt basado en instrucciones; incluir algunos ejemplos few-shot; instrucciones de esquema JSON. |
| Registro de métricas | metrics/metrics.csv or metrics/metrics.json | Métricas por ejecución: timestamp, tokens_prompt, tokens_completion, total_tokens, latency_ms, estimated_cost_usd. |
| Informe breve | reports/PI_report_en.md (1–2 pages) | Informe breve: visión de arquitectura, técnica(s) de prompting usada(s) y por qué, resumen de métricas con resultados de muestra, desafíos y posibles mejoras. |
| README | README.md | README: setup, variables de entorno, comandos de ejecución, cómo reproducir métricas, limitaciones conocidas. |
| Tests | tests/test_core.py | tests/test_core.py |
| Manejo de seguridad (bonus) | src/safety.py + docs in report | Seguridad (bonus): paso de moderación o fallback; ejemplo de prompt adversarial y resultado; registro (logging) de decisiones. |

## ✅Checklist de entrega

- Uso de la API key documentado mediante variable de entorno (OPENAI_API_KEY). Incluir .env.example.
- Al menos una ejecución registrada que produzca JSON y métricas.
- Reporte y README completos y consistentes entre sí.
