#!/usr/bin/env python3
"""
Next Week's News — HTML generator.

Reads next_weeks_news.json (produced by iching_news.py) and generates
a single-file HTML news site: next_weeks_news.html

Usage:
    ./build_site.py
    ./build_site.py --input next_weeks_news.json --output next_weeks_news.html
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_INPUT  = "next_weeks_news.json"
DEFAULT_OUTPUT = "next_weeks_news.html"

# ---------------------------------------------------------------------------
# Image generation (OpenAI DALL-E 3)
# ---------------------------------------------------------------------------

def generate_featured_image(article: dict) -> str:
    """
    Generate a photojournalistic image for the predicted article using DALL-E 3.
    Returns a data URI string ("data:image/png;base64,...") or "" on failure.
    """
    try:
        import openai
    except ImportError:
        print("openai package not installed — skipping image generation", file=sys.stderr)
        return ""

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("OPENAI_API_KEY not set — skipping image generation", file=sys.stderr)
        return ""

    predicted  = article.get("predicted_article", "")
    headline   = article.get("original_headline", "")
    result_hex = article.get("result_hexagram", {})
    pairpath   = result_hex.get("pairpath", "") or result_hex.get("name", "")

    # Build a concise, descriptive prompt — no text/words in the image
    summary = predicted[:400].replace("\n", " ").strip()
    prompt = (
        f"Photojournalistic editorial photograph for a news story: {headline}. "
        f"One week later: {summary}. "
        f"Theme: {pairpath}. "
        "Realistic, dramatic lighting, no text, no words, no logos. "
        "Wide cinematic composition, high detail."
    )

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1792x1024",
            response_format="url",
        )
        image_url = response.data[0].url
        print(f"  Image generated — fetching from URL …")
        with urllib.request.urlopen(image_url) as resp:
            raw = resp.read()
        b64 = base64.b64encode(raw).decode("ascii")
        return f"data:image/png;base64,{b64}"
    except Exception as exc:
        print(f"  Image generation failed: {exc}", file=sys.stderr)
        return ""


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def esc(text: str) -> str:
    """HTML-escape a string."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def article_paragraphs(text: str) -> str:
    """Convert plain text with blank-line paragraph breaks to <p> tags."""
    paras = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    return "\n".join(f"<p>{esc(p)}</p>" for p in paras)


# ---------------------------------------------------------------------------
# Card rendering
# ---------------------------------------------------------------------------

def render_card(article: dict, index: int, image_uri: str = "") -> str:
    headline   = esc(article.get("original_headline", ""))
    synopsis   = esc(article.get("original_synopsis", ""))
    result_hex = article.get("result_hexagram", {})
    pairpath   = esc(result_hex.get("pairpath", "") or result_hex.get("name", ""))
    published  = esc(article.get("published", ""))
    url        = article.get("url", "#")

    modal_id = f"modal-{index}"

    # Featured (index 0) with image: two-column layout
    if index == 0 and image_uri:
        return f"""
    <article class="card featured-image-card">
      <img class="featured-img" src="{image_uri}" alt="Featured story image" />
      <div class="featured-text">
        <div class="card-meta">
          <a class="today-tag" href="{esc(url)}" target="_blank" rel="noopener">Today &#8599;</a>
          <span class="region-tag">{pairpath}</span>
        </div>
        <h2 class="card-headline">{headline}</h2>
        <p class="card-synopsis">{synopsis}</p>
        <div class="card-footer">
          <span class="dateline">{published}</span>
          <button class="read-more-btn" onclick="openModal('{modal_id}')">
            Next Week&#8217;s News <span class="arrow">&#8594;</span>
          </button>
        </div>
      </div>
    </article>"""

    return f"""
    <article class="card">
      <div class="card-meta">
        <a class="today-tag" href="{esc(url)}" target="_blank" rel="noopener">Today &#8599;</a>
        <span class="region-tag">{pairpath}</span>
      </div>
      <h2 class="card-headline">{headline}</h2>
      <p class="card-synopsis">{synopsis}</p>
      <div class="card-footer">
        <span class="dateline">{published}</span>
        <button class="read-more-btn" onclick="openModal('{modal_id}')">
          Next Week&#8217;s News <span class="arrow">&#8594;</span>
        </button>
      </div>
    </article>"""


def render_modal(article: dict, index: int) -> str:
    headline   = esc(article.get("original_headline", ""))
    synopsis   = esc(article.get("original_synopsis", ""))
    published  = esc(article.get("published", ""))
    url        = article.get("url", "")
    result_hex = article.get("result_hexagram", {})
    pairpath   = esc(result_hex.get("pairpath", "") or result_hex.get("name", ""))
    predicted  = article.get("predicted_article", "")

    body_html  = article_paragraphs(predicted)
    modal_id   = f"modal-{index}"

    source_link = (
        f'<a class="modal-source-link" href="{esc(url)}" target="_blank" rel="noopener">'
        f'Read original AP story &#8599;</a>'
    ) if url else ""

    return f"""
  <div class="modal-overlay" id="{modal_id}" onclick="closeModalIfBackground(event, '{modal_id}')">
    <div class="modal">
      <button class="modal-close" onclick="closeModal('{modal_id}')">&times;</button>

      <!-- Original story blurb -->
      <div class="modal-original-block">
        <div class="modal-original-label">&#128197; Original AP Story &mdash; {published}</div>
        <p class="modal-original-synopsis">{synopsis}</p>
        {source_link}
      </div>

      <div class="modal-divider"></div>

      <!-- Predicted article -->
      <div class="modal-tag">{pairpath}</div>
      <h2 class="modal-headline">{headline}</h2>
      <div class="modal-body">
        {body_html}
      </div>
    </div>
  </div>"""


# ---------------------------------------------------------------------------
# Full page
# ---------------------------------------------------------------------------

def build_html(data: dict, featured_image_uri: str = "") -> str:
    articles = data.get("articles", [])
    generated = data.get("generated", "")
    source = data.get("source", "")

    # Split into featured (first) + secondary grid
    featured_html = ""
    grid_html = ""
    modals_html = ""

    if articles:
        featured_html = render_card(articles[0], 0, image_uri=featured_image_uri)
        modals_html  += render_modal(articles[0], 0)

        secondary = articles[1:]
        grid_cards = "\n".join(render_card(a, i + 1) for i, a in enumerate(secondary))
        grid_html  = f'<div class="grid">{grid_cards}</div>'
        for i, a in enumerate(secondary):
            modals_html += render_modal(a, i + 1)

    now_utc = datetime.now(timezone.utc).strftime("%A, %B %-d, %Y")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Next Week's News</title>
  <style>
    /* ── Reset & Base ── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --ink:        #0d0d0d;
      --ink-light:  #444;
      --ink-faint:  #888;
      --rule:       #d6d0c4;
      --bg:         #f7f4ee;
      --bg-card:    #ffffff;
      --accent:     #b5000b;
      --accent-dim: #7a0008;
      --tag-bg:     #f0ece3;
      --sans: "Inter", "Helvetica Neue", Arial, sans-serif;
      --serif: "Georgia", "Times New Roman", serif;
    }}

    body {{
      font-family: var(--sans);
      background: var(--bg);
      color: var(--ink);
      line-height: 1.6;
      min-height: 100vh;
    }}

    /* ── Masthead ── */
    .masthead {{
      background: var(--ink);
      color: #fff;
      padding: 0 2rem;
    }}
    .masthead-inner {{
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 1rem 0 0.8rem;
      border-bottom: 3px solid var(--accent);
    }}
    .masthead-title {{
      font-family: var(--serif);
      font-size: clamp(1.8rem, 4vw, 3rem);
      font-weight: 700;
      letter-spacing: -0.02em;
      line-height: 1;
    }}
    .masthead-title span {{
      color: var(--accent);
    }}
    .masthead-right {{
      text-align: right;
    }}
    .masthead-date {{
      font-size: 0.78rem;
      color: #bbb;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}
    .masthead-tagline {{
      font-size: 0.72rem;
      color: #888;
      font-style: italic;
      margin-top: 0.2rem;
    }}

    /* ── Nav bar ── */
    .navbar {{
      background: #1a1a1a;
      border-bottom: 1px solid #333;
    }}
    .navbar-inner {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 0 2rem;
      display: flex;
      gap: 0;
      overflow-x: auto;
    }}
    .navbar a {{
      color: #ccc;
      text-decoration: none;
      font-size: 0.78rem;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 0.65rem 1.1rem;
      display: block;
      white-space: nowrap;
      border-bottom: 2px solid transparent;
      transition: color .15s, border-color .15s;
    }}
    .navbar a:hover, .navbar a.active {{
      color: #fff;
      border-bottom-color: var(--accent);
    }}

    /* ── Layout wrapper ── */
    .page-wrap {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 2rem 2rem 4rem;
    }}

    /* ── Section label ── */
    .section-label {{
      font-size: 0.68rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--ink-faint);
      font-weight: 600;
      border-top: 2px solid var(--ink);
      padding-top: 0.4rem;
      margin-bottom: 1.2rem;
    }}

    /* ── Featured card ── */
    .featured-wrap {{
      margin-bottom: 2.5rem;
    }}
    .featured-wrap .card {{
      background: var(--bg-card);
      border: 1px solid var(--rule);
      border-left: 4px solid var(--accent);
      padding: 2rem 2.2rem;
      display: grid;
      grid-template-rows: auto;
    }}
    /* Featured card with image: image left, text right */
    .featured-wrap .featured-image-card {{
      padding: 0;
      display: grid;
      grid-template-columns: 420px 1fr;
      grid-template-rows: auto;
      overflow: hidden;
    }}
    .featured-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .featured-text {{
      padding: 2rem 2.2rem;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    @media (max-width: 768px) {{
      .featured-wrap .featured-image-card {{
        grid-template-columns: 1fr;
      }}
      .featured-img {{
        height: 240px;
      }}
    }}
    .featured-wrap .card-headline {{
      font-family: var(--serif);
      font-size: clamp(1.4rem, 3vw, 2.2rem);
      font-weight: 700;
      line-height: 1.2;
      margin-bottom: 0.9rem;
      color: var(--ink);
    }}
    .featured-wrap .card-synopsis {{
      font-size: 1.05rem;
      color: var(--ink-light);
      line-height: 1.65;
      max-width: 72ch;
      margin-bottom: 1.2rem;
    }}

    /* ── Grid ── */
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.5rem;
    }}

    /* ── Standard card ── */
    .card {{
      background: var(--bg-card);
      border: 1px solid var(--rule);
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
    }}
    .card:hover {{
      box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }}
    .card-meta {{
      margin-bottom: 0.55rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .today-tag {{
      font-size: 0.64rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      font-weight: 700;
      color: #fff;
      background: #1a6b2e;
      padding: 0.18rem 0.5rem;
      border-radius: 2px;
      text-decoration: none;
      transition: background .15s;
    }}
    .today-tag:hover {{ background: #145424; }}
    .modal-original-block {{
      background: #f5f9f6;
      border-left: 3px solid #1a6b2e;
      padding: 1rem 1.2rem;
      margin-bottom: 0;
    }}
    .modal-original-label {{
      font-size: 0.68rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      font-weight: 700;
      color: #1a6b2e;
      margin-bottom: 0.5rem;
    }}
    .modal-original-synopsis {{
      font-family: var(--serif);
      font-size: 0.95rem;
      line-height: 1.65;
      color: var(--ink-light);
      margin-bottom: 0.7rem;
    }}
    .modal-divider {{
      border: none;
      border-top: 2px solid var(--rule);
      margin: 1.5rem 0;
    }}
    .modal-published {{
      font-size: 0.78rem;
      color: var(--ink-faint);
      font-style: italic;
      margin-bottom: 1.2rem;
    }}
    .modal-source-link {{
      display: inline-block;
      color: #1a6b2e;
      font-size: 0.78rem;
      font-weight: 600;
      text-decoration: none;
      border-bottom: 1px solid currentColor;
    }}
    .modal-source-link:hover {{ color: #145424; }}
    .region-tag {{
      font-size: 0.68rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      font-weight: 600;
      color: var(--accent);
      background: var(--tag-bg);
      padding: 0.2rem 0.55rem;
      border-radius: 2px;
    }}
    .card-headline {{
      font-family: var(--serif);
      font-size: 1.15rem;
      font-weight: 700;
      line-height: 1.3;
      margin-bottom: 0.65rem;
      color: var(--ink);
    }}
    .card-synopsis {{
      font-size: 0.88rem;
      color: var(--ink-light);
      line-height: 1.6;
      flex: 1;
      margin-bottom: 1.1rem;
      display: -webkit-box;
      -webkit-line-clamp: 4;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--rule);
      padding-top: 0.8rem;
      margin-top: auto;
    }}
    .dateline {{
      font-size: 0.72rem;
      color: var(--ink-faint);
      font-style: italic;
      max-width: 60%;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .read-more-btn {{
      background: var(--accent);
      color: #fff;
      border: none;
      padding: 0.45rem 0.9rem;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.04em;
      cursor: pointer;
      border-radius: 2px;
      white-space: nowrap;
      transition: background .15s;
    }}
    .read-more-btn:hover {{ background: var(--accent-dim); }}
    .read-more-btn .arrow {{ margin-left: 0.3rem; }}

    /* ── Modal ── */
    .modal-overlay {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.6);
      z-index: 1000;
      overflow-y: auto;
      padding: 2rem 1rem;
    }}
    .modal-overlay.open {{ display: flex; align-items: flex-start; justify-content: center; }}
    .modal {{
      background: var(--bg-card);
      max-width: 720px;
      width: 100%;
      margin: auto;
      padding: 2.5rem 3rem;
      position: relative;
      border-top: 4px solid var(--accent);
    }}
    .modal-close {{
      position: absolute;
      top: 1rem; right: 1.2rem;
      background: none;
      border: none;
      font-size: 1.8rem;
      cursor: pointer;
      color: var(--ink-faint);
      line-height: 1;
    }}
    .modal-close:hover {{ color: var(--ink); }}
    .modal-tag {{
      font-size: 0.68rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--accent);
      font-weight: 700;
      margin-bottom: 0.9rem;
    }}
    .modal-headline {{
      font-family: var(--serif);
      font-size: clamp(1.3rem, 3vw, 1.8rem);
      font-weight: 700;
      line-height: 1.25;
      margin-bottom: 1.5rem;
      color: var(--ink);
    }}
    .modal-body p {{
      font-family: var(--serif);
      font-size: 1.05rem;
      line-height: 1.8;
      color: #222;
      margin-bottom: 1.1rem;
      max-width: 66ch;
    }}

    /* ── Footer ── */
    .site-footer {{
      background: var(--ink);
      color: #888;
      text-align: center;
      padding: 1.5rem 2rem;
      font-size: 0.75rem;
      letter-spacing: 0.04em;
    }}
    .site-footer strong {{ color: #ccc; }}

    /* ── Divider ── */
    .section-divider {{
      border: none;
      border-top: 1px solid var(--rule);
      margin: 2rem 0;
    }}

    /* ── Responsive ── */
    @media (max-width: 640px) {{
      .masthead-inner {{ flex-direction: column; align-items: flex-start; gap: 0.5rem; }}
      .masthead-right {{ text-align: left; }}
      .page-wrap {{ padding: 1.2rem 1rem 3rem; }}
      .modal {{ padding: 1.8rem 1.5rem; }}
    }}
  </style>
</head>
<body>

  <!-- Masthead -->
  <header class="masthead">
    <div class="masthead-inner">
      <div class="masthead-title">Next Week's<span> News</span></div>
      <div class="masthead-right">
        <div class="masthead-date">{now_utc}</div>
        <div class="masthead-tagline">Predictive journalism &mdash; tomorrow&#8217;s headlines, today</div>
      </div>
    </div>
  </header>

  <!-- Nav -->
  <nav class="navbar">
    <div class="navbar-inner">
      <a href="#" class="active">Top Stories</a>
      <a href="#">World</a>
      <a href="#">Politics</a>
      <a href="#">Economy</a>
      <a href="#">Science</a>
      <a href="#">Conflict</a>
    </div>
  </nav>

  <!-- Main content -->
  <main class="page-wrap">

    <!-- Featured story -->
    <section class="featured-wrap">
      <div class="section-label">Lead Story</div>
      {featured_html}
    </section>

    <hr class="section-divider" />

    <!-- Story grid -->
    <section>
      <div class="section-label">More Stories</div>
      {grid_html}
    </section>

  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <strong>Next Week&#8217;s News</strong> &nbsp;&bull;&nbsp;
    Generated {generated} &nbsp;&bull;&nbsp;
    Source: {esc(source)} &nbsp;&bull;&nbsp;
    Predictive analysis via pattern recognition
  </footer>

  <!-- Modals (at body level, outside all cards) -->
  {modals_html}

  <script>
    function openModal(id) {{
      document.getElementById(id).classList.add('open');
      document.body.style.overflow = 'hidden';
    }}
    function closeModal(id) {{
      document.getElementById(id).classList.remove('open');
      document.body.style.overflow = '';
    }}
    function closeModalIfBackground(event, id) {{
      if (event.target === event.currentTarget) closeModal(id);
    }}
    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') {{
        document.querySelectorAll('.modal-overlay.open').forEach(function(el) {{
          el.classList.remove('open');
        }});
        document.body.style.overflow = '';
      }}
    }});
  </script>

</body>
</html>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build Next Week's News HTML site from JSON analysis file."
    )
    parser.add_argument(
        "--input", "-i",
        default=DEFAULT_INPUT,
        help=f"Input JSON file (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT,
        help=f"Output HTML file (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--no-image",
        action="store_true",
        help="Skip DALL-E image generation for the featured story",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    n = len(data.get("articles", []))
    print(f"Building site from {n} articles in {input_path.name} …")

    featured_image_uri = ""
    articles = data.get("articles", [])
    if articles and not args.no_image:
        print("Generating featured image via DALL-E 3 …")
        featured_image_uri = generate_featured_image(articles[0])
        if featured_image_uri:
            print("  Image embedded successfully.")
        else:
            print("  No image — continuing without it.")

    html = build_html(data, featured_image_uri=featured_image_uri)

    output_path = Path(args.output)
    output_path.write_text(html, encoding="utf-8")
    print(f"Saved → {output_path}  ({output_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
