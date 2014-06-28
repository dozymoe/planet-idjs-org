import bleach

ALLOWED_TAGS = bleach.ALLOWED_TAGS + [
    'br', 'cite', 'div', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'p', 'pre', 'q',
    's', 'small', 'span', 'sub', 'sup', 'svg', 'time', 'u',
    'dl', 'dt', 'dd',
    'legend', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr',
]
ALLOWED_ATTRIBUTES = bleach.ALLOWED_ATTRIBUTES
ALLOWED_ATTRIBUTES.update({
    '*': ['aria-label', 'class', 'style'],
    'img': ['alt', 'height', 'src', 'title', 'width'],
    'time': ['datetime'],
})
ALLOWED_STYLES = [
    'font-style', 'font-weight',
]

def filter_html(text, loader_context):
    return bleach.clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
                        strip=True)
