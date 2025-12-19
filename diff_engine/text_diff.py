import difflib

def generate_text_diff(old_text, new_text):
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile="before",
        tofile="after",
        lineterm=""
    )

    return "\n".join(diff)
