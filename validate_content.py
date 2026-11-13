"""Local consistency and safe-citation validator. Run before publishing."""
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse
import json
p=Path(__file__).parent
T=json.loads((p/'topics.json').read_text(encoding='utf8'))
C=json.loads((p/'categories.json').read_text(encoding='utf8'))
E=json.loads((p/'evidence.json').read_text(encoding='utf8'))
assert len(T)==253 and len(C)==24
ids={t['id'] for t in T}
assert len(ids)==len(T)
assert {t['category'] for t in T}=={c['name'] for c in C}
for cat in C:assert cat['count']==sum(t['category']==cat['name'] for t in T)
for t in T:
 has=t['id'] in E['entries']
 assert (t['status']=='intro')==has,t
 if has:
  entry=E['entries'][t['id']]
  assert entry['sourceIds'] and entry['answer'] and entry['reviewStatus'] in ('editorial_draft','reviewed')
  for sid in entry['sourceIds']:
   s=E['sources'][sid]
   assert s['type'] in ('quran','hadith','council','scholar')
   assert s['quoteMode'] in ('verbatim','excerpt','summary')
   assert s['quote'] and s['citation'] and s['by']
   assert urlparse(s['url']).scheme=='https'
for src in E['sources'].values():
 assert urlparse(src['url']).hostname in ('quran.com','dorar.net','iifa-aifi.org','www.islamweb.net')
assert "fetch('topics.json')" in (p/'app.js').read_text()
assert "state.categories.slice(0,12)" not in (p/'app.js').read_text()
assert './topics.json' in (p/'worker.js').read_text()
print(f"PASS: {len(C)} categories, {len(T)} topics, {len(E['entries'])} introductory entries, {len(E['sources'])} references")
print('Status:',dict(Counter(t['status'] for t in T)))
