from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 1. Pfad zum Brave-Browser
BRAVE_PATH = r"C:\Users\monsi\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"

# 2. Optionen konfigurieren
options = Options()
options.binary_location = BRAVE_PATH
options.add_argument("--window-size=1920,1080")

# 3. WebDriver starten 
# Wir lassen den Pfad einfach leer - Selenium sucht sich den Treiber jetzt selbst!
try:
    print("Suche passenden Treiber und starte Brave...")
    service = Service() 
    driver = webdriver.Chrome(service=service, options=options)

    # Test-Aufruf
    driver.get("https://www.google.com/search?q=lead+generation+tools&oq=lead+generation+tools")
    print("Erfolg! Brave läuft.")
    
    time.sleep(5) # Damit wir kurz schauen können

finally:
    if 'driver' in locals():
        driver.quit()