from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
html = (ROOT / 'index.html').read_text()
script_match = re.search(r'<script>([\s\S]*)</script>', html)
if not script_match:
    raise SystemExit('No inline game script found')
script_path = Path('/tmp/speedy-chef-inline.js')
script_path.write_text(script_match.group(1))
result = subprocess.run(['node', '--check', str(script_path)], capture_output=True, text=True)
if result.returncode:
    print(result.stderr)
    raise SystemExit(result.returncode)
required = [
    'id="gameActionBtn"', 'id="chefCards"', 'function selectChef',
    'function scheduleNextCustomer', 'function resetKitchen',
    "getElementById('targetMoney').innerText = lvl.target",
    'state.customers = state.customers.filter',
]
missing = [item for item in required if item not in html]
if missing:
    raise SystemExit('Missing required implementation markers: ' + ', '.join(missing))
if 'state.target;' in html:
    raise SystemExit('Legacy undefined target reference remains')
print('JavaScript syntax: PASS')
print('Required implementation markers: PASS')
print(f'HTML size: {len(html):,} bytes')
