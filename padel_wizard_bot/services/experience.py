"""Utilities for calculating and normalizing player experience."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional


Q1_OPTION_MONTHS: dict[str, float] = {
    "q1_1_hours_10": 0.0,
    "q1_1_hours_20_50": 1.0,
    "q1_1_hours_50_100": 2.0,
    "q1_1_hours_100_140": 4.0,
    "q1_1_hours_120_190": 5.0,
    "q1_1_hours_190_290": 7.0,
    "q1_1_hours_290_430": 10.0,
    "q1_1_hours_430_580": 18.0,
    "q1_1_hours_580_plus": 24.0,
}

Q2_OPTION_MONTHS: dict[str, float] = {
    "q2_hours_10": 0.0,
    "q2_hours_20_50": 1.0,
    "q2_hours_50_100": 2.0,
    "q2_hours_100_140": 4.0,
    "q2_hours_120_190": 5.0,
    "q2_hours_190_290": 7.0,
    "q2_hours_290_430": 10.0,
    "q2_hours_430_580": 18.0,
    "q2_hours_580_plus": 24.0,
}

PRIMARY_RACKET_SPORT_OPTIONS: dict[str, str] = {
    "racket_sport_tennis": "Большой теннис",
    "racket_sport_table_tennis": "Настольный теннис",
    "racket_sport_squash": "Сквош",
    "racket_sport_badminton": "Бадминтон",
    "racket_sport_pickleball": "Пикклбол",
    "racket_sport_multiple": "Несколько видов ракетного спорта",
}

RACKET_SPORT_EXPERIENCE_COEFFICIENTS: dict[str, float] = {
    "Большой теннис": 0.65,
    "Настольный теннис": 0.25,
    "Сквош": 0.3,
    "Бадминтон": 0.35,
    "Пикклбол": 0.5,
    "Несколько видов ракетного спорта": 0.5,
}


@dataclass
class PlayerExperience:
    """Normalized representation of combined questionnaire experience."""

    q1_months: float
    q2_months: float
    total_months: float
    level: str
    primary_racket_sport: Optional[str]


EXPERIENCE_LEVEL_THRESHOLDS: tuple[tuple[float, str], ...] = (
    (1.0, "E-"),
    (2.0, "E"),
    (4.0, "E+"),
    (6.0, "D-"),
    (8.0, "D"),
    (11.0, "D+"),
    (15.0, "C-"),
    (24.0, "C"),
)


def calculate_player_experience(
    answers: Iterable[dict[str, Any]]
) -> Optional[PlayerExperience]:
    """Return calculated player experience from questionnaire answers.

    The calculation multiplies the experience selected in q1.1 (other racket
    sports) by a sport-specific coefficient, adds padel experience from q2,
    and maps the total to the configured level thresholds.
    Returns ``None`` until q2 is answered because the padel experience is
    mandatory for deriving the total.
    """

    q1_months = 0.0
    q2_months: Optional[float] = None
    primary_racket_sport: Optional[str] = None

    for answer in answers:
        option_id = answer.get("option_id")
        if option_id in Q1_OPTION_MONTHS:
            q1_months = Q1_OPTION_MONTHS[option_id]
        elif option_id in Q2_OPTION_MONTHS:
            q2_months = Q2_OPTION_MONTHS[option_id]
        elif option_id in PRIMARY_RACKET_SPORT_OPTIONS:
            primary_racket_sport = PRIMARY_RACKET_SPORT_OPTIONS[option_id]

    if q2_months is None:
        return None

    if primary_racket_sport is None:
        racket_sport_coefficient = 1.0
    else:
        racket_sport_coefficient = RACKET_SPORT_EXPERIENCE_COEFFICIENTS.get(
            primary_racket_sport, 1.0
        )
    normalized_q1_months = q1_months * racket_sport_coefficient
    total_months = normalized_q1_months + q2_months
    level = _map_total_months_to_level(total_months)
    return PlayerExperience(
        q1_months=q1_months,
        q2_months=q2_months,
        total_months=total_months,
        level=level,
        primary_racket_sport=primary_racket_sport,
    )


def _map_total_months_to_level(total_months: float) -> str:
    for threshold, level in EXPERIENCE_LEVEL_THRESHOLDS:
        if total_months < threshold:
            return level
    return "C+"
