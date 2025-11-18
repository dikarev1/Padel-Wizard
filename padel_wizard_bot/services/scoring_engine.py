from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Mapping, MutableMapping, Optional, Sequence


# ---------- RATING SCALE ----------

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


# ---------- QUESTION-BASED RATING MAPS ----------

# mapping: question_id -> {answer_option_id -> rating_value}
SKILL_QUESTIONS_RATING_MAP: MutableMapping[str, Dict[str, float]] = {
    "q3": {},
    "q4": {},
    "q5": {},
    "q6": {},
}

# mapping: question_id -> {answer_option_id -> rating_value}
EXPERIENCE_QUESTIONS_RATING_MAP: MutableMapping[str, Dict[str, float]] = {
    "q1.1": {},
    "q2": {},
}


# ---------- EXPERIENCE AGGREGATION ----------

@dataclass
class ExperienceEntry:
    """Represents experience in a single racket sport."""

    sport_id: str
    hours: float
    multiplier: float

    def to_padel_hours(self) -> float:
        """Project experience into padel equivalent using multiplier."""
        return self.hours * self.multiplier


@dataclass
class ExperienceSummary:
    """Aggregated experience across padel and other racket sports."""

    padel_hours: float
    other_sports: Sequence[ExperienceEntry] = field(default_factory=tuple)

    @property
    def total_effective_hours(self) -> float:
        """Total padel-equivalent experience hours."""
        additional_hours = sum(entry.to_padel_hours() for entry in self.other_sports)
        return self.padel_hours + additional_hours


def map_experience_to_rating(summary: ExperienceSummary) -> Optional[float]:
    """Convert aggregated experience hours into a rating placeholder.

    The concrete mapping will be defined later based on business logic.
    """

    # Placeholder for future mapping logic.
    return None


# ---------- FINAL RATING ENGINE ----------

@dataclass
class RatingEngine:
    """Coordinates the rating calculation pipeline."""

    skill_map: Mapping[str, Dict[str, float]] = field(
        default_factory=lambda: SKILL_QUESTIONS_RATING_MAP
    )
    experience_map: Mapping[str, Dict[str, float]] = field(
        default_factory=lambda: EXPERIENCE_QUESTIONS_RATING_MAP
    )

    def calculate_skill_rating(self, answers: Mapping[str, str]) -> Optional[float]:
        """Map skill-related answers (q3–q6) to a rating placeholder."""

        # Placeholder for future aggregation logic.
        return None

    def calculate_experience_rating(
        self, experience_answers: Mapping[str, str], summary: ExperienceSummary
    ) -> Optional[float]:
        """Evaluate experience-based rating before adjustments."""

        # Placeholder for future experience rating logic.
        return map_experience_to_rating(summary)

    def calculate_final_rating(
        self, answers: Mapping[str, str], summary: ExperienceSummary
    ) -> Optional[float]:
        """Calculate final rating based on questionnaire answers and experience.

        The algorithm starts from the experience-derived rating and then adjusts it
        up or down using skill answers. Final reconciliation rules will be applied
        later.
        """

        experience_rating = self.calculate_experience_rating({}, summary)
        skill_rating = self.calculate_skill_rating(answers)

        # Placeholder for future rating engine logic.
        _ = experience_rating, skill_rating
        return None
