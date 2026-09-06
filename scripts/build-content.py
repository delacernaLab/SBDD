"""Validate editable Markdown records and generate Quarto includes before rendering."""
from pathlib import Path
from datetime import date
import html
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_generated'

def records(kind):
    result = []
    for path in sorted((ROOT / 'content' / kind).glob('*.md')):
        try:
            _, header, body = path.read_text(encoding='utf-8').split('---', 2)
            item = yaml.safe_load(header)
            if not isinstance(item, dict):
                raise ValueError('metadata must be a mapping')
            if item.get('draft', False):
                continue
            if not body.strip():
                raise ValueError('body cannot be empty')
            if not isinstance(item.get('categories', []), list):
                raise ValueError('categories must be a list')
            item['categories'] = list(dict.fromkeys(str(t).strip() for t in item.get('categories', [])))
            if kind == 'news':
                if not item.get('title'): raise ValueError('title is required')
                item['date'] = date.fromisoformat(str(item['date']))
            else:
                item['year'] = int(item['year'])
                item['order'] = int(item['order'])
            if item.get('image'):
                image = (ROOT / item['image'].lstrip('/')).resolve()
                if not image.is_relative_to(ROOT) or not image.is_file():
                    raise ValueError(f"image does not exist: {item['image']}")
            item.update(body=body.strip(), slug=path.stem)
            result.append(item)
        except Exception as error:
            raise ValueError(f'{path.relative_to(ROOT)}: {error}') from error
    if kind == 'publications' and len({i['order'] for i in result}) != len(result):
        raise ValueError('Publication order values must be unique')
    return sorted(result, key=lambda i: (i['date'], i['slug']) if kind == 'news' else (i['year'], i['order']), reverse=True)

def attr(value):
    return html.escape(str(value), quote=True)

def tags(items):
    return ' '.join(f'[{t}]{{.tag}}' for t in items)

def picture(item, cls):
    if not item.get('image'): return ''
    alt = item.get('image_alt', item.get('title', 'Publication illustration')).replace('"', '&quot;')
    return f'![]({item["image"]}){{.{cls} fig-alt="{alt}" loading="lazy"}}\n\n'

def generate():
    news, pubs = records('news'), records('publications')
    timeline = []
    for item in news:
        stamp = item.get('date_label', item['date'].strftime('%b %d, %Y'))
        timeline.append(f'::::: {{.timeline-item #{item["slug"]}}}\n\n[{stamp}]{{.timeline-date}}\n\n:::: timeline-content\n\n### {item["title"]}\n\n{item["body"]}\n\n{picture(item,"timeline-image")}{tags(item["categories"])}\n\n::::\n:::::\n')
    latest = []
    for item in news[:3]:
        latest.append(f'::: latest-item\n\n[{item["date"].strftime("%b %d, %Y")}]{{.news-date}}\n\n### [{item["title"]}](/news/index.qmd#{item["slug"]})\n\n{tags(item["categories"])}\n\n:::\n')
    cards = []
    for number, item in zip(range(len(pubs),0,-1),pubs):
        categories = ','.join([str(item['year']), *item['categories']])
        cards.append(f'::::: {{.pub-card data-tags="{attr(categories)}"}}\n\n{picture(item,"pub-thumb")}:::: pub-info\n\n[{number}]{{.pub-number}}\n\n{item["body"]}\n\n{tags([str(item["year"]),*item["categories"]])}\n\n::::\n:::::\n')
    OUT.mkdir(exist_ok=True)
    for name, content in [('news', timeline),('latest',latest),('publications',cards)]:
        (OUT / f'{name}.qmd').write_text('\n'.join(content), encoding='utf-8')
    print(f'Validated and generated {len(news)} stories and {len(pubs)} publications.')

if __name__ == '__main__':
    generate()
