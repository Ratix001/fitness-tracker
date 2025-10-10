import flet as ft
from logic.workout_controller import save_new_workout, get_all_workouts

def main(page: ft.Page):
    page.title = "🏋️ Edzésnapló"
    page.vertical_alignment = ft.MainAxisAlignment.START
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

    page.add(
        ft.Text("🏋️ Saját edzésnapló", size=30, weight="bold"),
        tipus_input,
        ido_input,
        kaloria_input,
        ft.Row([hozzaad_btn, frissit_btn]),
        ft.Divider(),
        ft.Text("Korábbi edzések:", size=20, weight="bold"),
        lista
    )

    betoltes()
