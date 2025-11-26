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
        text="Вопрос 6️⃣ \ 6️⃣:\n\n"
        "Наконец, какими ударами ты владеешь?",
        options=(
            AnswerOption("q6_opt1", "Forehand", None),
            AnswerOption("q6_opt2", "Forehand, Backhand", None),
            AnswerOption("q6_opt3", "Удары выше + Volley, Lob", None),
            AnswerOption("q6_opt4", "Удары выше + Backhand Volley, half-Volley", None),
            AnswerOption("q6_opt5", "Удары выше + Bandeja, flat Smash/x4", None),
            AnswerOption("q6_opt6", "Удары выше + Bajada, Vibora", None),
            AnswerOption("q6_opt7", "Удары выше + Gancho/Rulo, Chiquita, Drop-shot", None),
            AnswerOption("q6_opt8", "Удары выше + Smash x3/Topspin", None),
            AnswerOption("q6_opt9", "Практически все доступные удары и с контролем вращения", None),
        ),
    )

    q5 = Question(
        id="q5",
        text="Вопрос 5️⃣ \ 6️⃣:\n\n"
        "Как бы ты описал свою игру от стекла?",
        options=(
            AnswerOption("q5_opt1", "Не играю от стекла — мне проще сыграть с лёта", "q6"),
            AnswerOption("q5_opt2", "Иногда получается играть от заднего стекла", "q6"),
            AnswerOption("q5_opt3", "Активно обучаюсь игре от заднего стекла", "q6"),
            AnswerOption("q5_opt4", "Регулярно получается играть от заднего стекла", "q6"),
            AnswerOption("q5_opt5", "Уверенно возвращаю удары от заднего стекла, но мне сложно вернуть от двойного", "q6"),
            AnswerOption("q5_opt6", "Регулярно получается защитить удары от двойного стекла и очень низкие мячи", "q6"),
        ),
    )

    q4 = Question(
        id="q4",
        text="Вопрос 4️⃣ \ 6️⃣:\n\n"
        "Как бы ты описал свою игру <b>у сетки</b>?",
        options=(
            AnswerOption("q4_opt1", "Не выхожу к сетке", "q5"),
            AnswerOption("q4_opt2", "Очень редко выхожу к сетке", "q5"),
            AnswerOption("q4_opt3", "Выхожу к сетке, но чувствую себя неуверенно", "q5"),
            AnswerOption("q4_opt4", "Могу ударить с лёту c двух рук, но с некоторыми трудностями", "q5"),
            AnswerOption("q4_opt5", "Занимаю верную позицию у сетки и уверенно играю с лёту", "q5"),
            AnswerOption("q4_opt6", "Атакую с лёту глубоко и с низким отскоком от стекла", "q5"),
        ),
    )

    q3 = Question(
        id="q3",
        text=(
            "Вопрос 3️⃣ \ 6️⃣:\n\n"
            "В скольких процентах случаев ты бы отбил *сложный мяч, примерно как на видео ниже?\n"
            "*Сложный мяч — это мяч с низким отскоком и высокой скоростью. "
            "Либо мяч, который застал игрока вне позиции в результате удачной комбинации ударов противника"
            ""
        ),
        options=(
            AnswerOption("q3_opt1", "Стараюсь просто попадать по мячу", "q4"),
            AnswerOption("q3_opt2", "5-10%", "q4"),
            AnswerOption("q3_opt3", "10–20%", "q4"),
            AnswerOption("q3_opt4", "20–30%", "q4"),
            AnswerOption("q3_opt5", "30–40%", "q4"),
            AnswerOption("q3_opt6", "40–50%", "q4"),
            AnswerOption("q3_opt7", "50–60%", "q4"),
            AnswerOption("q3_opt8", "60-75%", "q4"),
            AnswerOption("q3_opt9", "75%–90%", "q4"),
        ),
    )

    q2 = Question(
        id="q2",
        text=(
        "Вопрос 2️⃣ \ 6️⃣:\n\n"
        "Переходим к опыту* игры в Падел.\n"
        "Как долго ты игрыаешь в Падел-теннис?\n" 
        "(*Один месяц игры приведен из расчета в 3-5 часов в неделю)"
        ),
        options=(
            AnswerOption("q2_hours_10", "Меньше месяца", "q3"),
            AnswerOption("q2_hours_20_50", "1–2 месяца", "q3"),
            AnswerOption("q2_hours_50_100", "2–4 месяца", "q3"),
            AnswerOption("q2_hours_100_140", "4–6 месяца", "q3"),
            AnswerOption("q2_hours_120_190", "5–8 месяцев", "q3"),
            AnswerOption("q2_hours_190_290", "7–11 месяцев", "q3"),
            AnswerOption("q2_hours_290_430", "10–15 месяцев", "q3"),
            AnswerOption("q2_hours_430_580", "1.5–2 года", "q3"),
            AnswerOption("q2_hours_580_plus", "2+ года", "q3"),
        ),
    )

    q1_1 = Question(
        id="q1.1",
        text="Вопрос 1️⃣ \ 6️⃣:\n\n"
        "Какой сумарный опыт* игры?\n\n"
        "(*Один месяц игры приведен из расчета в 3-5 часов в неделю)"
        ,
        options=(
            AnswerOption("q1_1_hours_10", "Меньше месяца", "q2"),
            AnswerOption("q1_1_hours_20_50", "1–2 месяца", "q2"),
            AnswerOption("q1_1_hours_50_100", "2–4 месяца", "q2"),
            AnswerOption("q1_1_hours_100_140", "4–6 месяцев", "q2"),
            AnswerOption("q1_1_hours_120_190", "5–8 месяцев", "q2"),
            AnswerOption("q1_1_hours_190_290", "7–11 месяцев", "q2"),
            AnswerOption("q1_1_hours_290_430", "10–15 месяцев", "q2"),
            AnswerOption("q1_1_hours_430_580", "1.5–2 года", "q2"),
            AnswerOption("q1_1_hours_580_plus", "2+ года", "q2"),
        ),
    )

    q1_2 = Question(
        id="q1.2",
        text="Какой опыт игры в этот вид?"
        ,
        options=(
            AnswerOption("hours_10", "10", "q2"),
            AnswerOption("hours_100", "100", "q2"),
            AnswerOption("hours_500", "500", "q2"),
            AnswerOption("hours_1000", "1000", "q2"),
        ),
    )

    q1_sports = Question(
        id="q1.sports",
        text=f"Вопрос 1️⃣ \ 6️⃣:\n\n"
        "Супер! В каком у тебя сыграно заметно больше всего часов?\n"
        "(если одного такого нет - выбери вариант «Несколько видов»)",
        options=(
            AnswerOption("racket_sport_tennis", "Большой теннис", "q1.1"),
            AnswerOption("racket_sport_table_tennis", "Настольный теннис", "q1.1"),
            AnswerOption("racket_sport_squash", "Бадминтон", "q1.1"),
            AnswerOption("racket_sport_badminton", "Cквош", "q1.1"),
            AnswerOption("racket_sport_pickleball", "Пикклбол", "q1.1"),
            AnswerOption("racket_sport_multiple", "Несколько видов", "q1.1"),
        ),
    )

    q1 = Question(
        id="q1",
        text=(
        "⬇︎\n"
        "Вопрос 1️⃣ \ 6️⃣:\n\n"
        "Есть ли у тебя <b>опыт игры</b> в другие виды спорта, в которых как и в Паддле <b>используется ракетка и мяч?</b>\n"
        ),
        options=(
            AnswerOption("has_experience", "Да, у меня есть опыт", "q1.sports"),
            AnswerOption("no_experience", "Нет, у меня отсуствует или очень мало опыта", "q2"),
        ),
    )

    return QuestionnaireFlow(
        questions=(q1, q1_sports, q1_1, q1_2, q2, q3, q4, q5, q6),
        first_question_id="q1",
    )


DEFAULT_FLOW = build_default_flow()
