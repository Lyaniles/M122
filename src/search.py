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

from src.utils import get_browser_path

class GoogleScraper:
    def __init__(self, config_path="config.json", config_dict=None):
        if config_dict:
            self.config = config_dict
        else:
            self.config = self._load_config(config_path)
            
        self.driver = None
        self.results = []
        self.seen_urls = set()

    def _load_config(self, path):
        # Try loading specific path
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading {path}: {e}")

        # Try fallback to template
        template_path = "config.template.json"
        if os.path.exists(template_path):
             try:
                with open(template_path, "r", encoding="utf-8") as f:
                    return json.load(f)
             except:
                 pass

        # Defaults
        return {
            "brave_path": get_browser_path(), # Dynamic default
            "search_query": "test query",
            "output_file": "results.csv",
            "headless": False,
            "scrape_delay": 5
        }

    def setup_driver(self):
        options = Options()
        
        # Determine browser path: Config > Auto-detect > None
        browser_path = self.config.get("brave_path")
        if not browser_path or not os.path.exists(browser_path):
            print(f"Configured path '{browser_path}' not found. Attempting auto-detection...")
            browser_path = get_browser_path()
        
        if not browser_path:
            print("Error: Could not find Brave or Chrome browser. Please set 'brave_path' in settings.")
            return False

        options.binary_location = browser_path
        print(f"Using browser at: {browser_path}")
        
        # Use a persistent profile to keep cookies/session and avoid Captchas
        profile_dir = os.path.join(os.getcwd(), "automation_profile")
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)
        options.add_argument(f"--user-data-dir={profile_dir}")
        
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

        if len(raw_results) == 0:
            print("WARNING: No results found. Saving debug screenshot...")
            try:
                # Ensure debug directory exists
                if not os.path.exists("debug"):
                    os.makedirs("debug")
                    
                self.driver.save_screenshot(os.path.join("debug", "debug_screenshot.png"))
                with open(os.path.join("debug", "debug_page_source.html"), "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
            except Exception as e:
                print(f"Failed to save debug info: {e}")

        new_leads = []
        new_count = 0
        for res in raw_results:
            title_el = res.find('h3')
            link_el = res.find('a')
            
            # Attempt to find the description (snippet)
            desc_el = res.select_one(".VwiC3b, .lyLwlc, .yXK7lf, div[style*='-webkit-line-clamp']")
            description = desc_el.get_text(strip=True) if desc_el else "No description found"

            if title_el and link_el:
                title = title_el.get_text(strip=True)
                link = link_el.get('href')
                
                if link and link.startswith("http") and link not in self.seen_urls:
                    entry = [title, link, description]
                    self.results.append(entry)
                    new_leads.append(entry)
                    self.seen_urls.add(link)
                    new_count += 1
        
        print(f"DEBUG: Added {new_count} new unique leads.")
        return new_leads

    def save_to_csv(self):
        filename = self.config.get("output_file", os.path.join("output", "leads_export.csv"))
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(filename)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Name / Title", "URL", "Description"])
                writer.writerows(self.results)
            
            abs_path = os.path.abspath(filename)
            if self.results:
                print(f"\nSUCCESS: {len(self.results)} leads found and saved!")
            else:
                print("\nWARNING: No leads extracted.")
                
            print(f"File path: {abs_path}")
        except Exception as e:
            print(f"Error saving CSV: {e}")

    def go_to_next_page(self):
        # List of possible selectors for the "Next" button
        selectors = [
            (By.ID, "pnnext"),
            (By.CSS_SELECTOR, 'a[aria-label="Next page"]'),
            (By.CSS_SELECTOR, 'a[aria-label="Nächste Seite"]'),
            (By.XPATH, "//span[contains(text(), 'Next')]/ancestor::a"),
            (By.XPATH, "//span[contains(text(), 'Weiter')]/ancestor::a")
        ]
        
        for strategy, selector in selectors:
            try:
                next_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((strategy, selector))
                )
                next_button.click()
                print(f"Navigating to next page (found via {strategy})...")
                time.sleep(self.config.get("scrape_delay", 5))
                return True
            except:
                continue # Try next selector
        
        print("Next page button not found (or last page reached).")
        return False

    def run(self):
        if not self.setup_driver():
            return

        try:
            self.search()
            
            max_pages = self.config.get("pages_to_scrape", 1)
            for page in range(1, max_pages + 1):
                print(f"--- Processing Page {page} ---")
                self.extract_results()
                
                if page < max_pages:
                    if not self.go_to_next_page():
                        print("Stopping pagination.")
                        break
            
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