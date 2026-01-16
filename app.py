import streamlit as st
import pandas as pd
import json
import os
import time
from search import GoogleScraper
from database import ScraperDB

st.set_page_config(page_title=" Google Scraper", layout="wide")

# Initialize Database with config settings
# Load config initially to connect to DB
try:
    with open("config.json", "r", encoding="utf-8") as f:
        initial_config = json.load(f)
except:
    initial_config = {}

db = ScraperDB(config_dict=initial_config)

st.title("🚀 Gemini Google Scraper")

# --- Tabs for Scraper and History ---
tab1, tab2 = st.tabs(["🔍 Scraper", "📂 Database History"])

with tab1:
    st.markdown("Enter your search query below to extract leads directly from Google.")

    # --- Sidebar Configuration ---
    st.sidebar.header("Settings")
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception:
        config = {
            "brave_path": "C:\\Users\\monsi\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            "search_query": "lead generation tools",
            "output_file": "leads_export.csv",
            "headless": True,
            "scrape_delay": 5,
            "pages_to_scrape": 3
        }

    brave_path = st.sidebar.text_input("Brave Browser Path", value=config.get("brave_path"))
    headless = st.sidebar.checkbox("Headless Mode (Hide Browser)", value=config.get("headless", True))
    scrape_delay = st.sidebar.slider("Delay between pages (seconds)", 2, 15, config.get("scrape_delay", 5))
    pages_to_scrape = st.sidebar.number_input("Pages to scrape", min_value=1, max_value=10, value=config.get("pages_to_scrape", 3))

    # --- Main UI ---
    query = st.text_input("What are you looking for?", placeholder="e.g. Marketing Agencies in Zurich")

    if st.button("Start Scraping", type="primary"):
        if not query:
            st.error("Please enter a search query!")
        else:
            # Generate unique filename to avoid locking issues
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            output_file = f"leads_{timestamp}.csv"

            # Update config dictionary for the scraper
            run_config = {
                "brave_path": brave_path,
                "search_query": query,
                "output_file": output_file,
                "headless": headless,
                "scrape_delay": scrape_delay,
                "pages_to_scrape": pages_to_scrape
            }
            
            # Save temporary config for the session
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(run_config, f, indent=4)

            with st.status("Scraping Google...", expanded=True) as status:
                st.write("Initializing Browser...")
                # Pass the configuration directly to the class
                scraper = GoogleScraper(config_dict=run_config)
                
                if scraper.setup_driver():
                    st.write(f"Searching for '{query}'...")
                    scraper.search()
                    
                    max_p = run_config["pages_to_scrape"]
                    for p in range(1, max_p + 1):
                        st.write(f"Processing Page {p}...")
                        scraper.extract_results()
                        
                        # Save to Database immediately
                        new_leads_count = 0
                        for row in scraper.results:
                            # scraper.results contains [title, link, description]
                            # We check if this specific row was just added to prevent duplicates in loop,
                            # but db.insert_lead handles unique URL check anyway.
                            saved = db.insert_lead(query, row[0], row[1], row[2])
                            if saved:
                                new_leads_count += 1
                        
                        if p < max_p:
                            if not scraper.go_to_next_page():
                                break
                    
                    scraper.save_to_csv()
                    scraper.driver.quit()
                    status.update(label="Scraping Complete!", state="complete", expanded=False)
                else:
                    st.error("Failed to initialize browser. Check the Brave path in settings.")

            # --- Display Results ---
            if os.path.exists(output_file):
                df = pd.read_csv(output_file)
                st.subheader(f"Found {len(df)} Leads (Saved to Database)")
                # Fixed deprecated parameter
                st.dataframe(df, width=1000) 
                
                # Download Button
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="Download CSV",
                        data=f,
                        file_name=output_file,
                        mime="text/csv"
                    )

with tab2:
    st.header("📂 Database History")
    if st.button("Refresh Data"):
        st.rerun()
        
    all_data = db.fetch_all()
    st.dataframe(all_data, width=1000)
    
    st.download_button(
        label="Download Full Database as CSV",
        data=all_data.to_csv(index=False).encode('utf-8'),
        file_name="google_scraper_full_history.csv",
        mime="text/csv"
    )
