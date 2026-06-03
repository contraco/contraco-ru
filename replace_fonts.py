#!/usr/bin/env python3
import os, glob

FIND = '<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">'

REPLACE = """<style>
@font-face { font-family: 'Crimson Text'; font-style: normal; font-weight: 400; src: url('/fonts/crimson-text-v21-latin-regular.woff2') format('woff2'); font-display: swap; }
@font-face { font-family: 'Crimson Text'; font-style: normal; font-weight: 600; src: url('/fonts/crimson-text-v21-latin-600.woff2') format('woff2'); font-display: swap; }
@font-face { font-family: 'Crimson Text'; font-style: italic; font-weight: 400; src: url('/fonts/crimson-text-v21-latin-italic.woff2') format('woff2'); font-display: swap; }
@font-face { font-family: 'Inter'; font-style: normal; font-weight: 300; src: url('/fonts/inter-v20-latin-300.woff2') format('woff2'); font-display: swap; }
@font-face { font-family: 'Inter'; font-style: normal; font-weight: 400; src: url('/fonts/inter-v20-latin-regular.woff2') format('woff2'); font-display: swap; }
@font-face { font-family: 'Inter'; font-style: normal; font-weight: 500; src: url('/fonts/inter-v20-latin-500.woff2') format('woff2'); font-display: swap; }
@font-face { font-family: 'Inter'; font-style: normal; font-weight: 600; src: url('/fonts/inter-v20-latin-600.woff2') format('woff2'); font-display: swap; }
@font-face { font-family: 'Inter'; font-style: normal; font-weight: 700; src: url('/fonts/inter-v20-latin-700.woff2') format('woff2'); font-display: swap; }
</style>"""

os.chdir('/home/user/contraco-ru')
changed = 0
for path in sorted(glob.glob('*.html')):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if FIND in content:
        new = content.replace(FIND, REPLACE)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        print(f"Updated: {path}")
        changed += 1
    else:
        print(f"No match: {path}")

print(f"\nTotal updated: {changed}")
