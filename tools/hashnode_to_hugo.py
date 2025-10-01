#!/usr/bin/env python3
"""
Convert a Hashnode JSON export into Hugo Markdown posts and local images.

Usage:
  python tools/hashnode_to_hugo.py /path/to/hashnode.json --download-images [--draft]

Output:
  content/posts/<slug>.md
  static/images/hashnode/<slug>/<downloaded-files>

Notes:
- Requires: requests (mandatory), markdownify (optional; only if your export stores HTML)
- Safe to re-run; will overwrite existing .md files for the same slug.
"""

import argparse
import json
import os
import pathlib
import re
import sys
import urllib.parse
from typing import Any, Dict, List, Optional

# ---------- Optional HTML -> MD ----------
try:
    from markdownify import markdownify as html_to_md
except Exception:
    html_to_md = None

# ---------- Required HTTP ----------
try:
    import requests
except Exception:
    print("This script requires 'requests'. Install with:", file=sys.stderr)
    print("  pip install requests markdownify", file=sys.stderr)
    sys.exit(1)

# ---------- Paths ----------
ROOT = pathlib.Path(__file__).resolve().parents[1]  # repo root (assumes tools/ folder)
CONTENT_DIR = ROOT / "content" / "posts"
STATIC_DIR = ROOT / "static" / "images" / "hashnode"

# ---------- Regex helpers ----------
# Normalize smart quotes before other processing
SMARTS = (
    ('“', '"'), ('”', '"'), ('’', "'"),
    ('\u00A0', ' '),  # non-breaking space
)

# Image pattern:
#   ![alt](URL [junk like align="center"])
# Capture URL as the first non-space token; ignore the rest inside (...) parentheses.
IMG_MD = re.compile(r'!\[([^\]]*)\]\((\S+?)(?:\s+[^)]*)?\)')

# Strip triple-backtick code blocks for excerpt building
FENCE = re.compile(r'```.*?```', flags=re.S)
INLINE_CODE = re.compile(r'`[^`]+`')
MD_IMG = re.compile(r'!\[[^\]]*\]\([^)]+\)')
MD_LINK = re.compile(r'\[([^\]]*)\]\([^)]+\)')


# ---------- Utilities ----------
def norm_smart_quotes(text: str) -> str:
    for a, b in SMARTS:
        text = text.replace(a, b)
    return text


def slugify(s: str) -> str:
    s = norm_smart_quotes(s or "").strip().lower()
    s = re.sub(r'[^a-z0-9\-_\s]+', '', s)
    s = re.sub(r'[\s]+', '-', s)
    s = re.sub(r'-{2,}', '-', s).strip('-')
    return s or "post"


def to_iso(dt: Any) -> str:
    """Normalize common Hashnode date shapes (ISO, epoch ms/s) to RFC3339-ish."""
    import datetime
    if dt is None:
        return datetime.datetime.now(datetime.timezone.utc).isoformat()
    if isinstance(dt, (int, float)):
        # epoch ms if too large
        if dt > 10_000_000_000:
            dt = dt / 1000.0
        return datetime.datetime.utcfromtimestamp(dt).replace(tzinfo=datetime.timezone.utc).isoformat()
    if isinstance(dt, str):
        try:
            return datetime.datetime.fromisoformat(dt.replace('Z', '+00:00')).astimezone(datetime.timezone.utc).isoformat()
        except Exception:
            pass
    # fallback now
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def is_url(x: str) -> bool:
    try:
        u = urllib.parse.urlparse(x)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except Exception:
        return False


def unique_path(base: pathlib.Path) -> pathlib.Path:
    """Return a non-colliding path by appending -1, -2, ... if needed."""
    if not base.exists():
        return base
    stem, ext = base.stem, base.suffix
    i = 1
    while True:
        cand = base.with_name(f"{stem}-{i}{ext}")
        if not cand.exists():
            return cand
        i += 1


def download_image(url: str, outdir: pathlib.Path) -> Optional[str]:
    """Download url into outdir. Return site-relative path '/static/..' style for Markdown."""
    try:
        outdir.mkdir(parents=True, exist_ok=True)
        parsed = urllib.parse.urlparse(url)
        name = os.path.basename(parsed.path) or "image"
        # Strip querystring
        name = name.split("?")[0]
        # Default extension if none
        if "." not in name:
            name += ".jpg"
        local = unique_path(outdir / name)
        r = requests.get(url, timeout=25)
        r.raise_for_status()
        local.write_bytes(r.content)
        # Return site path (what goes in Markdown)
        site_path = "/" + str(local.relative_to(ROOT)).replace(os.sep, "/")
        return site_path
    except Exception as e:
        print(f"warn: failed to download {url}: {e}", file=sys.stderr)
        return None


def rewrite_images(md: str, slug: str, enable_downloads: bool) -> (str, Optional[str]):
    """Rewrite Markdown images:
       - normalize smart quotes
       - strip Hashnode's 'align="center"' junk
       - optionally download and replace with local paths
       - return (new_markdown, first_image_path_for_cover)
    """
    md = norm_smart_quotes(md)
    first_local = None
    outdir = STATIC_DIR / slug

    def repl(m: re.Match) -> str:
        nonlocal first_local
        alt, url = m.group(1), m.group(2)
        # If URL contains a closing parenthesis from bad formatting, trim it
        url = url.rstrip(')')

        if enable_downloads and is_url(url):
            local = download_image(url, outdir)
            if local and not first_local:
                first_local = local
            return f"![{alt}]({local or url})"
        # No download: keep cleaned URL only
        return f"![{alt}]({url})"

    new_md = IMG_MD.sub(repl, md)
    return new_md, first_local


def extract_posts(obj: Any) -> List[Dict[str, Any]]:
    """Find an array of posts in several common Hashnode export shapes."""
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for key in ("posts", "articles", "stories"):
            v = obj.get(key)
            if isinstance(v, list):
                return v
        # GraphQL-ish nesting
        data = obj.get("data") if isinstance(obj.get("data"), dict) else obj
        pub = (((data or {}).get("user") or {}).get("publication") or {})
        if isinstance(pub.get("posts"), list):
            return pub["posts"]
    raise ValueError("Could not find a list of posts in the provided JSON.")


def pick_content(p: Dict[str, Any]) -> str:
    # Prefer Markdown
    for k in ("contentMarkdown", "contentMd", "markdown", "bodyMarkdown"):
        v = p.get(k)
        if isinstance(v, str) and v.strip():
            return v
    # Fall back to HTML
    html = p.get("content") or p.get("bodyHtml") or ""
    if html and html_to_md:
        try:
            return html_to_md(html, heading_style="ATX") or ""
        except Exception:
            return html
    return html or ""


def pick_title(p: Dict[str, Any]) -> str:
    for k in ("title", "name", "headline"):
        if p.get(k):
            return str(p[k])
    return "Untitled"


def pick_description(p: Dict[str, Any]) -> Optional[str]:
    for k in ("brief", "subtitle", "excerpt", "description"):
        v = p.get(k)
        if isinstance(v, str) and v.strip():
            return norm_smart_quotes(v.strip())
    # derive from body
    txt = pick_content(p)
    txt = FENCE.sub("", txt)
    txt = INLINE_CODE.sub("", txt)
    txt = MD_IMG.sub("", txt)
    txt = MD_LINK.sub(r"\1", txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt[:160] if txt else None


def pick_tags(p: Dict[str, Any]) -> List[str]:
    v = p.get("tags") or p.get("tagList") or []
    if isinstance(v, list):
        out = []
        for t in v:
            if isinstance(t, str):
                out.append(t)
            elif isinstance(t, dict) and t.get("name"):
                out.append(str(t["name"]))
        return out
    if isinstance(v, str):
        return [x.strip() for x in v.split(",") if x.strip()]
    return []


def write_post(md_path: pathlib.Path, title: str, date_iso: str, draft: bool,
               desc: Optional[str], tags: List[str], slug: str, cover: Optional[str], body_md: str):
    md_path.parent.mkdir(parents=True, exist_ok=True)
    safe_title = title.replace('"', '\\"')
    body_md = body_md.rstrip() + "\n"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f'title: "{safe_title}"\n')
        f.write(f"date: {date_iso}\n")
        f.write(f"draft: {'true' if draft else 'false'}\n")
        if desc:
            safe_desc = desc.replace('"', '\\"')
            f.write(f'description: "{safe_desc}"\n')
        if tags:
            f.write("tags:\n")
            for t in tags:
                f.write(f"  - {t}\n")
        f.write(f"slug: {slug}\n")
        if cover:
            f.write(f'cover: "{cover}"\n')
        f.write("---\n\n")
        f.write(body_md)


def main():
    ap = argparse.ArgumentParser(description="Convert Hashnode JSON export -> Hugo Markdown with local images.")
    ap.add_argument("json_file", help="Path to Hashnode export JSON")
    ap.add_argument("--download-images", action="store_true", help="Download images to static/images/hashnode/<slug>/ and rewrite links")
    ap.add_argument("--draft", action="store_true", help="Mark imported posts as draft")
    args = ap.parse_args()

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

    data = json.load(open(args.json_file, "r", encoding="utf-8"))
    posts = extract_posts(data)

    written = 0
    for p in posts:
        title = pick_title(p)
        slug = slugify(p.get("slug") or p.get("slugifiedTitle") or title)
        date_iso = to_iso(p.get("publishedAt") or p.get("dateAdded") or p.get("createdAt"))

        tags = pick_tags(p)
        body = pick_content(p)
        body = norm_smart_quotes(body)

        # Rewrites images and optionally downloads them
        body, first_local = rewrite_images(body, slug, enable_downloads=args.download_images)

        # Cover: prefer explicit cover field; otherwise first image we downloaded
        cover_field = p.get("coverImage") or p.get("coverImageUrl") or p.get("cover")
        cover = first_local or (cover_field if isinstance(cover_field, str) and not args.download_images else None)

        desc = pick_description(p)

        out_md = CONTENT_DIR / f"{slug}.md"
        write_post(out_md, title, date_iso, args.draft, desc, tags, slug, cover, body)
        written += 1
        print(f"wrote: {out_md}")

    print(f"✅ Done. Wrote {written} posts to {CONTENT_DIR}")
    if args.download_images:
        print(f"   Images saved under {STATIC_DIR}/<slug>/")

if __name__ == "__main__":
    main()
