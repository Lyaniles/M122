<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Selenium-Automation-43B02A?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium">
  <img src="https://img.shields.io/badge/MariaDB-Database-003545?style=for-the-badge&logo=mariadb&logoColor=white" alt="MariaDB">
</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">🚀 Google Lead Scraper 🚀</h3>

  <p align="center">
    A professional-grade, automated lead generation tool with a powerful Streamlit UI.
    <br />
    <br />
    <a href="#getting-started"><strong>Get Started »</strong></a>
    &middot;
    <a href="#usage">Usage</a>
    &middot;
    <a href="#troubleshooting">Troubleshooting</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#key-features">✨ Key Features</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#troubleshooting">Troubleshooting</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This repository contains a professional-grade web scraper designed to automate the process of finding business leads (Title, URL, Description) from Google Search results. It features an interactive UI built with Streamlit, robust automation with Selenium, and seamless integration with a MariaDB database.

It solves the problem of manual prospecting by providing a tool that mimics human behavior to safely scrape multiple pages of results and organize them instantly.

## ✨ Key Features

- **🎯 Interactive UI:** Built with **Streamlit** for a modern, easy-to-use experience. No coding knowledge required to run searches.
- **🌍 Universal Support:** **Auto-detects** your browser (Brave or Chrome) on Windows, Mac, and Linux.
- **🤖 Robust Automation:** Uses **Selenium** to navigate Google, handle cookies, and manage pagination automatically.
- **🗄️ Database Integration:**
  - **MariaDB Support:** Automatically stores all scraped leads in a local MariaDB database.
  - **Auto-Deduplication:** Prevents duplicate URLs from entering the database.
  - **History View:** View and export your entire scraping history directly from the UI.
- **🕵️ Anti-Detection:** 
  - Implements a **Persistent User Profile** (`automation_profile/`) to maintain Google "trust" and reduce Captchas.
  - Randomizes delays and mimics human behavior.
- **📂 Smart Output:**
  - **CSV Exports:** Saved automatically to the `output/` folder.
  - **Debug Logs:** Screenshots and HTML dumps saved to `debug/` if errors occur.

<!-- GETTING STARTED -->
## Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

To run this application, you need the following installed on your system:

1.  **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
    *   *Make sure to check "Add Python to PATH" during installation.*
2.  **MariaDB Server**: [Download MariaDB](https://mariadb.org/download/)
    *   *Install and run the service. The app uses user `root` with no password by default (common for local setups).*
3.  **Browser**: [Brave Browser](https://brave.com/) (Recommended) or Google Chrome.

### Installation

1.  **Clone the repo**
    ```sh
    git clone https://github.com/your_username/google-lead-scraper.git
    cd google-lead-scraper
    ```

2.  **Verify Database**
    Ensure your MariaDB service is running. 
    *   *Tip: You can check this in Windows Services (`services.msc`). Look for "MariaDB".*

<!-- USAGE EXAMPLES -->
## Usage

We have simplified the startup process for you.

### Option 1: One-Click Start (Windows)
Double-click the file named **`start_app.bat`** in the project folder.
*   This will automatically install any missing libraries.
*   It will launch the application in your default web browser.

### Option 2: Manual Start (Command Line)
If you prefer the command line or are on Mac/Linux:

1.  Create/Activate Virtual Environment:
    ```sh
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  Install Requirements:
    ```sh
    pip install -r requirements.txt
    ```
3.  Run the App:
    ```sh
    streamlit run app.py
    ```

### 🖥️ Using the Application

1.  **Sidebar Settings**:
    *   **Browser Path**: The app tries to find Brave/Chrome automatically. If it's wrong, paste the correct path here.
    *   **Headless Mode**: Check this to hide the browser window (faster). Uncheck to watch the bot work (good for debugging).
2.  **Scraping**:
    *   Enter your search term (e.g., "Digital Marketing Agencies London").
    *   Click **Start Scraping**.
    *   Results will appear live in the table.
3.  **Downloading**:
    *   Click "Download CSV" to get the file (saved in `output/`).
    *   Go to the **Database History** tab to see *all* leads ever found.

<!-- PROJECT STRUCTURE -->
## Project Structure

The project is organized to keep the workspace clean:

```text
├── app.py                  # Main Application (UI)
├── start_app.bat           # One-click launcher script
├── config.template.json    # Default settings template
├── src/                    # Core Logic
│   ├── search.py           # Scraping Engine (Selenium)
│   ├── database.py         # Database Connection Manager
│   └── utils.py            # System Utilities
├── output/                 # CSV files are saved here
├── debug/                  # Error screenshots are saved here
└── automation_profile/     # Browser cookies (do not delete to keep session)
```

<!-- CONFIGURATION -->
## Configuration

The application uses `config.json` to store your local settings.
*   When you run the app for the first time, it creates `config.json` from `config.template.json`.
*   **Database Credentials**: If your MariaDB has a password, open `config.json` and edit:
    ```json
    "db_password": "your_password"
    ```

<!-- TROUBLESHOOTING -->
## Troubleshooting

| Problem | Solution |
|ost | est |
| **"Brave Path not found"** | Uncheck "Headless Mode" to see if the browser opens. If not, copy the path to `brave.exe` manually into the Sidebar. |
| **Database Connection Error** | 1. Check if MariaDB is running. <br> 2. Check `config.json` for correct user/password. |
| **App closes immediately** | Run `start_app.bat` again or check the terminal window for error messages. |
| **No results found** | Google might be showing a Captcha. Uncheck "Headless Mode" to solve it manually once. |

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the Unlicense License. See `LICENSE.txt` for more information.