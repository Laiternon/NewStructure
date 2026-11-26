import sys, os, json, glob, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcgen import *
from packs import sao, naruto_ghibli as ng, more1, dark, more2
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'main', 'resources', 'data', 'animebuilder', 'structures')
for f in glob.glob(OUT + '/*.json'): os.remove(f)
builds = [sao.cottage(), dark.dark_castle(), ng.hokage(), ng.ichiraku(), ng.bathhouse()] + more1.all_builds() + [dark.guild_hall()] + more2.all_builds()
names = set(); idx = []; bad = 0
for b in builds:
    b.finalize(); bad += len(validate(b, verbose=False))
    d = b.export(OUT); idx.append(b.id)
    for st in b.b.values(): names.add(st[0])
    n = sum(1 for s in b.b.values() if s[0] != 'air')
    print(f'{b.id:24s} {n:6d} blocks  [{b.category}]  {b.name}')
json.dump({'structures': idx}, open(OUT + '/index.json', 'w'))
print('PROBLEMS:', bad, ' structures:', len(idx))
print(' '.join(sorted(names)))
