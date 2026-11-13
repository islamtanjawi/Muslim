"""Validate the static source-to-topic map. No external dependencies."""
import json
from pathlib import Path
p=Path(__file__).parent
T=json.loads((p/'data/topics.json').read_text(encoding='utf-8'))
C=json.loads((p/'data/categories.json').read_text(encoding='utf-8'))
E=json.loads((p/'data/evidence.json').read_text(encoding='utf-8'))
ids=[t['id'] for t in T]
assert len(ids)==len(set(ids))
categories={c['name'] for c in C}
assert len(categories)==len(C)
assert set(t['category'] for t in T)==categories
for cat in C:assert cat['count']==sum(t['category']==cat['name'] for t in T),cat['name']
for t in T:
 has=t['id'] in E['entries']
 assert (t['status']=='intro')==has,t['id']
 if has:
  d=E['entries'][t['id']]
  assert d['answer'] and d['sourceIds']
  for sid in d['sourceIds']:
   s=E['sources'][sid]
   assert s['by'] and s['citation'] and s['quote'] and s['url'].startswith('https://'),(t['id'],sid)
print('OK:',len(C),'categories,',len(T),'topics,',len(E['entries']),'sourced articles,',len(E['sources']),'distinct sources')
