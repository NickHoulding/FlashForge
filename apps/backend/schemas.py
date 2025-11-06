from pydantic import BaseModel
from typing import List

class Flashcard(BaseModel):
    question: str
    answer: str

class StudySet(BaseModel):
    flashcards: List[Flashcard]
