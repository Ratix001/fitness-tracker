from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


DATETIME_FMT = "%Y-%m-%d %H:%M"
DATE_FMT = "%Y-%m-%d"


@dataclass
class Workout:
    datum: str
    tipus: str
    ido_perc: int
    kaloria: Optional[int] = None

    @staticmethod
    def now(tipus: str, ido_perc: int, kaloria: Optional[int]) -> "Workout":
        return Workout(
            datum=datetime.now().strftime(DATETIME_FMT),
            tipus=tipus,
            ido_perc=ido_perc,
            kaloria=kaloria,
        )

    @staticmethod
    def from_csv_row(row: List[str]) -> Optional["Workout"]:
        if not row or len(row) < 4:
            return None
        datum, tipus, ido_str, kaloria_str = row[0], row[1], row[2], row[3]
        try:
            # Validate date format but keep as string for UI compatibility
            datetime.strptime(datum, DATETIME_FMT)
        except Exception:
            # Try fallback where seconds might exist, slice to minutes
            try:
                datum = datum[:16]
                datetime.strptime(datum, DATETIME_FMT)
            except Exception:
                return None
        try:
            ido_perc = int(ido_str)
        except Exception:
            return None
        kal: Optional[int]
        if kaloria_str and kaloria_str != "-":
            try:
                kal = int(kaloria_str)
            except Exception:
                kal = None
        else:
            kal = None
        return Workout(datum=datum, tipus=tipus, ido_perc=ido_perc, kaloria=kal)

    def to_csv_row(self) -> List[str]:
        return [
            self.datum,
            self.tipus,
            str(self.ido_perc),
            str(self.kaloria) if self.kaloria is not None else "-",
        ]

    def date_str(self) -> str:
        """Return 'YYYY-MM-DD' portion for week calculations."""
        return self.datum[:10]
