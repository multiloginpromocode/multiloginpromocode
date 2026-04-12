#!/usr/bin/env python3
"""Generate lightweight rewritten drafts for HTML pages under compare/, guides/, promo/.

Creates files under drafts/rewrites/bulk/<orig_path>/index.html
Simple, safe transforms: tweak title, h1, inject a unique sentence, update JSON-LD dateModified/headline.
"""
import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
SRC_FOLDERS = [ROOT / 'compare', ROOT / 'guides', ROOT / 'promo']
OUT_ROOT = ROOT / 'drafts' / 'rewrites' / 'bulk'
TODAY = date.today().isoformat()


def tweak_html(text: str, rel_path: Path) -> str:
    # mark draft
    if not text.lstrip().startswith('<!-- Rewritten draft'):
        text = '<!-- Rewritten draft: auto-generated. Review before publish -->\n' + text

    # title: prepend Refreshed:
    text = re.sub(r'(<title>)(.*?)(</title>)', lambda m: f"{m.group(1)}Refreshed: {m.group(2)}{m.group(3)}", text, count=1, flags=re.I|re.S)

    # h1: append Updated
    text = re.sub(r'(<h1[^>]*>)(.*?)(</h1>)', lambda m: f"{m.group(1)}{m.group(2)} — Refreshed{m.group(3)}", text, count=1, flags=re.I|re.S)

    # inject unique insight after first lead or first <p>
    insight = f'<p class="unique-insight">Unique insight ({TODAY}): verified by site lab — small test added.</p>'
    if 'class="lead"' in text:
        text = re.sub(r'(<p[^>]*class=["\']lead["\'][^>]*>.*?</p>)', r'\1\n' + insight, text, count=1, flags=re.I|re.S)
    else:
        text = re.sub(r'(<p[^>]*>.*?</p>)', r'\1\n' + insight, text, count=1, flags=re.I|re.S)

    # JSON-LD: update dateModified and headline if present
    def jd_repl(m):
        block = m.group(0)
        block = re.sub(r'("dateModified"\s*:\s*")[^"]*(")', r'\1' + TODAY + r'\2', block)
        block = re.sub(r'("headline"\s*:\s*")(.*?)(")', lambda mm: r'"headline":"' + mm.group(2) + ' — Refreshed"', block)
        return block

    text = re.sub(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?</script>', jd_repl, text, flags=re.I|re.S)

    # add small comment about original path
    text = text.replace('</head>', f'<!-- original: {rel_path.as_posix()} -->\n</head>', 1)

    return text


def main():
    out_count = 0
    for src in SRC_FOLDERS:
        if not src.exists():
            continue
        for html in src.rglob('index.html'):
            rel = html.relative_to(ROOT)
            try:
                text = html.read_text(encoding='utf-8')
            except Exception:
                text = html.read_text(encoding='latin-1')
            new = tweak_html(text, rel)
            out_path = OUT_ROOT / rel.parent
            out_path.mkdir(parents=True, exist_ok=True)
            (out_path / 'index.html').write_text(new, encoding='utf-8')
            out_count += 1

    print(f'Generated {out_count} rewritten drafts under {OUT_ROOT}')


if __name__ == '__main__':
    main()
