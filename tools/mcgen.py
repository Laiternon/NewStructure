"""Structure authoring toolkit: DSL, stair-shape resolver, physical validator, JSON exporter, isometric preview."""
import json, math, os, hashlib
from collections import defaultdict, deque

OPP = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
CW = {'north': 'east', 'east': 'south', 'south': 'west', 'west': 'north'}
CCW = {v: k for k, v in CW.items()}
DV = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}
DIRS = ['north', 'east', 'south', 'west']
COLORS = ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black']


def P(name, **props):
    return (name, {k: str(v).lower() if isinstance(v, bool) else str(v) for k, v in props.items()})


def norm(b):
    if isinstance(b, tuple):
        return (b[0].replace('minecraft:', ''), dict(b[1]))
    return (b.replace('minecraft:', ''), {})


def fmt(st):
    n, p = st
    if not p:
        return 'minecraft:' + n
    return 'minecraft:' + n + '[' + ','.join(f'{k}={v}' for k, v in sorted(p.items())) + ']'


class Build:
    def __init__(self, id, category, name, foundation='cobblestone'):
        self.id, self.category, self.name, self.foundation = id, category, name, foundation
        self.b = {}

    # ---------------------------------------------------------------- primitives
    def set(self, x, y, z, blk, **props):
        if props and isinstance(blk, str):
            blk = P(blk, **props)
        self.b[(x, y, z)] = norm(blk)
        return self

    def setnew(self, x, y, z, blk):
        if (x, y, z) not in self.b:
            self.set(x, y, z, blk)

    def get(self, x, y, z):
        return self.b.get((x, y, z))

    def fill(self, x1, y1, z1, x2, y2, z2, blk):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.set(x, y, z, blk)
        return self

    def walls(self, x1, y1, z1, x2, y2, z2, blk):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if x in (x1, x2) or z in (z1, z2):
                        self.set(x, y, z, blk)
        return self

    def shell(self, x1, y1, z1, x2, y2, z2, blk):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if x in (x1, x2) or y in (y1, y2) or z in (z1, z2):
                        self.set(x, y, z, blk)
        return self

    def carve(self, x1, y1, z1, x2, y2, z2):
        return self.fill(x1, y1, z1, x2, y2, z2, 'air')

    def clear(self, x1, y1, z1, x2, y2, z2):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.b.pop((x, y, z), None)
        return self

    # ---------------------------------------------------------------- round shapes
    def disc(self, cx, y, cz, r, blk, hole=0):
        ri = int(math.ceil(r)) + 1
        for x in range(-ri, ri + 1):
            for z in range(-ri, ri + 1):
                d = math.hypot(x, z)
                if d <= r + 0.3 and d >= hole:
                    self.set(cx + x, y, cz + z, blk)
        return self

    def ring(self, cx, y, cz, r, blk):
        ri = int(math.ceil(r)) + 1
        for x in range(-ri, ri + 1):
            for z in range(-ri, ri + 1):
                d = math.hypot(x, z)
                if r - 0.85 < d <= r + 0.3:
                    self.set(cx + x, y, cz + z, blk)
        return self

    def tube(self, cx, y1, y2, cz, r, blk, solid=False):
        for y in range(y1, y2 + 1):
            (self.disc if solid else self.ring)(cx, y, cz, r, blk)
        return self

    def sphere(self, cx, cy, cz, r, blk, hollow=False, ry=None):
        ry = ry or r
        ri = int(math.ceil(max(r, ry))) + 1
        for x in range(-ri, ri + 1):
            for y in range(-ri, ri + 1):
                for z in range(-ri, ri + 1):
                    d = math.sqrt((x / r) ** 2 + (y / ry) ** 2 + (z / r) ** 2)
                    if d <= 1.0 and (not hollow or d > 1 - 1.15 / r):
                        self.set(cx + x, cy + y, cz + z, blk)
        return self

    def line(self, p, q, blk):
        (x1, y1, z1), (x2, y2, z2) = p, q
        n = max(abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)) or 1
        for i in range(n + 1):
            self.set(round(x1 + (x2 - x1) * i / n), round(y1 + (y2 - y1) * i / n), round(z1 + (z2 - z1) * i / n), blk)
        return self

    # ---------------------------------------------------------------- directional blocks
    def stair(self, x, y, z, name, facing, half='bottom'):
        return self.set(x, y, z, P(name, facing=facing, half=half, shape='straight', waterlogged=False))

    def slab(self, x, y, z, name, type='bottom'):
        return self.set(x, y, z, P(name, type=type))

    def log(self, x, y, z, name, axis='y'):
        return self.set(x, y, z, P(name, axis=axis))

    def column(self, x, y1, y2, z, blk):
        return self.fill(x, y1, z, x, y2, z, blk)

    def door(self, x, y, z, name, facing, hinge='left', open=False):
        self.set(x, y, z, P(name, facing=facing, half='lower', hinge=hinge, open=open))
        self.set(x, y + 1, z, P(name, facing=facing, half='upper', hinge=hinge, open=open))
        return self

    def trap(self, x, y, z, name, facing, open=True, half='bottom'):
        return self.set(x, y, z, P(name, facing=facing, open=open, half=half))

    def bed(self, x, y, z, color, facing):
        self.set(x, y, z, P(color + '_bed', facing=facing, part='foot'))
        dx, dz = DV[facing]
        self.set(x + dx, y, z + dz, P(color + '_bed', facing=facing, part='head'))
        return self

    def lantern(self, x, y, z, hanging=False, soul=False):
        return self.set(x, y, z, P('soul_lantern' if soul else 'lantern', hanging=hanging))

    def chain(self, x, y1, y2, z):
        return self.fill(x, y1, z, x, y2, z, P('chain', axis='y'))

    def hang_lantern(self, x, ytop, z, length=1, soul=False):
        """Chain from block above (ytop is the ceiling block y); lantern hangs below."""
        for i in range(length):
            self.set(x, ytop - 1 - i, z, P('chain', axis='y'))
        self.lantern(x, ytop - 1 - length, z, True, soul)
        return self

    def facing(self, x, y, z, name, facing, **kw):
        return self.set(x, y, z, P(name, facing=facing, **kw))

    def chest(self, x, y, z, facing):
        return self.set(x, y, z, P('chest', facing=facing, type='single'))

    def ladder(self, x, y1, y2, z, facing, wall='spruce_planks'):
        dx, dz = DV[OPP[facing]]
        for y in range(y1, y2 + 1):
            self.set(x, y, z, P('ladder', facing=facing))
            self.setnew(x + dx, y, z + dz, wall)
        return self

    def wall_torch(self, x, y, z, facing, soul=False):
        return self.set(x, y, z, P('soul_wall_torch' if soul else 'wall_torch', facing=facing))

    def fence_row(self, x1, z1, x2, z2, y, blk):
        return self.fill(x1, y, z1, x2, y, z2, blk)

    def candle(self, x, y, z, color=None, n=1, lit=True):
        return self.set(x, y, z, P((color + '_candle') if color else 'candle', candles=n, lit=lit))

    def carpet_rect(self, x1, z1, x2, z2, y, colors):
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                self.set(x, y, z, colors(x, z) if callable(colors) else colors)
        return self

    # ---------------------------------------------------------------- roofs
    def gable(self, x1, x2, z1, z2, y, stair, beam, ridge_axis='x', gable_fill=None, gable_span=None, cap=None):
        """Pitched roof. Ridge runs along `ridge_axis`. gable_fill = block closing the two triangular ends."""
        def P2(u, v):  # u along the ridge, v across
            return (u, v) if ridge_axis == 'x' else (v, u)
        u1, u2, v1, v2 = (x1, x2, z1, z2) if ridge_axis == 'x' else (z1, z2, x1, x2)
        fu1, fu2 = gable_span if gable_span else (u1 + 1, u2 - 1)
        lo, hi = v1, v2
        i = 0
        lo_f, hi_f = ('south', 'north') if ridge_axis == 'x' else ('east', 'west')
        while lo < hi:
            for u in range(u1, u2 + 1):
                a = P2(u, lo); c = P2(u, hi)
                self.stair(a[0], y + i, a[1], stair, lo_f)
                self.stair(c[0], y + i, c[1], stair, hi_f)
                if i > 0:
                    self.setnew(a[0], y + i - 1, a[1], beam)
                    self.setnew(c[0], y + i - 1, c[1], beam)
            if gable_fill:
                for v in range(lo + 1, hi):
                    for u in (fu1, fu2):
                        q = P2(u, v)
                        self.set(q[0], y + i, q[1], gable_fill)
            lo += 1; hi -= 1; i += 1
        if lo == hi:
            for u in range(u1, u2 + 1):
                q = P2(u, lo)
                self.set(q[0], y + i - 1, q[1], beam) if (q[0], y + i - 1, q[1]) not in self.b else None
                if cap:
                    self.slab(q[0], y + i, q[1], cap)
            if gable_fill:
                for u in (fu1, fu2):
                    q = P2(u, lo)
                    self.set(q[0], y + i - 1, q[1], gable_fill)
        return i

    def gable_low(self, x1, x2, z1, z2, y, stair, slab, beam, gable_fill=None, gspan=None):
        """Gentle 2:1 pitched roof (slab, stair, slab, stair...). Ridge along X. Returns ridge top y."""
        lo, hi, s = z1, z2, 0
        gx1, gx2 = gspan if gspan else (x1 + 1, x2 - 1)
        while lo <= hi:
            yy = y + s // 2
            if lo == hi:
                for x in range(x1, x2 + 1):
                    self.slab(x, yy, lo, slab, 'bottom'); self.setnew(x, yy - 1, lo, beam)
                if gable_fill:
                    for gx in (gx1, gx2): self.set(gx, yy, lo, gable_fill)
                break
            for x in range(x1, x2 + 1):
                for (z, f) in ((lo, 'south'), (hi, 'north')):
                    if s % 2 == 0: self.slab(x, yy, z, slab, 'bottom')
                    else: self.stair(x, yy, z, stair, f)
                    self.setnew(x, yy - 1, z, beam)
            if gable_fill:
                for z in range(lo + 1, hi):
                    for gx in (gx1, gx2): self.set(gx, yy, z, gable_fill)
            lo += 1; hi -= 1; s += 1
        return y + s // 2

    def hip_low(self, x1, z1, x2, z2, y, stair, slab, beam, rings=99):
        """Gentle hip roof (2:1). After `rings` rings the middle is closed flat. Returns y of the flat top / ridge."""
        s = 0
        while x1 <= x2 and z1 <= z2:
            yy = y + s // 2
            if x2 - x1 < 2 or z2 - z1 < 2 or s >= rings:
                for x in range(x1, x2 + 1):
                    for z in range(z1, z2 + 1):
                        self.setnew(x, yy - 1, z, beam)
                        if s >= rings and x2 - x1 >= 2 and z2 - z1 >= 2: self.set(x, yy, z, beam)
                        else: self.slab(x, yy, z, slab, 'bottom')
                return yy
            def put(x, z, f):
                if s % 2 == 0: self.slab(x, yy, z, slab, 'bottom')
                else: self.stair(x, yy, z, stair, f)
                self.setnew(x, yy - 1, z, beam)
            for x in range(x1, x2 + 1):
                put(x, z1, 'south'); put(x, z2, 'north')
            for z in range(z1 + 1, z2):
                put(x1, z, 'east'); put(x2, z, 'west')
            x1 += 1; z1 += 1; x2 -= 1; z2 -= 1; s += 1
        return y + s // 2

    def hip(self, x1, z1, x2, z2, y, stair, beam, cap=None):
        i = 0
        while x1 <= x2 and z1 <= z2:
            if x2 - x1 < 2 or z2 - z1 < 2:
                for x in range(x1, x2 + 1):
                    for z in range(z1, z2 + 1):
                        self.setnew(x, y + i - 1, z, beam)
                        if cap:
                            self.slab(x, y + i, z, cap)
                        else:
                            self.set(x, y + i, z, beam)
                break
            for x in range(x1, x2 + 1):
                self.stair(x, y + i, z1, stair, 'south'); self.stair(x, y + i, z2, stair, 'north')
            for z in range(z1 + 1, z2):
                self.stair(x1, y + i, z, stair, 'east'); self.stair(x2, y + i, z, stair, 'west')
            if i > 0:
                for x in range(x1, x2 + 1):
                    self.setnew(x, y + i - 1, z1, beam); self.setnew(x, y + i - 1, z2, beam)
                for z in range(z1 + 1, z2):
                    self.setnew(x1, y + i - 1, z, beam); self.setnew(x2, y + i - 1, z, beam)
            x1 += 1; z1 += 1; x2 -= 1; z2 -= 1; i += 1
        return i

    def cone(self, cx, cz, r, y, blk, stair=None, dec=1.0, rmin=0.5, first_solid=False):
        """Hollow round roof, rim made of stairs rising inward. Radius shrinks by `dec` per layer. Returns the top layer y."""
        thick = dec + 0.9
        i = 0; rr = float(r); last = y
        while rr >= rmin:
            yy = y + i; ri = int(math.ceil(rr)) + 1
            solid = rr - dec < rmin or (first_solid and i == 0)
            for x in range(-ri, ri + 1):
                for z in range(-ri, ri + 1):
                    d = math.hypot(x, z)
                    if d <= rr + 0.3 and (solid or d > rr - thick):
                        if stair and d > rr - 0.75 and not solid:
                            f = ('west' if x > 0 else 'east') if abs(x) >= abs(z) else ('north' if z > 0 else 'south')
                            self.stair(cx + x, yy, cz + z, stair, f)
                        else:
                            self.set(cx + x, yy, cz + z, blk)
            last = yy; rr -= dec; i += 1
        return last

    def ring_cell(self, cx, cz, r, ang_deg):
        best = None
        ri = int(math.ceil(r)) + 1
        for x in range(-ri, ri + 1):
            for z in range(-ri, ri + 1):
                d = math.hypot(x, z)
                if r - 0.85 < d <= r + 0.3:
                    a = math.degrees(math.atan2(z, x)) % 360
                    diff = min(abs(a - ang_deg % 360), 360 - abs(a - ang_deg % 360))
                    if best is None or diff < best[0]: best = (diff, cx + x, cz + z)
        return best[1], best[2]

    def ring_windows(self, cx, cz, r, y1, y2, count, blk='glass_pane', start=0):
        for k in range(count):
            x, z = self.ring_cell(cx, cz, r, start + 360.0 * k / count)
            for y in range(y1, y2 + 1): self.set(x, y, z, blk)

    def stamp(self, other, ox, oy, oz, rot=0):
        """Copy another Build into this one, rotated clockwise by rot*90deg around its origin."""
        for (x, y, z), (n, pr) in other.b.items():
            p = dict(pr)
            for _ in range(rot):
                x, z = -z, x
                if 'facing' in p and p['facing'] in CW: p['facing'] = CW[p['facing']]
                if p.get('axis') in ('x', 'z'): p['axis'] = 'z' if p['axis'] == 'x' else 'x'
            self.b[(x + ox, y + oy, z + oz)] = (n, p)
        return self

    # ---------------------------------------------------------------- finalise
    def _stair_shapes(self):
        def is_st(st): return st is not None and st[0].endswith('_stairs')
        for (x, y, z), st in list(self.b.items()):
            if not is_st(st) or 'facing' not in st[1]:
                continue
            f, h = st[1]['facing'], st[1]['half']
            dx, dz = DV[f]
            nb = self.b.get((x + dx, y, z + dz))
            shape = 'straight'

            def can_take(face):
                o = self.b.get((x + DV[face][0], y, z + DV[face][1]))
                return not is_st(o) or o[1]['facing'] != f or o[1]['half'] != h
            if is_st(nb) and nb[1]['half'] == h and nb[1]['facing'] in (CW[f], CCW[f]) and can_take(OPP[nb[1]['facing']]):
                shape = 'outer_left' if nb[1]['facing'] == CCW[f] else 'outer_right'
            else:
                bx, bz = DV[OPP[f]]
                nb2 = self.b.get((x + bx, y, z + bz))
                if is_st(nb2) and nb2[1]['half'] == h and nb2[1]['facing'] in (CW[f], CCW[f]) and can_take(nb2[1]['facing']):
                    shape = 'inner_left' if nb2[1]['facing'] == CCW[f] else 'inner_right'
            st[1]['shape'] = shape

    def finalize(self):
        self._stair_shapes()
        return self

    def export(self, outdir):
        self.finalize()
        xs = [k[0] for k in self.b]; zs = [k[2] for k in self.b]
        mx, mz = min(xs), min(zs)
        pal, idx, flat = [], {}, []
        for (x, y, z), st in sorted(self.b.items(), key=lambda kv: (kv[0][1], kv[0][0], kv[0][2])):
            s = fmt(st)
            if s not in idx:
                idx[s] = len(pal); pal.append(s)
            flat += [x - mx, y, z - mz, idx[s]]
        data = {'id': self.id, 'category': self.category, 'name': self.name, 'foundation': 'minecraft:' + self.foundation,
                'palette': pal, 'blocks': flat}
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, self.id + '.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        return data


# ==================================================================== validation
AIRLIKE = ('air',)
NONSOLID = ('torch', 'lantern', 'carpet', 'pressure_plate', 'ladder', 'sign', 'candle', 'flower_pot', 'potted', 'water', 'lava', 'fire', 'door',
            'bed', 'campfire', 'chain', 'button', 'lever', 'rail', 'banner', 'head', 'skull', 'vine', 'azalea', 'fern', 'flower', 'rose', 'tulip',
            'poppy', 'dandelion', 'grass', 'lily', 'sapling', 'mushroom', 'bush', 'cobweb', 'cauldron_x')
PLANTS = ('azalea', 'fern', 'flower', 'rose_bush', 'tulip', 'poppy', 'dandelion', 'cornflower', 'lily_of_the_valley', 'allium', 'peony', 'lilac',
          'tall_grass', 'short_grass', 'grass', 'sunflower', 'orchid', 'azure_bluet', 'oxeye_daisy', 'sweet_berry', 'bamboo', 'sapling', 'torchflower', 'pitcher')
SOIL = ('grass_block', 'dirt', 'podzol', 'moss_block', 'coarse_dirt', 'rooted_dirt', 'mud', 'mycelium', 'farmland', 'clay', 'sand', 'flowering_azalea_leaves')
PLANT_SET = {'azalea', 'flowering_azalea', 'fern', 'large_fern', 'tall_grass', 'grass', 'poppy', 'dandelion', 'cornflower', 'azure_bluet', 'oxeye_daisy',
             'allium', 'lily_of_the_valley', 'rose_bush', 'peony', 'lilac', 'sunflower', 'sweet_berry_bush', 'blue_orchid', 'red_tulip', 'pink_tulip',
             'white_tulip', 'orange_tulip', 'wither_rose', 'torchflower', 'brown_mushroom', 'red_mushroom', 'dead_bush', 'bamboo', 'sapling'}
GRAVITY = ('sand', 'gravel', 'concrete_powder')


def is_air(st): return st is None or st[0] == 'air'
def has(n, keys): return any(k in n for k in keys)


def solid_full(st):
    if is_air(st): return False
    n = st[0]
    if n in ('water', 'lava'): return False
    if has(n, ('torch', 'lantern', 'carpet', 'pressure_plate', 'ladder', 'sign', 'candle', 'flower_pot', 'potted', 'fire', 'door', 'bed', 'chain', 'button',
               'lever', 'banner', 'vine', 'cobweb', 'fence', 'wall', 'pane', 'bars', 'trapdoor', 'stairs', 'slab', 'campfire', 'cauldron', 'leaves')) and not n.endswith('_wall') is False:
        pass
    return not has(n, ('torch', 'lantern', 'carpet', 'pressure_plate', 'ladder', 'sign', 'candle', 'flower_pot', 'potted', 'fire', 'door', 'bed', 'chain', 'button',
                       'lever', 'banner', 'vine', 'cobweb', 'pane', 'bars', 'trapdoor', 'campfire', 'azalea', 'fern', 'flower', 'rose_bush', 'tulip', 'poppy',
                       'grass', 'sapling', 'bamboo', 'lightning_rod', 'end_rod', 'rail', 'head', 'skull', 'sweet_berry', 'brewing', 'lily', 'pointed_dripstone', 'amethyst_cluster'))


def sturdy_top(st):
    """Can a lantern / torch / carpet / door stand on this?"""
    if is_air(st): return False
    n = st[0]
    if n in ('water', 'lava'): return False
    if has(n, ('chain', 'ladder', 'torch', 'carpet', 'pressure_plate', 'sign', 'candle', 'vine', 'flower_pot', 'potted', 'bed', 'door', 'banner', 'cobweb',
               'button', 'lever', 'fern', 'azalea', 'flower', 'grass', 'rose', 'tulip', 'poppy', 'lantern', 'lightning_rod', 'end_rod')):
        return False
    if n.endswith('_slab') and st[1].get('type') == 'bottom': return True
    if n.endswith('_stairs') and st[1].get('half') == 'bottom': return True
    if n.endswith('_trapdoor'): return st[1].get('open') == 'false' and st[1].get('half') == 'top' or False
    if n.endswith('_slab') and st[1].get('type') == 'top': return True
    return True


def validate(bd, verbose=True):
    b = bd.b
    problems = []
    nodes = {p for p, s in b.items() if not is_air(s)}
    def at(x, y, z): return b.get((x, y, z))

    # ---- connectivity: every block must be connected (face adjacency) to the ground plane (y <= 0)
    seen = set(); comps = []
    for p in nodes:
        if p in seen: continue
        comp = []; q = deque([p]); seen.add(p)
        while q:
            c = q.popleft(); comp.append(c)
            for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                n = (c[0] + d[0], c[1] + d[1], c[2] + d[2])
                if n in nodes and n not in seen:
                    seen.add(n); q.append(n)
        comps.append(comp)
    for comp in comps:
        if not any(p[1] <= 0 for p in comp):
            problems.append(f'FLOATING component of {len(comp)} blocks near {comp[0]} ({b[comp[0]][0]})')

    for (x, y, z), st in b.items():
        n, pr = st
        if n == 'air': continue
        below, above = at(x, y - 1, z), at(x, y + 1, z)
        where = f'{n} at ({x},{y},{z})'
        if n == 'ladder':
            dx, dz = DV[OPP[pr['facing']]]
            if not solid_full(at(x + dx, y, z + dz)): problems.append('ladder without wall: ' + where)
        elif n in ('wall_torch', 'soul_wall_torch') or n.endswith('_wall_sign') or n.endswith('wall_banner'):
            dx, dz = DV[OPP[pr['facing']]]
            if not solid_full(at(x + dx, y, z + dz)): problems.append('wall attachment without wall: ' + where)
        elif n in ('torch', 'soul_torch') or n.endswith('_candle') or n == 'candle' or n in ('campfire', 'soul_campfire') or n.endswith('pressure_plate') \
                or n.endswith('_carpet') or n == 'flower_pot' or n.startswith('potted_') or n.endswith('_sign') and 'wall' not in n or n in ('moss_carpet',):
            if not sturdy_top(below): problems.append('needs solid floor: ' + where)
        elif n in ('lantern', 'soul_lantern'):
            if pr.get('hanging') == 'true':
                if is_air(above) or above[0] in ('water', 'lava') or has(above[0], ('torch', 'lantern', 'carpet')): problems.append('hanging lantern without anchor: ' + where)
            elif not sturdy_top(below): problems.append('standing lantern without floor: ' + where)
        elif n.endswith('_door'):
            if pr['half'] == 'lower':
                if not sturdy_top(below): problems.append('door without floor: ' + where)
                u = at(x, y + 1, z)
                if is_air(u) or not u[0].endswith('_door') or u[1]['half'] != 'upper': problems.append('door missing upper half: ' + where)
            else:
                l = at(x, y - 1, z)
                if is_air(l) or not l[0].endswith('_door') or l[1]['half'] != 'lower': problems.append('door upper without lower: ' + where)
        elif n.endswith('_bed'):
            dx, dz = DV[pr['facing']]
            if pr['part'] == 'foot':
                h = at(x + dx, y, z + dz)
                if is_air(h) or h[0] != n or h[1]['part'] != 'head': problems.append('bed missing head: ' + where)
            else:
                f = at(x - dx, y, z - dz)
                if is_air(f) or f[0] != n or f[1]['part'] != 'foot': problems.append('bed head without foot: ' + where)
            if not sturdy_top(below): problems.append('bed without floor: ' + where)
        elif n in ('water',):
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nb = at(x + d[0], y, z + d[1])
                if is_air(nb) or (nb[0] not in ('water',) and not solid_full(nb) and not nb[0].endswith(('_slab', '_stairs', '_wall', '_fence'))):
                    problems.append(f'water leaks sideways at ({x},{y},{z})'); break
            if is_air(below) or (below[0] != 'water' and not solid_full(below)): problems.append(f'water leaks down at ({x},{y},{z})')
        elif n == 'lava':
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nb = at(x + d[0], y, z + d[1])
                if is_air(nb) or (nb[0] != 'lava' and not solid_full(nb)): problems.append(f'lava leaks sideways at ({x},{y},{z})'); break
            if is_air(below) or (below[0] != 'lava' and not solid_full(below)): problems.append(f'lava leaks down at ({x},{y},{z})')
        elif n == 'lily_pad':
            if is_air(below) or below[0] != 'water': problems.append('lily pad not on water: ' + where)
        elif n == 'bamboo':
            if is_air(below) or not (below[0] == 'bamboo' or has(below[0], SOIL)): problems.append('bamboo not on soil: ' + where)
        elif n in PLANT_SET:
            if is_air(below) or not has(below[0], SOIL + ('moss',)): problems.append('plant on non-soil: ' + where)
            if 'tall' in n or n in ('rose_bush', 'peony', 'lilac', 'sunflower', 'large_fern'):
                pass
        elif has(n, GRAVITY):
            if not sturdy_top(below): problems.append('gravity block unsupported: ' + where)
        elif n.endswith('_leaves'):
            if pr.get('persistent') != 'true': problems.append('leaves would decay (persistent!=true): ' + where)
        elif n == 'chain':
            if is_air(above) and is_air(below): problems.append('floating chain: ' + where)
    seen_msgs = set(); out = []
    for p in problems:
        if p not in seen_msgs: seen_msgs.add(p); out.append(p)
    if verbose:
        n_blocks = len(nodes)
        print(f'[{bd.id}] {n_blocks} blocks, {len(out)} problems')
        for p in out[:25]: print('   -', p)
        if len(out) > 25: print(f'   ... +{len(out) - 25} more')
    return out


# ==================================================================== preview
def color_of(n, pr):
    from_name = [
        ('water', (60, 110, 210)), ('lava', (240, 110, 20)), ('grass_block', (95, 160, 60)), ('moss', (80, 120, 40)), ('podzol', (90, 65, 35)),
        ('dirt', (125, 90, 60)), ('leaves', (45, 115, 40)), ('azalea', (80, 130, 50)), ('dark_oak', (62, 42, 22)), ('spruce', (105, 78, 48)),
        ('oak', (178, 140, 85)), ('birch', (215, 205, 155)), ('acacia', (175, 95, 55)), ('cherry', (232, 175, 195)), ('jungle', (160, 115, 80)),
        ('mangrove', (120, 50, 50)), ('bamboo', (205, 190, 80)), ('crimson', (130, 45, 65)), ('warped', (40, 125, 115)),
        ('stone_brick', (125, 125, 125)), ('cobblestone', (112, 112, 112)), ('polished_blackstone', (45, 40, 52)), ('blackstone', (38, 33, 44)),
        ('deepslate', (65, 65, 70)), ('quartz', (236, 231, 226)), ('nether_brick', (70, 30, 35)), ('red_nether', (110, 25, 30)),
        ('brick', (150, 72, 56)), ('terracotta', (160, 95, 75)), ('glass', (170, 210, 230)), ('lantern', (255, 200, 90)), ('glowstone', (250, 210, 120)),
        ('sea_lantern', (200, 240, 235)), ('shroomlight', (250, 160, 70)), ('campfire', (240, 150, 50)), ('torch', (255, 210, 90)),
        ('copper', (190, 110, 80)), ('gold', (250, 215, 70)), ('iron', (210, 210, 210)), ('stone', (128, 128, 128)), ('andesite', (140, 140, 140)),
        ('diorite', (200, 200, 200)), ('granite', (160, 105, 90)), ('bone', (225, 220, 195)), ('obsidian', (25, 15, 45)), ('purpur', (165, 120, 165)),
        ('sand', (225, 210, 150)), ('hay', (200, 170, 40)), ('bookshelf', (130, 95, 60)), ('prismarine', (95, 160, 150)), ('snow', (245, 248, 250)),
        ('mud', (70, 55, 50)), ('wool', (235, 235, 235)), ('smooth_basalt', (60, 60, 65)), ('tuff', (110, 110, 100)), ('calcite', (225, 225, 220)),
        ('soul', (60, 160, 190)), ('netherrack', (110, 50, 50)), ('magma', (170, 60, 20)), ('end_stone', (225, 225, 160)), ('sculk', (15, 60, 70)),
    ]
    for c in COLORS:
        if c in n.replace('light_gray', 'light_gray'):
            base = {'white': (235, 235, 235), 'orange': (225, 120, 30), 'magenta': (180, 70, 170), 'light_blue': (90, 170, 220), 'yellow': (235, 200, 40),
                    'lime': (120, 190, 40), 'pink': (235, 140, 170), 'gray': (70, 75, 80), 'light_gray': (150, 150, 145), 'cyan': (30, 130, 140),
                    'purple': (120, 50, 170), 'blue': (50, 60, 160), 'brown': (110, 70, 40), 'green': (80, 110, 40), 'red': (170, 40, 40), 'black': (25, 25, 30)}[c]
            if c == 'gray' and 'light_gray' in n: continue
            return base
    for k, col in from_name:
        if k in n:
            return col
    h = hashlib.md5(n.encode()).digest()
    return (90 + h[0] % 120, 90 + h[1] % 120, 90 + h[2] % 120)


def render(bd, path, scale=None, view=0, ymax=None, xr=None, zr=None, noleaves=False):
    from PIL import Image, ImageDraw
    items = []
    for (x, y, z), (n, pr) in bd.b.items():
        if n == 'air': continue
        if ymax is not None and y > ymax: continue
        if xr and not (xr[0] <= x <= xr[1]): continue
        if zr and not (zr[0] <= z <= zr[1]): continue
        if noleaves and n.endswith('_leaves'): continue
        items.append((x, y, z, n, pr))
    if view:  # rotate the model by 90deg increments (to look at other sides)
        for _ in range(view):
            items = [(-z, y, x, n, pr) for (x, y, z, n, pr) in items]
    xs = [i[0] for i in items]; zs = [i[2] for i in items]; ys = [i[1] for i in items]
    # iso projection helpers
    def proj(a, bb, y, s):
        return ((a - bb) * s * 0.866, (a + bb) * s * 0.5 - y * s)
    mx, Mx, mz, Mz, my, My = min(xs), max(xs), min(zs), max(zs), min(ys), max(ys)
    if scale is None:
        w = (Mx - mx + Mz - mz + 2) * 0.866; h = (Mx - mx + Mz - mz + 2) * 0.5 + (My - my + 2)
        scale = max(3, min(18, int(min(1500 / w, 1000 / h))))
    s = scale
    corners = [proj(a, bb, y, s) for a in (mx, Mx + 1) for bb in (-Mz - 1, -mz) for y in (my, My + 1)]
    ox = -min(c[0] for c in corners) + 10; oy = -min(c[1] for c in corners) + 10
    W = int(max(c[0] for c in corners) + ox + 10); H = int(max(c[1] for c in corners) + oy + 10)
    img = Image.new('RGB', (W, H), (150, 190, 225)); d = ImageDraw.Draw(img, 'RGBA')
    items.sort(key=lambda i: (i[0] - i[2] + i[1] * 1.001, i[1]))
    thin = ('carpet', 'pressure_plate')
    narrow = ('fence', 'wall', 'pane', 'bars', 'chain', 'torch', 'lantern', 'ladder', 'rod', 'candle', 'pot', 'sign', 'cauldron_')
    for x, y, z, n, pr in items:
        col = color_of(n, pr)
        a0, a1 = x, x + 1; b0, b1 = -z - 1, -z
        y0, y1 = y, y + 1
        if n.endswith('_slab'):
            if pr.get('type') == 'bottom': y1 = y + 0.5
            elif pr.get('type') == 'top': y0 = y + 0.5
        elif has(n, thin): y1 = y + 0.08
        elif has(n, narrow) and not n.endswith('_wall') or n.endswith('_wall') and False:
            a0, a1, b0, b1 = x + .35, x + .65, -z - .65, -z - .35
        elif n.endswith('_wall') and 'sign' not in n and 'torch' not in n:
            a0, a1, b0, b1 = x + .25, x + .75, -z - .75, -z - .25
        alpha = 255
        if n == 'water': alpha = 170; y1 = y + 0.9
        if 'glass' in n: alpha = 150
        def P_(a, bb, yy): px, py = proj(a, bb, yy, s); return (px + ox, py + oy)
        top = [P_(a0, b0, y1), P_(a1, b0, y1), P_(a1, b1, y1), P_(a0, b1, y1)]
        east = [P_(a1, b0, y0), P_(a1, b1, y0), P_(a1, b1, y1), P_(a1, b0, y1)]
        north = [P_(a0, b1, y0), P_(a1, b1, y0), P_(a1, b1, y1), P_(a0, b1, y1)]
        lit = (255, 220, 120) if has(n, ('lantern', 'glowstone', 'torch', 'campfire', 'sea_lantern', 'shroomlight', 'lava', 'magma')) else None
        def sh(f): return tuple(min(255, int(c * f)) for c in col)
        d.polygon(top, fill=sh(1.0) + (alpha,)); d.polygon(north, fill=sh(0.78) + (alpha,)); d.polygon(east, fill=sh(0.58) + (alpha,))
        if lit: d.polygon(top, fill=lit + (190,))
    img.save(path)
    return img.size
