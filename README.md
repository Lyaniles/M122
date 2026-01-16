# M122
Dies ist ein Repo für das Modul 122 der TBZ.

---
# Guide um Github Repo mit VS Code zu verbinden.


#  1. Das Remote-Repository verknüpfen

Bevor du Daten übertragen kannst, muss dein lokaler Ordner wissen, wohin die Reise geht. Mit dem Befehl `remote add` stellst du die Verbindung zu deinem GitHub-Repository her. Wir nennen diese Verbindung standardmäßig `origin`

``` Shell
 git remote add origin https://github.com/Lyaniles/M122
```

# 2. Abgleich mit dem Server (Synchronisation)

Um sicherzustellen, dass dein lokaler Stand nicht mit Änderungen auf GitHub kollidiert, führen wir einen `pull` durch. Die Flag `--rebase` sorgt dabei für eine saubere Historie, indem sie deine lokalen Änderungen "oben auf" die neuesten Änderungen vom Server setzt, anstatt einen unübersichtlichen Merge-Commit zu erstellen.

``` Shell
git pull origin main --rebase
```
> **Hinweis:** Falls dein Haupt-Branch auf GitHub anders heißt (z.B. `master`), passe den Namen im Befehl entsprechend an. 

# 3. Die Daten hochladen

Sobald dein lokaler Stand aktuell ist, kannst du deine Arbeit auf GitHub veröffentlichen. Mit der Flag `-u` (kurz für `--set-upstream`) speicherst du die Verbindung für die Zukunft. Das bedeutet, dass du ab jetzt einfach nur noch `git push` eingeben musst, ohne jedes Mal `origin main` zu wiederholen.

``` Shell
git push -u origin main
```

### 1. Änderungen speichern (Der Standard-Zyklus)

Wenn du Dateien bearbeitet hast, musst du diese „stagen“ (vormerken) und dann „committen“ (festschreiben).

- **Status prüfen:** Schau nach, welche Dateien geändert wurden:
    ``` Shell
    git status
    ```
    
- **Dateien hinzufügen:** Alle Änderungen für den nächsten Commit vormerken:
    ```Sh
    git add .
    ```
    
- **Änderungen festschreiben:** Erstelle einen Snapshot deiner Arbeit mit einer kurzen Nachricht:
    ```Sh
    git commit -m "Hier beschreiben, was du gemacht hast"
    ```
    
- **Hochladen:** Deine Commits an GitHub senden:
    ```Sh
    git push
    ```

### 2. Mit Branches arbeiten (Parallel arbeiten)

Falls du ein neues Feature ausprobieren willst, ohne den Hauptcode (`main`) zu gefährden, solltest du einen eigenen Zweig (Branch) verwenden.

- **Neuen Branch erstellen:**
    ```Sh
    git checkout -b mein-neues-feature
    ```
    
- **Zwischen Branches wechseln:**
    ```Sh
    git checkout main
    ```
    
- **Branches zusammenführen (Merge):** Wenn dein Feature fertig ist, wechselst du zurück in den `main` und holst dir die Änderungen:
    ```Sh
    git checkout main
    git merge mein-neues-feature
    ```
    

---

# 🚀 Gemini Lead Scraper Product

This repository contains a professional-grade web scraper built for **Module 122**. It automates the process of finding business leads (Title, URL, Description) from Google Search results using the Brave Browser and saves them to a MariaDB database.

## ✨ Key Features

- **Interactive UI:** Built with **Streamlit** for a modern, easy-to-use experience. No coding knowledge required to run searches.
- **Robust Automation:** Uses **Selenium** to navigate Google, handle cookies, and manage pagination automatically.
- **Database Integration:**
  - **MariaDB Support:** Automatically stores all scraped leads in a local or remote MariaDB 10.11+ database.
  - **Auto-Deduplication:** Prevents duplicate URLs from entering the database.
  - **History View:** View and export your entire scraping history directly from the UI.
- **Anti-Detection:** 
  - Implements a **Persistent User Profile** to maintain Google "trust" and drastically reduce Captchas.
  - Randomizes delays and mimics human behavior.
- **Data Quality:**
  - **Enrichment:** Extracts Title, URL, and the Snippet Description.
  - **Smart Export:** Saves CSV files with unique timestamps (`leads_YYYYMMDD-HHMMSS.csv`) to prevent file locking errors.
- **Error Handling:** Automatically captures debug screenshots if Google blocks the request or changes layout.

## 🛠️ Installation & Usage

### Prerequisites
1.  **Python 3.10+** installed.
2.  **Brave Browser** installed (Path is configurable in the UI).
3.  **MariaDB Server (10.11+)** installed and running.
    - The application will automatically create the `google_scraper` database if the user has permissions.

### Quick Start (Windows)
Double-click the `start_app.bat` file. 
This script will:
1.  Create a virtual environment (`venv`).
2.  Install dependencies (`requirements.txt`).
3.  Launch the User Interface in your default browser.

### Manual Start
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

## ⚙️ Configuration
The settings are managed via the UI but saved to `config.json` for persistence.
- **Database:**
  - `db_host`: Database host (default: `localhost`)
  - `db_user`: Database user (default: `root`)
  - `db_password`: Database password (leave empty if none)
  - `db_name`: Database name (default: `google_scraper`)
- **Scraper:**
  - **Brave Browser Path:** Location of your `brave.exe`.
  - **Headless Mode:** Run without opening a visible window (Uncheck this to solve Captchas manually).
  - **Pages:** How deep to scrape (1-10 pages).

## 📂 Project Structure
- `app.py`: The frontend application (Streamlit).
- `search.py`: The backend scraping logic (`GoogleScraper` class).
- `database.py`: Handles MariaDB connection and data insertion.
- `start_app.bat`: One-click launcher for stakeholders.
- `automation_profile/`: Folder storing browser cookies/session (Do not delete if you want to avoid Captchas).
