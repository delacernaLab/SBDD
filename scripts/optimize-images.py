"""Generate web copies while preserving the original lab images."""
from pathlib import Path
import json
from PIL import Image, ImageOps

root = Path(__file__).resolve().parents[1]
mapping = json.loads((root / 'scripts/image-sources.json').read_text())
before = after = 0
for output, source in mapping.items():
    original, target = (root / source).resolve(), (root / output).resolve()
    if not original.is_relative_to(root) or not target.is_relative_to(root):
        raise ValueError('Image paths must stay within the project')
    if not original.is_file():
        raise FileNotFoundError(f'Missing original image: {source}')
    with Image.open(original) as image:
        image = ImageOps.exif_transpose(image)
        image.thumbnail((1000, 1000))
        image.save(target, 'WEBP', quality=85, method=6)
    before += original.stat().st_size
    after += target.stat().st_size
print(f'Generated {len(mapping)} web images: {before:,} → {after:,} bytes.')
