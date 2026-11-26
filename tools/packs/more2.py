import random, math
from mcgen import *
from common import *


def shrine():
    rnd = random.Random(31)
    b = Build('itomori_shrine', 'Your Name', 'Святилище Миямидзу на холме', foundation='cobblestone')
    X1, X2 = 1, 19
    def surf(z):
        if z < 3: return 0
        if z < 9: return z - 3 + 1          # flight 1: 1..6
        if z < 12: return 6
        if z < 18: return 6 + (z - 12) + 1  # flight 2: 7..12
        if z < 21: return 12
        return 12
    for z in range(0, 40):
        h = surf(z)
        for x in range(X1, X2 + 1):
            for y in range(0, h):
                b.set(x, y, z, 'cobblestone' if (x in (X1, X2) or z in (0,)) else 'dirt')
            top = 'grass_block' if h > 0 or z >= 3 else 'grass_block'
            b.set(x, h, z, top) if not (8 <= x <= 12) else None
        for x in range(8, 13):                                   # stone path / steps
            step = (3 <= z < 9) or (12 <= z < 18)
            if step:
                for y in range(0, h): b.set(x, y, z, 'cobblestone')
                b.stair(x, h, z, 'stone_brick_stairs', 'north')
            else:
                for y in range(0, h): b.set(x, y, z, 'cobblestone')
                b.set(x, h, z, 'stone_bricks' if (x + z) % 2 else 'mossy_stone_bricks')
    # retaining wall edge
    for z in range(3, 21):
        h = surf(z)
        for x in (X1, X2): b.set(x, h, z, 'stone_brick_wall') if False else None
    # torii gates
    for (z, h) in ((1, 0), (10, 6)):
        for x in (7, 13): b.fill(x, h + 1, z, x, h + 7, z, 'red_terracotta')
        b.fill(6, h + 8, z, 14, h + 8, z, 'black_concrete'); b.fill(7, h + 6, z, 13, h + 6, z, 'red_terracotta') if False else b.fill(8, h + 6, z, 12, h + 6, z, 'red_terracotta')
        b.fill(7, h + 7, z, 13, h + 7, z, 'red_terracotta') if False else None
        b.slab(5, h + 8, z, 'black_concrete') if False else None
        b.set(6, h + 9, z, 'black_concrete') if False else None
    b.fill(6, 8, 1, 14, 8, 1, 'black_concrete'); b.fill(5, 9, 1, 15, 9, 1, 'black_concrete')
    # stone lanterns along the stairs
    for (z, h) in ((4, 2), (7, 5), (13, 8), (16, 11), (10, 6), (19, 12)):
        for x in (7, 13):
            b.set(x, h + 1, z, 'mossy_cobblestone_wall'); b.set(x, h + 2, z, 'mossy_cobblestone_wall'); b.lantern(x, h + 3, z)
    # main hall on the summit
    H0 = 12
    b.fill(3, H0, 22, 17, H0, 34, 'stone_bricks')
    for x in range(3, 18):
        for z in range(22, 35): b.set(x, H0, z, 'stone_bricks' if (x + z) % 3 else 'polished_andesite')
    b.walls(5, H0 + 1, 24, 15, H0 + 5, 32, 'white_terracotta')
    for (x, z) in [(5, 24), (15, 24), (5, 32), (15, 32), (10, 24), (10, 32), (5, 28), (15, 28)]:
        b.fill(x, H0 + 1, z, x, H0 + 5, z, 'red_terracotta')
    b.fill(5, H0 + 5, 24, 15, H0 + 5, 24, 'red_terracotta'); b.fill(5, H0 + 5, 32, 15, H0 + 5, 32, 'red_terracotta')
    b.fill(5, H0 + 5, 24, 5, H0 + 5, 32, 'red_terracotta'); b.fill(15, H0 + 5, 24, 15, H0 + 5, 32, 'red_terracotta')
    b.carve(8, H0 + 1, 24, 12, H0 + 4, 24)
    b.fill(8, H0 + 4, 24, 12, H0 + 4, 24, 'dark_oak_planks') if False else None
    for x in (8, 9, 11, 12): b.fill(x, H0 + 2, 24, x, H0 + 3, 24, 'dark_oak_trapdoor') if False else b.fill(x, H0 + 1, 24, x, H0 + 3, 24, 'white_stained_glass_pane')
    b.fill(10, H0 + 1, 24, 10, H0 + 3, 24, 'air')
    for x in (7, 13): b.fill(x, H0 + 2, 32, x, H0 + 3, 32, 'white_stained_glass_pane')
    for z in (26, 30): b.fill(5, H0 + 2, z, 5, H0 + 3, z, 'white_stained_glass_pane'); b.fill(15, H0 + 2, z, 15, H0 + 3, z, 'white_stained_glass_pane')
    top = b.hip_low(2, 21, 18, 35, H0 + 6, 'oxidized_cut_copper_stairs', 'oxidized_cut_copper_slab', 'dark_oak_planks', rings=99)
    b.set(10, top + 1, 28, 'gold_block') if False else None
    # veranda fence, steps, offering box, bell on a rope
    for x in range(3, 18):
        if not 8 <= x <= 12: b.set(x, H0 + 1, 22, 'crimson_fence')
    for z in range(22, 35): b.set(3, H0 + 1, z, 'crimson_fence'); b.set(17, H0 + 1, z, 'crimson_fence')
    for x in range(3, 18):
        b.set(x, H0 + 1, 34, 'crimson_fence')
    for x in (3, 17):
        b.fill(x, H0 + 1, 22, x, H0 + 4, 22, 'red_terracotta') if False else None
    b.fill(8, H0 + 1, 21, 12, H0 + 1, 21, 'air') if False else None
    for x in (9, 10, 11): b.set(x, H0 + 1, 23, 'oak_slab') if False else None
    b.set(10, H0 + 1, 23, 'barrel'); b.set(10, H0 + 2, 23, P('oak_trapdoor', facing='south', open=False, half='bottom')) if False else None
    for x in (8, 12): b.fill(x, H0 + 1, 22, x, H0 + 4, 22, 'red_terracotta')
    b.fill(8, H0 + 5, 22, 12, H0 + 5, 22, 'red_terracotta')
    b.set(10, H0 + 4, 22, P('bell', attachment='ceiling', facing='north', powered=False)) if False else None
    b.set(9, H0 + 4, 22, 'chain') if False else None
    b.set(10, H0 + 4, 22, P('chain', axis='y')); b.set(10, H0 + 3, 22, P('chain', axis='y')); b.set(10, H0 + 2, 22, P('bell', attachment='ceiling', facing='north', powered=False))
    # interior: altar, candles, tatami
    for x in range(6, 15):
        for z in range(25, 32): b.set(x, H0 + 1, z, 'white_carpet' if (x + z) % 2 else 'light_gray_carpet')
    b.fill(8, H0 + 1, 30, 12, H0 + 1, 31, 'smooth_quartz'); b.fill(9, H0 + 2, 31, 11, H0 + 2, 31, 'smooth_quartz_slab') if False else None
    for x in (8, 12): b.candle(x, H0 + 2, 30, 'white', 3)
    b.set(10, H0 + 2, 31, 'lectern') if False else b.set(10, H0 + 2, 31, 'gold_block')
    for x in (7, 13): b.hang_lantern(x, H0 + 5, 28, 1) if False else None
    # sakura trees on the hill + maples
    for (x, z) in [(4, 5), (16, 6), (3, 14), (17, 15), (3, 38), (17, 38), (2, 27), (18, 27)]:
        h = surf(z)
        tree(b, x, z, 6 if z < 22 else 7, 'cherry', leaf='cherry_leaves', crown=3.2, base_y=h, rnd=rnd)
    scatter(b, rnd, [(2, 22, 18, 40)], 0, ['poppy'])
    return b


def urahara():
    rnd = random.Random(2)
    b = Build('urahara_shop', 'Bleach', 'Лавка Урахары', foundation='cobblestone')
    b.fill(0, 0, 0, 10, 0, 9, 'spruce_planks')
    b.walls(0, 1, 0, 10, 4, 9, 'dark_oak_planks')
    b.walls(0, 5, 0, 10, 9, 9, 'white_terracotta')
    for x in (0, 5, 10):
        for z in (0, 9): b.column(x, 1, 9, z, P('dark_oak_log', axis='y'))
    for z in (0, 9):
        pass
    b.fill(0, 5, 0, 10, 5, 0, P('dark_oak_log', axis='x')); b.fill(0, 5, 9, 10, 5, 9, P('dark_oak_log', axis='x'))
    b.fill(0, 5, 0, 0, 5, 9, P('dark_oak_log', axis='z')); b.fill(10, 5, 0, 10, 5, 9, P('dark_oak_log', axis='z'))
    b.fill(1, 5, 1, 9, 5, 8, 'spruce_planks')
    top = b.gable_low(-2, 12, -2, 11, 10, 'deepslate_tile_stairs', 'deepslate_tile_slab', 'dark_oak_planks', gable_fill='white_terracotta', gspan=(0, 10))
    for x in (2, 4, 6, 8): b.fill(x, 7, 0, x, 8, 0, 'white_stained_glass_pane')
    for x in (1, 3, 7, 9):
        for y in (2, 3): b.trap(x, y, 0, 'dark_oak_trapdoor', 'south', False, 'top') if False else b.set(x, y, 0, 'dark_oak_trapdoor' if False else P('spruce_trapdoor', facing='south', open=True, half='bottom'))
    b.carve(4, 1, 0, 6, 3, 0)
    b.door(4, 1, 0, 'spruce_door', 'north', 'left'); b.door(6, 1, 0, 'spruce_door', 'north', 'right'); b.fill(5, 1, 0, 5, 3, 0, 'white_stained_glass_pane')
    for x in range(-1, 12): b.set(x, 4, -1, 'green_wool' if x % 2 else 'white_wool')
    for x in (-1, 11): b.fill(x, 1, -1, x, 3, -1, 'dark_oak_fence')
    for x in (1, 9): b.set(x, 0, -2, 'stone_bricks'); b.fill(x, 1, -2, x, 2, -2, 'dark_oak_fence'); b.lantern(x, 3, -2)
    b.fill(2, 6, -1, 8, 6, -1, 'dark_oak_planks') if False else None
    b.fill(3, 4, 0, 7, 4, 0, 'dark_oak_planks') if False else None
    for z in range(-6, -1):
        for x in (4, 5, 6): b.set(x, 0, z, 'stone_bricks' if (x + z) % 2 else 'mossy_stone_bricks')
    # candy-shop interior
    for x in range(1, 10): b.set(x, 1, 3, 'spruce_planks'); b.slab(x, 2, 3, 'spruce_slab', 'bottom')
    for x in range(1, 10, 2): b.set(x, 1, 8, 'bookshelf'); b.set(x, 2, 8, 'bookshelf'); b.set(x, 3, 8, 'potted_cornflower') if False else None
    for x in (2, 4, 6, 8): b.set(x, 3, 8, 'bookshelf') if False else None
    b.set(1, 1, 5, 'barrel'); b.set(1, 1, 6, 'barrel'); b.set(9, 1, 5, 'barrel'); b.chest(9, 1, 6, 'west')
    for x in range(3, 8):
        for z in range(5, 8): b.set(x, 1, z, 'green_carpet' if (x + z) % 2 else 'lime_carpet')
    b.set(5, 1, 6, 'brewing_stand') if False else None
    b.set(3, 1, 7, 'potted_fern'); b.set(7, 1, 7, 'potted_lily_of_the_valley')
    b.hang_lantern(3, 5, 4, 1); b.hang_lantern(7, 5, 4, 1)
    # ladder to upper floor (living area)
    b.fill(9, 5, 2, 9, 5, 2, 'air'); b.ladder(9, 1, 8, 2, 'west')
    b.bed(2, 6, 7, 'white', 'east'); b.set(7, 6, 7, 'bookshelf'); b.set(8, 6, 7, 'bookshelf'); b.set(7, 6, 2, 'crafting_table'); b.hang_lantern(5, 10, 4, 0) if False else None
    for x in range(3, 9):
        for z in range(3, 7): b.set(x, 6, z, 'brown_carpet') if False else None
    # Japanese garden: bamboo fence, bamboo, stones, lantern
    for x in range(-4, 15):
        b.set(x, 1, 12, 'bamboo_fence') if False else b.set(x, 1, 12, 'jungle_fence')
        b.set(x, 0, 12, 'grass_block')
    for z in range(10, 12):
        for x in range(2, 9): b.set(x, 0, z, 'gravel') if False else b.set(x, 0, z, 'stone_bricks' if (x + z) % 2 else 'cobblestone')
    for (x, z) in [(0, 13), (3, 14), (9, 13), (12, 14), (-2, 14)]:
        b.set(x, 0, z, 'grass_block')
        for y in range(1, rnd.randint(6, 9)): b.set(x, y, z, P('bamboo', age=1, leaves='large' if y > 5 else 'small', stage=0))
    b.set(5, 1, 14, 'mossy_cobblestone_wall'); b.set(5, 2, 14, 'mossy_cobblestone_wall'); b.lantern(5, 3, 14); b.set(5, 0, 14, 'grass_block')
    return b


def pokemon_center():
    b = Build('pokemon_center', 'Pokémon', 'Покецентр', foundation='stone_bricks')
    X1, X2, Z1, Z2 = 0, 18, 0, 11
    b.fill(X1, 0, Z1, X2, 0, Z2, 'smooth_quartz')
    for x in range(X1, X2 + 1):
        for z in range(Z1, Z2 + 1):
            if (x + z) % 2: b.set(x, 0, z, 'white_concrete')
    b.walls(X1, 1, Z1, X2, 6, Z2, 'white_concrete')
    for x in (X1, X2):
        for z in (Z1, Z2): b.column(x, 1, 6, z, 'light_gray_concrete')
    b.fill(X1, 1, Z1, X2, 1, Z1, 'light_gray_concrete'); b.fill(X1, 1, Z2, X2, 1, Z2, 'light_gray_concrete')
    # automatic glass doors + front glazing
    b.carve(8, 1, Z1, 10, 3, Z1)
    b.fill(8, 1, Z1, 10, 3, Z1, 'light_blue_stained_glass_pane') if False else None
    b.door(8, 1, Z1, 'iron_door', 'north', 'left'); b.door(10, 1, Z1, 'iron_door', 'north', 'right'); b.set(9, 1, Z1, 'glass_pane'); b.set(9, 2, Z1, 'glass_pane'); b.set(9, 3, Z1, 'glass_pane')
    for x in (2, 3, 4, 5, 13, 14, 15, 16): b.fill(x, 2, Z1, x, 4, Z1, 'light_blue_stained_glass_pane')
    for x in (2, 3, 4, 5, 8, 9, 10, 13, 14, 15, 16): b.fill(x, 3, Z2, x, 4, Z2, 'light_blue_stained_glass_pane') if False else None
    for z in (3, 4, 7, 8): b.fill(X1, 2, z, X1, 4, z, 'light_blue_stained_glass_pane'); b.fill(X2, 2, z, X2, 4, z, 'light_blue_stained_glass_pane')
    # pink-red roof with the iconic front emblem
    b.fill(X1 - 1, 7, Z1 - 1, X2 + 1, 7, Z2 + 1, 'red_concrete')
    t = b.hip_low(X1 - 2, Z1 - 2, X2 + 2, Z2 + 2, 7, 'crimson_stairs' if False else 'red_nether_brick_stairs', 'red_nether_brick_slab', 'red_concrete', rings=5)
    # Poke Ball on the front gable wall above the entrance (vertical disc)
    cxb, cyb, zb = 9, 10, Z1 - 1
    b.fill(cxb - 4, 8, zb, cxb + 4, 8, zb, 'white_concrete') if False else None
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            d = math.hypot(dx, dy)
            if d <= 3.4:
                col = 'black_concrete' if (abs(dy) == 0 or d > 2.8 and False) else ('red_concrete' if dy > 0 else 'white_concrete')
                if d <= 1.0 and dy == 0: col = 'white_concrete'
                if dy == 0 and d > 1.4: col = 'black_concrete'
                if d > 2.9: col = 'black_concrete'
                b.set(cxb + dx, cyb + dy, zb, col)
    # canopy over the entrance
    b.fill(6, 4, -2, 12, 4, -1, 'red_concrete'); 
    for x in (6, 12): b.fill(x, 1, -2, x, 3, -2, 'white_concrete')
    for x in (7, 11): b.hang_lantern(x, 4, -1, 1) if False else None
    # interior: reception counter, healing machine, PCs, sofas, beds wing
    for x in range(5, 14): b.set(x, 1, 5, 'smooth_quartz'); b.slab(x, 2, 5, 'smooth_quartz_slab', 'bottom') if x % 2 else b.set(x, 2, 5, 'smooth_quartz_slab') if False else b.slab(x, 2, 5, 'smooth_quartz_slab', 'bottom')
    b.set(9, 1, 7, 'iron_block'); b.set(9, 2, 7, 'redstone_lamp') if False else b.set(9, 2, 7, 'sea_lantern')
    for (x, z) in [(8, 7), (10, 7)]: b.set(x, 1, z, 'iron_block'); b.set(x, 2, z, 'lime_stained_glass')
    for x in (2, 4, 14, 16): b.set(x, 1, 9, P('lectern', facing='north')); b.set(x, 2, 9, 'light_blue_stained_glass_pane') if False else None
    for x in (2, 3, 4): b.stair(x, 1, 3, 'quartz_stairs', 'north') if False else None
    for x in range(2, 6): b.stair(x, 1, 2, 'red_nether_brick_stairs', 'south')
    for x in range(13, 17): b.stair(x, 1, 2, 'red_nether_brick_stairs', 'south')
    b.set(1, 1, 10, 'potted_azalea_bush') if False else b.set(1, 1, 10, 'potted_fern'); b.set(17, 1, 10, 'potted_fern')
    for (x, z) in [(3, 10), (6, 10), (12, 10), (15, 10)]: b.bed(x, 1, z - 1 if False else 9, 'pink', 'south') if False else None
    for x in (3, 6, 12, 15):
        b.bed(x, 1, 9, 'pink', 'south') if False else None
    for x in range(3, 16):
        b.set(x, 5, 6, 'sea_lantern') if (x % 3 == 0) else None
    for x in (3, 6, 12, 15): b.set(x, 6, 6, 'air') if False else None
    # ceiling to hang lights: flat ceiling at y=6 inside
    b.fill(X1 + 1, 6, Z1 + 1, X2 - 1, 6, Z2 - 1, 'white_concrete')
    for x in range(3, 16, 3): b.set(x, 5, 6, 'sea_lantern')
    for x in (3, 6, 12, 15): b.bed(x, 1, 9, 'pink', 'south')
    # outside: potted trees + lamp posts + path
    for z in range(-6, -1):
        for x in range(7, 12): b.set(x, 0, z, 'smooth_stone' if (x + z) % 2 else 'stone_bricks')
    for x in (4, 14):
        b.set(x, 0, -3, 'grass_block'); b.set(x, 1, -3, 'azalea') if False else b.set(x, 1, -3, 'flowering_azalea')
    for x in (3, 15): b.set(x, 0, -4, 'stone_bricks'); b.fill(x, 1, -4, x, 3, -4, 'iron_bars'); b.set(x, 4, -4, 'sea_lantern')
    return b


def all_builds():
    return [shrine(), urahara(), pokemon_center()]
