#!/usr/bin/env python3
"""Build the static, deployable site from pages/*.dc.html.

Output goes to the repo root: index.html (home), About.html, Explorations.html,
Case-*.html, plus dc-lite.js. Assets stay in assets/. Run from anywhere:
    python3 build/build.py
"""
import os, re, json, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, 'pages')

def out_name(stem):
    return 'index.html' if stem == 'Main' else stem + '.html'

def transform(src, props=None, title=None):
    s = src
    head_extra = ('<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                  '<link rel="icon" href="data:,">\n')
    if props:
        head_extra += '<script>window.__DC_PROPS__=' + json.dumps(props) + ';</script>\n'
    head_extra += '<script src="dc-lite.js"></script>'
    s = s.replace('<script src="./support.js"></script>', head_extra, 1)
    if title:
        s = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', s, count=1, flags=re.S)
    s = s.replace('<x-dc>', '<template id="dc-tpl">', 1).replace('</x-dc>', '</template>', 1)
    s = s.replace('../assets/', 'assets/')
    s = s.replace('Main.dc.html', 'index.html').replace('.dc.html', '.html')
    s = s.replace("'Main': 'Home'", "'index': 'Home', 'Main': 'Home'")
    return s

def main():
    built = []
    shared = open(os.path.join(PAGES, 'CaseStudy.dc.html'), encoding='utf-8').read()
    for f in sorted(os.listdir(PAGES)):
        if not f.endswith('.dc.html'):
            continue
        stem = f[:-len('.dc.html')]
        if stem == 'CaseStudy':
            continue  # shared template, rendered through the Case-* pages
        src = open(os.path.join(PAGES, f), encoding='utf-8').read()
        imp = re.search(r'<dc-import name="CaseStudy" pid="([a-z]+)"', src)
        if imp:
            t = re.search(r'<title>(.*?)</title>', src, re.S)
            html = transform(shared, props={'pid': imp.group(1)}, title=t.group(1) if t else None)
        else:
            html = transform(src)
        open(os.path.join(ROOT, out_name(stem)), 'w', encoding='utf-8').write(html)
        built.append(out_name(stem))
    shutil.copy2(os.path.join(ROOT, 'build', 'dc-lite.js'), os.path.join(ROOT, 'dc-lite.js'))
    print('built:', ', '.join(built))

if __name__ == '__main__':
    main()
