import csv
from datetime import datetime

FILENAME = "edzesnaplo.csv"

def add_workout(tipus, ido, kaloria):
    datum = datetime.now().strftime("%Y-%m-%d %H:%M")
    kaloria = kaloria or "-"
    with open(FILENAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datum, tipus, ido, kaloria])

def load_workouts():
    try:
        with open(FILENAME, mode="r") as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        return []
