from xml.sax.saxutils import (
    escape as xml_escape, unescape as xml_unescape,
)

html_escape_table = {
    '"': "&quot;",
    "'": "&apos;",
}
html_unescape_table = {v:k for (k, v) in html_escape_table.items()}

def escape(text):
    return xml_escape(text, html_escape_table)

def unescape(text):
    return xml_unescape(text, html_unescape_table)
