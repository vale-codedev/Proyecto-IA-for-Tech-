# Proyecto IA for Tech - Agente RAG para documentos

Aplicacion web que implementa un agente inteligente capaz de responder preguntas usando como fuente un documento en PDF o CSV. El proyecto esta preparado para el Challenge Alura Agente: incluye codigo fuente organizado, documentacion, ejemplos de uso y archivos base para ejecutar localmente o desplegar en Oracle Cloud Infrastructure (OCI).

## Descripcion general

El agente usa una arquitectura RAG (Retrieval-Augmented Generation):

1. Carga documentos PDF o CSV desde la carpeta `data/` o desde un archivo subido por el usuario.
2. Extrae y divide el contenido en fragmentos consultables.
3. Calcula similitud entre la pregunta y los fragmentos del documento.
4. Genera una respuesta basada unicamente en los fragmentos mas relevantes.
5. Muestra las fuentes utilizadas para que la respuesta sea verificable.

La aplicacion funciona sin llaves de API externas. Esto permite probar el challenge de forma local y reproducible. Si luego deseas conectarlo a un modelo generativo externo, el punto natural de integracion esta en `src/agent.py`.

## Arquitectura

```text
.
├── app.py                    # Interfaz web con Streamlit
├── data/
│   └── ejemplo_agente.csv    # Documento de ejemplo para probar el agente
├── docs/
│   └── deploy_oci.md         # Guia y evidencia del despliegue en OCI
├── src/
│   ├── agent.py              # Logica principal del agente
│   ├── document_loader.py    # Lectura de PDF y CSV
│   └── text_processing.py    # Limpieza y division de texto
├── tests/
│   └── test_agent.py         # Pruebas unitarias basicas
├── Dockerfile                # Imagen lista para despliegue
├── requirements.txt          # Dependencias Python
└── .gitignore
```

## Tecnologias y herramientas

- Python 3.11+
- Streamlit para la interfaz web
- csv de la libreria estandar para leer archivos CSV
- pypdf para extraer texto de PDF
- busqueda por similitud de texto implementada con libreria estandar
- pytest para pruebas
- Docker para empaquetar la aplicacion
- Oracle Cloud Infrastructure (OCI) para el despliegue

## Como ejecutar el proyecto

### 1. Crear y activar un entorno virtual

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicacion

```bash
streamlit run app.py
```

La aplicacion quedara disponible normalmente en:

```text
http://localhost:8501
```

## Uso

1. Abre la aplicacion.
2. Usa el documento de ejemplo incluido o sube tu propio PDF/CSV.
3. Escribe una pregunta relacionada con el contenido.
4. Revisa la respuesta y los fragmentos fuente utilizados por el agente.

## Ejemplos de preguntas

Con el archivo `data/ejemplo_agente.csv`, puedes probar:

- Que problema resuelve el agente?
- Que tecnologias utiliza el proyecto?
- Como se demuestra el deploy en OCI?
- Que entregables pide el challenge?
- Como se ejecuta la aplicacion localmente?

## Ejemplos de respuestas generadas por el agente

Pregunta:

```text
Que problema resuelve el agente?
```

Respuesta esperada:

```text
Segun el documento, el agente responde preguntas basadas en documentos PDF o CSV. Para hacerlo, procesa el contenido, encuentra los fragmentos mas relevantes y construye una respuesta verificable usando esas fuentes.
```

Pregunta:

```text
Como se demuestra el deploy en OCI?
```

Respuesta esperada:

```text
Segun el documento, la evidencia del despliegue en OCI puede incluir el enlace publico de la aplicacion y una captura de pantalla donde se vea la aplicacion funcionando correctamente.
```

## Deploy en OCI

La guia de despliegue y el espacio para registrar la evidencia estan en [docs/deploy_oci.md](docs/deploy_oci.md).

Cuando tengas tu aplicacion publicada, actualiza esa seccion con:

- URL publica del deploy.
- Captura de pantalla guardada en `docs/assets/`.
- Fecha de despliegue.

## Pruebas

```bash
pytest
```

## Estado del challenge

- [x] Repositorio preparado para GitHub
- [x] Estructura organizada
- [x] README con descripcion, arquitectura, tecnologias e instrucciones
- [x] Agente funcional para PDF/CSV
- [x] Codigo para leer y procesar documentos
- [x] Dockerfile para despliegue
- [ ] Enlace publico de OCI
- [ ] Captura de pantalla del deploy en OCI
