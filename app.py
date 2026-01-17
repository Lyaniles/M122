import streamlit as st
import pandas as pd
import json
import os
import time
from src.search import GoogleScraper
from src.database import ScraperDB
from src.utils import get_browser_path

st.set_page_config(page_title="Google Scraper", layout="wide")

def load_config():
    """Load config from config.json or fallback to template/defaults."""
    config = {}
    
    # 1. Load template first for defaults
    if os.path.exists("config.template.json"):
        try:
            with open("config.template.json", "r", encoding="utf-8") as f:
                config.update(json.load(f))
        except Exception:
            pass

    # 2. Override with local config if exists
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config.update(json.load(f))
        except Exception:
            pass
            
    return config

# Load configuration once
config = load_config()

st.title(" Google Scraper")

# --- Tabs for Scraper and History ---
tab1, tab2 = st.tabs(["🔍 Scraper", "📂 Database History"])

with tab1:
    st.markdown("Enter your search query below to extract leads directly from Google.")

    # --- Sidebar Configuration ---
    st.sidebar.header("Settings")
    
    # Defaults
    detected_browser = get_browser_path()
    config_browser = config.get("brave_path")
    
    # Use config value if valid, else detected, else empty string
    default_brave = config_browser if config_browser else (detected_browser if detected_browser else "")
    
    brave_path = st.sidebar.text_input("Brave/Chrome Browser Path", value=default_brave)
    if not brave_path:
        st.sidebar.warning("Could not auto-detect browser. Please enter path manually.")
    headless = st.sidebar.checkbox("Headless Mode (Hide Browser)", value=config.get("headless", True))
    scrape_delay = st.sidebar.slider("Delay between pages (seconds)", 2, 15, config.get("scrape_delay", 5))
    pages_to_scrape = st.sidebar.number_input("Pages to scrape", min_value=1, max_value=10, value=config.get("pages_to_scrape", 3))

    # --- Main UI ---
    query = st.text_input("What are you looking for?", placeholder="e.g. Marketing Agencies in Zurich")

    if st.button("Start Scraping", type="primary"):
        if not query:
            st.error("Please enter a search query!")
        else:
            # Generate unique filename for this run
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            output_file = os.path.join("output", f"leads_{timestamp}.csv")

            # Runtime config
            run_config = config.copy()
            run_config.update({
                "brave_path": brave_path,
                "search_query": query,
                "output_file": output_file,
                "headless": headless,
                "scrape_delay": scrape_delay,
                "pages_to_scrape": pages_to_scrape
            })

            with st.status("Scraping Google...", expanded=True) as status:
                st.write("Initializing Browser...")
                
                # Initialize Scraper
                scraper = GoogleScraper(config_dict=run_config)
                
                # Initialize Database (using Context Manager)
                try:
                    with ScraperDB(config_dict=run_config) as db:
                        if scraper.setup_driver():
                            st.write(f"Searching for '{query}'...")
                            scraper.search()
                            
                            max_p = run_config["pages_to_scrape"]
                            for p in range(1, max_p + 1):
                                st.write(f"Processing Page {p}...")
                                
                                # Extract newly found leads
                                new_leads = scraper.extract_results()
                                
                                # Save to Database immediately
                                saved_count = 0
                                for row in new_leads:
                                    # row = [title, url, description]
                                    if db.insert_lead(query, row[0], row[1], row[2]):
                                        saved_count += 1
                                
                                # Only navigate if not the last page
                                if p < max_p:
                                    if not scraper.go_to_next_page():
                                        st.write("No more pages.")
                                        break
                            
                            scraper.save_to_csv()
                            scraper.driver.quit()
                            status.update(label="Scraping Complete!", state="complete", expanded=False)

                            # --- Display Results from Memory ---
                            if scraper.results:
                                df = pd.DataFrame(scraper.results, columns=["Name / Title", "URL", "Description"])
                                st.subheader(f"Found {len(df)} Leads (Saved to Database)")
                                st.dataframe(df, width=1000)
                                
                                # Download Button (using in-memory data)
                                csv_data = df.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label="Download CSV",
                                    data=csv_data,
                                    file_name=output_file,
                                    mime="text/csv"
                                )
                            else:
                                st.warning("No leads found.")
                        else:
                            st.error("Failed to initialize browser. Check the Brave path in settings.")
                except Exception as e:
                    st.error(f"Database Error: {e}")

with tab2:
    st.header("📂 Database History")
    if st.button("Refresh Data"):
        st.rerun()
        
    try:
        with ScraperDB(config_dict=config) as db:
            all_data = db.fetch_all()
            st.dataframe(all_data, width=1000)
            
            st.download_button(
                label="Download Full Database as CSV",
                data=all_data.to_csv(index=False).encode('utf-8'),
                file_name="google_scraper_full_history.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Could not connect to database: {e}")