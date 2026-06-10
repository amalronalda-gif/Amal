"""News & event-risk layer for gold.

Two free sources, no API keys:
  - ForexFactory weekly economic calendar (high-impact USD events move gold)
  - Yahoo Finance RSS headlines for gold futures (GC=F)

Headline sentiment is deliberately crude (keyword counting) and labeled as
such — it adds context, it is not deep NLP.
"""

from __future__ import annotations

import json
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone

CALENDAR_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
HEADLINES_URL = ("https://feeds.finance.yahoo.com/rss/2.0/headline"
                 "?s=GC=F&region=US&lang=en-US")

# countries whose data moves XAU/USD; "All" covers OPEC/G7-style events
RELEVANT_COUNTRIES = {"USD", "All"}

BULLISH_WORDS = re.compile(
    r"\b(rall(?:y|ies)|surge[sd]?|soar(?:s|ed)?|jump(?:s|ed)?|gain(?:s|ed)?|"
    r"climb(?:s|ed)?|record high|haven|safe.haven|rate cut|dovish|"
    r"weak(?:er)? dollar|inflation fears|buy(?:ing)? gold)\b", re.I)
BEARISH_WORDS = re.compile(
    r"\b(fall(?:s|ing)?|fell|drop(?:s|ped)?|slump(?:s|ed)?|slide[sd]?|"
    r"plunge[sd]?|tumble[sd]?|pressure[sd]?|rate hike|hawkish|"
    r"strong(?:er)? dollar|sell(?:ing|.off)|profit.taking)\b", re.I)

_cache: dict[str, tuple[float, object]] = {}
CACHE_TTL = 1800  # 30 min: both feeds update slowly; be a polite client


def _cached(key: str, fetcher):
    now = time.time()
    hit = _cache.get(key)
    if hit and now - hit[0] < CACHE_TTL:
        return hit[1]
    value = fetcher()
    _cache[key] = (now, value)
    return value


def _http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()


@dataclass
class CalendarEvent:
    title: str
    country: str
    impact: str          # High / Medium / Low / Holiday
    when: datetime
    forecast: str
    previous: str

    def hours_from_now(self) -> float:
        return (self.when - datetime.now(timezone.utc)).total_seconds() / 3600


@dataclass
class Headline:
    title: str
    link: str
    sentiment: int       # +1 bullish-ish, -1 bearish-ish, 0 neutral


def upcoming_events(hours_ahead: float = 24.0,
                    hours_back: float = 2.0) -> list[CalendarEvent]:
    """High/Medium-impact USD events from -hours_back to +hours_ahead."""
    def fetch():
        rows = json.loads(_http_get(CALENDAR_URL).decode())
        events = []
        for r in rows:
            try:
                when = datetime.fromisoformat(r["date"]).astimezone(timezone.utc)
            except (KeyError, ValueError):
                continue
            events.append(CalendarEvent(r.get("title", "?"), r.get("country", "?"),
                                        r.get("impact", "?"), when,
                                        r.get("forecast", ""), r.get("previous", "")))
        return events

    events = _cached("calendar", fetch)
    out = [e for e in events
           if e.country in RELEVANT_COUNTRIES
           and e.impact in ("High", "Medium")
           and -hours_back <= e.hours_from_now() <= hours_ahead]
    out.sort(key=lambda e: e.when)
    return out


def gold_headlines(limit: int = 6) -> list[Headline]:
    def fetch():
        root = ET.fromstring(_http_get(HEADLINES_URL))
        items = []
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            if title:
                items.append(Headline(title, link, _sentiment(title)))
        return items

    return _cached("headlines", fetch)[:limit]


def _sentiment(text: str) -> int:
    score = len(BULLISH_WORDS.findall(text)) - len(BEARISH_WORDS.findall(text))
    return (score > 0) - (score < 0)


def event_risk(events: list[CalendarEvent] | None = None,
               window_hours: float = 8.0) -> CalendarEvent | None:
    """The next high-impact USD event inside the danger window, if any."""
    if events is None:
        try:
            events = upcoming_events(hours_ahead=window_hours)
        except Exception:
            return None
    for e in events:
        if e.impact == "High" and 0 <= e.hours_from_now() <= window_hours:
            return e
    return None
