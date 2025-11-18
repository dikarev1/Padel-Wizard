from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Mapping, Optional

logger = logging.getLogger(__name__)

RATING_SCALE: Mapping[str, float] = {
    "E-": 0.7,
    "E": 1.0,
    "E+": 1.33,
    "D-": 1.66,
    "D": 2.0,
    "D+": 2.33,
    "C-": 2.66,
    "C": 3.0,
    "C+": 3.33,
    "B-": 3.66,
}

SPORT_MULTIPLIERS: Mapping[str, float] = {
    "sport_tennis": 0.65,
    "sport_table_tennis": 0.25,
    "sport_squash": 0.3,
    "sport_badminton": 0.35,
    "sport_pickleball": 0.5,
    "sport_multiple": 0.52,
}

# fmt: off
EXPERIENCE_RANGE_BY_KEY: Mapping[str, tuple[float, Optional[float]]] = {
    "months_lt_1": (0, 1),
    "months_1_2": (1, 2),
    "months_2_4": (2, 4),
    "months_4_6": (4, 6),
    "months_5_8": (5, 8),
    "months_7_11": (7, 11),
    "months_10_15": (10, 15),
    "months_18_24": (18, 24),
    "months_24_plus": (24, None),
}

EXPERIENCE_LEVEL_RANGES: tuple[tuple[str, tuple[float, Optional[float]]], ...] = (
    ("E-", (0, 1)),
    ("E", (1, 2)),
    ("E+", (2, 4)),
    ("D-", (4, 6)),
    ("D", (5, 8)),
    ("D+", (7, 11)),
    ("C-", (10, 15)),
    ("C", (18, 24)),
    ("C+", (24, None)),
)
# fmt: on


@dataclass(frozen=True)
class ExperienceResult:
    other_sport_option_id: Optional[str]
    raw_other_months: float
    adjusted_other_months: float
    padel_months: float
    total_months: float
    level: str
    rating_value: float

    def as_dict(self) -> dict[str, object]:
        return {
            "other_sport_option_id": self.other_sport_option_id,
            "raw_other_months": self.raw_other_months,
            "adjusted_other_months": self.adjusted_other_months,
            "padel_months": self.padel_months,
            "total_months": self.total_months,
            "level": self.level,
            "rating_value": self.rating_value,
        }


def _extract_range_key(option_id: str) -> str:
    if "months" not in option_id:
        raise KeyError(f"Option id {option_id!r} does not contain months mapping")

    start_index = option_id.index("months")
    return option_id[start_index:]


def _range_to_months(range_key: str) -> float:
    lower, upper = EXPERIENCE_RANGE_BY_KEY[range_key]
    if upper is None:
        return float(lower)
    return (lower + upper) / 2


def months_from_option(option_id: str) -> float:
    range_key = _extract_range_key(option_id)
    if range_key not in EXPERIENCE_RANGE_BY_KEY:
        raise KeyError(f"Unknown experience range key: {range_key!r}")
    return _range_to_months(range_key)


def select_level_for_months(total_months: float) -> str:
    matched_levels = []
    for level, (lower, upper) in EXPERIENCE_LEVEL_RANGES:
        if total_months < lower:
            continue
        if upper is not None and total_months > upper:
            continue
        matched_levels.append(level)

    if not matched_levels:
        future_levels = [
            (level, lower)
            for level, (lower, _upper) in EXPERIENCE_LEVEL_RANGES
            if lower > total_months
        ]
        if future_levels:
            return min(future_levels, key=lambda item: item[1])[0]
        raise ValueError(f"No rating level matches {total_months} months")

    selected = max(matched_levels, key=lambda lvl: RATING_SCALE[lvl])
    return selected


def calculate_experience(
    *,
    padel_option_id: str,
    other_sport_option_id: Optional[str],
    other_experience_option_id: Optional[str],
) -> ExperienceResult:
    padel_months = months_from_option(padel_option_id)

    if other_sport_option_id is None or other_experience_option_id is None:
        adjusted_other = 0.0
        raw_other = 0.0
    else:
        raw_other = months_from_option(other_experience_option_id)
        multiplier = SPORT_MULTIPLIERS.get(other_sport_option_id, 0.0)
        adjusted_other = raw_other * multiplier

    total_months = padel_months + adjusted_other
    level = select_level_for_months(total_months)
    rating_value = RATING_SCALE[level]

    logger.debug(
        "Calculated experience: padel_months=%.2f, raw_other=%.2f, adjusted_other=%.2f, "
        "total_months=%.2f, level=%s, rating_value=%.2f",
        padel_months,
        raw_other,
        adjusted_other,
        total_months,
        level,
        rating_value,
    )

    return ExperienceResult(
        other_sport_option_id=other_sport_option_id,
        raw_other_months=raw_other,
        adjusted_other_months=adjusted_other,
        padel_months=padel_months,
        total_months=total_months,
        level=level,
        rating_value=rating_value,
    )
