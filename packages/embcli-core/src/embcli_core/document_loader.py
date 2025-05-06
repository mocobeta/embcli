import csv
from pathlib import Path

from .document import Document


def load_from_csv(file_path: str | Path, delimiter: str = ",") -> list[Document]:
    """
    Load documents from a CSV file. The first column is treated as the document ID,
    and the rest of the columns are treated as the document text.

    Args:
        file_path (str): Path to the CSV file.
        delimiter (str): Delimiter used in the CSV file. Default is ",".

    Returns:
        list[Document]: List of Document objects.
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        documents = []
        reader = csv.reader(file, delimiter=delimiter)
        for row in reader:
            if len(row) < 2:
                continue
            doc_id = row[0]
            doc_text = ",".join(row[1:])
            doc = Document(id=doc_id, text=doc_text)
            documents.append(doc)
    return documents
