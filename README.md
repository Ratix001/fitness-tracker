# Fitness Tracker

🏋️‍♂️ Edzésnapló – Flet alapú desktop alkalmazás

Ez egy egyszerű, letisztult, Flet keretrendszerrel készült asztali alkalmazás, amely lehetővé teszi a felhasználók számára edzéseik rögzítését, megjelenítését és elemzését.
Az adatok CSV fájlban tárolódnak a felhasználó saját gépén, és az alkalmazás képes heti és havi statisztikák grafikus megjelenítésére (Plotly grafikonok).

# ✨ Funkciók

- 📒 Edzések rögzítése (típus, időtartam, kalória)

- 📁 Adatok mentése és olvasása CSV fájból

- 📅 Edzések listázása napokra bontva

- 📊 Heti és havi statisztikák megjelenítése Plotly diagramokon

- 📦 Telepíthető Windows alkalmazás (Inno Setup installer)

- 🚀 PyInstallerrel buildelhető .exe fájl

# 🛠️ Fejlesztői környezet beállítása

### Python ellenőrzése

A projekt Python 3.10+ verzióval működik (ha szükséges módosítsd).
Ellenőrizd a Python verziót:
- `python --version`
  
Ha a rendszered python3-at használ (Linux/macOS):
- `python3 --version`

### Virtuális környezet létrehozása (erősen ajánlott)

A virtuális környezet biztosítja, hogy a projektedhez tartozó csomagok ne keveredjenek a rendszer más Python programjaival.

🔹 Windows
```
python -m venv venv
venv\Scripts\activate
```
🔹 Linux / macOS
```
python3 -m venv venv
source venv/bin/activate
```

Ha sikerült, a parancssorban megjelenik:

- `(venv)`

### Könyvtárak telepítése

Minden szükséges csomag fel van sorolva a requirements.txt fájlban.

Futtasd:

- `pip install -r requirements.txt`

Ez telepíti az összes szükséges modult:

- Flet → a GUI-hoz

- Plotly → grafikonok

- stb.

👉 Tipp: Ha hibaüzenetet kapsz, futtasd ezt:

- `pip install --upgrade pip`

# ▶️ Futtatási módok

Az alkalmazás két különböző futtatási módot támogat:

### - 🔧 Fejlesztői mód (DEV)

Fejlesztés közben a programot a forráskódból indítod:

- `python main.py`

Ebben az esetben:

Az edzesnaplo.csv fájl a projekt gyökérkönyvtárában jön létre és ide is menti az adatokat.

Ez a mód hasznos debughoz, fejlesztéshez és teszteléshez.

### - 🚀 Buildelt alkalmazás (PROD)

Ha az alkalmazást PyInstallerrel lebuildelted, és az elkészült .exe fájlt futtatod:

Az adatok nem a projekt mappába, hanem a felhasználó saját könyvtárába kerülnek.

A mentett adatfájl helye:

- `C:\Users\<Felhasználó>\Edzesnaplo\edzesnaplo.csv`

Ez biztosítja, hogy a felhasználó adatai mindig elérhetők legyenek, függetlenül attól, hova másolja vagy telepíti az alkalmazást.

# 🏗️ Build készítése PyInstallerrel

A projekt tartalmaz egy testreszabott main.spec fájlt, amely biztosítja, hogy:

- minden szükséges Plotly fájl bekerüljön,

- Flet helyesen becsomagolódjon.

A build indítása:

- `pyinstaller main.spec`

A futtatható állomány a dist/ mappában jelenik meg.

# 📄 CSV fájl formátum

Az alkalmazás automatikusan hozza létre, nem kell kézzel készíteni.

- CSV tartalma:

```
id,datum,tipus,ido_perc,kaloria
1,2025-01-12 18:30, Futás, 45, 320
2,2025-01-13 20:10, Séta, 30, 120
```

A mezők automatikusan a Workout osztály mezőiből származnak.

# 👨‍💻 Használt technológiák

- Python 3.10+
- Flet – UI
- Plotly – grafikonok
- PyInstaller – build
- Inno Setup – Windows installer
- CSV – adatkezelés

A requirements.txt fájl felsorolja az alkalmazás futtatásához és fejlesztéséhez szükséges Python csomagokat, valamint azok pontos verziószámait.

# Letöltés / Download

Csak ki szeretnéd próbálni az alkalmazást?  
Töltsd le az előre elkészített Windows telepítőt:

👉 **[setup.exe Letöltés / Download]()**  (Link folyamatban...)


