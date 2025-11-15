"""FSM states used in the questionnaire flow."""
from aiogram.fsm.state import State, StatesGroup


class QuestionnaireStates(StatesGroup):
    waiting_for_answer = State()
