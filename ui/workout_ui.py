import flet as ft
from logic.workout_controller import save_new_workout, get_all_workouts

def main(page: ft.Page):
    page.title = "🏋️ Edzésnapló"
    greeting_text = ft.Text("Fitness Tracker", size=22, weight="bold", color="#27ae60")
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    tipus_input = ft.TextField(label="Edzés típusa (pl. futás, súlyzós)", width=300)
    ido_input = ft.TextField(label="Időtartam (perc)", width=300)
    kaloria_input = ft.TextField(label="Kalória (opcionális)", width=300)

    lista = ft.Column()

    def betoltes(e=None):
        lista.controls.clear()
        for sor in get_all_workouts():
            lista.controls.append(
                ft.Text(f"{sor[0]} | {sor[1]} | {sor[2]} perc | {sor[3]} kcal")
            )
        page.update()
        try:
            refresh_week_row()
        except Exception:
            pass

    def edzes_hozzaad(e):
        uzenet = save_new_workout(tipus_input.value, ido_input.value, kaloria_input.value)

        snack = ft.SnackBar(
            content=ft.Text(uzenet, color="white"),
            bgcolor="#27ae60" if "✅" in uzenet else "#c0392b",
            duration=3000
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

        tipus_input.value = ""
        ido_input.value = ""
        kaloria_input.value = ""
        page.update()
        betoltes()

    hozzaad_btn = ft.ElevatedButton("Edzés mentése", on_click=edzes_hozzaad)
    frissit_btn = ft.OutlinedButton("Lista frissítése", on_click=betoltes)

    # Aktuális hét napjai
    import calendar
    from datetime import date, timedelta
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    days = [(start_of_week + timedelta(days=i)) for i in range(7)]
    day_names = [calendar.day_abbr[d.weekday()] for d in days]

    week_row = ft.Row([], alignment=ft.MainAxisAlignment.CENTER)

    def refresh_week_row():
        workouts_local = get_all_workouts()
        workout_days_local = set()
        for w in workouts_local:
            try:
                workout_date = w[0][:10]
                workout_days_local.add(workout_date)
            except Exception:
                pass

        day_circles_local = []
        for i, d in enumerate(days):
            day_str = d.strftime("%Y-%m-%d")
            bg = "#27ae60" if day_str in workout_days_local else "white"
            fg = "white" if bg != "white" else "#27ae60"
            day_circles_local.append(
                ft.Container(
                    content=ft.Text(day_names[i], size=16, weight="bold", color=fg),
                    width=40,
                    height=40,
                    bgcolor=bg,
                    border_radius=20,
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(right=8),
                    border=ft.border.all(1, "#27ae60")
                )
            )

        week_row.controls.clear()
        week_row.controls.extend(day_circles_local)
        page.update()

    # Tracker szekciók (Víz, Lépések)
    def viz_click(e):
        page.update()
    def lepes_click(e):
        page.update()
    tracker_row = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.WATER_DROP, size=32, color="#27ae60"),
                ft.Row([
                    ft.Text("2 350", size=26, weight="bold", color="#27ae60"),
                    ft.Text("ml", size=14, color="#27ae60", italic=True)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Text("Víz", size=16, weight="bold", color="#27ae60", text_align="start"),
                ft.Row([
                    ft.ProgressBar(value=0.75, color="#27ae60", bgcolor="#d4f5e9", width=110, height=8),
                    ft.Text("105%", size=12, color="#27ae60", weight="bold", text_align="right")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True, spacing=8, height=20, width=140),
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START, spacing=8),
            width=170,
            height=160,
            bgcolor="#eafaf1",
            border_radius=24,
            alignment=ft.alignment.top_left,
            margin=ft.margin.only(right=16),
            padding=12,
            on_click=viz_click,
        ),
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.DIRECTIONS_WALK, size=32, color="#27ae60"),
                ft.Row([
                    ft.Text("6 517", size=26, weight="bold", color="#27ae60"),
                    ft.Text("Lépés", size=14, color="#27ae60", italic=True)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Text("Lépések", size=16, weight="bold", color="#27ae60", text_align="start"),
                ft.Row([
                    ft.ProgressBar(value=0.65, color="#27ae60", bgcolor="#d4f5e9", width=110, height=8),
                    ft.Text("65%", size=12, color="#27ae60", weight="bold", text_align="right")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True, spacing=8, height=20, width=140),
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START, spacing=8),
            width=170,
            height=160,
            bgcolor="#eafaf1",
            border_radius=24,
            alignment=ft.alignment.top_left,
            padding=12,
            on_click=lepes_click,
        )
    ], alignment=ft.MainAxisAlignment.CENTER)

    page.add(
        ft.Column([
            greeting_text,
            week_row,
            tracker_row,
            tipus_input,
            ido_input,
            kaloria_input,
            ft.Row([hozzaad_btn, frissit_btn], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Text("Korábbi edzések:", size=20, weight="bold"),
            lista
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    betoltes()
