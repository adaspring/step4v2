import json
from bs4 import BeautifulSoup
import os

def load_injection_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"⚠️ Warning: {filename} not found. Skipping injection for this section.")
        return []

def inject_code(html_file):
    # Load the translated HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Load injection code or fallback to empty
    head_code = load_injection_file("before_head.json")
    body_code = load_injection_file("before_body.json")

    # Inject into <head>
    if soup.head:
        for code in head_code:
            injected = BeautifulSoup(code, 'html.parser')
            soup.head.append(injected)

    # Inject before </body>
    if soup.body:
        for code in body_code:
            injected = BeautifulSoup(code, 'html.parser')
            soup.body.append(injected)

    # Rewrite internal links (including those with #anchors)
    for tag in soup.find_all(['a', 'form', 'link', 'script', 'img', 'iframe']):
        for attr in ['href', 'src', 'action']:
            if tag.has_attr(attr):
                url = tag[attr]
                if (
                    url.endswith('.html') and
                    not url.startswith(('http://', 'https://', 'ftp://', 'mailto:', 'tel:', '/', '#'))
                ):
                    name, ext = os.path.splitext(url)
                    tag[attr] = f"{name}-fr{ext}"
                elif '.html#' in url and not url.startswith(('http://', 'https://', 'ftp://', 'mailto:', 'tel:', '/', '#')):
                    base, fragment = url.split('#', 1)
                    name, ext = os.path.splitext(base)
                    tag[attr] = f"{name}-fr{ext}#{fragment}"

    # Save with originalname-fr.html
    base_name = os.path.splitext(os.path.basename(html_file))[0]
    if base_name.startswith("translated_output"):
        base_name = "index"
    output_file = f"{base_name}-fr.html"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"✅ Step 4 complete: injected code and updated internal links. Saved as {output_file}.")

# Run if script is executed directly
if __name__ == "__main__":
    inject_code("translated_output.html")
