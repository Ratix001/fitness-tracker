from datetime import date, timedelta
from typing import Dict, Any, List, Optional, Set, Tuple

from models.workout import Workout
import data.workout_repository as wr


def save_new_workout(tipus: str, ido: str, kaloria: Optional[str]) -> Dict[str, Any]:
    """
    Validate inputs, persist, and return a structured result:
    { ok: bool, message: str, data: Optional[Workout] }
    """
    tipus = (tipus or "").strip()
    ido = (ido or "").strip()
    kaloria = (kaloria or "").strip() if kaloria is not None else None

    if not tipus or not ido:
        return {"ok": False, "message": "Töltsd ki az edzés típusát és idejét!", "data": None}

    try:
        ido_perc = int(ido)
        if ido_perc <= 0:
            raise ValueError
    except Exception:
        return {"ok": False, "message": "Az időtartam legyen pozitív egész szám (perc)!", "data": None}

    kal: Optional[int] = None
    if kaloria:
        try:
            kal = int(kaloria)
            if kal < 0:
                raise ValueError
        except Exception:
            return {"ok": False, "message": "A kalória opcionális, de ha megadod, legyen nemnegatív egész szám!", "data": None}

    workout = Workout.now(tipus=tipus, ido_perc=ido_perc, kaloria=kal)
    wr.add_workout(workout)
    return {"ok": True, "message": "Edzés elmentve!", "data": workout}


def delete_workout_by_id(workout_id: str) -> Dict[str, Any]:
    wr.delete_workout(workout_id)
    return {"ok": True, "message": "Edzés törölve!"}


def delete_all_workouts_controller() -> Dict[str, Any]:
    wr.delete_all_workouts()
    return {"ok": True, "message": "Összes edzés törölve!"}


def get_all_workouts() -> List[Workout]:
    return wr.load_workouts()


def get_week_overview(today: Optional[date] = None) -> Set[str]:
    """
    Return set of 'YYYY-MM-DD' strings that have workouts in the current week.
    """
    if today is None:
        today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    days_with_workout: Set[str] = set()
    for w in wr.load_workouts():
        try:
            d_str = w.date_str()
            d_obj = date.fromisoformat(d_str)
            if start_of_week <= d_obj < end_of_week:
                days_with_workout.add(d_str)
        except Exception:
            continue
    return days_with_workout


def get_weekly_minutes(today: Optional[date] = None) -> List[int]:
    """
    Returns a list of 7 integers representing total minutes per day
    for the current week (Monday..Sunday), based on saved workouts.
    """
    if today is None:
        today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=7)

    totals = [0] * 7  # Mon..Sun
    for w in wr.load_workouts():
        try:
            d_obj = date.fromisoformat(w.date_str())
        except Exception:
            continue
        if start_of_week <= d_obj < end_of_week:
            idx = (d_obj - start_of_week).days
            if 0 <= idx < 7:
                totals[idx] += int(w.ido_perc or 0)
    return totals


def get_weekly_calories(today: Optional[date] = None) -> List[int]:
    """
    Returns a list of 7 integers representing total calories per day
    for the current week (Monday..Sunday), based on saved workouts.
    """
    if today is None:
        today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    totals = [0] * 7
    for w in wr.load_workouts():
        try:
            d_obj = date.fromisoformat(w.date_str())
        except Exception:
            continue
        if start_of_week <= d_obj < end_of_week:
            idx = (d_obj - start_of_week).days
            if 0 <= idx < 7 and w.kaloria is not None:
                totals[idx] += int(w.kaloria)
    return totals


def _get_month_bounds(today: Optional[date] = None) -> Tuple[date, date, int]:
    if today is None:
        today = date.today()
    first_day = today.replace(day=1)
    if first_day.month == 12:
        next_month = date(first_day.year + 1, 1, 1)
    else:
        next_month = date(first_day.year, first_day.month + 1, 1)
    days_in_month = (next_month - first_day).days
    return first_day, next_month, days_in_month


def get_month_day_labels(today: Optional[date] = None) -> List[str]:
    _, _, days_in_month = _get_month_bounds(today)
    return [f"{i + 1:02d}" for i in range(days_in_month)]


def get_monthly_minutes(today: Optional[date] = None) -> List[int]:
    first_day, next_month, days_in_month = _get_month_bounds(today)
    totals = [0] * days_in_month
    for w in wr.load_workouts():
        try:
            d_obj = date.fromisoformat(w.date_str())
        except Exception:
            continue
        if first_day <= d_obj < next_month:
            idx = (d_obj - first_day).days
            if 0 <= idx < days_in_month:
                totals[idx] += int(w.ido_perc or 0)
    return totals


def get_monthly_calories(today: Optional[date] = None) -> List[int]:
    first_day, next_month, days_in_month = _get_month_bounds(today)
    totals = [0] * days_in_month
    for w in wr.load_workouts():
        try:
            d_obj = date.fromisoformat(w.date_str())
        except Exception:
            continue
        if first_day <= d_obj < next_month and w.kaloria is not None:
            idx = (d_obj - first_day).days
            if 0 <= idx < days_in_month:
                totals[idx] += int(w.kaloria)
    return totals
