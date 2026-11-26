import random
from mcgen import *
from common import *

CAT = 'Sword Art Online'


def cottage():
    """22nd floor log cabin by the lake: warm, quiet, cosy."""
    rnd = random.Random(22)
    b = Build('kirito_asuna_cottage', CAT, 'Домик Кирито и Асуны (22-й этаж)', foundation='dirt')
    X1, X2, Z1, Z2 = 6, 16, 0, 8
    LOG, CORNER, PLANK = 'oak_log', 'stripped_oak_log', 'oak_planks'
    WALL_TOP = 7

    pond(b, -4, -3, 8, 6)
    # ---------- floor
    b.fill(X1, 0, Z1, X2, 0, Z2, 'spruce_planks')
    for x in range(X1 + 1, X2):
        for z in range(Z1 + 1, Z2):
            if (x * 2 + z) % 3 == 0: b.set(x, 0, z, PLANK)
    # ---------- log walls, stone base course
    for y in range(1, WALL_TOP + 1):
        for x in range(X1, X2 + 1):
            for z in (Z1, Z2): b.set(x, y, z, P(LOG, axis='x'))
        for z in range(Z1, Z2 + 1):
            for x in (X1, X2): b.set(x, y, z, P(LOG, axis='z'))
    for x in range(X1, X2 + 1):
        for z in range(Z1, Z2 + 1):
            if x in (X1, X2) or z in (Z1, Z2):
                b.set(x, 1, z, 'mossy_cobblestone' if (x + z) % 3 == 0 else 'cobblestone')
    for (x, z) in [(X1, Z1), (X2, Z1), (X1, Z2), (X2, Z2)]:
        b.fill(x, 2, z, x, WALL_TOP, z, P(CORNER, axis='y'))
    # ---------- openings
    b.door(11, 1, Z1, 'spruce_door', 'north')
    for x in (8, 9, 13, 14): b.fill(x, 2, Z1, x, 3, Z1, 'glass_pane')
    for x in (7, 10, 12, 15):
        for y in (2, 3): b.trap(x, y, Z1 - 1, 'spruce_trapdoor', 'south', True)
    b.fill(10, 5, Z1, 12, 6, Z1, 'glass_pane')                         # loft window above door
    for z in (2, 3, 5, 6): b.fill(X1, 2, z, X1, 3, z, 'glass_pane')
    for x in (8, 9, 13, 14): b.fill(x, 2, Z2, x, 3, Z2, 'glass_pane')
    b.fill(10, 5, Z2, 12, 6, Z2, 'glass_pane')
    for z in (6,): b.fill(X2, 2, z, X2, 3, z, 'glass_pane')
    for (wx, wz, dx) in [(X1, 2, -1), (X1, 6, -1)]:                    # flower boxes on the lake side
        pass
    # ---------- roof: porch + loft under one low gable
    top = b.gable_low(X1 - 1, X2 + 1, Z1 - 3, Z2 + 1, WALL_TOP + 1, 'spruce_stairs', 'spruce_slab', 'spruce_planks', gable_fill=PLANK, gspan=(X1, X2))
    for gx in (X1, X2):
        b.fill(gx, 8, 3, gx, 9, 3, 'glass_pane')
    # roof ridge accent + eaves lanterns
    for x in range(X1 - 1, X2 + 2):
        b.set(x, top, 3, P('spruce_log', axis='x')) if False else None
    # ---------- loft floor with dark beams
    b.fill(X1 + 1, 4, 4, X2 - 2, 4, Z2 - 1, 'spruce_planks')
    for x in range(X1 + 1, X2 - 1):
        if x % 3 == 0: b.fill(x, 4, 4, x, 4, Z2 - 1, P('dark_oak_log', axis='z'))
    b.fill(X1 + 1, 4, 4, X2 - 2, 4, 4, P('dark_oak_log', axis='x'))
    # ---------- porch
    b.fill(X1, 0, Z1 - 3, X2, 0, Z1 - 1, 'spruce_planks')
    for x in range(X1, X2 + 1):
        for z in range(Z1 - 3, Z1):
            if (x + z) % 2: b.set(x, 0, z, 'oak_planks')
    for x in (X1, 11, X2): b.fill(x, 1, Z1 - 3, x, WALL_TOP, Z1 - 3, P('dark_oak_log', axis='y'))
    for x in range(X1 + 1, X2):
        if x not in (10, 11, 12): b.set(x, 1, Z1 - 3, 'spruce_fence')
    for z in (Z1 - 2, Z1 - 1):
        b.set(X1, 1, z, 'spruce_fence'); b.set(X2, 1, z, 'spruce_fence')
    for z in range(Z1 - 9, Z1 - 3):
        for x in (10, 11, 12): b.set(x, 0, z, 'stone_bricks' if (x + z) % 2 else 'mossy_stone_bricks')
    for x in (8, 14): b.hang_lantern(x, WALL_TOP + 1, Z1 - 3, 1) if False else None
    b.lantern(8, 2, Z1 - 3) if False else None
    for x in (8, 14):
        b.set(x, 1, Z1 - 3, 'spruce_fence'); b.set(x, 2, Z1 - 3, 'spruce_fence'); b.lantern(x, 3, Z1 - 3)
    b.hang_lantern(11, WALL_TOP + 1, Z1 - 2, 2)
    b.stair(8, 1, Z1 - 2, 'spruce_stairs', 'north'); b.stair(9, 1, Z1 - 2, 'spruce_stairs', 'north')
    b.set(13, 1, Z1 - 2, 'barrel'); b.set(14, 1, Z1 - 2, 'barrel'); b.set(13, 2, Z1 - 2, 'potted_azalea_bush'); b.lantern(14, 2, Z1 - 2)
    b.set(7, 1, Z1 - 1, 'potted_cornflower'); b.set(15, 1, Z1 - 1, 'potted_oxeye_daisy')
    # ---------- dock
    for x in range(-9, X1):
        for z in (Z1 - 3, Z1 - 2):
            b.set(x, 0, z, 'spruce_planks' if (x + z) % 2 else 'oak_planks')
    for x in range(-9, X1, 3):
        for z in (Z1 - 3, Z1 - 2): b.fill(x, -3, z, x, -1, z, P('spruce_log', axis='y'))
    b.fill(-9, 1, Z1 - 3, -9, 2, Z1 - 3, 'spruce_fence'); b.lantern(-9, 3, Z1 - 3)
    b.stair(-8, 1, Z1 - 2, 'spruce_stairs', 'north'); b.stair(-7, 1, Z1 - 2, 'spruce_stairs', 'north'); b.set(-5, 1, Z1 - 2, 'barrel')
    # ---------- chimney + fireplace (east)
    for y in range(0, 14):
        for x in (15, 16, 17):
            for z in (3, 4):
                b.set(x, y, z, 'cobblestone' if (x * 3 + y + z) % 5 == 0 else 'stone_bricks')
    b.carve(15, 1, 3, 15, 2, 4)
    for z in (3, 4):
        b.set(15, 1, z, P('campfire', facing='west', lit=True, signal_fire=False, waterlogged=False))
        b.stair(14, 1, z, 'stone_brick_stairs', 'west')
    for (x, z) in [(15, 3), (16, 3), (17, 3), (15, 4), (16, 4), (17, 4)]:
        b.set(x, 14, z, 'stone_brick_wall')
    b.set(16, 14, 3, P('campfire', facing='north', lit=True, signal_fire=False, waterlogged=False))
    b.set(14, 4, 3, 'air'); 
    b.candle(14, 2, 3) if False else None
    # ---------- stairs to loft (west wall)
    for i, z in enumerate(range(1, 5)):
        b.stair(7, 1 + i, z, 'spruce_stairs', 'south')
        for yy in range(1, 1 + i): b.set(7, yy, z, 'spruce_planks')
    for x in range(8, 15): b.set(x, 5, 4, 'spruce_fence')
    # ---------- living room
    for x in range(9, 14):
        for z in range(2, 6):
            b.set(x, 1, z, 'red_carpet' if (x + z) % 2 == 0 and (x in (9, 13) or z in (2, 5)) else 'white_carpet')
    for z in (3, 4, 5): b.stair(9, 1, z, 'spruce_stairs', 'east')
    b.slab(11, 1, 4, 'spruce_slab', 'top'); b.slab(12, 1, 4, 'spruce_slab', 'top')
    b.candle(11, 2, 4, 'white', 2); b.set(12, 2, 4, 'potted_lily_of_the_valley')
    b.set(10, 1, 1, 'potted_fern'); b.set(12, 1, 1, 'barrel')
    b.stair(13, 1, 4, 'spruce_stairs', 'west'); b.stair(13, 1, 5, 'spruce_stairs', 'west') if False else None
    # bookshelves on the west wall nook
    for z in (5, 6, 7):
        for y in (1, 2, 3): b.set(8, y, z, 'bookshelf')
    b.set(8, 4, 7, 'air') if False else None
    # kitchen along back wall
    b.set(10, 1, 7, 'barrel'); b.set(11, 1, 7, P('smoker', facing='north', lit=False)); b.set(12, 1, 7, P('water_cauldron', level=3))
    b.set(13, 1, 7, 'crafting_table'); b.set(14, 1, 7, P('furnace', facing='north', lit=False)); b.chest(15, 1, 7, 'north')
    for x in (10, 11, 13, 14): b.slab(x, 3, 7, 'spruce_slab', 'bottom')
    b.set(10, 4, 7, 'potted_dandelion') if False else None
    b.set(11, 2, 7, 'air') if False else None
    # hanging lanterns in the tall front room (from the z=2 roof beam)
    for x in (9, 13): b.hang_lantern(x, 9, 2, 2)
    b.hang_lantern(11, 9, 2, 3)
    # ---------- loft
    for x in range(8, 14):
        for z in range(5, 8): b.set(x, 5, z, 'light_gray_carpet' if (x + z) % 2 else 'white_carpet')
    b.bed(11, 5, 5, 'white', 'south'); b.bed(12, 5, 5, 'light_blue', 'south')
    b.set(10, 5, 7, 'barrel'); b.set(13, 5, 7, 'barrel'); b.lantern(10, 6, 7); b.lantern(13, 6, 7)
    b.set(9, 5, 7, 'bookshelf'); b.set(9, 6, 7, 'bookshelf'); b.set(8, 5, 7, 'bookshelf')
    b.stair(8, 5, 5, 'spruce_stairs', 'east'); b.set(8, 5, 6, 'lectern') if False else None
    b.hang_lantern(12, 8, 6, 0)
    # ---------- fire pit by the lake, garden, trees, flowers
    for (x, z) in [(2, 4), (3, 4), (4, 4), (2, 5), (4, 5), (2, 6), (3, 6), (4, 6), (3, 5)]:
        b.set(x, 0, z, 'stone_bricks' if (x + z) % 2 else 'cobblestone')
    b.set(3, 1, 5, P('campfire', facing='north', lit=True, signal_fire=False, waterlogged=False))
    b.stair(1, 1, 5, 'spruce_stairs', 'east') if False else None
    b.set(3, 0, 5, 'stone_bricks')
    b.set(0, 0, 5, 'grass_block')
    for (x, z, f) in [(1, 5, 'east'), (5, 5, 'west'), (3, 3, 'south'), (3, 7, 'north')]:
        b.set(x, 0, z, 'grass_block' if (x, 0, z) not in b.b else b.b[(x, 0, z)])
        b.stair(x, 1, z, 'spruce_stairs', f)
    path(b, [(x, 4) for x in (5,)], 'dirt_path') if False else None
    for (x, z, h, k) in [(21, 4, 8, 'oak'), (22, 11, 9, 'oak'), (18, 14, 7, 'birch'), (4, 12, 9, 'oak'), (-8, 9, 8, 'oak'), (-12, 3, 7, 'birch'),
                         (25, -2, 8, 'oak'), (12, 14, 8, 'oak'), (-3, 14, 8, 'birch')]:
        tree(b, x, z, h, k, crown=3.2, rnd=rnd)
    for (x, z, h) in [(-11, -9, 8), (24, 9, 10), (-14, 9, 9)]:
        conifer(b, x, z, h, rnd=rnd)
    scatter(b, rnd, [(-13, -12, 5, -8), (17, -10, 28, 15), (-13, 5, 5, 15), (6, 10, 27, 16), (0, -12, 28, -5), (-1, 7, 6, 12)], 70,
            ['poppy', 'dandelion', 'cornflower', 'azure_bluet', 'oxeye_daisy', 'allium', 'lily_of_the_valley', 'fern'],
            avoid=lambda x, z: (X1 - 2 <= x <= X2 + 4 and Z1 - 5 <= z <= Z2 + 2) or (-14 <= x <= 5 and -10 <= z <= 3) or (1 <= x <= 5 and 3 <= z <= 7) or (9 <= x <= 13 and z < 0))
    for (x, z) in [(-8, -5), (-2, -1), (-6, 0), (0, -6), (-9, -2), (-5, -7)]:
        if b.get(x, -1, z) and b.get(x, -1, z)[0] == 'water' and (x, 0, z) not in b.b or (b.get(x, 0, z) and b.get(x, 0, z)[0] == 'air'):
            if b.get(x, -1, z) and b.get(x, -1, z)[0] == 'water': b.set(x, 0, z, 'lily_pad')
    b.set(5, 0, 3, 'grass_block'); b.set(5, 1, 3, 'azalea'); b.set(5, 0, 7, 'grass_block'); b.set(5, 1, 7, 'flowering_azalea')
    b.set(17, 0, 7, 'grass_block'); b.set(17, 1, 7, 'azalea'); b.set(17, 0, 1, 'grass_block'); b.set(17, 1, 1, 'flowering_azalea')
    return b


def all_builds():
    return [cottage()]
