import csv
from datetime import datetime

FILENAME = "edzesnaplo.csv"

def uj_edzes():
    datum = datetime.now().strftime("%Y-%m-%d %H:%M")
    tipus = input("Edzés típusa (pl. súlyzós, futás, nyújtás): ")
    ido = input("Időtartam (perc): ")
    kaloria = input("Elégetett kalória (ha tudod, különben üresen hagyhatod): ")

    with open(FILENAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datum, tipus, ido, kaloria])
    print("Edzés sikeresen hozzáadva!\n")

def listazas():
    try:
        with open(FILENAME, mode="r") as file:
            reader = csv.reader(file)
            print("\n--- Edzésnapló ---")
            for sor in reader:
                print(f"Dátum: {sor[0]}, Típus: {sor[1]}, Idő: {sor[2]} perc, Kalória: {sor[3]}")
            print("-------------------\n")
    except FileNotFoundError:
        print("Még nincs elmentett edzés.\n")

def menu():
    while True:
        print("1 - Új edzés felvétele")
        print("2 - Edzések listázása")
        print("3 - Kilépés")

        valasztas = input("Válassz: ")

        if valasztas == "1":
            uj_edzes()
        elif valasztas == "2":
            listazas()
        elif valasztas == "3":
            print("Kilépés...")
            break
        else:
            print("Hibás választás, próbáld újra!\n")

if __name__ == "__main__":
    menu()
