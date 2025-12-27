import os
import re
from typing import List, Dict


def get_nav_items(template_dir: str = None) -> List[Dict[str, str]]:
    """Scan HTML files in `template_dir` for <a href="...">text</a> links
    and return a list of unique nav items in discovery order.

    Each item is a dict: {'href': '/path', 'text': 'Label'}
    """
    if template_dir is None:
        base = os.path.dirname(os.path.dirname(__file__))
        template_dir = os.path.join(base, 'templates')

    # Build nav from templates folder structure.
    def humanize_token(token: str) -> str:
        parts = re.split(r'[-_\s]+', token)
        return ' '.join(p.capitalize() for p in parts if p)

    # Files that are partials or not intended as top-level nav targets
    exclude_files = {
        'header.html', 'sidebar.html', '3d_view.html', 'three.html',
        'test.html', 'question.html', 'quiz_result.html', 'thesis_search_result.html'
    }

    items: List[Dict[str, str]] = []
    seen = set()

    for root, _, files in os.walk(template_dir):
        for fname in sorted(files):
            if not fname.lower().endswith('.html'):
                continue
            if fname in exclude_files:
                continue

            full_path = os.path.join(root, fname)
            rel = os.path.relpath(full_path, template_dir).replace(os.path.sep, '/')
            # rel example: '3d_model_viewer/3dpreview.html' or 'home.html'
            rel_no_ext = rel[:-5]

            # Map home/index -> directory root
            if rel_no_ext == 'home' or rel_no_ext.endswith('/home') or rel_no_ext.endswith('/index'):
                if '/' in rel_no_ext:
                    dirpart = rel_no_ext.rsplit('/', 1)[0]
                    href = f'/{dirpart}/'
                else:
                    href = '/'
            else:
                href = '/' + rel_no_ext

            # Simplify common folder-based paths to nicer routes used by the app
            # e.g. /music_library/library -> /library/
            parts = rel_no_ext.split('/')
            if len(parts) > 1:
                folder, fname = parts[0], parts[-1]
                if folder == 'music_library':
                    href = '/library/'
                elif folder == 'thesis_archive' and fname == 'thesis':
                    href = '/thesis'
                elif folder == '3d_vietnamese_map' and fname == 'vnmap':
                    href = '/vnmap'
                elif folder == '3d_model_viewer' and fname == '3dpreview':
                    href = '/3dpreview'
                elif folder == 'quiz' and fname == 'quiz':
                    href = '/quiz/'

            # Read file to extract <title> or first <h1> for label
            label = None
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    txt = f.read()
                m = re.search(r'<title\s*>\s*(.*?)\s*</title>', txt, re.I | re.S)
                if m:
                    label = re.sub(r"\s+", ' ', m.group(1).strip())
                else:
                    m2 = re.search(r'<h1[^>]*>(.*?)</h1>', txt, re.I | re.S)
                    if m2:
                        label = re.sub(r"\s+", ' ', m2.group(1).strip())
            except Exception:
                label = None

            # If title/h1 is generic site title or empty, prefer filename-derived label
            if label:
                norm = re.sub(r"\s+", ' ', label).strip().lower()
                if norm in ('the gioi am nhac', 'index page', 'home', 'index'):
                    label = None

            if not label:
                # Fallback: use last token from rel_no_ext (file or folder)
                token = rel_no_ext.split('/')[-1]
                # If token is 'home', use parent folder name
                if token in ('home', 'index') and '/' in rel_no_ext:
                    token = rel_no_ext.rsplit('/', 1)[0].split('/')[-1]
                label = humanize_token(token)

            key = (href, label)
            if key in seen:
                continue
            seen.add(key)
            items.append({'href': href, 'text': label})

    return items
