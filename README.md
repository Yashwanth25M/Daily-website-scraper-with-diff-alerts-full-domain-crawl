![Python](https://img.shields.io/badge/Python-3.13-blue)
![Scrapy](https://img.shields.io/badge/Scrapy-2.13-green)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Platform](https://img.shields.io/badge/Platform-Windows-informational)
![License](https://img.shields.io/badge/License-Academic%20Use-orange)
# Daily Website Scraper with Diff Alerts (Full-Domain Crawl)


## Project Overview

This project is a Python-based system that monitors websites for content changes.  
It crawls all accessible pages of a given domain, stores snapshots of page content, compares successive crawls, and generates a human-readable HTML report highlighting what has changed.

The system presents detected changes in two ways:
- A clean, interactive web dashboard for visual inspection
- An automated HTML email summary for notifications

Changes are displayed in a human-readable format:
- Newly added pages are shown as clickable links
- Modified pages display clear **Before / After** content
- Removed pages include a preview of the removed content


It supports both **local websites** (for controlled testing) and **live public websites**, and sends the change report via email in HTML format.
## Features

- Full-domain website crawling with strict in-domain scope control  
- Supports both local websites (for testing) and live public websites  
- Stores versioned snapshots of page content for every crawl run  
- Hash-based change detection for fast comparison between runs  
- Accurate detection of:
  - Newly added pages
  - Removed pages
  - Modified pages  
- Human-readable change summaries with clear Before / After comparisons  
- Clean separation of new, removed, and modified pages  
- Clickable links for newly added pages  
- Preview of removed page content  

## Tech Stack / Libraries Used

- **Python 3.13** – Core programming language used for crawling, change detection, reporting, automation, and the web dashboard  
- **Scrapy** – Framework for full-domain website crawling and in-domain link discovery  
- **BeautifulSoup** – HTML parsing and structured text extraction from web pages  
- **SQLite** – Embedded relational database for storing crawl runs, content snapshots, and run history  
- **hashlib** – Used to generate content hashes for fast and efficient change detection  
- **difflib** – Performs text-level differencing to extract Before / After content changes  
- **Streamlit** – Interactive web dashboard for running scans, viewing summaries, and inspecting changes  
- **APScheduler** – Cron-style scheduling for automated daily scans  
- **smtplib** – Sends HTML email notifications containing human-readable change summaries  
- **python-dotenv** – Secure loading of environment variables and SMTP credentials  

## Project Architecture

The system follows a modular, pipeline-based architecture where each component is responsible for a single concern.  
Data flows sequentially from crawling to storage, comparison, reporting, and notification.

- **CLI Runner (`cli.py`)**  
  Acts as the orchestration layer. It triggers crawling, manages crawl runs, initiates comparison between snapshots, and invokes report generation and notification.

- **Crawler (`crawler/spider.py`)**  
  Performs full-domain crawling using Scrapy. Discovers internal links, fetches HTML pages, extracts meaningful content (scoped to the `<main>` section), and passes content for storage.

- **Storage Layer (`storage/db.py`)**  
  Stores page snapshots in an SQLite database. Each crawl is recorded with a unique run identifier, enabling historical comparisons between runs.

- **Diff Engine (`diff_engine/`)**  
  Compares snapshots from two crawl runs. Uses hash comparison for fast change detection and text differencing for precise identification of added and removed content.

- **Report Generator (`reports/report.py`)**  
  Converts diff results into a structured, human-readable HTML report that highlights file-level and section-level changes.

- **Notification Module (`reports/emailer.py`)**  
  Sends the generated HTML report via email after each comparison run.

- **Web Dashboard (`frontend/app.py`)**  
  A Streamlit-based frontend that allows users to Trigger scans manually ,View scan summaries ,Inspect what changed using Before / After comparisons


This separation of concerns makes the system easy to extend, test, and maintain.
## System Flow

```text
┌──────────────────┐
│ CLI Command      │
│ (python cli.py)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Web Crawler      │
│ (Scrapy Spider)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Snapshot Storage │
│ (SQLite DB)      │
│ - url            │
│ - content hash   │
│ - extracted text │
│ - run_id         │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Diff Engine      │
│ - hash compare   │
│ - text diff      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Web Dashboard    │
│ (Streamlit UI)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ HTML Report      │
│ Generation       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│Email Notification│
│ (HTML Report)    │
└──────────────────┘
```
## Project Structure

```text
daily-website-diff-scraper/
├── cli.py
├── scheduler.py
├── frontend/
│   └── app.py
├── crawler/
│   └── spider.py
├── diff_engine/
│   ├── compare.py
│   ├── hasher.py
│   └── text_diff.py
├── storage/
│   └── db.py
├── reports/
│   ├── report.py
│   └── emailer.py
├── snapshots.db
├── README.md
├── .env
└── .gitignore

```
## Setup Instructions (Windows)

1. **Install Python**
   - Install Python 3.13 or later from the official Python website.
   - Ensure Python is added to the system PATH.

2. **Create a virtual environment**
  ```powershell
   py -m venv venv
  ```
3. **Activate the virtual environment**
  ```powershell
  venv\Scripts\activate
  ```
4. **Install required dependencies**
  ```powershell
 py -m pip install -r requirements.txt
  ```
5. **Verify installation**
  ```powershell
  py --version
  scrapy version
  ```
  ## Environment Configuration

The project uses environment variables to manage configuration and sensitive information such as email credentials.
Configure Environment Variables


1. **Configure Environment Variables**

   Create a file named .env in the project root
2.**Configure email settings**

Update the .env file with appropriate values.
  ```powershell
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USER=your_email@gmail.com
  SMTP_PASS=your_app_password
  FROM_EMAIL=your_email@gmail.com
  TO_EMAIL=recipient_email@gmail.com
  ```
3.**Secure sensitive data**

Ensure the following entries exist in .gitignore to prevent accidental commits:
  ```powershell
  .env
  venv/
  __pycache__/
  ```
## How to Run

### Run on a Local Website (Recommended for Demo)

1. **Start the local website**

   Open a terminal and run:
  ```powershell
   cd local_site
   py -m http.server 8000
  ```

2.**Run the crawler (first run – baseline)**
  Open another terminal:

  ```powershell
  py cli.py http://localhost:8000
  ```

  This creates the initial baseline snapshot.

3.**Modify website content**

  Edit any HTML file inside the ```<main>``` section and save the changes.

4.**Run the crawler again (diff detection)**
  ```powershell
  python cli.py http://localhost:8000
  ```
  An HTML diff report will be generated and sent via email.


5.**Run the Web Dashboard (UI)**

```powershell
py -m streamlit run frontend/app.py
```


A Streamlit-based frontend that allows users to:
- Trigger scans manually  
- View scan summaries  
- Inspect what changed using Before / After comparisons  
- Review recent scan history  
- Optionally send email notifications


## Testing (Pytest)

This project includes unit tests written using **pytest** to validate the core logic of the system.

### What Is Tested

The following components are covered by unit tests:

- Content hashing logic
- Snapshot comparison and diff detection
- HTML report generation

Components that depend on external systems (web crawling, email delivery, and network access) are excluded from unit tests and are validated through manual execution.

### Test Directory Structure

```text
tests/
├── test_hasher.py
├── test_compare.py
├── test_report.py
```
## Running Tests

1. **Install pytest**
```powershell
pip install pytest
```
2. **Run all tests from the project root**
```powershell
pytest
```
3. **Expected result**

All tests should pass without errors, confirming that the core comparison and reporting logic works as expected.


---
## Output & Reports

- **SQLite Database (`snapshots.db`)**  
  Stores versioned snapshots of crawled pages, including URLs, extracted text, content hashes, and run identifiers.

- **Change Summary Report**
  Generates a clean, human-readable HTML summary that highlights:
  - New pages
  - Removed pages
  - Modified pages with added and removed content
  - File name and HTML section where changes occurred

- **Email Notification**  
  Sends the HTML diff report via email after each successful comparison run.

- **Console Output**  
  Displays execution status, crawl progress, and baseline or diff detection messages during runtime.
## Notes & Best Practices

- Always ensure you have permission to crawl the target website.
- Respect polite crawling practices such as limiting crawl scope and avoiding excessive requests.
- Use a local website for testing to produce controlled and reproducible content changes.
- Run the crawler at least twice on the same website to enable comparison between runs.
- Keep crawling, storage, diffing, and reporting logic modular to simplify maintenance and future extensions.
- Avoid hard-coding credentials; use environment variables for all sensitive configuration.
## Limitations

- JavaScript-heavy websites are only partially supported, as the crawler does not execute client-side JavaScript.
- Authentication-protected pages are not crawled unless additional authentication handling is implemented.
- Very large domains may require crawl-rate tuning to manage execution time and resource usage.
- Email delivery depends on network availability and SMTP server configuration.
## Success Criteria

- Successful crawling of all accessible in-domain pages for a given website  
- Correct storage of content snapshots for each crawl run  
- Accurate detection of:
  - Newly added pages
  - Removed pages
  - Modified page content  
- Clear and human-readable HTML diff reports showing what changed and where  
- Reliable comparison across multiple consecutive crawl runs  
- No hard-coded credentials or sensitive data in source code  
## Author / Submission Context

This project was developed as part of an academic assignment to demonstrate practical skills in web crawling, data persistence, change detection, and automated reporting.

The implementation emphasizes:
- Clean and modular architecture
- Practical problem-solving
- Real-world applicability of web monitoring systems

All code and documentation are original and created for educational purposes.

---

## Disclaimer

This tool is intended for monitoring websites that you own or have explicit permission to crawl.  
The author is not responsible for misuse of this software or violations of website terms of service.
