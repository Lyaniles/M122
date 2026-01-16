from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import csv
import os

BRAVE_PATH = r"C:\Users\monsi\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"

options = Options()
options.binary_location = BRAVE_PATH
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

try:
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    print("Rufe Google auf...")
    driver.get("https://www.google.com/search?q=lead+generation+tools")

    # 1. Cookie-Banner (warten bis zu 10 Sek)
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button//div[contains(text(), 'Alle akzeptieren') or contains(text(), 'I agree') or contains(text(), 'Accept all')]/.."))
        )
        cookie_button.click()
        print("Cookies akzeptiert.")
    except:
        print("Kein Cookie-Banner gefunden oder Pfad falsch.")

    # 2. WICHTIG: Wartezeit nach dem Klick, damit die Suche lädt
    print("Warte auf Suchergebnisse...")
    time.sleep(5) 

    # 3. HTML analysieren
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Wir suchen nach verschiedenen möglichen Containern (Google ändert diese oft)
    # Muster: Suche alle div-Container, die ein h3 (Titel) enthalten
    leads = []
    
    # Wir probieren verschiedene gängige Selektoren aus
    results = soup.find_all('div', dict(cfg=True)) or soup.select(".g") or soup.select(".tF2Cxc")

    print(f"DEBUG: Anzahl gefundener Roh-Container: {len(results)}")

    for res in results:
        title_el = res.find('h3')
        link_el = res.find('a')
        
        if title_el and link_el:
            title = title_el.get_text(strip=True)
            link = link_el.get('href')
            
            if link and link.startswith("http"):
                leads.append([title, link])

    # 4. CSV Speichern
    filename = "leads_export.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name / Titel", "URL"])
        writer.writerows(leads)

    absoluter_pfad = os.path.abspath(filename)
    if leads:
        print(f"\nERFOLG: {len(leads)} Leads gefunden und gespeichert!")
    else:
        print("\nFEHLER: Keine Leads extrahiert. Google blockiert eventuell oder das Layout ist anders.")
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("INFO: Die Datei 'debug_page.html' wurde erstellt. Öffne sie, um zu sehen, was der Bot sieht.")

    print(f"\nDatei-Pfad: {absoluter_pfad}")

except Exception as e:
    print(f"Kritischer Fehler: {e}")

finally:
    input("\nDrücke Enter zum Beenden...")
    driver.quit()