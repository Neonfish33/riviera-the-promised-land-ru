# -*- coding: utf-8 -*-
import json, io, glob, os
tr = json.load(io.open('translations.json', encoding='utf-8'))
merged = 0
for f in glob.glob('result_*.json'):
    d = json.load(io.open(f, encoding='utf-8'))
    for k, v in d.items():
        tr[k] = v
        merged += 1
    print(f"{f}: {len(d)} entries")
json.dump(tr, io.open('translations.json','w',encoding='utf-8'), ensure_ascii=False)
print(f"\nИтого добавлено: {merged}, всего в translations.json: {len(tr)}")
