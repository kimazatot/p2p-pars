import logging
from django.utils.html import format_html
import jazzmin.templatetags.jazzmin as jazzmin_tags

logger = logging.getLogger(__name__)

def patch_jazzmin():
    def safe(html_str):
        try:
            if not html_str:
                return ""
            return format_html(html_str)
        except Exception as e:
            logger.warning(f"Jazzmin paginator failed: {e}")
            return ""
    jazzmin_tags.jazzmin_paginator_number = safe
