import random
from mcgen import *
from common import *


def hokage():
    b = Build('hokage_building', 'Naruto', 'Здание Хокаге (Коноха)', foundation='stone_bricks')
    cx = cz = 13
    RB, RS = 'red_nether_bricks', 'red_nether_brick_stairs'
    b.disc(cx, 0, cz, 13, 'stone_bricks'); b.ring(cx, 0, cz, 13, 'smooth_stone'); b.disc(cx, 0, cz, 8, 'spruce_planks')
    for z in range(cz - 13, cz - 7): b.fill(cx - 2, 0, z, cx + 2, 0, z, 'stone_bricks' if z % 2 else 'polished_andesite')
    # tier 1 (tall white drum with dark timber ribs)
    b.tube(cx, 1, 9, cz, 7.5, 'white_terracotta')
    for ang in range(0, 360, 30):
        x, z = b.ring_cell(cx, cz, 7.5, ang)
        b.fill(x, 1, z, x, 9, z, 'stripped_spruce_log' if False else P('spruce_log', axis='y'))
    b.ring_windows(cx, cz, 7.5, 4, 6, 12, 'glass_pane', 15)
    b.carve(cx - 1, 1, cz - 8, cx + 1, 4, cz - 7); b.door(cx, 1, cz - 8, 'dark_oak_door', 'north')
    for x in (cx - 2, cx + 2): b.fill(x, 1, cz - 8, x, 3, cz - 8, 'spruce_fence'); b.lantern(x, 4, cz - 8)
    top1 = b.cone(cx, cz, 11, 10, RB, RS, dec=3, rmin=5)
    # tier 2
    b.tube(cx, top1 + 1, top1 + 7, cz, 5.5, 'white_terracotta')
    for ang in range(0, 360, 45):
        x, z = b.ring_cell(cx, cz, 5.5, ang); b.fill(x, top1 + 1, z, x, top1 + 7, z, P('spruce_log', axis='y'))
    b.ring_windows(cx, cz, 5.5, top1 + 3, top1 + 5, 8, 'glass_pane', 22)
    top2 = b.cone(cx, cz, 8, top1 + 8, RB, RS, dec=3, rmin=3)
    # tier 3 (the Hokage office)
    b.tube(cx, top2 + 1, top2 + 5, cz, 3.4, 'white_terracotta')
    for ang in range(0, 360, 90):
        x, z = b.ring_cell(cx, cz, 3.4, ang); b.fill(x, top2 + 1, z, x, top2 + 5, z, P('spruce_log', axis='y'))
    b.ring_windows(cx, cz, 3.4, top2 + 2, top2 + 4, 4, 'glass_pane', 45)
    top3 = b.cone(cx, cz, 6.5, top2 + 6, RB, RS, dec=1.5, rmin=0.5, first_solid=True)
    b.set(cx, top3 + 1, cz, 'gold_block'); b.set(cx, top3 + 2, cz, 'lightning_rod')
    for ang in range(0, 360, 30):
        x, z = b.ring_cell(cx, cz, 10.2, ang)
        if (x, 10, z) in b.b and (x, 9, z) not in b.b: b.lantern(x, 9, z, True)
    # interior: office + ladders between floors
    b.fill(cx - 4, top1, cz - 4, cx + 4, top1, cz + 4, 'spruce_planks') if False else None
    b.set(cx, 1, cz + 5, 'lectern'); b.set(cx - 2, 1, cz + 5, 'bookshelf'); b.set(cx + 2, 1, cz + 5, 'bookshelf')
    b.ladder(cx + 5, 1, top1, cz, 'west')
    return b


def ichiraku():
    b = Build('ichiraku_ramen', 'Naruto', 'Лавка рамэна Ичираку', foundation='cobblestone')
    b.fill(0, 0, 0, 10, 0, 8, 'spruce_planks')
    b.walls(0, 1, 2, 10, 4, 8, 'white_terracotta')
    for x in (0, 10):
        for z in (2, 8): b.column(x, 1, 4, z, P('dark_oak_log', axis='y'))
    b.fill(0, 5, 2, 10, 5, 8, 'dark_oak_planks')
    top = b.gable_low(-1, 11, 1, 9, 6, 'dark_oak_stairs', 'dark_oak_slab', 'dark_oak_planks', gable_fill='white_terracotta', gspan=(0, 10))
    # open counter front (z=2 wall removed, replaced by bar)
    b.carve(1, 1, 2, 9, 3, 2)
    for x in range(1, 10): b.set(x, 1, 2, P('spruce_slab', type='top')) if False else None
    for x in range(1, 10): b.stair(x, 1, 2, 'spruce_stairs', 'north', 'top') if False else b.set(x, 1, 2, 'spruce_planks')
    for x in range(1, 10): b.slab(x, 2, 2, 'spruce_slab', 'bottom')
    for x in (2, 4, 6, 8): b.set(x, 1, 1, 'barrel') if False else b.stair(x, 1, 0, 'spruce_stairs', 'south') if False else None
    for x in (2, 4, 6, 8): b.set(x, 1, 0, 'barrel') if False else None
    for x in (2, 4, 6, 8): b.set(x, 1, 1, 'spruce_slab') if False else b.slab(x, 1, 1, 'spruce_slab', 'bottom')   # stools
    # noren curtains (red/white banners)
    for x in range(1, 10): b.set(x, 4, 2, 'red_wool' if x % 2 else 'white_wool')
    for x in (0, 10): b.set(x, 3, 2, 'dark_oak_fence')
    # kitchen
    b.set(2, 1, 5, 'smoker'); b.set(3, 1, 5, 'barrel'); b.set(4, 1, 5, P('water_cauldron', level=3)); b.set(8, 1, 5, 'crafting_table') if False else None
    b.set(6, 1, 5, 'cauldron'); b.set(7, 1, 5, P('furnace', facing='south', lit=False)); b.chest(8, 1, 7, 'north'); b.set(9, 1, 7, 'barrel')
    b.set(5, 2, 5, 'air') if False else None
    for x in (3, 5, 7): b.hang_lantern(x, 5, 4, 1)
    for x in (2, 8): b.set(x, 3, 3, 'air') if False else None
    b.fill(0, 2, 5, 0, 3, 6, 'glass_pane'); b.fill(10, 2, 5, 10, 3, 6, 'glass_pane')
    b.door(5, 1, 8, 'spruce_door', 'south')
    b.set(1, 1, 7, 'potted_fern'); b.set(1, 1, 6, 'bookshelf')
    # sign + lanterns + front decor
    b.fill(0, 6, 2, 10, 6, 2, 'air') if False else None
    for x in (1, 9): b.fill(x, 1, 0, x, 2, 0, 'spruce_fence'); b.lantern(x, 3, 0)
    for x in (3, 5, 7): b.set(x, 3, 0, 'air') if False else None
    b.set(5, 1, -1, 'potted_cornflower') if False else None
    return b


def bathhouse():
    b = Build('spirit_bathhouse', 'Studio Ghibli', 'Купальня духов', foundation='stone_bricks')
    R = 'red_nether_bricks'; CS, CB, CSL = 'cut_copper_stairs', 'cut_copper', 'cut_copper_slab'
    b.fill(-3, 0, -4, 23, 0, 17, 'stone_bricks')
    for z in range(-16, -4):                              # lantern bridge
        b.fill(8, 0, z, 12, 0, z, 'red_terracotta' if z % 2 else 'crimson_planks')
        b.set(7, 0, z, 'crimson_planks'); b.set(13, 0, z, 'crimson_planks')
        b.set(7, 1, z, 'crimson_fence'); b.set(13, 1, z, 'crimson_fence')
        if z % 4 == 0:
            b.fill(7, 2, z, 7, 2, z, 'crimson_fence'); b.fill(13, 2, z, 13, 2, z, 'crimson_fence'); b.lantern(7, 3, z); b.lantern(13, 3, z)
    # tier 1: long hall
    b.walls(0, 1, 0, 20, 7, 14, R)
    b.fill(1, 0, 1, 19, 0, 13, 'spruce_planks')
    for x in range(2, 19, 2):
        for z in (0, 14): b.fill(x, 3, z, x, 5, z, 'glass_pane') if x != 10 else None
    for x in range(0, 21, 4):
        b.fill(x, 1, 0, x, 7, 0, P('crimson_stem', axis='y')); b.fill(x, 1, 14, x, 7, 14, P('crimson_stem', axis='y'))
    b.carve(9, 1, 0, 11, 5, 0); b.door(10, 1, 0, 'crimson_door', 'north'); b.fill(9, 6, 0, 11, 6, 0, 'gold_block') if False else None
    b.fill(-1, 8, -2, 21, 8, 16, CB)
    t1 = b.hip_low(-3, -4, 23, 18, 8, CS, CSL, 'dark_oak_planks', rings=5)
    # tier 2
    b.walls(3, t1 + 1, 2, 17, t1 + 6, 12, 'red_concrete')
    for x in range(5, 16, 2):
        for z in (2, 12): b.fill(x, t1 + 3, z, x, t1 + 5, z, 'glass_pane')
    for x in (3, 10, 17):
        b.fill(x, t1 + 1, 2, x, t1 + 6, 2, P('gold_block')) if False else b.fill(x, t1 + 1, 2, x, t1 + 6, 2, P('crimson_stem', axis='y'))
    t2 = b.hip_low(1, 0, 19, 14, t1 + 7, CS, CSL, 'dark_oak_planks', rings=4)
    # tier 3: tower with the big gabled crest
    b.walls(6, t2 + 1, 4, 14, t2 + 6, 10, 'red_terracotta')
    for x in (8, 10, 12): b.fill(x, t2 + 3, 4, x, t2 + 5, 4, 'glass_pane')
    t3 = b.hip_low(4, 2, 16, 12, t2 + 7, CS, CSL, 'dark_oak_planks', rings=99)
    b.set(10, t3 + 1, 7, 'gold_block'); b.set(10, t3 + 2, 7, 'lightning_rod')
    for x in range(-2, 23, 4):
        if (x, 8, -3) in b.b or (x, 9, -4) in b.b: pass
    for x in range(0, 21, 4): b.lantern(x, 7, -1, True) if (x, 8, -1) in b.b and (x, 7, -1) not in b.b else None
    # interior: tatami hall and a bath
    for x in range(2, 10):
        for z in range(2, 13): b.set(x, 1, z, 'red_carpet')
    b.fill(12, 0, 3, 18, 0, 12, 'polished_andesite')
    b.set(3, 1, 12, 'barrel'); b.set(4, 1, 12, 'barrel'); b.chest(5, 1, 12, 'north'); b.set(8, 1, 12, 'lectern')
    for x in (4, 8, 15): b.hang_lantern(x, 8, 8, 2)
    return b


