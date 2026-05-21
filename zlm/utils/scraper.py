"""
-----------------------------------------------------------------------
File: scraper.py
Creation Time: May 2025
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------

Web scraping with Firecrawl (primary) and Jina Reader (fallback).

Priority order:
  1. Firecrawl  — API-based, handles JS/anti-bot; requires FIRECRAWL_API_KEY
  2. Jina       — Zero-dep prefix trick (r.jina.ai); always available
"""

import logging
import os

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Firecrawl
# ---------------------------------------------------------------------------

try:
    from firecrawl import FirecrawlApp as _FirecrawlApp
    _firecrawl_available = True
except ImportError:
    _firecrawl_available = False


def _scrape_firecrawl(url: str) -> str | None:
    """Scrape *url* with Firecrawl and return clean markdown, or None on failure."""
    api_key = os.environ.get("FIRECRAWL_API_KEY", "").strip()
    if not api_key:
        logger.debug("FIRECRAWL_API_KEY not set — skipping Firecrawl")
        return None
    if not _firecrawl_available:
        logger.debug("firecrawl-py not installed — skipping Firecrawl")
        return None

    try:
        app = _FirecrawlApp(api_key=api_key)
        result = app.scrape_url(url, params={"formats": ["markdown"]})
        markdown = result.get("markdown", "").strip()
        if markdown:
            logger.info("Firecrawl: successfully scraped %s (%d chars)", url, len(markdown))
            return markdown
        logger.warning("Firecrawl: empty markdown for %s", url)
        return None
    except Exception as exc:
        logger.warning("Firecrawl failed for %s: %s", url, exc)
        return None


# ---------------------------------------------------------------------------
# Jina Reader
# ---------------------------------------------------------------------------

_JINA_PREFIX = "https://r.jina.ai/"
_JINA_TIMEOUT = 30  # seconds


def _scrape_jina(url: str) -> str | None:
    """Scrape *url* via Jina Reader and return the response text, or None."""
    jina_url = f"{_JINA_PREFIX}{url}"
    try:
        resp = httpx.get(jina_url, timeout=_JINA_TIMEOUT, follow_redirects=True)
        resp.raise_for_status()
        content = resp.text.strip()
        if content:
            logger.info("Jina: successfully scraped %s (%d chars)", url, len(content))
            return content
        logger.warning("Jina: empty response for %s", url)
        return None
    except Exception as exc:
        logger.warning("Jina failed for %s: %s", url, exc)
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def scrape_url(url: str) -> str | None:
    """Return clean text/markdown for *url*.

    Tries Firecrawl first (if ``FIRECRAWL_API_KEY`` is set), then falls back
    to Jina Reader.  Returns ``None`` if both strategies fail.

    Args:
        url: The web page URL to scrape.

    Returns:
        Scraped content as a string, or ``None`` if all strategies failed.
    """
    if not url or not url.strip():
        return None

    content = _scrape_firecrawl(url)
    if content:
        return content

    logger.info("Falling back to Jina Reader for %s", url)
    return _scrape_jina(url)
