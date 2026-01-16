<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium">
  <img src="https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white" alt="MariaDB">
</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">🚀 Google Lead Scraper 🚀</h3>

  <p align="center">
    A professional-grade, automated lead generation tool with a powerful Streamlit UI.
    <br />
    <br />
    <a href="#about-the-project"><strong>Explore the features »</strong></a>
    <br />
    <br />
    <a href="#getting-started">Getting Started</a>
    &middot;
    <a href="#usage">Usage</a>
    &middot;
    <a href="#contributing">Contribute</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#key-features">✨ Key Features</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#database-integration">🗄️ Database Integration</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This repository contains a professional-grade web scraper designed to automate the process of finding business leads (Title, URL, Description) from Google Search results. It features an interactive UI built with Streamlit, robust automation with Selenium, and seamless integration with a MariaDB database.

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

### Built With

*   [Python](https://www.python.org/)
*   [Streamlit](https://streamlit.io/)
*   [Selenium](https://www.selenium.dev/)
*   [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
*   [Pandas](https://pandas.pydata.org/)
*   [MySQL-Connector-Python](https://pypi.org/project/mysql-connector-python/)
*   [MariaDB](https://mariadb.org/)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

*   **Python 3.10+**
*   **Brave Browser**
*   **MariaDB Server (10.11+)**

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/your_username/your_repository.git
    ```
2.  Navigate to the project directory
    ```sh
    cd your_repository
    ```
3.  Create and activate a virtual environment
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```
4.  Install the required packages
    ```sh
    pip install -r requirements.txt
    ```
5.  Configure your database connection and Brave Browser path in the `config.json` file or through the UI.

<!-- DATABASE INTEGRATION -->
## 🗄️ Database Integration

This application is designed to work seamlessly with a MariaDB database.

- **Automatic Schema Creation:** The application will automatically create the `google_scraper` database and the `leads` table if they don't exist, provided the database user has the necessary permissions.
- **Data Persistence:** All scraped leads are saved to the `leads` table, ensuring that your data is stored securely and persistently.
- **Deduplication:** The system automatically checks for existing URLs and prevents duplicate entries, ensuring data integrity.
- **Easy Viewing:** The "Database History" tab in the Streamlit UI allows you to view the entire contents of the `leads` table and export it to a CSV file.

<!-- USAGE EXAMPLES -->
## Usage

You can run the application using the **`start_app.bat`** file, which will automatically set up the environment and start the Streamlit server.

Alternatively, you can run the application manually with the following command:
```sh
streamlit run app.py
```
Once the application is running, open it in your browser, configure your settings in the sidebar, enter a search query, and click "Start Scraping".

<!-- CONFIGURATION -->
## Configuration
The settings are managed via the UI but saved to `config.json` for persistence.
- **Database:**
  - `db_host`: Database host (default: `localhost`)
  - `db_user`: Database user (default: `root`)
  - `db_password`: Database password (leave empty if none)
  - `db_name`: Database name (default: `google_scraper`)
- **Scraper:**
  - **Brave Browser Path:** Location of your `brave.exe`.
  - **Headless Mode:** Run without opening a visible window.
  - **Pages:** How many pages to scrape.

<!-- PROJECT STRUCTURE -->
## Project Structure
- `app.py`: The frontend application (Streamlit).
- `search.py`: The backend scraping logic (`GoogleScraper` class).
- `database.py`: Handles MariaDB connection and data insertion.
- `start_app.bat`: One-click launcher for stakeholders.
- `automation_profile/`: Stores browser cookies/session to avoid Captchas.

<!-- ROADMAP -->
## Roadmap

- [ ] Add support for other search engines.
- [ ] Add more data fields to be scraped.
- [ ] Improve error handling and reporting.

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

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
