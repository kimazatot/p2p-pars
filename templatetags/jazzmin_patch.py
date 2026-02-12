from django import template
from django.utils.html import format_html
import logging

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def safe_jazzmin_paginator_number(html_str):
    """
    Безопасный рендер пагинатора.
    Если html_str пустой, просто возвращаем пустую строку.
    """
    try:
        if not html_str:
            return ""
        return format_html(html_str)
    except Exception as e:
        logger.warning(f"Jazzmin paginator render failed: {e}")
        return ""
