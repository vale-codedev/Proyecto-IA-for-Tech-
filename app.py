from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st

from src.agent import DocumentAgent
from src.document_loader import load_document


PROJECT_ROOT = Path(__file__).parent
DEFAULT_DOCUMENT = PROJECT_ROOT / "data" / "ejemplo_agente.csv"


st.set_page_config(
    page_title="Agente IA for Tech",
    page_icon="IA",
    layout="wide",
)

st.title("Agente IA for Tech")
st.caption("Pregunta sobre el contenido de un documento PDF o CSV.")


@st.cache_resource(show_spinner=False)
def build_agent(file_path: str) -> DocumentAgent:
    document = load_document(Path(file_path))
    return DocumentAgent.from_document(document)


def save_uploaded_file(uploaded_file) -> Path:
    suffix = Path(uploaded_file.name).suffix
    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return Path(temp_file.name)


with st.sidebar:
    st.header("Documento")
    uploaded_file = st.file_uploader(
        "Sube un PDF o CSV",
        type=["pdf", "csv"],
    )
    st.info("Si no subes un archivo, se usara el CSV de ejemplo incluido.")

document_path = save_uploaded_file(uploaded_file) if uploaded_file else DEFAULT_DOCUMENT

try:
    agent = build_agent(str(document_path))
except Exception as exc:
    st.error(f"No se pudo cargar el documento: {exc}")
    st.stop()

question = st.text_input(
    "Pregunta",
    placeholder="Ejemplo: Como se demuestra el deploy en OCI?",
)

col1, col2 = st.columns([2, 1])

with col1:
    if question:
        answer = agent.answer(question)
        st.subheader("Respuesta")
        st.write(answer.text)

        st.subheader("Fuentes utilizadas")
        for index, source in enumerate(answer.sources, start=1):
            with st.expander(f"Fuente {index} - relevancia {source.score:.2f}"):
                st.write(source.text)
    else:
        st.subheader("Listo para responder")
        st.write(
            "Escribe una pregunta relacionada con el documento cargado para ver la respuesta del agente."
        )

with col2:
    st.subheader("Resumen del documento")
    st.metric("Fragmentos indexados", agent.chunk_count)
    st.write("Preguntas sugeridas:")
    for sample in agent.suggest_questions():
        st.button(sample, use_container_width=True, disabled=True)
