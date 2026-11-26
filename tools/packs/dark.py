import random, math
from mcgen import *
from common import *


def seal_basin(b, cells, fluid, lining, floor, depth=2):
    """Fill `cells` (set of (x,z)) with a fluid at y=-1..-depth, sealed with lining so it can never leak."""
    for (x, z) in cells:
        b.set(x, 0, z, 'air')
        for y in range(-depth, 0): b.set(x, y, z, fluid)
        b.set(x, -depth - 1, z, floor)
    for (x, z) in cells:
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, z + dz)
            if n not in cells:
                for y in range(-depth - 1, 0): b.set(n[0], y, n[1], lining)


def dark_castle():
    rnd = random.Random(666)
    b = Build('dark_lord_castle', 'Тёмные владыки', 'Замок Владыки Тьмы', foundation='blackstone')
    BK, DK, BS = 'polished_blackstone_bricks', 'deepslate_bricks', 'blackstone'
    S = lambda n, f, h='bottom': None
    C = 22
    # ---------- cursed ground
    for x in range(-2, 47):
        for z in range(-2, 47):
            if math.hypot(x - C, z - C) <= 29:
                r = rnd.random()
                b.set(x, 0, z, 'coarse_dirt' if r < .15 else 'soul_soil' if r < .3 else 'blackstone' if r < .75 else 'cobbled_deepslate' if r < .9 else 'magma_block')
    # ---------- lava moat around the curtain wall (x/z 6..38)
    moat = set()
    for x in range(1, 44):
        for z in range(1, 44):
            inside = 6 <= x <= 38 and 6 <= z <= 38
            ring = 2 <= x <= 42 and 2 <= z <= 42
            if ring and not (5 <= x <= 39 and 5 <= z <= 39):
                moat.add((x, z))
    seal_basin(b, moat, 'lava', 'blackstone', 'blackstone')
    # ---------- bridge (north), with skull spikes
    for z in range(-2, 6):
        for x in range(20, 25): b.set(x, 0, z, 'polished_blackstone_bricks' if (x + z) % 2 else 'blackstone')
        for x in (19, 25): b.set(x, 0, z, 'obsidian')
    for z in range(-2, 6, 2):
        for x in (19, 25):
            b.fill(x, 1, z, x, 3, z, 'nether_brick_fence'); b.set(x, 4, z, P('wither_skeleton_skull', rotation=8 if x == 19 else 8))
    # ---------- curtain wall
    b.walls(6, 1, 6, 38, 10, 38, BK)
    for x in range(6, 39):
        for z in (6, 38):
            if x % 2 == 0: b.set(x, 11, z, 'polished_blackstone_brick_wall')
    for z in range(6, 39):
        for x in (6, 38):
            if z % 2 == 0: b.set(x, 11, z, 'polished_blackstone_brick_wall')
    for x in range(6, 39):
        for y in (4, 7):
            b.set(x, y, 38, 'chiseled_polished_blackstone') if x % 6 == 0 else None
    # ---------- corner towers with spiked black cones
    for (tx, tz) in [(6, 6), (38, 6), (6, 38), (38, 38)]:
        b.tube(tx, 1, 17, tz, 3.6, DK)
        b.ring_windows(tx, tz, 3.6, 10, 13, 4, 'red_stained_glass_pane', 45)
        b.set(tx, 0, tz, 'blackstone')
        b.disc(tx, 18, tz, 5.0, 'blackstone')
        top = b.cone(tx, tz, 5.4, 19, 'blackstone', 'blackstone_stairs', dec=1.0, rmin=0.5)
        b.fill(tx, top + 1, tz, tx, top + 6, tz, 'iron_bars'); b.set(tx, top + 7, tz, 'crying_obsidian')
        for (dx, dz) in ((4, 0), (-4, 0), (0, 4), (0, -4)):
            b.stair(tx + dx, 18, tz + dz, 'blackstone_stairs', {(4, 0): 'west', (-4, 0): 'east', (0, 4): 'north', (0, -4): 'south'}[(dx, dz)])
            b.set(tx + dx, 19, tz + dz, P('wither_skeleton_skull', rotation=0)) if False else None
    # ---------- gatehouse: a giant skull; the gate is its open mouth
    b.fill(15, 1, 4, 29, 16, 9, 'bone_block')
    for x in range(15, 30):
        for y in range(1, 17):
            if (x + y) % 7 == 0: b.set(x, y, 4, 'calcite')
    b.fill(15, 1, 4, 29, 3, 9, DK); b.fill(15, 1, 4, 15, 16, 9, 'bone_block'); b.fill(29, 1, 4, 29, 16, 9, 'bone_block')
    # eyes + nose + brow
    for ex in (18, 25):
        b.fill(ex, 10, 4, ex + 2, 13, 4, 'magma_block'); b.fill(ex + 1, 11, 4, ex + 1, 12, 4, 'shroomlight')
    b.fill(21, 8, 4, 23, 9, 4, 'blackstone'); b.set(22, 9, 4, 'air')
    b.fill(16, 14, 4, 28, 14, 4, 'blackstone'); b.fill(15, 15, 4, 29, 16, 4, 'blackstone')
    # teeth + gate (mouth)
    b.fill(19, 1, 4, 25, 7, 9, 'air')
    for x in range(17, 28):
        b.set(x, 7, 4, 'bone_block' if x % 2 else 'blackstone')
    for x in range(17, 28, 2):
        for y in (4, 5): pass
    for x in (18, 26): b.fill(x, 4, 4, x, 6, 4, 'bone_block')
    for x in range(19, 26): b.fill(x, 4, 5, x, 7, 5, 'iron_bars')          # portcullis
    b.fill(15, 17, 4, 29, 17, 9, BS)
    for x in range(15, 30, 2): b.set(x, 18, 4, 'polished_blackstone_brick_wall'); b.set(x, 18, 9, 'polished_blackstone_brick_wall')
    for x in (16, 22, 28): b.set(x, 19, 4, P('wither_skeleton_skull', rotation=8)) if False else b.set(x, 19, 4, 'air')
    for x in (16, 22, 28):
        b.set(x, 18, 4, 'polished_blackstone_brick_wall'); b.set(x, 19, 4, P('wither_skeleton_skull', rotation=8))
    for x in (19, 25): b.hang_lantern(x, 8, 6, 1, soul=True) if False else None
    b.hang_lantern(21, 8, 7, 1, soul=True); b.hang_lantern(23, 8, 7, 1, soul=True)
    for x in (19, 25): b.wall_torch(x, 3, 8, 'north' if False else 'west' if x == 25 else 'east', soul=True) if False else None
    # ---------- courtyard floor and path
    for z in range(10, 38):
        for x in range(20, 25): b.set(x, 0, z, 'polished_blackstone_bricks' if (x + z) % 2 else 'polished_blackstone')
        b.set(22, 0, z, 'red_concrete') if z % 3 else None
    for z in range(10, 14):
        for x in range(19, 26): b.set(x, 0, z, 'chiseled_polished_blackstone' if (x + z) % 2 else 'polished_blackstone')
    # dead trees
    def dead_tree(x, z, h):
        b.set(x, 0, z, 'coarse_dirt')
        b.fill(x, 1, z, x, h, z, P('dark_oak_log', axis='y'))
        for (dx, dz, f) in ((1, 0, 'x'), (-1, 0, 'x'), (0, 1, 'z'), (0, -1, 'z')):
            y = h - rnd.randint(1, 3)
            b.set(x + dx, y, z + dz, P('dark_oak_log', axis=f)); b.set(x + 2 * dx, y, z + 2 * dz, P('dark_oak_log', axis=f)); b.set(x + 2 * dx, y + 1, z + 2 * dz, P('dark_oak_log', axis='y'))
    for (x, z, h) in [(10, 12, 8), (34, 14, 9), (11, 33, 7), (33, 34, 8)]: dead_tree(x, z, h)
    # graveyard (west of the keep)
    for i, (x, z) in enumerate([(9, 18), (9, 21), (9, 24), (12, 18), (12, 21), (12, 24), (9, 27), (12, 27)]):
        b.set(x, 0, z, 'coarse_dirt'); b.fill(x, 1, z, x, 2, z, 'cobblestone_wall' if False else 'mossy_cobblestone_wall'); b.slab(x, 3, z, 'stone_brick_slab', 'bottom')
        b.set(x + 1, 0, z, 'coarse_dirt'); b.set(x + 1, 1, z, P('skeleton_skull', rotation=rnd.randint(0, 15))) if i % 2 == 0 else None
    # braziers with eerie soul fire
    for (x, z) in [(18, 12), (26, 12), (18, 24), (26, 24), (18, 34), (26, 34)]:
        b.fill(x, 1, z, x, 3, z, 'polished_blackstone_brick_wall'); b.set(x, 4, z, 'soul_soil'); b.set(x, 5, z, P('soul_fire')) if False else b.set(x, 5, z, 'soul_fire')
    # ---------- the keep
    b.fill(14, 1, 14, 30, 22, 30, DK)
    b.carve(15, 1, 15, 29, 20, 29)
    b.fill(14, 23, 14, 30, 23, 30, 'deepslate_tiles')
    for x in range(14, 31, 4):
        for z in (14, 30): b.fill(x, 1, z, x, 23, z, 'polished_deepslate')
    for z in range(14, 31, 4):
        for x in (14, 30): b.fill(x, 1, z, x, 23, z, 'polished_deepslate')
    # buttresses
    for x in (18, 26):
        b.fill(x, 1, 13, x, 14, 13, 'deepslate_bricks')
        for y in range(15, 22): b.set(x, y, 13, 'deepslate_brick_stairs') if False else None
    # tall windows and the rose window
    for z in (18, 22, 26):
        for y0 in (5, 12):
            for x in (14, 30): b.fill(x, y0, z, x, y0 + 3, z, 'red_stained_glass_pane')
    for x in (17, 27):
        b.fill(x, 6, 14, x, 10, 14, 'red_stained_glass_pane') if False else None
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            d = math.hypot(dx, dy)
            if d <= 4.3: b.set(22 + dx, 17 + dy, 14, 'crying_obsidian' if d > 3.3 else 'red_stained_glass' if (dx + dy) % 2 else 'red_stained_glass_pane') if False else b.set(22 + dx, 17 + dy, 14, 'crying_obsidian' if d > 3.2 else 'red_stained_glass')
    # keep door (north) -> through the gate path
    b.carve(21, 1, 14, 23, 5, 14); b.door(21, 1, 14, 'iron_door', 'north', 'left'); b.door(23, 1, 14, 'iron_door', 'north', 'right')
    b.set(22, 1, 14, 'air'); b.set(22, 2, 14, 'air')
    for z in range(11, 14):
        for x in range(20, 25): b.set(x, 0, z, 'blackstone_stairs' if False else 'polished_blackstone_bricks')
    for x in (20, 24): b.fill(x, 1, 12, x, 4, 12, 'polished_blackstone_brick_wall'); b.set(x, 5, 12, 'soul_lantern') if False else b.lantern(x, 5, 12, False, True)
    # upper tower + spire
    b.walls(17, 24, 17, 27, 36, 27, 'deepslate_bricks'); b.fill(17, 24, 17, 27, 24, 27, 'deepslate_tiles')
    for y in (28, 32):
        for x in range(18, 27, 2): b.fill(x, y, 17, x, y + 2, 17, 'red_stained_glass_pane'); b.fill(x, y, 27, x, y + 2, 27, 'red_stained_glass_pane')
    for z in range(18, 27, 2): b.fill(17, 28, z, 17, 30, z, 'red_stained_glass_pane'); b.fill(27, 28, z, 27, 30, z, 'red_stained_glass_pane')
    b.fill(16, 37, 16, 28, 37, 28, 'blackstone')
    top = b.hip(16, 16, 28, 28, 38, 'blackstone_stairs', 'blackstone', 'blackstone_slab')
    b.fill(22, top + 1, 22, 22, top + 10, 22, 'iron_bars'); b.set(22, top + 11, 22, 'crying_obsidian'); b.set(22, top + 12, 22, 'lightning_rod')
    # corner turrets of the keep (black needles)
    for (tx, tz) in [(14, 14), (30, 14), (14, 30), (30, 30)]:
        b.tube(tx, 24, 31, tz, 2.4, 'deepslate_bricks', solid=True)
        tt = b.cone(tx, tz, 3.4, 32, 'blackstone', 'blackstone_stairs', dec=0.7, rmin=0.5)
        b.fill(tx, tt + 1, tz, tx, tt + 5, tz, 'iron_bars')
    # gargoyles + hanging chains on the front of the keep
    for x in (16, 28):
        b.set(x, 20, 13, 'blackstone_stairs') if False else b.stair(x, 20, 13, 'blackstone_stairs', 'north')
        b.set(x, 21, 13, P('wither_skeleton_skull', rotation=0)) if False else None
    # ---------- throne hall interior
    b.fill(15, 0, 15, 29, 0, 29, 'polished_blackstone')
    for x in range(15, 30):
        for z in range(15, 30):
            if (x + z) % 2 == 0: b.set(x, 0, z, 'polished_deepslate')
    for z in range(15, 29): b.fill(21, 0, z, 23, 0, z, 'air') if False else b.set(22, 1, z, 'red_carpet'); 
    for z in range(15, 28):
        for x in (21, 22, 23): b.set(x, 1, z, 'red_carpet')
    for z in (17, 21, 25):
        for x in (17, 27):
            b.fill(x, 1, z, x, 12, z, 'polished_deepslate'); b.set(x, 13, z, 'chiseled_deepslate')
            b.wall_torch(x + 1 if x == 17 else x - 1, 4, z, 'east' if x == 17 else 'west', soul=True)
            b.hang_lantern(x + (2 if x == 17 else -2), 14, z, 0) if False else None
    for z in (17, 21, 25):
        for x in (19, 25): b.hang_lantern(x, 21, z, 4, soul=True) if False else None
    # ceiling beams and chains with soul lanterns (cold blue light in a red-lit hall)
    b.fill(15, 20, 16, 29, 20, 16, P('polished_deepslate')) if False else None
    for z in (17, 22, 27):
        b.fill(15, 21, z, 29, 21, z, 'polished_blackstone_bricks')
        b.fill(15, 20, z, 15, 20, z, 'polished_blackstone_bricks') if False else None
    for z in (17, 22, 27):
        for x in (19, 22, 25): b.hang_lantern(x, 21, z, 3, soul=True)
    # the throne: three-step dais, towering black throne with skulls and spikes
    for i, (z0, h) in enumerate([(26, 1), (27, 2), (28, 3)]):
        b.fill(17, 1, z0, 27, h, 29 if i == 2 else z0 + 0, 'polished_blackstone_bricks') if False else None
    b.fill(17, 1, 26, 27, 1, 29, 'polished_blackstone_bricks')
    b.fill(18, 2, 27, 26, 2, 29, 'polished_blackstone_bricks')
    b.fill(20, 3, 28, 24, 3, 29, 'polished_blackstone_bricks')
    for x in range(21, 24): b.set(x, 1, 26, 'red_carpet') if False else None
    b.stair(22, 4, 28, 'nether_brick_stairs', 'north')
    b.fill(20, 4, 29, 24, 12, 29, 'blackstone')
    b.fill(21, 4, 28, 21, 6, 28, 'nether_brick_fence') if False else None
    for x in (20, 24): b.fill(x, 4, 28, x, 5, 28, 'blackstone'); b.slab(x, 6, 28, 'blackstone_slab', 'bottom')
    b.fill(22, 5, 29, 22, 12, 29, 'crying_obsidian')
    for x in (20, 24): b.fill(x, 13, 29, x, 16, 29, 'iron_bars')
    b.fill(19, 4, 29, 19, 9, 29, 'blackstone'); b.fill(25, 4, 29, 25, 9, 29, 'blackstone')
    b.set(19, 10, 29, P('wither_skeleton_skull', rotation=8)) if False else None
    for x in (19, 25): b.set(x, 10, 29, 'bone_block'); b.set(x, 11, 29, 'iron_bars'); b.set(x, 12, 29, 'iron_bars')
    b.set(21, 13, 29, 'bone_block'); b.set(23, 13, 29, 'bone_block')
    for x in (18, 26): b.set(x, 3, 28, P('soul_campfire', facing='north', lit=True, signal_fire=False, waterlogged=False)) if False else None
    for x in (18, 26):
        b.fill(x, 3, 27, x, 3, 27, 'polished_blackstone_brick_wall'); b.set(x, 4, 27, P('soul_campfire', facing='north', lit=True, signal_fire=False, waterlogged=False))
    # skull braziers at the hall entrance + cobwebs in the corners
    for (x, y, z) in [(15, 12, 15), (29, 12, 15), (15, 12, 29), (29, 12, 29), (15, 19, 15), (29, 19, 15), (15, 19, 29), (29, 19, 29), (15, 20, 22), (29, 20, 22)]:
        b.set(x, y, z, 'cobweb')
    # chains hanging from the ceiling with swinging cages (iron bars)
    for (x, z) in [(18, 20), (26, 20), (18, 24), (26, 24)]:
        b.fill(x, 15, z, x, 20, z, P('chain', axis='y')); b.fill(x, 12, z, x, 14, z, 'iron_bars')
    # bone-pile + lava crack in front of the dais
    for (x, z) in [(17, 20), (27, 19), (17, 24), (27, 23)]:
        b.set(x, 1, z, 'bone_block'); b.set(x + (1 if x == 17 else -1), 1, z, P('skeleton_skull', rotation=rnd.randint(0, 15)))
    # skulls impaled on spikes along the courtyard
    for (x, z) in [(17, 14), (27, 14), (17, 36), (27, 36), (12, 14), (32, 14)]:
        b.set(x, 0, z, 'blackstone'); b.fill(x, 1, z, x, 4, z, 'nether_brick_fence'); b.set(x, 5, z, P('wither_skeleton_skull', rotation=rnd.randint(0, 15)))
    return b


def guild_hall():
    rnd = random.Random(9)
    b = Build('fairy_guild_hall', 'Fairy Tail', 'Гильдия магов (Фейри Тейл)', foundation='stone_bricks')
    X1, X2, Z1, Z2 = 0, 24, 0, 16
    b.fill(X1, 0, Z1, X2, 0, Z2, 'spruce_planks')
    for x in range(X1, X2 + 1):
        for z in range(Z1, Z2 + 1):
            if (x + z) % 4 == 0: b.set(x, 0, z, 'oak_planks')
    b.walls(X1, 1, Z1, X2, 2, Z2, 'stone_bricks')
    b.walls(X1, 3, Z1, X2, 9, Z2, 'white_terracotta')
    for x in range(X1, X2 + 1, 4):
        for z in (Z1, Z2): b.fill(x, 1, z, x, 9, z, P('dark_oak_log', axis='y'))
    for z in range(Z1, Z2 + 1, 4):
        for x in (X1, X2): b.fill(x, 1, z, x, 9, z, P('dark_oak_log', axis='y'))
    for y in (5, 9):
        b.fill(X1, y, Z1, X2, y, Z1, P('dark_oak_log', axis='x')); b.fill(X1, y, Z2, X2, y, Z2, P('dark_oak_log', axis='x'))
        b.fill(X1, y, Z1, X1, y, Z2, P('dark_oak_log', axis='z')); b.fill(X2, y, Z1, X2, y, Z2, P('dark_oak_log', axis='z'))
    b.fill(1, 5, 1, X2 - 1, 5, Z2 - 1, 'spruce_planks')                     # mezzanine floor (carved in the middle later)
    # roof
    t = b.hip_low(-2, -2, X2 + 2, Z2 + 2, 10, 'brick_stairs', 'brick_slab', 'dark_oak_planks', rings=7)
    # windows
    for x in (2, 3, 6, 7, 10, 11, 14, 15, 18, 19, 22):
        for z in (Z1, Z2):
            b.fill(x, 3, z, x, 4, z, 'glass_pane'); b.fill(x, 7, z, x, 8, z, 'glass_pane') if x % 4 != 0 else None
    # grand entrance (north): double door, step, sign beam
    b.carve(11, 1, Z1, 13, 4, Z1); b.door(11, 1, Z1, 'spruce_door', 'north', 'left'); b.door(13, 1, Z1, 'spruce_door', 'north', 'right'); b.set(12, 1, Z1, 'spruce_door') if False else None
    b.carve(12, 1, Z1, 12, 4, Z1); b.fill(12, 1, Z1, 12, 3, Z1, 'glass_pane')
    for z in range(-5, 0):
        b.fill(10, 0, z, 14, 0, z, 'stone_bricks' if z % 2 else 'polished_andesite')
    b.fill(9, 5, -1, 15, 5, -1, 'dark_oak_planks'); b.fill(9, 6, -1, 15, 6, -1, 'orange_wool')
    for x in (9, 15): b.fill(x, 1, -1, x, 4, -1, P('dark_oak_log', axis='y'))
    for x in (10, 14): b.hang_lantern(x, 5, -1, 1)
    # central round tower with spired roof and a guild flag
    cx, cz = 12, 8
    b.tube(cx, 10, 20, cz, 4.4, 'white_terracotta')
    for ang in range(0, 360, 45):
        x, z = b.ring_cell(cx, cz, 4.4, ang); b.fill(x, 10, z, x, 20, z, P('dark_oak_log', axis='y'))
    b.ring_windows(cx, cz, 4.4, 14, 16, 4, 'glass_pane', 22)
    b.disc(cx, 9, cz, 4.8, 'spruce_planks')
    tt = b.cone(cx, cz, 6.4, 21, 'bricks', 'brick_stairs', dec=1.2, rmin=0.5, first_solid=True)
    b.fill(cx, tt + 1, cz, cx, tt + 8, cz, 'spruce_fence')
    for dy, w in ((7, 4), (6, 4), (5, 3), (4, 2)):
        for dx in range(1, w + 1): b.set(cx + dx, tt + dy, cz, 'blue_wool' if dy > 5 else 'white_wool')
    # interior: bar, tables, request board, chandeliers
    b.carve(5, 5, 4, X2 - 5, 5, Z2 - 4)
    for x in range(5, X2 - 4): b.set(x, 5, 4, 'spruce_fence'); b.set(x, 5, Z2 - 4, 'spruce_fence')
    for z in range(4, Z2 - 3): b.set(5, 5, z, 'spruce_fence'); b.set(X2 - 5, 5, z, 'spruce_fence')
    b.ladder(1, 1, 5, 12, 'east') if False else None
    for x in range(14, 22): b.set(x, 1, 13, 'dark_oak_planks'); b.slab(x, 2, 13, 'dark_oak_slab', 'bottom')
    for x in range(13, 22): b.set(x, 1, 15, 'barrel') if x % 2 else b.set(x, 1, 15, 'bookshelf')
    for x in range(14, 22): b.set(x, 2, 15, 'bookshelf') if x % 3 == 0 else None
    for (x, z) in [(4, 5), (4, 9), (8, 5), (8, 9), (17, 5), (21, 5), (17, 9), (21, 9), (4, 13)]:
        b.set(x, 1, z, 'spruce_fence'); b.slab(x, 2, z, 'spruce_slab', 'bottom'); b.stair(x - 1, 1, z, 'spruce_stairs', 'east'); b.stair(x + 1, 1, z, 'spruce_stairs', 'west')
    for z in (4, 6, 8, 10): b.set(1, 1, z, 'bookshelf'); b.set(1, 2, z, 'bookshelf'); b.set(1, 3, z, 'bookshelf') if z in (6,) else None
    for x in (7, 12, 17):
        b.fill(x, 9, 1, x, 9, Z2 - 1, P('dark_oak_log', axis='z')); b.hang_lantern(x, 9, 8, 2); b.hang_lantern(x, 9, 11, 2)
    b.chest(2, 1, 14, 'north'); b.chest(3, 1, 14, 'north'); b.set(22, 1, 14, 'barrel'); b.set(22, 1, 12, 'lectern')
    b.bed(2, 6, 2, 'blue', 'east'); b.bed(2, 6, 12, 'red', 'east'); b.bed(21, 6, 2, 'white', 'west'); b.bed(21, 6, 12, 'yellow', 'west')
    for x in range(8, 17): b.fill(x, 6, 15, x, 7, 15, 'bookshelf') if x % 2 == 0 else None
    b.fill(2, 5, 1, 2, 5, 1, 'spruce_planks')
    # side wings: two small gabled bay roofs + banners
    for x in (-1, X2 + 1):
        pass
    for x in (3, 21): b.fill(x, 1, -1, x, 3, -1, 'spruce_fence'); b.lantern(x, 4, -1)
    scatter(b, rnd, [(-4, -8, 28, -3), (-5, 18, 29, 22)], 24, ['poppy', 'dandelion', 'cornflower', 'oxeye_daisy', 'azure_bluet'],
            avoid=lambda x, z: 8 <= x <= 16 and z < 1)
    for (x, z, h) in [(-6, 4, 8), (30, 10, 9)]:
        tree(b, x, z, h, 'oak', crown=3.0, rnd=rnd)
    return b


def all_builds():
    return [dark_castle(), guild_hall()]
