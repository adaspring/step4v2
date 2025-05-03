import json
from bs4 import BeautifulSoup

TRANSLATABLE_ATTRS = {
    "alt", "title", "placeholder", "aria-label", "aria-placeholder", "value"
}

SEO_META_FIELDS = {
    "name": {"description", "keywords"},
    "property": {
        "og:title", "og:description",
        "twitter:title", "twitter:description"
    }
}

def merge_translations(html_file="non_translatable.html", json_file="translated.json", output_file="translated_output.html"):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    with open(json_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    # 1. Replace text nodes
    for text_node in soup.find_all(string=True):
        if text_node in translations:
            text_node.replace_with(translations[text_node])

    # 2. Replace attributes
    for tag in soup.find_all():
        for attr in TRANSLATABLE_ATTRS:
            if attr in tag.attrs:
                val = tag[attr]
                if val in translations:
                    tag[attr] = translations[val]

    # 3. Replace meta tag content
    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower()
        prop = meta.get("property", "").lower()
        content = meta.get("content", "")
        if content in translations and (
            name in SEO_META_FIELDS["name"] or prop in SEO_META_FIELDS["property"]
        ):
            meta["content"] = translations[content]

    # 4. Replace <title> tag
    if soup.title and soup.title.string and soup.title.string in translations:
        soup.title.string.replace_with(translations[soup.title.string])

    # Save output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print("✅ Step 3 complete: All translations merged into translated_output.html.")

if __name__ == "__main__":
    merge_translations()
