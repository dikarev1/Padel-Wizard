from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, Optional, Tuple


# ---------- MODELS ----------

@dataclass(frozen=True)
class AnswerOption:
    """Represents a selectable answer in the questionnaire."""
    id: str
    text: str
    next_question_id: Optional[str]


@dataclass(frozen=True)
class Question:
    """A questionnaire question with predefined answer options."""
    id: str
    text: str
    options: Tuple[AnswerOption, ...]

    def get_option(self, option_id: str) -> AnswerOption:
        for option in self.options:
            if option.id == option_id:
                return option
        raise KeyError(f"Option {option_id!r} is not defined for question {self.id!r}")


# ---------- FLOW ----------

class QuestionnaireFlow:
    """Stores questionnaire structure and navigation helpers."""

    def __init__(self, questions: Iterable[Question], first_question_id: str) -> None:
        self._questions: Dict[str, Question] = {q.id: q for q in questions}
        if first_question_id not in self._questions:
            raise ValueError("First question id must exist in the questionnaire")
        self._first_question_id = first_question_id

    @property
    def first_question_id(self) -> str:
        return self._first_question_id

    def get_question(self, question_id: str) -> Question:
        try:
            return self._questions[question_id]
        except KeyError as exc:
            raise KeyError(f"Question {question_id!r} is not registered in the flow") from exc

    def resolve_next(self, current_question_id: str, option_id: str) -> Optional[str]:
        question = self.get_question(current_question_id)
        option = question.get_option(option_id)
        return option.next_question_id


# ---------- DEFAULT FLOW ----------

def build_default_flow() -> QuestionnaireFlow:
    q6 = Question(
        id="q6",
        text="[Placeholder] Question 6 about padel specifics.",
        options=(
            AnswerOption("q6_opt1", "Sample answer", None),
            AnswerOption("q6_opt2", "Another sample answer", None),
        ),
    )

    q5 = Question(
        id="q5",
        text="[Placeholder] Question 5 that leads to the final screen.",
        options=(
            AnswerOption("q5_opt1", "Sample answer", "q6"),
            AnswerOption("q5_opt2", "Another sample answer", "q6"),
        ),
    )

    q4 = Question(
        id="q4",
        text="[Placeholder] Question 4 about tactical awareness.",
        options=(
            AnswerOption("q4_opt1", "Sample answer", "q5"),
            AnswerOption("q4_opt2", "Another sample answer", "q5"),
        ),
    )

    q3 = Question(
        id="q3",
        text="[Placeholder] Question 3 about technical skills.",
        options=(
            AnswerOption("q3_opt1", "Sample answer", "q4"),
            AnswerOption("q3_opt2", "Another sample answer", "q4"),
        ),
    )

    q2 = Question(
        id="q2",
        text="[Placeholder] Question 2 about padel experience.",
        options=(
            AnswerOption("q2_opt1", "Sample answer", "q3"),
            AnswerOption("q2_opt2", "Another sample answer", "q3"),
        ),
    )

    q1_1 = Question(
        id="q1.1",
        text="[Placeholder] Question 1.1 requesting details about racket sport experience.",
        options=(
            AnswerOption("q1_1_opt1", "Sample answer", "q2"),
            AnswerOption("q1_1_opt2", "Another sample answer", "q2"),
        ),
    )

    q1 = Question(
        id="q1",
        text="[Placeholder] Question 1 asking about racket sport experience.",
        options=(
            AnswerOption("has_experience", "Yes, I have racket sport experience", "q1.1"),
            AnswerOption("no_experience", "No, padel is my first racket sport", "q2"),
        ),
    )

    return QuestionnaireFlow(
        questions=(q1, q1_1, q2, q3, q4, q5, q6),
        first_question_id="q1",
    )


DEFAULT_FLOW = build_default_flow()
