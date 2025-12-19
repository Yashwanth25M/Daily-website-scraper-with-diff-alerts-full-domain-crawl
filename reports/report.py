from urllib.parse import urlparse


def _page_name(url):
    path = urlparse(url).path
    return path if path else "/"


def _extract_before_after(diff_text):
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


def _extract_removed_preview(old_text):
    if not old_text:
        return []

    lines = [l.strip() for l in old_text.splitlines() if l.strip()]
    return lines[:3]


def generate_html(added, removed, changed, old_texts=None):
    """
    Generates a clean, UI-style HTML email.
    """
    html = """
    <html>
    <body style="font-family:Segoe UI, Arial, sans-serif; background:#f8fafc; color:#1f2937;">
      <div style="max-width:700px;margin:auto;background:#ffffff;
                  padding:24px;border-radius:8px;
                  box-shadow:0 6px 18px rgba(0,0,0,0.08)">
        <h2 style="margin-top:0;">Daily Website Change Summary</h2>
    """

    # -----------------------------
    # New Pages
    # -----------------------------
    if added:
        html += "<h3 style='color:#16a34a;'>🟢 New Pages</h3><ul>"
        for url in added:
            html += f"<li><a href='{url}'>{_page_name(url)}</a></li>"
        html += "</ul>"

    # -----------------------------
    # Removed Pages
    # -----------------------------
    if removed:
        html += "<h3 style='color:#dc2626;'>🔴 Removed Pages</h3>"
        for url in removed:
            html += f"<b>{_page_name(url)}</b><ul>"
            if old_texts:
                preview = _extract_removed_preview(old_texts.get(url, ""))
                for line in preview:
                    html += f"<li>{line}</li>"
            html += "</ul>"

    # -----------------------------
    # Modified Pages (Before / After)
    # -----------------------------
    if changed:
        html += "<h3 style='color:#ea580c;'>🟠 Modified Pages</h3>"
        for url, diff_text in changed.items():
            before, after = _extract_before_after(diff_text)
            html += f"<b>{_page_name(url)}</b><ul>"
            if before:
                html += f"<li><b>Before:</b> {before}</li>"
            if after:
                html += f"<li><b>After:</b> {after}</li>"
            html += "</ul>"

    if not added and not removed and not changed:
        html += "<p>No changes detected.</p>"

    html += """
        <hr style="margin-top:24px;">
        <small style="color:#6b7280;">
            This email was generated automatically by Website Change Monitor.
        </small>
      </div>
    </body>
    </html>
    """

    return html
