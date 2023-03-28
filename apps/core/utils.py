from django.utils.html import format_html
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


def form_safe_link(url, text=None):
    """Form safe link for use in ModelAdmin."""
    text = text or "ссылка" if url else "-"
    return format_html("<a href='{url}'>{text}</a>", url=url, text=text)


def paginated_response(viewset, queryset, status=HTTP_200_OK):
    """
    Return paginating response.

    The function is the same as the `list()` method from ListModelMixin, except that
    it does not make a call to `self.get_queryset()`. This allows us to filter
    a queryset in @action methods before pagination.
    """
    page = viewset.paginate_queryset(queryset)
    if page is not None:
        serializer = viewset.get_serializer(page, many=True)
        return viewset.get_paginated_response(serializer.data)
    serializer = viewset.get_serializer(queryset, many=True)
    return Response(serializer.data, status=status)
