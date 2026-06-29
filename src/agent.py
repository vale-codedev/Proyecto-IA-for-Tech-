from dataclasses import dataclass
from math import sqrt
import re
from collections import Counter

from src.document_loader import LoadedDocument
from src.text_processing import chunk_text


@dataclass(frozen=True)
class Source:
    text: str
    score: float


@dataclass(frozen=True)
class AgentAnswer:
    text: str
    sources: list[Source]


class DocumentAgent:
    def __init__(self, chunks: list[str]):
        if not chunks:
            raise ValueError("El documento no contiene texto suficiente para responder.")

        self._chunks = chunks
        self._vectors = [self._vectorize(chunk) for chunk in chunks]

    @classmethod
    def from_document(cls, document: LoadedDocument) -> "DocumentAgent":
        return cls(chunk_text(document.text))

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)

    def retrieve(self, question: str, top_k: int = 3) -> list[Source]:
        query_vector = self._vectorize(question)
        scored_chunks = [
            (index, self._cosine_similarity(query_vector, chunk_vector))
            for index, chunk_vector in enumerate(self._vectors)
        ]
        ranked_chunks = sorted(scored_chunks, key=lambda item: item[1], reverse=True)[:top_k]

        return [
            Source(text=self._chunks[index], score=score)
            for index, score in ranked_chunks
            if score > 0
        ]

    def answer(self, question: str) -> AgentAnswer:
        cleaned_question = question.strip()
        if not cleaned_question:
            return AgentAnswer(
                text="Escribe una pregunta para consultar el documento.",
                sources=[],
            )

        sources = self.retrieve(cleaned_question)
        if not sources:
            return AgentAnswer(
                text=(
                    "No encontre informacion suficiente en el documento para responder "
                    "esa pregunta. Intenta reformularla usando terminos presentes en el archivo."
                ),
                sources=[],
            )

        evidence = " ".join(source.text for source in sources)
        response = (
            "Segun el documento, "
            f"{self._compose_response(cleaned_question, evidence)}"
        )
        return AgentAnswer(text=response, sources=sources)

    def suggest_questions(self) -> list[str]:
        return [
            "Que problema resuelve el agente?",
            "Que tecnologias utiliza el proyecto?",
            "Como se demuestra el deploy en OCI?",
            "Como se ejecuta la aplicacion?",
        ]

    def _compose_response(self, question: str, evidence: str) -> str:
        question_lower = question.lower()
        sentences = self._split_sentences(evidence)

        if any(word in question_lower for word in ["como", "ejecuta", "instala", "correr"]):
            return self._join_relevant(sentences, ["ejecut", "instal", "streamlit", "pip", "docker"])

        if any(word in question_lower for word in ["oci", "deploy", "desplieg"]):
            return self._join_relevant(sentences, ["oci", "deploy", "desplieg", "nube", "captura", "enlace"])

        if any(word in question_lower for word in ["tecnologia", "herramienta", "usa", "utiliza"]):
            return self._join_relevant(sentences, ["python", "streamlit", "pandas", "pdf", "csv", "docker"])

        if any(word in question_lower for word in ["problema", "resuelve", "objetivo"]):
            return self._join_relevant(sentences, ["agente", "preguntas", "documento", "pdf", "csv"])

        return self._join_relevant(sentences, [])

    def _join_relevant(self, sentences: list[str], keywords: list[str]) -> str:
        selected = []
        for sentence in sentences:
            normalized = sentence.lower()
            if not keywords or any(keyword in normalized for keyword in keywords):
                selected.append(sentence)
            if len(selected) == 3:
                break

        if not selected:
            selected = sentences[:3]

        return " ".join(selected).strip()

    def _split_sentences(self, text: str) -> list[str]:
        normalized = text.replace("\n", " ")
        raw_sentences = re.split(r"(?<=[.!?])\s+", normalized)
        return [sentence.strip() for sentence in raw_sentences if sentence.strip()]

    def _vectorize(self, text: str) -> Counter:
        tokens = re.findall(r"\b\w{3,}\b", text.lower())
        return Counter(tokens)

    def _cosine_similarity(self, left: Counter, right: Counter) -> float:
        if not left or not right:
            return 0.0

        common_tokens = set(left) & set(right)
        dot_product = sum(left[token] * right[token] for token in common_tokens)
        left_norm = sqrt(sum(value * value for value in left.values()))
        right_norm = sqrt(sum(value * value for value in right.values()))

        if left_norm == 0 or right_norm == 0:
            return 0.0

        return dot_product / (left_norm * right_norm)
