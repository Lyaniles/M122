import json
import csv
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class GoogleScraper:
    def __init__(self, config_path="config.json"):
        self.config = self._load_config(config_path)
        self.driver = None
        self.results = []

    def _load_config(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file '{path}' not found. Using defaults.")
            return {
                "brave_path": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                "search_query": "test query",
                "output_file": "results.csv",
                "headless": False,
                "scrape_delay": 5
            }

    def setup_driver(self):
        options = Options()
        options.binary_location = self.config.get("brave_path")
        
        if self.config.get("headless"):
            options.add_argument("--headless")
            
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        try:
            self.driver = webdriver.Chrome(options=options)
            
            # Stealth mode: overwrite webdriver property
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })
            return True
        except Exception as e:
            print(f"Error setting up driver: {e}")
            return False

    def handle_cookies(self):
        # 1. Cookie-Banner (wait up to 10 sec)
        try:
            cookie_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button//div[contains(text(), 'Alle akzeptieren') or contains(text(), 'I agree') or contains(text(), 'Accept all')]/.."))
            )
            cookie_button.click()
            print("Cookies accepted.")
            time.sleep(random.uniform(1, 2))
        except:
            print("No cookie banner found or path incorrect (proceeding anyway).")

    def search(self):
        query = self.config.get("search_query", "python")
        print(f"Searching for: {query}")
        self.driver.get(f"https://www.google.com/search?q={query}")
        
        self.handle_cookies()
        
        print("Waiting for search results...")
        # Smart wait for results container instead of hard sleep
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.g, div[data-cfg]"))
            )
        except:
            print("Timeout waiting for results.")

        # Additional random delay for human-like behavior
        time.sleep(self.config.get("scrape_delay", 5))

    def extract_results(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        
        # Patterns to find result containers
        raw_results = soup.find_all('div', dict(cfg=True)) or soup.select(".g") or soup.select(".tF2Cxc")
        print(f"DEBUG: Found {len(raw_results)} raw containers")

        for res in raw_results:
            title_el = res.find('h3')
            link_el = res.find('a')
            
            if title_el and link_el:
                title = title_el.get_text(strip=True)
                link = link_el.get('href')
                
                if link and link.startswith("http"):
                    self.results.append([title, link])

    def save_to_csv(self):
        filename = self.config.get("output_file", "leads_export.csv")
        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Name / Title", "URL"])
                writer.writerows(self.results)
            
            abs_path = os.path.abspath(filename)
            if self.results:
                print(f"\nSUCCESS: {len(self.results)} leads found and saved!")
            else:
                print("\nWARNING: No leads extracted.")
                
            print(f"File path: {abs_path}")
        except Exception as e:
            print(f"Error saving CSV: {e}")

    def run(self):
        if not self.setup_driver():
            return

        try:
            self.search()
            self.extract_results()
            self.save_to_csv()
        except Exception as e:
            print(f"Critical Error: {e}")
        finally:
            print("\nDone. Closing driver.")
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    bot = GoogleScraper()
    bot.run()