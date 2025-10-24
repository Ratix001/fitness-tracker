import flet as ft
from views.workout_ui import main as workout_main

if __name__ == "__main__":
    ft.app(target=workout_main, view=ft.AppView.WEB_BROWSER, port=8550)
