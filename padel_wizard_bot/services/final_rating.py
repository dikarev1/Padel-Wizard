"""Utilities for deriving the final padel rating from questionnaire answers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional

from padel_wizard_bot.services.experience import calculate_player_experience
from padel_wizard_bot.services.scoring_engine import (
    SkillRatings,
    derive_skill_ratings,
)


LEVEL_TO_SCORE: dict[str, float] = {
    "E-": 0.66,
    "E": 1.0,
    "E+": 1.33,
    "D-": 1.66,
    "D": 2.0,
    "D+": 2.33,
    "C-": 2.66,
    "C": 3.0,
    "C+": 3.33,
}


@dataclass(frozen=True)
class FinalRating:
    """Combined questionnaire rating mapped back to a padel level."""

    level: str
    score: float
    experience_level: str
    skill_levels: SkillRatings


def calculate_final_rating(
    answers: Iterable[dict[str, Any]]
) -> Optional[FinalRating]:
    """Return final aggregated rating from questionnaire answers.

    The algorithm doubles the experience score (q1 + q2), adds the skill
    scores from q3–q6, divides the sum by six, and maps the result back to the
    nearest level.
    """

    experience = calculate_player_experience(answers)
    if experience is None:
        return None

    skill_ratings = derive_skill_ratings(answers)
    skill_levels = [
        skill_ratings.reliability,
        skill_ratings.net_play,
        skill_ratings.glass_play,
        skill_ratings.strokes,
    ]

    if any(level is None for level in skill_levels):
        return None

    try:
        experience_score = LEVEL_TO_SCORE[experience.level]
        skill_scores = [_level_to_score(level) for level in skill_levels]
    except KeyError:
        return None

    total_score = experience_score * 2 + sum(skill_scores)
    average_score = total_score / 6
    final_level = _score_to_level(average_score)
    return FinalRating(
        level=final_level,
        score=average_score,
        experience_level=experience.level,
        skill_levels=skill_ratings,
    )


def _level_to_score(level: str) -> float:
    return LEVEL_TO_SCORE[level]


def _score_to_level(score: float) -> str:
    return min(LEVEL_TO_SCORE.items(), key=lambda item: abs(item[1] - score))[0]

