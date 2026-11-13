"""Verify structured content and app asset references. Does NOT certify religious rulings."""
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse
import json,re
r=Path(__file__).parent
read=lambda f:json.loads((r/f).read_text(encoding='utf8'))
t,c,e,h,d,l,v=(read(x) for x in ['topics.json','categories.json','evidence.json','hadith.json','doubts.json','learning.json','videos.json'])
assert len(c)==24 and len(t)==253 and len({x['id'] for x in t})==len(t)
assert len(h)==21 and len(d)==12 and len(l)==4 and sum(len(x['lessons']) for x in l)==20 and len(v)==2
for cat in c:assert cat['count']==sum(x['category']==cat['name'] for x in t)
for x in t:
 entry=e['entries'].get(x['id']);assert (x['status']=='intro')==bool(entry),x
 if entry:
  assert entry['answer'] and entry['sourceIds'] and entry['reviewStatus']
  for id in entry['sourceIds']:
   s=e['sources'][id]
   assert s['quote'] and s['citation'] and s['by']
   assert s['quoteMode'] in ['excerpt','verbatim','summary']
   assert s['type'] in ['hadith','quran','scholar','council']
   assert urlparse(s['url']).scheme=='https'
for x in h:
 assert x['citation'] and x['excerpt'] and 'sunnah.com'==urlparse(x['url']).hostname
for x in d:
 assert x['answer'] and x['sources'] and all(urlparse(s['url']).scheme=='https' for s in x['sources'])
for x in l:
 for lesson in x['lessons']: assert lesson['sources']
for video in v: assert urlparse(video['url']).hostname=='youtu.be' and video['reviewedTranscript'] is False
html=(r/'index.html').read_text();app=(r/'app.js').read_text()
for f in ['topics.json','categories.json','evidence.json','hadith.json','doubts.json','learning.json','videos.json']:
 assert (r/f).exists() and f"fetch('{f}')" in app
for page in ['home','library','hadith','doubts','learning','assistant','guides','bookmarks','references']:
 assert f'data-page="{page}"' in html and page in app
assert 'data/' not in html and "data/" not in app
print(f'PASS: {len(c)} doors, {len(t)} indexed topics, {len(e["entries"])} with evidence, {len(t)-len(e["entries"])} without detailed evidence')
print(f'PASS: {len(h)} selected sahih hadith, {len(d)} doubt explanations, {len(l)} learning tracks, {len(v)} video links')
print('All JSON in root, links syntax checked; live URL reachability and scholarly approval NOT guaranteed.')

# V4 extra checks: no general/misapplied source used for topics that need a specific ruling.
assert e['entries']['F009']['sourceIds']==['H-BUK-5736']
assert e['entries']['F181']['sourceIds']==['H-BUK-2363']
for fid in ['F106','F109','F111','F128','F164','F166','F185','F186','F187','F245','F251']:
 assert fid not in e['entries']
assert 'id="sourceLibrary"' in html and 'id="homeStats"' in html
assert 'function renderSources()' in app
assert 'styles.css?v=4' in html and 'app.js?v=4' in html
from bs4 import BeautifulSoup
soup=BeautifulSoup(html,'html.parser')
ids=[tag.get('id') for tag in soup.find_all(id=True)]
assert len(ids)==len(set(ids)), 'duplicate HTML ids'
for url in ['https://iifa-aifi.org/1789.html','https://iifa-aifi.org/ar/1849.html']:
 assert url in html
print('V4 checks: citation corrections, reference index, assets and unique IDs passed')
