"""Scoring utilities for mapping questionnaire answers to padel levels."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional


@dataclass(frozen=True)
class SkillRatings:
    """Container for skill-specific levels derived from questionnaire answers."""

    reliability: Optional[str]
    net_play: Optional[str]
    glass_play: Optional[str]
    strokes: Optional[str]


Q3_OPTION_LEVELS: dict[str, str] = {
    "q3_opt1": "E-",
    "q3_opt2": "E",
    "q3_opt3": "E+",
    "q3_opt4": "D-",
    "q3_opt5": "D",
    "q3_opt6": "D+",
    "q3_opt7": "C-",
    "q3_opt8": "C",
    "q3_opt9": "C+",
}

Q4_OPTION_LEVELS: dict[str, str] = {
    "q4_opt1": "E-",
    "q4_opt2": "E",
    "q4_opt3": "E+",
    "q4_opt4": "D",
    "q4_opt5": "C-",
    "q4_opt6": "C+",
}

Q5_OPTION_LEVELS: dict[str, str] = {
    "q5_opt1": "E-",
    "q5_opt2": "E",
    "q5_opt3": "E+",
    "q5_opt4": "D",
    "q5_opt5": "C-",
    "q5_opt6": "C",
}

Q6_OPTION_LEVELS: dict[str, str] = {
    "q6_opt1": "E-",
    "q6_opt2": "E",
    "q6_opt3": "E+",
    "q6_opt4": "D-",
    "q6_opt5": "D",
    "q6_opt6": "D+",
    "q6_opt7": "C-",
    "q6_opt8": "C",
    "q6_opt9": "C+",
}

QUESTION_LEVEL_FEATURES: dict[str, tuple[str, dict[str, str]]] = {
    "q3": ("reliability", Q3_OPTION_LEVELS),
    "q4": ("net_play", Q4_OPTION_LEVELS),
    "q5": ("glass_play", Q5_OPTION_LEVELS),
    "q6": ("strokes", Q6_OPTION_LEVELS),
}


def derive_skill_ratings(answers: Iterable[dict[str, Any]]) -> SkillRatings:
    """Return per-skill levels for answered skill questions."""

    ratings: dict[str, Optional[str]] = {
        "reliability": None,
        "net_play": None,
        "glass_play": None,
        "strokes": None,
    }

    for answer in answers:
        question_id = answer.get("question_id")
        option_id = answer.get("option_id")
        feature = QUESTION_LEVEL_FEATURES.get(str(question_id))
        if feature is None:
            continue

        attribute_name, option_levels = feature
        ratings[attribute_name] = option_levels.get(str(option_id))

    return SkillRatings(**ratings)
