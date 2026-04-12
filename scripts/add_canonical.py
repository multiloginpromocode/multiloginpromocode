#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://multiloginpromocode.com'
EXCLUDE = ['drafts', 'backups', '.venv']


def is_excluded(path: Path):
    return any(part in EXCLUDE for part in path.parts)


def canonical_url_for(path: Path) -> str:
    # path is absolute to repo, pointing to index.html
    rel = path.relative_to(ROOT)
    # remove index.html
    if rel.name == 'index.html':
        rel_dir = rel.parent.as_posix()
        if rel_dir == '.':
            return DOMAIN + '/'
        else:
            return DOMAIN + '/' + rel_dir + '/'
    return DOMAIN + '/' + rel.as_posix()


def process_file(path: Path):
    text = path.read_text(encoding='utf-8')
    url = canonical_url_for(path)
    link_tag = f'<link rel="canonical" href="{url}" />'

    # If existing canonical, replace it
    if re.search(r'<link[^>]+rel=["\']canonical["\']', text, flags=re.I):
        text = re.sub(r'<link[^>]+rel=["\']canonical["\'][^>]*>', link_tag, text, flags=re.I)
    else:
        # insert before </head>
        text = re.sub(r'</head>', link_tag + '\n</head>', text, count=1, flags=re.I)

    path.write_text(text, encoding='utf-8')


def main():
    files = list((ROOT).rglob('index.html'))
    count = 0
    for f in files:
        if is_excluded(f):
            continue
        process_file(f)
        count += 1
    print(f'Processed {count} index.html files; canonical tags added/updated.')


if __name__ == '__main__':
    main()
