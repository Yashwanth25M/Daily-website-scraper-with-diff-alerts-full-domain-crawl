from reports.report import generate_html

def test_generate_html_returns_string():
    html = generate_html([], [], {})
    assert isinstance(html, str)
    assert "<html>" in html.lower()
