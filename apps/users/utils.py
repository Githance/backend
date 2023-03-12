# TODO move utils.py to core app when it is created
from django.utils.html import format_html


def form_safe_link(url, text=None):
    """Form safe link for use in ModelAdmin."""
    text = text or "ссылка" if url else "-"
    return format_html("<a href='{url}'>{text}</a>", url=url, text=text)
