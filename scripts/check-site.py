"""Check generated pages for missing local links and assets (standard library only)."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys

root = Path(__file__).resolve().parents[1] / '_site'
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])
        for key in ('href', 'src', 'poster'):
            if key in attrs: self.links.append(attrs[key])

pages = {}
for page in root.rglob('*.html'):
    parsed = Links(); parsed.feed(page.read_text()); pages[page] = parsed
if not pages: sys.exit('No rendered pages found')
errors = []
for page, parsed in pages.items():
    for link in parsed.links:
        url = urlsplit(link)
        if url.scheme or url.netloc: continue
        path = unquote(url.path)
        target = (root / path.lstrip('/') if path.startswith('/') else page.parent / path).resolve() if path else page
        if target.is_dir(): target /= 'index.html'
        if not target.exists(): errors.append(f'{page.relative_to(root)}: missing {link}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{page.relative_to(root)}: missing anchor {link}')
if errors: sys.exit('\n'.join(sorted(set(errors))))
print(f'Checked links, assets and anchors in {len(pages)} rendered pages.')
