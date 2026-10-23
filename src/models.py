from pydantic import BaseModel, Field
import uuid
from typing import List


class MinimalSource(BaseModel):
    """
    Represents a single source of information,
    including its path and the range of characters it covers.
    """
    file_path: str
    first_character_index: int
    last_character_index: int

    @property
    def size(self) -> int:
        return self.last_character_index - self.first_character_index


class UnansweredQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    answer: str


class StudentSearchResults(BaseModel):
    search_results: List[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    search_results: List[MinimalAnswer]
    k: int
