from data.workout_repository import add_workout, load_workouts

def save_new_workout(tipus, ido, kaloria):
    if not tipus or not ido:
        return "❌ Töltsd ki az edzés típusát és idejét!"
    add_workout(tipus, ido, kaloria)
    return "✅ Edzés elmentve!"

def get_all_workouts():
    return load_workouts()
