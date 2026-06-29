from pathlib import Path

from src.agent import DocumentAgent
from src.document_loader import LoadedDocument


def test_agent_answers_using_document_context():
    document = LoadedDocument(
        path=Path("test.csv"),
        text=(
            "El agente responde preguntas sobre documentos PDF o CSV. "
            "El deploy en OCI se demuestra con un enlace publico y una captura de pantalla."
        ),
    )
    agent = DocumentAgent.from_document(document)

    answer = agent.answer("Como se demuestra el deploy en OCI?")

    assert "OCI" in answer.text or "oci" in answer.text
    assert answer.sources


def test_agent_handles_unknown_question():
    document = LoadedDocument(
        path=Path("test.csv"),
        text="Python y Streamlit ejecutan la aplicacion.",
    )
    agent = DocumentAgent.from_document(document)

    answer = agent.answer("Cual es el color favorito del usuario?")

    assert "No encontre informacion suficiente" in answer.text
