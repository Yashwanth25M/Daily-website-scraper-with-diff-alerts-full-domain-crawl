import sys
import os
import subprocess
from datetime import datetime

# Ensure project root is in path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from storage.db import (
    fetch_last_two_runs,
    fetch_hashes_by_run,
    fetch_texts_by_run
)
from diff_engine.compare import compare_runs
from reports.report import generate_html
from reports.emailer import send_email


def run(domain):
    # 1. Generate unique run ID
    run_id = datetime.now().isoformat()

    # 2. Run crawler and store snapshot
    subprocess.run([
        sys.executable,
        "-m",
        "scrapy",
        "runspider",
        "crawler/spider.py",
        "-a",
        f"domain={domain}",
        "-a",
        f"run_id={run_id}"
    ])

    # 3. Get last two runs from DB
    runs = fetch_last_two_runs()

    if len(runs) < 2:
        print("Baseline created. No diff yet.")
        return

    new_run, old_run = runs[0], runs[1]

    # 4. Load snapshots for comparison
    old_hashes = fetch_hashes_by_run(old_run)
    new_hashes = fetch_hashes_by_run(new_run)

    old_texts = fetch_texts_by_run(old_run)
    new_texts = fetch_texts_by_run(new_run)

    # 5. Compare old vs new
    added, removed, changed = compare_runs(
        old_hashes, new_hashes, old_texts, new_texts
    )

    # 6. Generate HTML report
    html_report = generate_html(added, removed, changed)

    # 7. Send email
    send_email(html_report)

    print("Diff detected and email sent successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cli.py <website_url>")
        sys.exit(1)

    run(sys.argv[1])
