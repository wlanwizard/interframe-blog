#!/usr/bin/env python3
import re, pathlib

POSTS = pathlib.Path("content/posts")

# matches <img ...> tags and captures src + alt (if present)
IMG = re.compile(
    r'<img\b([^>]*?)>', re.IGNORECASE | re.DOTALL
)

def get_attr(attrs, name):
    m = re.search(rf'\b{name}\s*=\s*"(.*?)"', attrs, re.IGNORECASE)
    if m: return m.group(1)
    m = re.search(rf'\b{name}\s*=\s*\'(.*?)\'', attrs, re.IGNORECASE)
    if m: return m.group(1)
    m = re.search(rf'\b{name}\s*=\s*([^\s">]+)', attrs, re.IGNORECASE)  # unquoted
    if m: return m.group(1)
    return None

def repl(m):
    attrs = m.group(1)
    src = get_attr(attrs, "src")
    alt = get_attr(attrs, "alt") or ""
    if not src:
        return m.group(0)  # keep original if no src
    # Normalize src that might have been unquoted and/or relative
    src = src.strip()
    # Ensure site-root path stays as-is. (Hugo serves /images/... from static/)
    return f'![{alt}]({src})'

def process(md_path):
    text = md_path.read_text(encoding="utf-8")
    new = IMG.sub(repl, text)
    if new != text:
        md_path.write_text(new, encoding="utf-8")
        print(f"updated: {md_path}")

def main():
    for p in POSTS.glob("*.md"):
        process(p)

if __name__ == "__main__":
    main()
