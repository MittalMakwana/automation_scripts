#!/opt/homebrew/bin/python3.11

import asyncio
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Pattern

from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession


@dataclass(frozen=True)
class RegexMatch:
    pattern_name: str
    matched_text: str
    groups: Dict[str, Optional[str]]


class RegexEngine:
    """Small regex registry that keeps pattern names and returns structured matches."""

    def __init__(self) -> None:
        self._patterns: Dict[str, Pattern[str]] = {}

    @classmethod
    def from_mapping(cls, patterns: Dict[str, str], flags: int = 0) -> "RegexEngine":
        engine = cls()
        for name, pattern in patterns.items():
            engine.register(name=name, pattern=pattern, flags=flags)
        return engine

    def register(self, name: str, pattern: str, flags: int = 0) -> None:
        self._patterns[name] = re.compile(pattern, flags)

    def match_first(self, text: str) -> Optional[RegexMatch]:
        for name, compiled in self._patterns.items():
            match = compiled.search(text)
            if match:
                return RegexMatch(
                    pattern_name=name,
                    matched_text=match.group(0),
                    groups=match.groupdict(),
                )
        return None

    def match_all(self, text: str) -> List[RegexMatch]:
        matches: List[RegexMatch] = []
        for name, compiled in self._patterns.items():
            for match in compiled.finditer(text):
                matches.append(
                    RegexMatch(
                        pattern_name=name,
                        matched_text=match.group(0),
                        groups=match.groupdict(),
                    )
                )
        return matches


async def fetch_websites(
    urls: List[str],
    impersonate: str = "chrome120",
    timeout: int = 10,
) -> Dict[str, Optional[str]]:
    """
    Fetch multiple websites asynchronously and return their HTML content.
    
    Args:
        urls: List of website URLs to fetch
        impersonate: Browser to impersonate (default: chrome120)
        timeout: Request timeout in seconds (default: 10)
    
    Returns:
        Dictionary with URL as key and HTML content as value
    
    Example:
        urls = ["https://example.com", "https://google.com"]
        data = await fetch_websites(urls)
        
        for url, html in data.items():
            soup = BeautifulSoup(html, "html.parser")
            print(soup.title)
    """
    results: Dict[str, Optional[str]] = {}

    async with AsyncSession() as session:
        tasks = []
        for url in urls:
            tasks.append(_fetch_single(session, url, impersonate, timeout))

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for url, response in zip(urls, responses):
            if isinstance(response, Exception):
                print(f"Error fetching {url}: {response}")
                results[url] = None
            else:
                results[url] = response

    return results


async def _fetch_single(
    session: AsyncSession,
    url: str,
    impersonate: str,
    timeout: int,
) -> str:
    """Helper function to fetch a single URL."""
    try:
        response = await session.get(
            url,
            impersonate=impersonate,
            timeout=timeout,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive"
            }
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise Exception(f"Failed to fetch {url}: {str(e)}")


def parse_html(html: str, parser: str = "html.parser") -> BeautifulSoup:
    """
    Parse HTML content with BeautifulSoup.
    
    Args:
        html: HTML content string
        parser: Parser to use (default: html.parser)
    
    Returns:
        BeautifulSoup object
    """
    return BeautifulSoup(html, parser)


async def fetch_and_parse(
    urls: List[str],
    impersonate: str = "chrome120",
    timeout: int = 10,
) -> Dict[str, Optional[BeautifulSoup]]:
    """
    Fetch multiple websites and return parsed BeautifulSoup objects.
    
    Args:
        urls: List of website URLs to fetch
        impersonate: Browser to impersonate (default: chrome120)
        timeout: Request timeout in seconds (default: 10)
    
    Returns:
        Dictionary with URL as key and BeautifulSoup object as value
    
    Example:
        urls = ["https://example.com", "https://google.com"]
        soups = await fetch_and_parse(urls)
        
        for url, soup in soups.items():
            if soup:
                print(f"{url}: {soup.title.string}")
    """
    html_data = await fetch_websites(urls, impersonate, timeout)
    
    parsed = {}
    for url, html in html_data.items():
        if html:
            parsed[url] = parse_html(html)
        else:
            parsed[url] = None
    
    return parsed


def extract_text_from_soup(
    soup: BeautifulSoup,
    selector: str = "body",
    separator: str = " ",
    strip: bool = True,
) -> str:
    """Extract text from a selected node, defaulting to the full body."""
    node = soup.select_one(selector)
    if node is None:
        return ""
    return node.get_text(separator=separator, strip=strip)


async def fetch_parse_and_match(
    urls: List[str],
    regex_engine: RegexEngine,
    text_selector: str = "body",
    impersonate: str = "chrome120",
    timeout: int = 10,
) -> Dict[str, Dict[str, Any]]:
    """
    End-to-end scraper helper.

    1) Fetches urls asynchronously with browser impersonation.
    2) Parses each page with BeautifulSoup.
    3) Runs all registered regex patterns on extracted page text.
    """
    html_map = await fetch_websites(urls=urls, impersonate=impersonate, timeout=timeout)

    results: Dict[str, Dict[str, Any]] = {}
    for url, html in html_map.items():
        if not html:
            results[url] = {
                "html": None,
                "soup": None,
                "title": None,
                "text": "",
                "regex_matches": [],
            }
            continue

        soup = parse_html(html)
        text = extract_text_from_soup(soup, selector=text_selector)
        matches = regex_engine.match_all(text)
        results[url] = {
            "html": html,
            "soup": soup,
            "title": soup.title.string.strip() if soup.title and soup.title.string else None,
            "text": text,
            "regex_matches": [
                {
                    "pattern_name": m.pattern_name,
                    "matched_text": m.matched_text,
                    "groups": m.groups,
                }
                for m in matches
            ],
        }

    return results


# Example usage
if __name__ == "__main__":
    async def main():
        urls = ["https://example.com", "https://python.org"]

        # Your maintained patterns can live in one mapping and be extended over time.
        patterns = {
            "year": r"\b(?P<year>19\d{2}|20\d{2})\b",
            "quality": r"\b(?P<quality>480p|720p|1080p|2160p)\b",
            "size": r"\[(?P<size>\d+(?:\.\d+)?(?:MB|GB))\]",
        }

        engine = RegexEngine.from_mapping(patterns=patterns, flags=re.IGNORECASE)
        data = await fetch_parse_and_match(urls=urls, regex_engine=engine)

        for url, item in data.items():
            print(f"\nURL: {url}")
            print(f"Title: {item['title']}")
            print(f"Matches: {len(item['regex_matches'])}")
            for match in item["regex_matches"][:3]:
                print(f"  - {match['pattern_name']}: {match['matched_text']}")

    asyncio.run(main())
