import flet as ft
import csv
from datetime import datetime

FILENAME = "edzesnaplo.csv"

def main(page: ft.Page):
    page.title = "🏋️ Edzésnapló"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "adaptive"

    tipus_input = ft.TextField(label="Edzés típusa (pl. futás, súlyzós)", width=300)
    ido_input = ft.TextField(label="Időtartam (perc)", width=300)
    kaloria_input = ft.TextField(label="Kalória (opcionális)", width=300)

    lista = ft.Column()

    def edzes_hozzaad(e):
        datum = datetime.now().strftime("%Y-%m-%d %H:%M")
        tipus = tipus_input.value
        ido = ido_input.value
        kaloria = kaloria_input.value or "-"

        with open(FILENAME, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datum, tipus, ido, kaloria])

        tipus_input.value = ""
        ido_input.value = ""
        kaloria_input.value = ""

        snack = ft.SnackBar(
        content=ft.Row(
            [
                ft.Text("✅ Edzés elmentve!", color="white"),
                ft.TextButton("OK", on_click=lambda e: snack.open == False)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        bgcolor="#27ae60",
        duration=3000
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()


    def betoltes(e):
        lista.controls.clear()
        try:
            with open(FILENAME, mode="r") as file:
                reader = csv.reader(file)
                for sor in reader:
                    lista.controls.append(
                        ft.Text(f"{sor[0]} | {sor[1]} | {sor[2]} perc | {sor[3]} kcal")
                    )
        except FileNotFoundError:
            pass
        page.update()

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

    betoltes(None)

ft.app(target=main)
