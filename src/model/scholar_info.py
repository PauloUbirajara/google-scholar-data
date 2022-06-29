from dataclasses import dataclass


@dataclass(frozen=True)
class ScholarInfo:
    h_index: int
    h10_index: int
    current_year_citations: int
    previous_5year_citations: int
