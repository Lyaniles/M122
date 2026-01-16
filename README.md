<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Google Scraper</h3>

  <p align="center">
    A Streamlit application that scrapes Google search results for leads.
    <br />
    <br />
    <a href="#about-the-project">About The Project</a>
    &middot;
    <a href="#getting-started">Getting Started</a>
    &middot;
    <a href="#usage">Usage</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
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

This project is a web scraper with a user-friendly interface built with Streamlit. It automates the process of finding business leads (Title, URL, Description) from Google Search results using Selenium and the Brave Browser. The scraped data is then saved to a MySQL database.

### Built With

This project is built with the following technologies:

*   [Python](https://www.python.org/)
*   [Streamlit](https://streamlit.io/)
*   [Selenium](https://www.selenium.dev/)
*   [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
*   [Pandas](https://pandas.pydata.org/)
*   [MySQL](https://www.mysql.com/)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

You need to have the following software installed on your machine:

*   Python 3.x
*   Brave Browser
*   MySQL Server

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/your_username/your_repository.git
    ```
2.  Navigate to the project directory
    ```sh
    cd your_repository
    ```
3.  Create a virtual environment
    ```sh
    python -m venv venv
    ```
4.  Activate the virtual environment
    ```sh
    venv\Scripts\activate
    ```
5.  Install the required packages
    ```sh
    pip install -r requirements.txt
    ```
6.  Configure your database connection and Brave Browser path in the `config.json` file.

<!-- USAGE EXAMPLES -->
## Usage

You can run the application using the `start_app.bat` file, which will automatically set up the environment and start the Streamlit server.

Alternatively, you can run the application manually with the following command:

```sh
streamlit run app.py
```

Once the application is running, you can open it in your browser and start scraping by entering a search query and clicking the "Start Scraping" button.

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
  - **Headless Mode:** Run without opening a visible window (Uncheck this to solve Captchas manually).
  - **Pages:** How deep to scrape (1-10 pages).

<!-- PROJECT STRUCTURE -->
## Project Structure
- `app.py`: The frontend application (Streamlit).
- `search.py`: The backend scraping logic (`GoogleScraper` class).
- `database.py`: Handles MariaDB connection and data insertion.
- `start_app.bat`: One-click launcher for stakeholders.
- `automation_profile/`: Folder storing browser cookies/session (Do not delete if you want to avoid Captchas).

<!-- ROADMAP -->
## Roadmap

- [ ] Add support for other search engines.
- [ ] Add more data fields to be scraped.
- [ ] Improve error handling and reporting.

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the Unlicense License. See `LICENSE.txt` for more information.
