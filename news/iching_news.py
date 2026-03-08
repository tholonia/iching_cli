#!/usr/bin/env python3
"""
I Ching News Analyzer

Reads headlines + synopses from a JSON file (produced by ap_scraper.py),
matches each to one of the 64 I Ching hexagrams, identifies moving lines,
computes the resulting hexagram, then rewrites the story as next-week's news
already happened — in the grave, authoritative tone of Walter Cronkite.

Usage:
    ./iching_news.py
    ./iching_news.py --input ap_news_headlines.json --limit 5
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
REGEN_DIR = Path(__file__).parent.parent / "book" / "v2" / "regen"
DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_INPUT = "ap_news_headlines.json"
DEFAULT_OUTPUT = "next_weeks_news.json"

# Traditional hexagram sequence: (seq_number, icon, binary_value, name)
HEXAGRAM_TABLE = [
    (1,  "䷀", 63, "Creative Force"),
    (2,  "䷁",  0, "Receptive Earth"),
    (3,  "䷂", 34, "Initial Difficulty"),
    (4,  "䷃", 20, "Youthful Inexperience"),
    (5,  "䷄", 59, "Patient Waiting"),
    (6,  "䷅", 58, "Conflict"),
    (7,  "䷆", 16, "Organization"),
    (8,  "䷇", 18, "Union"),
    (9,  "䷈", 55, "Minor Restraint"),
    (10, "䷉", 59, "Treading Carefully"),
    (11, "䷊", 14, "Harmony"),
    (12, "䷋", 49, "Stagnation"),
    (13, "䷌", 61, "Fellowship"),
    (14, "䷍", 47, "Great Possession"),
    (15, "䷎",  4, "Modesty"),
    (16, "䷏", 34, "Enthusiasm"),
    (17, "䷐", 25, "Following"),
    (18, "䷑", 38, "Decay and Repair"),
    (19, "䷒",  3, "Approach"),
    (20, "䷓", 48, "Contemplation"),
    (21, "䷔", 41, "Biting Through"),
    (22, "䷕", 37, "Grace"),
    (23, "䷖",  4, "Splitting Apart"),
    (24, "䷗",  1, "Return"),
    (25, "䷘", 57, "Innocence"),
    (26, "䷙", 55, "Great Taming"),
    (27, "䷚", 33, "Nourishment"),
    (28, "䷛", 30, "Great Excess"),
    (29, "䷜", 18, "Abysmal Water"),
    (30, "䷝", 45, "Clinging Fire"),
    (31, "䷞", 28, "Mutual Attraction"),
    (32, "䷟", 14, "Duration"),
    (33, "䷠", 60, "Retreat"),
    (34, "䷡", 15, "Great Power"),
    (35, "䷢", 40, "Progress"),
    (36, "䷣",  5, "Darkening of the Light"),
    (37, "䷤", 53, "Family"),
    (38, "䷥", 43, "Opposition"),
    (39, "䷦", 20, "Obstruction"),
    (40, "䷧", 10, "Liberation"),
    (41, "䷨", 35, "Decrease"),
    (42, "䷩", 23, "Increase"),
    (43, "䷪", 31, "Decisive Declaration"),
    (44, "䷫", 62, "Coming to Meet"),
    (45, "䷬", 24, "Gathering"),
    (46, "䷭",  6, "Ascending"),
    (47, "䷮", 26, "Exhaustion"),
    (48, "䷯", 22, "The Well"),
    (49, "䷰", 29, "Revolution"),
    (50, "䷱", 46, "The Cauldron"),
    (51, "䷲",  9, "Thunder"),
    (52, "䷳", 36, "Keeping Still"),
    (53, "䷴", 52, "Gradual Progress"),
    (54, "䷵", 11, "The Marrying Maiden"),
    (55, "䷶", 13, "Abundance"),
    (56, "䷷", 44, "The Wanderer"),
    (57, "䷸", 54, "The Gentle Wind"),
    (58, "䷹", 27, "The Joyous Lake"),
    (59, "䷺", 50, "Dispersion"),
    (60, "䷻", 19, "Limitation"),
    (61, "䷼", 51, "Inner Truth"),
    (62, "䷽", 12, "Small Excess"),
    (63, "䷾", 21, "After Completion"),
    (64, "䷿", 42, "Before Completion"),
]

# Build binary -> (seq, icon, name) lookup
BINARY_TO_HEX = {}
for seq, icon, binary, name in HEXAGRAM_TABLE:
    if binary not in BINARY_TO_HEX:
        BINARY_TO_HEX[binary] = (seq, icon, name)


# ---------------------------------------------------------------------------
# Hexagram data loading
# ---------------------------------------------------------------------------

def load_hexagrams(regen_dir: Path) -> dict[int, dict]:
    """
    Load all 64 hexagram JSON files from the regen directory.
    Returns a dict keyed by binary_sequence (0-63).
    """
    hexagrams: dict[int, dict] = {}
    for path in sorted(regen_dir.glob("*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            binary = data.get("binary_sequence")
            if binary is not None:
                hexagrams[binary] = data
        except Exception as exc:
            print(f"[warn] Could not load {path.name}: {exc}", file=sys.stderr)
    print(f"Loaded {len(hexagrams)} hexagram JSON files.")
    return hexagrams


def get_hex_name(data: dict) -> str:
    return data.get("name", "")

def get_hex_desc(data: dict) -> str:
    return data.get("description", "")

def get_hex_icon(data: dict) -> str:
    return data.get("hexagram_code", "")

def get_hex_seq(data: dict) -> int | None:
    kw = data.get("king_wen", {})
    return kw.get("sequence") if isinstance(kw, dict) else data.get("id")


# ---------------------------------------------------------------------------
# Input parser — reads JSON from ap_scraper.py
# ---------------------------------------------------------------------------

def parse_headlines(input_path: Path) -> list[dict]:
    """
    Read articles from a JSON file produced by ap_scraper.py.
    Returns list of dicts with 'title' and 'synopsis' keys.
    """
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    # Support both the ap_scraper envelope {"articles": [...]} and a bare list
    raw = data.get("articles", data) if isinstance(data, dict) else data

    articles = []
    for item in raw:
        title   = (item.get("title") or "").strip()
        synopsis = (item.get("synopsis") or item.get("description") or "").strip()
        if title and synopsis and len(title) >= 15 and len(synopsis) >= 20:
            articles.append({"title": title, "synopsis": synopsis, "published": item.get("published", ""), "url": item.get("url", "")})
    return articles


# ---------------------------------------------------------------------------
# Claude API helpers
# ---------------------------------------------------------------------------

def call_claude(
    client: anthropic.Anthropic,
    model: str,
    system: str,
    user: str,
    max_tokens: int = 1024,
    retries: int = 6,
) -> str:
    delay = 5.0
    for attempt in range(retries):
        try:
            msg = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return msg.content[0].text.strip()
        except anthropic.APIStatusError as exc:
            if exc.status_code in (429, 529) and attempt < retries - 1:
                wait = delay * (2 ** attempt)
                print(
                    f"\n    [overloaded/rate-limit, retrying in {wait:.0f}s...]",
                    end=" ",
                    flush=True,
                )
                time.sleep(wait)
            else:
                raise


def match_hexagram(
    client: anthropic.Anthropic,
    model: str,
    title: str,
    synopsis: str,
    hexagrams: dict[int, dict],
) -> int:
    """
    Ask Claude which of the 64 hexagrams best fits this news story.
    Returns binary_sequence (0-63).
    """
    hex_list = "\n".join(
        f"  binary={b}: {d.get('name','?')} — {d.get('description','')[:80]}"
        for b, d in sorted(hexagrams.items())
    )
    system = (
        "You are an expert in the I Ching. "
        "Given a news headline and synopsis, identify the single hexagram "
        "(from 0 to 63 by binary_sequence) whose core meaning, theme, and "
        "dynamic best reflects the essence of this news story. "
        "Reply with ONLY the integer binary_sequence value, nothing else."
    )
    user = (
        f"Headline: {title}\n\n"
        f"Synopsis: {synopsis}\n\n"
        f"Hexagrams:\n{hex_list}\n\n"
        "Which binary_sequence (0-63) best matches? Reply with the integer only."
    )
    raw = call_claude(client, model, system, user, max_tokens=16)
    m = re.search(r"\d+", raw)
    if not m:
        return 0
    val = int(m.group())
    return val if val in hexagrams else 0


def identify_moving_lines(
    client: anthropic.Anthropic,
    model: str,
    title: str,
    synopsis: str,
    hex_data: dict,
) -> list[int]:
    """
    Ask Claude which lines (1-6) are moving lines for this story.
    Returns a list of line numbers (1-indexed).
    """
    # Lines are stored highest position first; sort by position ascending (1=bottom)
    sorted_lines = sorted(hex_data.get("lines", []), key=lambda l: l.get("position", 0))
    lines_desc = "\n".join(
        f"  Line {line.get('position', i+1)} ({line.get('name','?')}): {line.get('meaning','')}"
        for i, line in enumerate(sorted_lines)
    )
    system = (
        "You are an expert in the I Ching. "
        "Given a news story and a hexagram, identify which lines (1-6) are "
        "'moving lines' — lines whose specific meaning is most directly "
        "activated or embodied by the situation described in the news. "
        "A moving line is one where the story's energy or tension specifically "
        "resonates with that line's description. "
        "Reply with ONLY a comma-separated list of line numbers (e.g. '2,4,6'), "
        "or 'none' if no lines are moving."
    )
    user = (
        f"Headline: {title}\n\n"
        f"Synopsis: {synopsis}\n\n"
        f"Hexagram: {hex_data.get('hexagram_name','')}\n"
        f"Lines:\n{lines_desc}\n\n"
        "Which lines are moving? Reply with comma-separated numbers only."
    )
    raw = call_claude(client, model, system, user, max_tokens=32)
    if "none" in raw.lower():
        return []
    nums = re.findall(r"[1-6]", raw)
    return sorted(set(int(n) for n in nums))


def flip_lines(binary_seq: int, moving_lines: list[int]) -> int:
    """
    Flip the specified lines (1-indexed, bottom=1) in the binary sequence.
    Returns the new binary_sequence (0-63).
    """
    result = binary_seq
    for pos in moving_lines:
        result ^= (1 << (pos - 1))
    return result & 0x3F


def rewrite_as_future_past(
    client: anthropic.Anthropic,
    model: str,
    title: str,
    synopsis: str,
    result_hex_data: dict,
    published: str = "",
) -> str:
    """
    Rewrite the story from the perspective of the resulting hexagram,
    as if reporting on events that will happen next week — in past tense,
    as though they already occurred.
    """
    # Compute the dateline date: original publish date + 7 days
    from datetime import timedelta
    future_date = ""
    if published:
        m = re.match(r"(\d{4}-\d{2}-\d{2})", published)
        if m:
            try:
                orig = datetime.strptime(m.group(1), "%Y-%m-%d")
                future = orig + timedelta(days=7)
                future_date = future.strftime("%B %-d, %Y")
            except ValueError:
                pass

    dateline_instruction = (
        f"Use exactly this date in the dateline: {future_date}."
        if future_date else
        "Use a dateline date approximately one week after the original story."
    )

    hex_name = get_hex_name(result_hex_data)
    hex_desc = get_hex_desc(result_hex_data)
    system = (
        "You are a wire service correspondent filing a breaking news dispatch — "
        "tight, fast, and definitive. Think AP style: short sentences, active voice, "
        "concrete facts, no throat-clearing. "
        "Your task: given a current news story, write a 3-paragraph dispatch reporting "
        "what happened ONE WEEK LATER as if it has just occurred. "
        "The story must ADVANCE — something concrete must have changed, been decided, "
        "escalated, or resolved. Do not rehash the original event; report what came NEXT. "
        "The I Ching hexagram provided shapes the nature of that development: "
        "use its core dynamic (conflict, resolution, transformation, etc.) to determine "
        "what kind of outcome occurred. "
        f"Format: start with a dateline (CITY — {future_date or 'Date'}.), "
        f"then 3 tight paragraphs, no headers, no markdown, no bullet points. "
        f"{dateline_instruction} "
        "Total length: 150-200 words maximum. Do not mention the I Ching."
    )
    user = (
        f"Current story headline: {title}\n\n"
        f"Current story synopsis: {synopsis}\n\n"
        f"Guiding hexagram (determines how situation develops): {hex_name} — {hex_desc}\n\n"
        "Write the 3-paragraph wire dispatch reporting what happened one week later."
    )
    return call_claude(client, model, system, user, max_tokens=512)


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def build_article_record(
    article: dict,
    hex_data: dict,
    moving_lines: list[int],
    result_binary: int,
    result_hex_data: dict,
    rewrite: str,
) -> dict:
    title   = article.get("title", "")
    synopsis = article.get("synopsis", "")
    hex_seq  = get_hex_seq(hex_data)
    hex_name = get_hex_name(hex_data)
    hex_icon = get_hex_icon(hex_data)
    hex_desc = get_hex_desc(hex_data)
    hex_binary = hex_data.get("binary_sequence")

    result_info = BINARY_TO_HEX.get(result_binary, (result_binary, "", "Unknown"))
    result_seq, result_icon, result_name = result_info

    # Lines sorted bottom (1) to top (6) by position
    sorted_lines = sorted(hex_data.get("lines", []), key=lambda l: l.get("position", 0))
    lines_out = []
    for line in sorted_lines:
        pos = line.get("position", 0)
        lines_out.append({
            "number": pos,
            "name": line.get("name", f"Line {pos}"),
            "description": line.get("meaning", ""),
            "moving": pos in moving_lines,
        })

    return {
        "original_headline": title,
        "original_synopsis": synopsis,
        "published": article.get("published", ""),
        "url": article.get("url", ""),
        "matched_hexagram": {
            "sequence": hex_seq,
            "binary": hex_binary,
            "icon": hex_icon,
            "name": hex_name,
            "description": hex_desc,
        },
        "lines": lines_out,
        "moving_lines": moving_lines,
        "result_hexagram": {
            "sequence": result_seq,
            "binary": result_binary,
            "icon": result_icon,
            "name": result_name,
            "pairpath": result_hex_data.get("pairpath", {}).get("title", ""),
        },
        "predicted_article": rewrite,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="I Ching news analyzer and future-past rewriter.")
    parser.add_argument(
        "--input", "-i",
        default=DEFAULT_INPUT,
        help=f"Input markdown file with headlines and synopses (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT,
        help=f"Output JSON file (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--model", "-m",
        default=DEFAULT_MODEL,
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=0,
        help="Max number of articles to process (0 = all)",
    )
    parser.add_argument(
        "--regen-dir",
        default=str(REGEN_DIR),
        help="Directory containing hexagram JSON files",
    )
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    regen_dir = Path(args.regen_dir)
    if not regen_dir.is_dir():
        print(f"Error: regen directory not found: {regen_dir}", file=sys.stderr)
        sys.exit(1)

    hexagrams = load_hexagrams(regen_dir)
    if not hexagrams:
        print("Error: no hexagram JSON files loaded.", file=sys.stderr)
        sys.exit(1)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    articles = parse_headlines(input_path)
    print(f"Parsed {len(articles)} articles from {input_path.name}")

    if args.limit > 0:
        articles = articles[: args.limit]
        print(f"Processing first {len(articles)} articles.")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    output = {
        "generated": now,
        "source": input_path.name,
        "model": args.model,
        "articles": [],
    }

    for idx, article in enumerate(articles, start=1):
        title = article["title"]
        synopsis = article["synopsis"]
        print(f"\n[{idx}/{len(articles)}] {title[:70]}")

        print("  → matching hexagram ...", end=" ", flush=True)
        binary = match_hexagram(client, args.model, title, synopsis, hexagrams)
        hex_data = hexagrams.get(binary, {})
        print(f"{get_hex_name(hex_data)} (binary {binary})")

        print("  → identifying moving lines ...", end=" ", flush=True)
        moving_lines = identify_moving_lines(client, args.model, title, synopsis, hex_data)
        print(moving_lines)

        result_binary = flip_lines(binary, moving_lines)

        result_hex_data = hexagrams.get(result_binary, {})
        print(f"  → transforms to: {get_hex_name(result_hex_data)} (binary {result_binary})")

        print("  → rewriting as future-past ...", end=" ", flush=True)
        rewrite = rewrite_as_future_past(
            client, args.model, title, synopsis, result_hex_data,
            published=article.get("published", ""),
        )
        print("done")

        output["articles"].append(
            build_article_record(article, hex_data, moving_lines, result_binary, result_hex_data, rewrite)
        )

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved {len(output['articles'])} articles to {output_path}")


if __name__ == "__main__":
    main()
