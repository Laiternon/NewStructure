import math, random
from mcgen import *


def tree(b, x, z, h, kind='oak', leaf=None, crown=2.6, base_y=0, rnd=None):
    """Natural tree: trunk on a dirt block, round crown with persistent leaves."""
    leaf = leaf or kind + '_leaves'
    b.set(x, base_y, z, 'grass_block')
    for y in range(base_y + 1, base_y + h + 1):
        b.set(x, y, z, P(kind + '_log', axis='y'))
    cy = base_y + h
    r = crown
    for dx in range(-4, 5):
        for dy in range(-3, 4):
            for dz in range(-4, 5):
                d = math.sqrt(dx * dx + (dy * 1.25) ** 2 + dz * dz)
                if d <= r and not (dx == 0 and dz == 0 and dy <= 0):
                    if rnd and d > r - 0.8 and rnd.random() < 0.3: continue
                    if (x + dx, cy + dy, z + dz) not in b.b:
                        b.set(x + dx, cy + dy, z + dz, P(leaf, persistent=True))
    _prune_leaves(b, x, z, base_y, h, leaf)
    return b


def _prune_leaves(b, x, z, base_y, h, leaf):
    # keep only leaves reachable from the trunk (so no leaf is ever left floating)
    from collections import deque
    start = [(x, y, z) for y in range(base_y + 1, base_y + h + 1)]
    seen = set(start); q = deque(start)
    while q:
        c = q.popleft()
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            n = (c[0] + d[0], c[1] + d[1], c[2] + d[2])
            if n in seen: continue
            st = b.b.get(n)
            if st and st[0] == leaf:
                seen.add(n); q.append(n)
    cx0 = x
    for p, st in list(b.b.items()):
        if st[0] == leaf and p not in seen and abs(p[0] - cx0) <= 5 and abs(p[2] - z) <= 5 and p[1] >= base_y + 1:
            del b.b[p]


def conifer(b, x, z, h, base_y=0, rnd=None):
    b.set(x, base_y, z, 'grass_block')
    for y in range(base_y + 1, base_y + h + 1):
        b.set(x, y, z, P('spruce_log', axis='y'))
    for i, y in enumerate(range(base_y + h + 1, base_y + 2, -1)):
        r = min(3, i // 2 + (1 if i > 0 else 0))
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) + abs(dz) <= r + (1 if r > 1 else 0) and not (dx == 0 and dz == 0 and y <= base_y + h):
                    if (x + dx, y, z + dz) not in b.b:
                        b.set(x + dx, y, z + dz, P('spruce_leaves', persistent=True))
    return b


def pond(b, cx, cz, rx, rz, lining='dirt', floor='clay', rim='grass_block', depth=2):
    """Self-contained pond: water surface at y=-1, sealed with lining so it can never leak. Returns set of water cells."""
    water = set()
    R = int(max(rx, rz)) + 3
    for x in range(-R, R + 1):
        for z in range(-R, R + 1):
            d = math.sqrt((x / rx) ** 2 + (z / rz) ** 2)
            X, Z = cx + x, cz + z
            if d <= 1.0:
                b.set(X, 0, Z, 'air')
                for y in range(-depth, 0):
                    b.set(X, y - 1 + 1 - 1 if False else y, Z, 'water')
                b.set(X, -depth - 1, Z, floor)
                water.add((X, Z))
            elif d <= 1.0 + 1.6 / min(rx, rz):
                for y in range(-depth - 1, 0):
                    b.set(X, y, Z, lining)
                b.set(X, 0, Z, rim)
    # seal: the lining must also surround water diagonally -> already covered by the ellipse offset
    return water


def flowers(b, pts, rnd, kinds=('poppy', 'dandelion', 'cornflower', 'azure_bluet', 'oxeye_daisy', 'allium', 'lily_of_the_valley')):
    for (x, z) in pts:
        if (x, 1, z) in b.b: continue
        b.set(x, 0, z, 'grass_block'); b.set(x, 1, z, rnd.choice(kinds))


def scatter(b, rnd, boxes, n, kinds, avoid=None, y=1):
    """Place small plants on grass at random spots inside [(x1,z1,x2,z2)] boxes if the column is free."""
    c = 0; tries = 0
    while c < n and tries < n * 20:
        tries += 1
        x1, z1, x2, z2 = rnd.choice(boxes)
        x, z = rnd.randint(x1, x2), rnd.randint(z1, z2)
        if (x, y, z) in b.b or (x, 0, z) in b.b and b.b[(x, 0, z)][0] not in ('grass_block',): continue
        if (x, y - 1, z) in b.b and b.b[(x, y - 1, z)][0] != 'grass_block': continue
        if avoid and avoid(x, z): continue
        b.set(x, 0, z, 'grass_block'); b.set(x, y, z, rnd.choice(kinds)); c += 1


def path(b, pts, blk='dirt_path', y=0):
    for (x, z) in pts:
        if (x, y, z) not in b.b:
            b.set(x, y, z, blk)


def post_lamp(b, x, z, y0=0, h=3, fence='spruce_fence'):
    b.fill(x, y0 + 1, z, x, y0 + h, z, fence)
    b.lantern(x, y0 + h + 1, z)


def counter_top(b, x, y, z):
    pass
