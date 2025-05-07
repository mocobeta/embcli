from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar


class DocumentBase(ABC):
    @abstractmethod
    def docid(self) -> str:
        pass

    @abstractmethod
    def source_text(self) -> str:
        pass


DocumentType = TypeVar("DocumentType", bound=DocumentBase)


@dataclass
class Document(DocumentBase):
    id: str
    text: str

    def docid(self):
        return self.id

    def source_text(self) -> str:
        return self.text


@dataclass
class HitDocument:
    score: float
    doc: Document
