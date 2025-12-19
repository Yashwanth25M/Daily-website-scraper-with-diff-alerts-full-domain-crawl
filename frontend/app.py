import streamlit as st

from storage.db import (
    fetch_last_two_runs,
    fetch_hashes_by_run,
    fetch_texts_by_run,
    fetch_recent_runs_with_counts
)
from diff_engine.compare import compare_runs
from cli import run as run_crawler

# EMAIL IMPORTS (important)
from reports.report import generate_html
from reports.emailer import send_email


# -------------------------------------------------
# Helper: extract before / after content
# -------------------------------------------------
def extract_before_after(diff_text):
    """
    Extracts one meaningful before/after change from diff text.
    Returns (before, after).
    """
    before = None
    after = None

    for line in diff_text.splitlines():
        if line.startswith("-") and not line.startswith("---"):
            text = line[1:].strip()
            if text:
                before = text
        elif line.startswith("+") and not line.startswith("+++"):
            text = line[1:].strip()
            if text:
                after = text

    return before, after


def extract_removed_content(old_text):
    """
    Returns a short preview of removed page content.
    """
    if not old_text:
        return ["Page removed"]

    lines = [l.strip() for l in old_text.splitlines() if l.strip()]
    return lines[:3]


# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Daily Website Change Monitor",
    layout="centered"
)

st.title("🔍 Daily Website Change Monitor")
st.caption(
    "Automatically tracks website updates and shows meaningful changes"
)

st.divider()


# -------------------------------------------------
# Run new scan
# -------------------------------------------------
st.subheader("Run New Scan")

url = st.text_input(
    "Website URL",
    placeholder="https://example.com"
)

send_email_toggle = st.checkbox(
    "Send email notification if changes are detected",
    value=True
)

run_clicked = st.button("Run Scan", type="primary")


# -------------------------------------------------
# Scan execution & results
# -------------------------------------------------
if run_clicked:
    if not url:
        st.warning("Please enter a valid website URL.")
    else:
        with st.spinner("Scanning website and analyzing changes..."):
            run_crawler(url)

        runs = fetch_last_two_runs()

        if len(runs) < 2:
            st.info("Baseline created. Run the scan again to detect changes.")
        else:
            new_run, old_run = runs[0], runs[1]

            old_hashes = fetch_hashes_by_run(old_run)
            new_hashes = fetch_hashes_by_run(new_run)
            old_texts = fetch_texts_by_run(old_run)
            new_texts = fetch_texts_by_run(new_run)

            added, removed, changed = compare_runs(
                old_hashes,
                new_hashes,
                old_texts,
                new_texts
            )

            st.success("Scan completed successfully.")

            # -----------------------------
            # Send Email (UI-triggered)
            # -----------------------------
            if send_email_toggle and (added or removed or changed):
                html_report = generate_html(added, removed, changed, old_texts)
                email_sent = send_email(html_report)

                if email_sent:
                    st.info("📧 Email notification sent.")
                else:
                    st.warning("Email not sent. Check SMTP configuration.")

            # -----------------------------
            # Scan summary
            # -----------------------------
            st.subheader("Scan Summary")
            st.caption("Comparison between the latest scan and the previous run")

            c1, c2, c3 = st.columns(3)
            c1.metric("New Pages", len(added))
            c2.metric("Removed Pages", len(removed))
            c3.metric("Modified Pages", len(changed))

            st.divider()

            # -----------------------------
            # New Pages (clickable)
            # -----------------------------
            if added:
                st.subheader("🟢 New Pages")
                for u in added:
                    st.markdown(f"• [{u}]({u})", unsafe_allow_html=True)
                st.divider()

            # -----------------------------
            # Removed Pages (what was removed)
            # -----------------------------
            if removed:
                st.subheader("🔴 Removed Pages")

                for page in removed:
                    st.markdown(f"**{page}**")

                    removed_preview = extract_removed_content(
                        old_texts.get(page, "")
                    )

                    for line in removed_preview:
                        st.write(f"• {line}")

                    st.write("")
                st.divider()

            # -----------------------------
            # Modified Pages (Before / After)
            # -----------------------------
            if changed:
                st.subheader("🟠 Modified Pages")

                for page, diff_text in changed.items():
                    st.markdown(f"**{page}**")

                    before, after = extract_before_after(diff_text)

                    if before and after:
                        st.write(f"• **Before:** {before}")
                        st.write(f"• **After:** {after}")
                    elif after:
                        st.write(f"• Updated to: {after}")
                    else:
                        st.write("• Page content changed")

                    st.write("")
            else:
                st.info("No content changes detected.")


# -------------------------------------------------
# Recent scan history
# -------------------------------------------------
st.divider()
st.subheader("Recent Scan History")

run_ids = fetch_recent_runs_with_counts(limit=5)

if len(run_ids) < 2:
    st.write("• Baseline created")
else:
    for i in range(1, len(run_ids)):
        current_run = run_ids[i]
        previous_run = run_ids[i - 1]

        old_hashes = fetch_hashes_by_run(previous_run)
        new_hashes = fetch_hashes_by_run(current_run)
        old_texts = fetch_texts_by_run(previous_run)
        new_texts = fetch_texts_by_run(current_run)

        added, removed, changed = compare_runs(
            old_hashes,
            new_hashes,
            old_texts,
            new_texts
        )

        ts = current_run.replace("T", " ")[:16]

        if not added and not removed and not changed:
            summary = "no changes"
        elif removed:
            summary = f"{len(removed)} page(s) removed"
        elif changed:
            summary = f"{len(changed)} page(s) modified"
        else:
            summary = "structure changed"

        st.write(f"• {ts} — {summary}")
