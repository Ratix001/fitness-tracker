import csv
from pathlib import Path
from typing import List

from models.workout import Workout

# Resolve CSV file relative to project root
FILENAME = str(Path(__file__).resolve().parents[1] / "edzesnaplo.csv")

def add_workout(workout: Workout) -> None:
    with open(FILENAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(workout.to_csv_row())

def load_workouts() -> List[Workout]:
    workouts: List[Workout] = []
    try:
        with open(FILENAME, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                w = Workout.from_csv_row(row)
                if w:
                    workouts.append(w)
    except FileNotFoundError:
        return []
    return workouts
