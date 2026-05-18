from bs4 import BeautifulSoup


def parse_page(html):
    """Parse HTML and extract h1, title, description."""
    soup = BeautifulSoup(html, 'html.parser')

    h1 = soup.h1.get_text(strip=True) if soup.h1 else None
    title = (
        soup.title.string.strip()
        if soup.title and soup.title.string
        else None
    )

    meta_desc = soup.find('meta', attrs={'name': 'description'})
    description = (
        meta_desc['content'].strip()
        if meta_desc and meta_desc.get('content')
        else None
    )

    return h1, title, description


def truncate(text, max_length=200):
    """Truncate text to max_length with ... suffix if exceeded."""
    if not text:
        return text
    if len(text) > max_length:
        return text[:max_length - 3] + '...'
    return text
