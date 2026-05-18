from urllib.parse import urlparse

import validators


def validate_url(url_input):
    """Validate raw URL input. Returns error message or None."""
    url_input = url_input.strip()

    if not url_input:
        return 'URL обязателен'

    if len(url_input) > 255:
        return 'URL превышает 255 символов'

    if not validators.url(url_input):
        return 'Некорректный URL'

    return None


def normalize_url(url_input):
    """Normalize URL to scheme + netloc."""
    parsed = urlparse(url_input.strip())
    return f"{parsed.scheme}://{parsed.netloc}"
