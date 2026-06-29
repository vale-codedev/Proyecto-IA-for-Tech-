from dataclasses import dataclass
import csv
from pathlib import Path


@dataclass(frozen=True)
class LoadedDocument:
    path: Path
    text: str


def load_document(path: Path) -> LoadedDocument:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text = _load_pdf(path)
    elif suffix == ".csv":
        text = _load_csv(path)
    else:
        raise ValueError("Formato no soportado. Usa un archivo PDF o CSV.")

    return LoadedDocument(path=path, text=text)


def _load_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Para leer archivos PDF instala las dependencias con: pip install -r requirements.txt"
        ) from exc

    reader = PdfReader(str(path))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(f"Pagina {page_number}: {text}")
    return "\n\n".join(pages)


def _load_csv(path: Path) -> str:
    rows = []
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row_number, row in enumerate(reader, start=1):
            values = [
                f"{column}: {value}"
                for column, value in row.items()
                if value and str(value).strip()
            ]
            rows.append(f"Fila {row_number}. " + ". ".join(values))

    if rows:
        return "\n".join(rows)

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for row_number, row in enumerate(reader, start=1):
            values = [value for value in row if value.strip()]
            if values:
                rows.append(f"Fila {row_number}. " + ". ".join(values))

    return "\n".join(rows)
