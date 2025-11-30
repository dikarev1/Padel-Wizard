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

LEVEL_ORDER: tuple[str, ...] = (
    "E-",
    "E",
    "E+",
    "D-",
    "D",
    "D+",
    "C-",
    "C",
    "C+",
)

MIN_EXPERIENCE_LEVEL = "E-"
MAX_EXPERIENCE_LEVEL = "C+"

LEVEL_DESCRIPTIONS: dict[str, str] = {
    "E-": "Новичок",
    "E": "Начинающий",
    "E+": "Продвинутый начинающий",
    "D-": "Базовый уровень",
    "D": "Любитель",
    "D+": "Продвинутый любитель",
    "C-": "Начинающих средний",
    "C": "Средний уровень",
    "C+": "Продвинутый средний",
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

    The algorithm weights the experience score (q1 + q2) based on the player's
    experience band (×3 for E-/E/E+/D-, ×2.5 for D/D+/C-, ×2 for C/C+), adds the
    skill scores from q3–q6, divides the sum by the total weight (experience
    weight + four skill weights), and maps the result back to the nearest
    level.
    
    """

    experience = calculate_player_experience(answers)
    if experience is None:
        return None

    skill_ratings = derive_skill_ratings(answers)
    reliability_level = skill_ratings.reliability
    net_play_level = skill_ratings.net_play
    glass_play_level = skill_ratings.glass_play
    strokes_level = skill_ratings.strokes

    if (
        reliability_level is None
        or net_play_level is None
        or glass_play_level is None
        or strokes_level is None
    ):
        return None

    try:
        experience_score = LEVEL_TO_SCORE[experience.level]
        experience_multiplier = _get_experience_multiplier(experience.level)
        skill_scores = [
            _level_to_score(reliability_level),
            _level_to_score(net_play_level),
            _level_to_score(glass_play_level),
            _level_to_score(strokes_level),
        ]
    except (KeyError, ValueError):
        return None

    total_score = experience_score * experience_multiplier + sum(skill_scores)
    total_weight = experience_multiplier + len(skill_scores)
    average_score = total_score / total_weight
    final_level = _score_to_level(average_score)
    final_level = _clamp_level_by_experience(final_level, experience.level)
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


def _get_experience_multiplier(experience_level: str) -> float:
    if experience_level in ("E-", "E", "E+", "D-"):
        return 3.0
    if experience_level in ("D", "D+", "C-"):
        return 2.5
    if experience_level in ("C", "C+"):
        return 2.0
    raise ValueError(f"Unknown experience level: {experience_level}")


def _clamp_level_by_experience(final_level: str, experience_level: str) -> str:
    try:
        experience_index = LEVEL_ORDER.index(experience_level)
        final_index = LEVEL_ORDER.index(final_level)
    except ValueError:
        return final_level

    min_experience_index = LEVEL_ORDER.index(MIN_EXPERIENCE_LEVEL)
    max_experience_index = LEVEL_ORDER.index(MAX_EXPERIENCE_LEVEL)

    min_index = max(min_experience_index, experience_index - 3)
    max_index = min(max_experience_index, experience_index + 3)

    if final_index < min_index:
        return LEVEL_ORDER[min_index]
    if final_index > max_index:
        return LEVEL_ORDER[max_index]
    return final_level


def get_target_level(level: str) -> str:
    """Return the next level the player can aim for."""

    try:
        current_index = LEVEL_ORDER.index(level)
    except ValueError:
        return level

    next_index = current_index + 1
    if next_index >= len(LEVEL_ORDER):
        return level

    return LEVEL_ORDER[next_index]


def get_level_description(level: str) -> Optional[str]:
    """Return human-readable description for a padel level if known."""

    return LEVEL_DESCRIPTIONS.get(level)

