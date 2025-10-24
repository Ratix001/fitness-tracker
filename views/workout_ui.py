import flet as ft
from controllers.workout_controller import (
    save_new_workout,
    get_all_workouts,
    get_week_overview,
    get_weekly_minutes,
)
from flet.plotly_chart import PlotlyChart
import plotly.graph_objects as go

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
    chart_container = ft.Container(
        margin=ft.margin.only(top=8),
        width=720,
        height=300,
        alignment=ft.alignment.center
    )

    def betoltes(e=None):
        lista.controls.clear()
        for w in get_all_workouts():
            kal_text = f"{w.kaloria} kcal" if w.kaloria is not None else "- kcal"
            lista.controls.append(
                ft.Text(f"{w.datum} | {w.tipus} | {w.ido_perc} perc | {kal_text}")
            )
        page.update()
        try:
            refresh_week_row()
            refresh_chart()
        except Exception as ex:
            print(f"[betoltes] refresh error: {ex}")

    def edzes_hozzaad(e):
        result = save_new_workout(tipus_input.value, ido_input.value, kaloria_input.value)
        uzenet = result.get("message", "")
        snack = ft.SnackBar(
            content=ft.Text(uzenet, color="white"),
            bgcolor="#27ae60" if result.get("ok") else "#c0392b",
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
        workout_days_local = get_week_overview()
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

    def refresh_chart():
        try:
            # Heti percek lekérése
            minutes = get_weekly_minutes()
            labels = day_names
            theme_color = "#27ae60"

            # Ha nincs adat ezen a héten, mutassunk üzenetet
            if not minutes or sum(minutes) == 0:
                chart_container.content = ft.Container(
                    content=ft.Text("Nincs adat ezen a héten.", color="#7f8c8d"),
                    alignment=ft.alignment.center
                )
                page.update()
                return

            fig = go.Figure(
                data=[go.Bar(x=labels, y=minutes, marker_color=theme_color, hovertemplate="%{x}: %{y} perc<extra></extra>")]
            )
            fig.update_layout(
                title=dict(text="Heti összesített idő (perc)", x=0.5, font=dict(color=theme_color, size=25)),
                margin=dict(l=20, r=20, t=80, b=20),
                yaxis=dict(title="Perc", rangemode="tozero", gridcolor="#e5f7ee", tickfont=dict(size=25), title_font=dict(size=25)),
                xaxis=dict(title="", tickfont=dict(size=25)),
                height=425,
                width=700,
                paper_bgcolor="white",
                plot_bgcolor="white",
            )
            chart_container.content = PlotlyChart(fig, expand=True)
        except Exception as ex:
            chart_container.content = ft.Text(
                f"Nem sikerült betölteni a diagramot: {ex}", color="#c0392b"
            )
        page.update()


    page.add(
        ft.Column([
            greeting_text,
            week_row,
            tipus_input,
            ido_input,
            kaloria_input,
            ft.Row([hozzaad_btn, frissit_btn], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            chart_container,
            ft.Divider(),
            ft.Text("Korábbi edzések:", size=20, weight="bold"),
            lista,
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    betoltes()
