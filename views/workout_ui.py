import flet as ft
from controllers.workout_controller import (
    save_new_workout,
    get_all_workouts,
    get_week_overview,
    get_weekly_minutes,
    get_weekly_calories,
    get_month_day_labels,
    get_monthly_minutes,
    get_monthly_calories,
)
from flet.plotly_chart import PlotlyChart
import plotly.graph_objects as go
from collections import defaultdict

def main(page: ft.Page):
    page.title = "🏋️ Edzésnapló"
    title_bar = ft.Text("Fitness Tracker", size=22, weight="bold", color="#27ae60")
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    tipus_input = ft.TextField(label="Edzés típusa (pl. futás, súlyzós)", width=300)
    ido_input = ft.TextField(label="Időtartam (perc)", width=300)
    kaloria_input = ft.TextField(label="Kalória (opcionális)", width=300)

    lista = ft.Column(spacing=6, width=720)
    chart_container = ft.Container(
        margin=ft.margin.only(top=0),
        width=720,
        height=300,
        alignment=ft.alignment.center
    )
    monthly_chart_container = ft.Container(
        margin=ft.margin.only(top=0),
        width=720,
        height=320,
        alignment=ft.alignment.center,
    )

    def make_loader(label: str) -> ft.Container:
        return ft.Container(
            width=720,
            height=310,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.ProgressRing(width=70, height=70, stroke_width=6, color="#27ae60"),
                    ft.Text(label, size=16, weight="bold"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def show_chart_loading():
        chart_container.content = make_loader("Heti adatok betöltése…")
        monthly_chart_container.content = make_loader("Havi adatok betöltése…")
        chart_container.update()
        monthly_chart_container.update()


    def betoltes(e=None):
        show_chart_loading()
        try:
            workouts = get_all_workouts()
            grouped = defaultdict(list)
            for w in workouts:
                grouped[w.datum[:10]].append(w)

            lista.controls.clear()
            if not grouped:
                lista.controls.append(ft.Text("Nincs rögzített edzés.", italic=True))
            else:
                for day in sorted(grouped.keys(), reverse=True):
                    tiles = []
                    for w in sorted(grouped[day], key=lambda item: item.datum, reverse=True):
                        kal_text = f"{w.kaloria} kcal" if w.kaloria is not None else "- kcal"
                        tiles.append(
                            ft.ListTile(
                                title=ft.Text(f"{w.datum[11:]} • {w.tipus}"),
                                subtitle=ft.Text(f"{w.ido_perc} perc | {kal_text}"),
                            )
                        )
                    lista.controls.append(
                        ft.ExpansionTile(
                            title=ft.Text(day, weight="bold"),
                            controls=tiles,
                            initially_expanded=False,
                        )
                    )
            lista.update()
            refresh_week_row()
            refresh_chart()
            refresh_month_chart()
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

    week_row = ft.ResponsiveRow(
        columns=18,
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
        run_spacing=8,
        controls=[]
    )

    def refresh_week_row():
        workout_days_local = get_week_overview()
        day_circles_local = []
        for i, d in enumerate(days):
            day_str = d.strftime("%Y-%m-%d")
            bg = "#27ae60" if day_str in workout_days_local else "white"
            fg = "white" if bg != "white" else "#27ae60"
            day_circles_local.append(
                ft.Container(
                    content=ft.Text(
                        day_names[i],
                        size=16,
                        weight="bold",
                        color=fg,
                        no_wrap=True,
                        max_lines=1,
                    ),
                    width=40,
                    height=40,
                    bgcolor=bg,
                    border_radius=20,
                    alignment=ft.alignment.center,
                    col={"xs":4, "sm":2, "md":1},
                    border=ft.border.all(1, "#27ae60"),
                )
            )

        week_row.controls.clear()
        week_row.controls.extend(day_circles_local)
        page.update()

    def refresh_chart():
        try:
            minutes = get_weekly_minutes()
            calories = get_weekly_calories()

            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=day_names,
                    y=minutes,
                    name="Percek",
                    marker_color="#27ae60",
                    hovertemplate="%{x}: %{y} perc<extra></extra>",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=day_names,
                    y=calories,
                    name="Kalória",
                    mode="lines+markers",
                    yaxis="y2",
                    line=dict(color="#e67e22", width=3),
                    marker=dict(size=16),
                    hovertemplate="%{x}: %{y} kcal<extra></extra>",
                )
            )
            fig.update_layout(
                template="plotly_dark",
                margin=dict(l=20, r=20, t=30, b=20),
                font=dict(size=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=24)),
                yaxis=dict(title="Percek"),
                yaxis2=dict(title="Kalória", overlaying="y", side="right"),
            )
            chart_container.content = PlotlyChart(fig, expand=True)
        except Exception as ex:
            chart_container.content = ft.Text(f"Grafikon hiba: {ex}", color="#c0392b")
        page.update()

    def refresh_month_chart():
        try:
            day_labels = get_month_day_labels()
            minutes = get_monthly_minutes()
            calories = get_monthly_calories()

            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=day_labels,
                    y=minutes,
                    name="Percek",
                    marker_color="#2980b9",
                    hovertemplate="Nap %{x}: %{y} perc<extra></extra>",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=day_labels,
                    y=calories,
                    name="Kalória",
                    mode="lines+markers",
                    yaxis="y2",
                    line=dict(color="#e74c3c", width=3),
                    marker=dict(size=10),
                    hovertemplate="Nap %{x}: %{y} kcal<extra></extra>",
                )
            )
            fig.update_layout(
                template="plotly_dark",
                margin=dict(l=20, r=20, t=30, b=20),
                font=dict(size=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=18),
                ),
                xaxis=dict(
                    title=dict(text="Nap", font=dict(size=18)),
                    tickfont=dict(size=18),
                    tickmode="linear",
                    dtick=2,
                ),
                yaxis=dict(
                    title=dict(text="Percek", font=dict(size=18)),
                    tickfont=dict(size=18),
                ),
                yaxis2=dict(
                    title=dict(text="Kalória", font=dict(size=18)),
                    overlaying="y",
                    side="right",
                    tickfont=dict(size=18),
                ),
            )
            monthly_chart_container.content = PlotlyChart(fig, expand=True)
        except Exception as ex:
            monthly_chart_container.content = ft.Text(f"Havi grafikon hiba: {ex}", color="#c0392b")
        page.update()


    # UI összeállítása
    page.add(
        ft.SafeArea(
            top=True,
            bottom=True,
            left=True,
            right=True,
            content=ft.Container(
                padding=ft.padding.only(top=30, bottom=30),
                content=ft.Column(
                    [
                        title_bar,
                        week_row,
                        ft.Divider(),
                        ft.Text("Heti kimutatás:", size=20, weight="bold"),
                        chart_container,
                        ft.Text("Havi kimutatás:", size=20, weight="bold"),
                        monthly_chart_container,
                        ft.Divider(),
                        ft.Text("Edzés felvétele:", size=20, weight="bold"),
                        tipus_input,
                        ido_input,
                        kaloria_input,
                        ft.ResponsiveRow(
                            columns=12,
                            spacing=20,
                            run_spacing=12,
                            controls=[
                                ft.Container(content=hozzaad_btn, col={"xs":12, "sm":6, "md":6}),
                                ft.Container(content=frissit_btn, col={"xs":12, "sm":6, "md":6}),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Text("Korábbi edzések:", size=20, weight="bold"),
                        lista,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
        )
    )

    betoltes()
