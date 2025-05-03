import os
import json
import uuid
from bs4 import BeautifulSoup, Comment

# Tags containing visible text that should be translated
TRANSLATABLE_TAGS = {
    "p", "span", "div", "h1", "h2", "h3", "h4", "h5", "h6",
    "label", "button", "li", "td", "th", "a", "strong", "em",
    "b", "i", "caption", "summary", "figcaption", "option", "optgroup"
}

# Attributes that contain translatable UI text
TRANSLATABLE_ATTRS = {
    "alt", "title", "placeholder", "aria-label", "aria-placeholder", "value"
}

# SEO-related meta tags to translate (name or property)
SEO_META_FIELDS = {
    "name": {"description", "keywords"},
    "property": {
        "og:title", "og:description",
        "twitter:title", "twitter:description"
    }
}

# Tags we explicitly skip (technical or non-visible)
SKIP_PARENTS = {
    "script", "style", "code", "pre", "noscript", "template", "svg", "canvas"
}

def is_translatable_text(tag):
    return (
        tag.parent.name in TRANSLATABLE_TAGS and
        tag.parent.name not in SKIP_PARENTS and
        not isinstance(tag, Comment) and
        tag.strip()
    )

def generate_token():
    return f"__TRANS_{uuid.uuid4().hex}__"

def extract_translatable_html(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    translatable_map = {}

    # 1. Extract visible text nodes
    for element in soup.find_all(string=True):
        if is_translatable_text(element):
            token = generate_token()
            translatable_map[token] = element.strip()
            element.replace_with(token)

    # 2. Extract translatable attributes
    for tag in soup.find_all():
        for attr in TRANSLATABLE_ATTRS:
            if attr in tag.attrs and isinstance(tag[attr], str):
                value = tag[attr].strip()
                if value:
                    token = generate_token()
                    translatable_map[token] = value
                    tag[attr] = token

    # 3. Extract SEO meta tags
    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower()
        prop = meta.get("property", "").lower()
        content = meta.get("content", "").strip()
        if content:
            if name in SEO_META_FIELDS["name"] or prop in SEO_META_FIELDS["property"]:
                token = generate_token()
                translatable_map[token] = content
                meta["content"] = token

    # 4. Extract <title> content
    title_tag = soup.title
    if title_tag and title_tag.string and title_tag.string.strip():
        token = generate_token()
        translatable_map[token] = title_tag.string.strip()
        title_tag.string.replace_with(token)

    # Save outputs
    with open("translatable.json", "w", encoding="utf-8") as f:
        json.dump(translatable_map, f, indent=2, ensure_ascii=False)

    with open("non_translatable.html", "w", encoding="utf-8") as f:
        f.write(str(soup))

    print("✅ Step 1 complete: generated translatable.json and non_translatable.html.")

import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python translate_extract_step1.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    extract_translatable_html(input_file)
