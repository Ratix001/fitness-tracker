import csv
import sys
import os
from pathlib import Path
from typing import List
from models.workout import Workout


if getattr(sys, "frozen", False):
    # PROD
    user_data_dir = os.path.join(os.path.expanduser("~"), "Edzesnaplo")
    os.makedirs(user_data_dir, exist_ok=True)
else:
    # DEV
    user_data_dir = Path(__file__).resolve().parents[1]

FILE = os.path.join(user_data_dir, "edzesnaplo.csv")
FIELDNAMES = ["id", "datum", "tipus", "ido_perc", "kaloria"]

def add_workout(workout: Workout) -> None:

    file_exists = os.path.exists(FILE)

    with open(FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(workout.to_csv_row())


def load_workouts() -> List[Workout]:
    workouts: List[Workout] = []
    try:
        with open(FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                w = Workout.from_csv_row(list(row.values()))
                if w:
                    workouts.append(w)
    except FileNotFoundError:
        return []
    return workouts


def delete_workout(workout_id: str) -> None:
    rows = []
    with open(FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["id"] != workout_id:
                rows.append(row)

    with open(FILE, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

