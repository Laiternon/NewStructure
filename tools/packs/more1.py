import random
from mcgen import *
from common import *


def totoro_house():
    rnd = random.Random(7)
    b = Build('satsuki_mei_house', 'Studio Ghibli', 'Дом Сацуки и Мэй с камфорным деревом', foundation='cobblestone')
    b.fill(0, 0, 0, 12, 0, 9, 'spruce_planks')
    b.walls(0, 0, 0, 12, 1, 9, 'cobblestone')
    b.walls(0, 2, 0, 12, 4, 9, 'white_terracotta')
    for x in (0, 4, 8, 12):
        for z in (0, 9): b.column(x, 1, 4, z, P('dark_oak_log', axis='y'))
    for z in (0, 4, 9):
        for x in (0, 12): b.column(x, 1, 4, z, P('dark_oak_log', axis='y'))
    b.fill(0, 4, 0, 12, 4, 0, P('dark_oak_log', axis='x')); b.fill(0, 4, 9, 12, 4, 9, P('dark_oak_log', axis='x'))
    b.fill(0, 4, 0, 0, 4, 9, P('dark_oak_log', axis='z')); b.fill(12, 4, 0, 12, 4, 9, P('dark_oak_log', axis='z'))
    b.fill(1, 4, 1, 11, 4, 8, 'spruce_planks')
    top = b.gable_low(-1, 13, -4, 10, 5, 'spruce_stairs', 'spruce_slab', 'spruce_planks', gable_fill='white_terracotta', gspan=(0, 12))
    b.fill(0, top, 3, 0, top, 3, 'air') if False else None
    for gx in (0, 12): b.fill(gx, 6, 2, gx, 6, 3, 'glass_pane')
    # engawa veranda
    b.fill(0, 0, -3, 12, 0, -1, 'oak_planks')
    for x in (0, 6, 12): b.column(x, 1, 4, -3, P('dark_oak_log', axis='y'))
    for x in range(1, 12):
        if x != 6: b.set(x, 1, -3, 'dark_oak_fence') if False else None
    b.hang_lantern(3, 5, -2, 1) if False else None
    for x in (3, 9): b.set(x, 4, -2, 'air') if False else None
    b.fill(3, 1, -3, 3, 2, -3, 'spruce_fence'); b.lantern(3, 3, -3); b.fill(9, 1, -3, 9, 2, -3, 'spruce_fence'); b.lantern(9, 3, -3)
    b.set(1, 1, -2, 'potted_cornflower'); b.set(11, 1, -2, 'barrel'); b.set(10, 1, -2, 'potted_fern')
    # sliding screens + entrance
    for x in (2, 3, 9, 10):
        b.fill(x, 2, 0, x, 3, 0, 'white_stained_glass_pane')
    b.carve(5, 1, 0, 7, 3, 0); b.door(6, 1, 0, 'birch_door', 'north')
    for z in (3, 6): b.fill(0, 2, z, 0, 3, z, 'white_stained_glass_pane'); b.fill(12, 2, z, 12, 3, z, 'white_stained_glass_pane')
    # interior (tatami room, kotatsu, kitchen)
    for x in range(1, 12):
        for z in range(1, 9): b.set(x, 1, z, 'lime_carpet' if (x < 8 and z < 6) else 'spruce_planks') if False else None
    for x in range(1, 8):
        for z in range(1, 6): b.set(x, 1, z, 'green_carpet' if (x + z) % 2 else 'lime_carpet')
    b.slab(4, 1, 3, 'spruce_slab', 'top'); b.slab(5, 1, 3, 'spruce_slab', 'top'); b.candle(4, 2, 3, 'orange') if False else b.set(4, 2, 3, P('orange_candle', candles=1, lit=True))
    b.bed(9, 1, 6, 'red', 'south') if False else b.bed(2, 1, 7, 'white', 'east')
    b.set(10, 1, 2, 'bookshelf'); b.set(10, 2, 2, 'bookshelf'); b.set(11, 1, 2, 'bookshelf')
    b.set(9, 1, 8, P('furnace', facing='north', lit=False)); b.set(10, 1, 8, P('smoker', facing='north', lit=False)); b.set(11, 1, 8, P('water_cauldron', level=3)); b.chest(11, 1, 6, 'west')
    b.hang_lantern(6, 4, 4, 1) if False else None
    b.fill(6, 5, 4, 6, 5, 4, 'dark_oak_planks') if False else None
    # camphor tree
    tx, tz = -11, 4
    b.sphere(tx, 17, tz, 8.5, P('oak_leaves', persistent=True), ry=6)
    b.sphere(tx + 6, 13, tz + 3, 4.5, P('oak_leaves', persistent=True)); b.sphere(tx - 5, 13, tz - 3, 4.5, P('oak_leaves', persistent=True))
    for y in range(0, 17): b.disc(tx, y, tz, 2.0 if y > 2 else 3.2, P('oak_log', axis='y'))
    for (dx, dz) in ((4, 0), (-4, 0), (0, 4), (0, -4)):
        b.fill(tx + dx, 0, tz + dz, tx + dx, 2, tz + dz, P('oak_log', axis='y'))
    b.carve(tx + 2, 1, tz, tx + 2, 2, tz)
    b.set(tx + 2, 0, tz, 'moss_block')
    b.set(tx + 1, 1, tz, 'lantern') if False else None
    # shimenawa rope band (chain ring) + lanterns
    b.ring(tx, 8, tz, 2.6, 'chain') if False else None
    # garden: well, vegetables, scarecrow, path
    for z in range(-12, -3): b.fill(5, 0, z, 7, 0, z, 'dirt_path' if True else 'dirt')
    b.walls(16, 0, 1, 18, 1, 3, 'cobblestone'); b.set(17, 1, 2, P('water_cauldron', level=3)) if False else None
    b.fill(17, 0, 2, 17, 0, 2, 'cobblestone'); b.set(17, 1, 2, 'cauldron') if False else None
    for x in range(15, 20):
        for z in range(5, 9):
            b.set(x, 0, z, 'dirt'); b.set(x, 1, z, rnd.choice(['pumpkin', 'melon', 'air', 'air', 'hay_block'])) if (x + z) % 2 == 0 else None
    b.column(17, 1, 2, 3, 'oak_fence'); b.set(17, 3, 3, 'hay_block'); b.set(17, 4, 3, 'carved_pumpkin'); b.set(16, 3, 3, 'air') if False else None
    for (x, z, h) in [(-4, -8, 8), (19, -6, 9), (16, 13, 8)]:
        tree(b, x, z, h, 'oak', crown=3.0, rnd=rnd)
    scatter(b, rnd, [(-8, -10, 20, -4), (14, 10, 22, 14), (-2, 11, 14, 14)], 40, ['dandelion', 'poppy', 'cornflower', 'oxeye_daisy', 'azure_bluet'],
            avoid=lambda x, z: (-1 <= x <= 13 and -4 <= z <= 10) or (4 <= x <= 8 and z < 0) or (-16 <= x <= -6 and -2 <= z <= 10))
    return b


def bakery():
    b = Build('witch_bakery', 'Studio Ghibli', 'Пекарня юной ведьмы (Гучокипан)', foundation='cobblestone')
    b.fill(0, 0, 0, 10, 0, 9, 'spruce_planks')
    b.walls(0, 1, 0, 10, 12, 9, 'white_terracotta')
    for x in (0, 10):
        for z in (0, 9): b.column(x, 1, 12, z, P('dark_oak_log', axis='y'))
    for y in (5, 9):                                   # floor belts + floors
        b.fill(0, y, 0, 10, y, 0, P('dark_oak_log', axis='x')); b.fill(0, y, 9, 10, y, 9, P('dark_oak_log', axis='x'))
        b.fill(0, y, 0, 0, y, 9, P('dark_oak_log', axis='z')); b.fill(10, y, 0, 10, y, 9, P('dark_oak_log', axis='z'))
        b.fill(1, y, 1, 9, y, 8, 'spruce_planks')
    b.fill(0, 13, 0, 10, 13, 9, 'dark_oak_planks') if False else None
    # shop front
    b.fill(1, 1, 0, 9, 1, 0, 'cobblestone')
    for x in (1, 2, 3, 7, 8, 9): b.fill(x, 2, 0, x, 4, 0, 'glass_pane')
    b.carve(4, 2, 0, 6, 3, 0); b.set(4, 1, 0, 'air'); b.carve(4, 1, 0, 6, 1, 0)
    b.door(5, 1, 0, 'oak_door', 'north'); b.fill(4, 1, 0, 4, 1, 0, 'cobblestone'); b.fill(6, 1, 0, 6, 1, 0, 'cobblestone')
    b.fill(4, 2, 0, 4, 3, 0, 'glass_pane'); b.fill(6, 2, 0, 6, 3, 0, 'glass_pane')
    for x in range(0, 11): b.set(x, 5, -1, 'red_wool' if x % 2 else 'white_wool') if False else None
    for x in range(-1, 12):                                   # striped awning
        for z in (-1,):
            b.stair(x, 4, z, 'red_terracotta' if False else 'brick_stairs', 'south') if False else None
    for x in range(0, 11): b.slab(x, 4, -1, 'red_nether_brick_slab' if x % 2 else 'spruce_slab', 'bottom'); b.setnew(x, 3, -1, 'air') if False else None
    for x in (0, 10): b.fill(x, 1, -1, x, 3, -1, 'spruce_fence')
    # upper windows + balcony
    for x in (2, 4, 6, 8):
        b.fill(x, 7, 0, x, 8, 0, 'glass_pane'); b.fill(x, 11, 0, x, 11, 0, 'glass_pane')
        b.fill(x, 7, 9, x, 8, 9, 'glass_pane')
    for x in (3, 7): b.trap(x - 1 if False else x - 1, 7, -1, 'spruce_trapdoor', 'south', True) if False else None
    b.fill(0, 5, -3, 10, 5, -2, 'spruce_planks') if False else None
    for x in range(0, 11):
        b.set(x, 6, -1, 'spruce_fence') if False else None
    for x in (2, 4, 6, 8): b.set(x, 6, -1, 'spruce_planks') if False else None
    b.fill(2, 9, -2, 8, 9, -1, 'spruce_planks')                   # balcony off the 3rd floor
    for x in range(2, 9): b.set(x, 10, -2, 'spruce_fence')
    for z in (-1,): b.set(2, 10, z, 'spruce_fence'); b.set(8, 10, z, 'spruce_fence')
    b.carve(5, 10, 0, 5, 11, 0); b.door(5, 10, 0, 'spruce_door', 'north')
    for x in (3, 7): b.set(x, 10, -1, 'potted_poppy') if False else b.set(x, 10, -1, P('potted_poppy'))
    # roof: steep red hip with a chimney and a little dormer-like clock face
    top = b.hip(-1, -3, 11, 10, 13, 'red_nether_brick_stairs', 'red_nether_bricks', 'red_nether_brick_slab')
    b.fill(8, 14, 5, 8, top + 4, 5, 'bricks'); b.set(8, top + 5, 5, 'campfire') if False else b.set(8, top + 5, 5, P('campfire', facing='north', lit=True, signal_fire=False, waterlogged=False))
    b.fill(5, 12, 0, 5, 12, 0, 'air') if False else None
    # inside: shop counter, ovens, shelves, stairs
    for x in range(2, 9): b.stair(x, 1, 2, 'spruce_stairs', 'north', 'bottom') if False else b.set(x, 1, 2, 'spruce_planks')
    for x in range(2, 9): b.slab(x, 2, 2, 'spruce_slab', 'bottom')
    for x in (3, 5, 7): b.set(x, 3, 2, 'potted_fern') if False else None
    b.set(1, 1, 7, P('smoker', facing='east', lit=False)); b.set(1, 1, 6, P('furnace', facing='east', lit=False)); b.set(1, 1, 5, 'barrel'); b.set(1, 1, 8, 'crafting_table')
    b.chest(9, 1, 7, 'west'); b.set(9, 1, 6, 'barrel'); b.set(9, 1, 5, 'bookshelf'); b.set(9, 2, 5, 'bookshelf') if False else None
    for i, y in enumerate(range(1, 5)):
        pass
    b.ladder(9, 1, 8, 4, 'west', wall='spruce_planks') if False else b.ladder(9, 1, 12, 3, 'west')
    b.fill(9, 5, 3, 9, 5, 3, 'air'); b.fill(9, 9, 3, 9, 9, 3, 'air')
    b.ladder(9, 1, 12, 3, 'west')
    b.bed(2, 6, 7, 'red', 'east'); b.bed(2, 10, 7, 'white', 'east')
    b.set(8, 6, 7, 'barrel'); b.lantern(8, 7, 7); b.set(8, 10, 7, 'bookshelf'); b.lantern(5, 4, 5) if False else None
    for y in (4, 8): b.hang_lantern(5, y, 5, 1) if False else None
    b.hang_lantern(5, 5, 4, 1); b.hang_lantern(5, 9, 4, 1)
    return b


def forge():
    rnd = random.Random(3)
    b = Build('swordsmith_forge', 'Demon Slayer', 'Кузница деревни мечников', foundation='cobblestone')
    b.fill(0, 0, 0, 14, 0, 10, 'stone_bricks')
    b.walls(0, 1, 0, 14, 1, 10, 'stone_bricks')
    b.walls(0, 2, 0, 14, 5, 10, 'white_terracotta')
    for x in range(0, 15, 2):
        for z in (0, 10): b.column(x, 1, 5, z, P('dark_oak_log', axis='y'))
    for z in range(0, 11, 5):
        for x in (0, 14): b.column(x, 1, 5, z, P('dark_oak_log', axis='y'))
    b.fill(0, 5, 0, 14, 5, 0, P('dark_oak_log', axis='x')); b.fill(0, 5, 10, 14, 5, 10, P('dark_oak_log', axis='x'))
    b.fill(1, 5, 1, 13, 5, 9, 'dark_oak_planks')
    top = b.gable_low(-2, 16, -2, 12, 6, 'deepslate_tile_stairs', 'deepslate_tile_slab', 'dark_oak_planks', gable_fill='white_terracotta', gspan=(0, 14))
    for gx in (0, 14): b.fill(gx, 7, 4, gx, 7, 6, 'glass_pane') if False else None
    # open front (forge workspace): remove front wall between posts
    b.carve(1, 2, 0, 13, 4, 0); b.carve(1, 1, 0, 13, 1, 0)
    b.fill(1, 0, 0, 13, 0, 0, 'stone_bricks')
    for x in (4, 10): b.hang_lantern(x, 5, 1, 1)
    # workspace
    b.set(2, 1, 2, P('anvil', facing='east')); b.set(2, 1, 5, P('grindstone', face='floor', facing='east')); b.set(2, 1, 7, 'smithing_table')
    b.set(5, 1, 8, P('blast_furnace', facing='south', lit=False)); b.set(6, 1, 8, P('blast_furnace', facing='south', lit=False)); b.set(7, 1, 8, P('smoker', facing='south', lit=False))
    for y in range(2, 6): b.set(6, y, 9, 'bricks')
    b.set(10, 1, 8, 'lava_cauldron'); b.set(11, 1, 8, P('water_cauldron', level=3)); b.set(12, 1, 8, 'cauldron')
    b.chest(13, 1, 2, 'west'); b.set(13, 1, 3, 'barrel'); b.set(13, 1, 4, 'barrel')
    b.set(9, 1, 2, 'iron_block'); b.set(9, 2, 2, P('iron_trapdoor', facing='north', open=False, half='bottom'))
    for z in range(1, 6): b.set(4, 0, z, 'polished_andesite')
    b.set(8, 1, 5, P('campfire', facing='north', lit=True, signal_fire=False, waterlogged=False))
    b.fill(8, 0, 5, 8, 0, 5, 'stone_bricks')
    # chimney
    b.fill(6, 6, 9, 6, 11, 9, 'bricks'); b.set(6, 12, 9, 'campfire')
    # annex: charcoal shed + bamboo fence
    b.fill(16, 0, 1, 20, 0, 5, 'cobblestone'); b.fill(17, 1, 2, 19, 1, 4, 'coal_block'); b.fill(17, 2, 3, 18, 2, 3, 'coal_block')
    for z in range(-3, 14): b.set(-4, 0, z, 'grass_block') if False else None
    # little stream with a bridge
    for x in range(-12, 27):
        for z in (-8, -7, -6):
            if abs(z + 7) == 1: b.set(x, -1, z, 'dirt'); b.set(x, 0, z, 'grass_block') if False else None
    wat = set()
    for x in range(-12, 27):
        for z in (-8, -7, -6):
            b.set(x, 0, z, 'air'); b.set(x, -1, z, 'water' if z == -7 else 'dirt'); b.set(x, -2, z, 'dirt')
        b.set(x, -1, -7, 'water')
    for x in range(-12, 27): b.set(x, 0, -8, 'grass_block'); b.set(x, 0, -6, 'grass_block')
    for x in range(-12, 27):
        b.set(x, -1, -8, 'dirt'); b.set(x, -1, -6, 'dirt')
        b.set(x, -2, -7, 'clay')
    for x in range(-12, 27): b.set(x, 0, -7, 'air')
    b.set(-13, -1, -7, 'dirt'); b.set(27, -1, -7, 'dirt')
    for z in range(-9, -3):
        for x in (6, 7, 8): b.set(x, 0, z, 'spruce_planks' if z in (-8, -7, -6) else 'dirt_path')
    for z in (-8, -6):
        b.set(6, 1, z, 'spruce_fence'); b.set(8, 1, z, 'spruce_fence')
    for z in range(-5, -2):
        for x in (6, 7, 8): b.set(x, 0, z, 'dirt_path')
    b.set(7, 0, -7, 'spruce_planks')
    # lanterns on posts along path
    for z in (-3, 2): b.fill(4, 1, z - 3 if False else z, 4, 2, z, 'spruce_fence') if False else None
    b.fill(9, 1, -2, 9, 3, -2, 'spruce_fence'); b.lantern(9, 4, -2); b.fill(5, 1, -2, 5, 3, -2, 'spruce_fence'); b.lantern(5, 4, -2)
    # bamboo grove (soil + bamboo) behind
    for (x, z) in [(-3, 4), (-4, 6), (-2, 8), (-5, 2), (-3, 10), (-4, 9), (17, 9), (19, 8), (18, 11), (20, 10)]:
        b.set(x, 0, z, 'grass_block')
        for y in range(1, 1 + rnd.randint(7, 11)): b.set(x, y, z, P('bamboo', age=1, leaves='large' if y > 6 else 'small', stage=0))
    for (x, z, h) in [(-7, 2, 7), (23, 8, 8)]:
        tree(b, x, z, h, 'oak', crown=3.0, rnd=rnd)
    return b


def wall_gate():
    rnd = random.Random(5)
    b = Build('wall_maria_gate', 'Attack on Titan', 'Врата Стены Мария', foundation='stone_bricks')
    L, T, H = 31, 7, 20
    for x in range(L):
        for z in range(T):
            for y in range(0, H + 1):
                if x in (0, L - 1) or z in (0, T - 1) or y in (0, H):
                    r = rnd.random()
                    b.set(x, y, z, 'cracked_stone_bricks' if r < .1 else 'mossy_stone_bricks' if r < .18 else 'stone_bricks')
    for x in range(0, L, 3):                                 # crenellations
        for z in (0, T - 1): b.set(x, H + 1, z, 'stone_brick_wall' if False else 'stone_bricks'); b.set(x, H + 2, z, 'stone_brick_slab') if False else None
    for x in range(0, L):
        for z in (0, T - 1):
            if x % 3 != 1: b.set(x, H + 1, z, 'stone_brick_wall')
    for x in (0, L - 1):
        for z in range(T): b.set(x, H + 1, z, 'stone_brick_wall')
    # gate tunnel
    for x in (12, 18):
        b.fill(x, 1, 0, x + 0, H - 1, T - 1, 'stone_bricks') if False else None
    b.fill(11, 1, 0, 19, H - 1, T - 1, 'stone_bricks')
    b.fill(12, 1, 0, 18, 9, T - 1, 'air'); b.fill(13, 10, 0, 17, 10, T - 1, 'air'); b.fill(12, 9, 0, 12, 9, T - 1, 'stone_brick_stairs') if False else None
    for z in range(T):
        b.stair(12, 9, z, 'stone_brick_stairs', 'east', 'top'); b.stair(18, 9, z, 'stone_brick_stairs', 'west', 'top')
        b.set(12, 10, z, 'stone_bricks') if False else None
    for z in (0, T - 1):
        b.fill(11, 1, z, 11, 10, z, 'chiseled_stone_bricks'); b.fill(19, 1, z, 19, 10, z, 'chiseled_stone_bricks')
        b.fill(12, 11, z, 18, 11, z, 'chiseled_stone_bricks')
    b.fill(12, 0, 0, 18, 0, T - 1, 'stone_bricks')
    for x in range(12, 19):
        for z in range(T): b.set(x, 0, z, 'cobblestone' if (x + z) % 3 else 'stone_bricks')
    for x in range(13, 18): b.fill(x, 6, 2, x, 9, 2, 'iron_bars')              # raised portcullis
    b.fill(13, 9, 2, 17, 9, 2, 'iron_bars')
    for x in (13, 14, 16, 17):                                                   # open wooden gate leaves
        b.fill(x, 1, T - 2, x, 8, T - 2, 'dark_oak_planks') if x in (13, 17) else None
    b.fill(13, 1, T - 2, 13, 8, T - 2, 'dark_oak_planks'); b.fill(17, 1, T - 2, 17, 8, T - 2, 'dark_oak_planks')
    for y in (2, 5, 8): b.fill(13, y, T - 2, 13, y, T - 2, 'iron_block'); b.fill(17, y, T - 2, 17, y, T - 2, 'iron_block')
    for y in (2, 6): b.wall_torch(12, y, 3, 'east'); b.wall_torch(18, y, 3, 'west')
    # hollow interior with floors and ladder (guards live inside)
    b.carve(1, 1, 1, 10, H - 1, T - 2); b.carve(20, 1, 1, L - 2, H - 1, T - 2)
    for lvl in (7, 14):
        b.fill(1, lvl, 1, 10, lvl, T - 2, 'spruce_planks'); b.fill(20, lvl, 1, L - 2, lvl, T - 2, 'spruce_planks')
    b.ladder(2, 1, H - 1, 1, 'south', wall='stone_bricks') if False else None
    for (x0, x1) in ((1, 10), (20, L - 2)):
        for lvl0 in (0, 7, 14):
            b.chest(x0 + 1, lvl0 + 1, T - 2, 'north') if lvl0 else None
        b.set(x0 + 3, 1, T - 2, 'barrel'); b.set(x0 + 4, 1, T - 2, 'barrel'); b.set(x0 + 6, 8, T - 2, 'barrel'); b.bed(x0 + 2, 15, T - 3, 'blue', 'south') if False else None
        for lvl0 in (1, 8, 15):
            b.hang_lantern(x0 + 4, lvl0 + 6 if lvl0 + 6 <= H else H, 3, 1) if lvl0 + 6 <= H else None
    for x0 in (2, 22):
        for y in range(1, 7): b.set(x0, y, 1, P('ladder', facing='south'))
        for y in range(8, 14): b.set(x0, y, 1, P('ladder', facing='south'))
        for y in range(15, H): b.set(x0, y, 1, P('ladder', facing='south'))
        b.fill(x0, 7, 1, x0, 7, 1, 'air'); b.fill(x0, 14, 1, x0, 14, 1, 'air')
        for lvl in (7, 14): b.set(x0, lvl, 2, 'spruce_planks')
        b.fill(x0, H, 1, x0, H, 1, 'air')
    # gatehouse on the wall-walk
    b.walls(10, H + 1, 1, 20, H + 4, 5, 'white_terracotta')
    for x in (10, 15, 20):
        for z in (1, 5): b.column(x, H + 1, H + 4, z, P('dark_oak_log', axis='y'))
    for x in (12, 14, 16, 18): b.fill(x, H + 2, 1, x, H + 3, 1, 'glass_pane'); b.fill(x, H + 2, 5, x, H + 3, 5, 'glass_pane')
    b.fill(9, H + 5, 0, 21, H + 5, 6, 'dark_oak_planks') if False else None
    b.gable_low(9, 21, 0, 6, H + 5, 'deepslate_tile_stairs', 'deepslate_tile_slab', 'dark_oak_planks', gable_fill='white_terracotta', gspan=(10, 20))
    b.carve(14, H + 1, 1, 16, H + 3, 4) if False else None
    b.set(15, H + 1, 3, 'barrel'); b.set(13, H + 1, 3, 'lectern') if False else None
    # flags and torches along the parapet
    for x in range(2, L - 2, 5):
        b.set(x, H + 1, 1, 'stone_brick_wall') if False else None
    for x in range(3, L - 3, 6):
        if x < 9 or x > 21: b.wall_torch(x, H + 2, T - 2, 'north') if False else None
    for x in (4, 26): b.fill(x, H + 1, 3, x, H + 4, 3, 'spruce_fence'); b.set(x, H + 5, 3, P('lantern', hanging=False))
    # outer ladder to the top (back)
    b.ladder(3, 1, H, T, 'south', wall='stone_bricks') if False else None
    return b


def rockbell():
    rnd = random.Random(11)
    b = Build('rockbell_automail', 'Fullmetal Alchemist', 'Мастерская автоброни Рокбелл', foundation='cobblestone')
    b.fill(0, 0, 0, 11, 0, 9, 'oak_planks')
    b.walls(0, 1, 0, 11, 1, 9, 'stone_bricks')
    b.walls(0, 2, 0, 11, 9, 9, 'cut_sandstone')
    for x in (0, 11):
        for z in (0, 9): b.column(x, 1, 9, z, P('dark_oak_log', axis='y'))
    b.fill(0, 5, 0, 11, 5, 9, 'dark_oak_planks'); b.fill(1, 5, 1, 10, 5, 8, 'spruce_planks')
    for y in (5,):
        b.fill(0, y, 0, 11, y, 0, P('dark_oak_log', axis='x')); b.fill(0, y, 9, 11, y, 9, P('dark_oak_log', axis='x'))
    # windows (two floors)
    for x in (2, 3, 8, 9):
        b.fill(x, 2, 0, x, 3, 0, 'glass_pane'); b.fill(x, 7, 0, x, 8, 0, 'glass_pane')
    for x in (2, 3, 8, 9): b.fill(x, 2, 9, x, 3, 9, 'glass_pane'); b.fill(x, 7, 9, x, 8, 9, 'glass_pane')
    for z in (3, 6): b.fill(0, 2, z, 0, 3, z, 'glass_pane'); b.fill(11, 2, z, 11, 3, z, 'glass_pane'); b.fill(0, 7, z, 0, 8, z, 'glass_pane'); b.fill(11, 7, z, 11, 8, z, 'glass_pane')
    for x in (1, 4, 7, 10):
        for y in (2, 3, 7, 8): b.trap(x, y, -1, 'dark_oak_trapdoor', 'south', True) if x in (1, 4, 7, 10) and x not in (4, 7) else None
    b.carve(5, 1, 0, 6, 3, 0); b.door(5, 1, 0, 'dark_oak_door', 'north', 'left'); b.door(6, 1, 0, 'dark_oak_door', 'north', 'right')
    for y in (4,): b.fill(5, y, 0, 6, y, 0, 'dark_oak_planks')
    b.fill(4, 6, -1, 7, 8, -1, 'air') if False else None
    # roof: orange tile, steep gable with dormer window gable on front
    top = b.gable_low(-1, 12, -2, 11, 10, 'brick_stairs', 'brick_slab', 'dark_oak_planks', gable_fill='cut_sandstone', gspan=(0, 11))
    b.fill(0, 10, 0, 11, 10, 9, 'air') if False else None
    for gx in (0, 11): b.fill(gx, 10, 4, gx, 11, 5, 'glass_pane')
    # sign board above the door (planks + gear of iron)
    b.fill(3, 4, -1, 8, 4, -1, 'dark_oak_planks'); b.fill(3, 4, -1, 8, 4, -1, 'dark_oak_slab') if False else None
    b.set(5, 4, -1, 'iron_block'); b.set(6, 4, -1, 'iron_block'); b.set(4, 4, -1, 'iron_trapdoor') if False else None
    b.fill(2, 1, -1, 9, 1, -1, 'dark_oak_slab') if False else None
    # porch
    b.fill(2, 0, -3, 9, 0, -1, 'spruce_planks'); b.fill(2, 1, -3, 2, 3, -3, 'dark_oak_fence') if False else None
    for x in (2, 9): b.column(x, 1, 4, -3, P('dark_oak_log', axis='y'))
    b.fill(2, 4, -3, 9, 4, -3, P('dark_oak_log', axis='x')); b.fill(2, 4, -2, 9, 4, -1, 'dark_oak_planks')
    b.hang_lantern(5, 4, -2, 1) if False else None
    b.lantern(3, 1, -2) if False else None
    for x in (3, 8): b.hang_lantern(x, 4, -2, 1)
    b.set(3, 1, -1, 'potted_dandelion'); b.set(8, 1, -1, 'barrel'); b.stair(7, 1, -2, 'spruce_stairs', 'north')
    # chimney
    b.fill(10, 6, 7, 10, 14, 7, 'bricks'); b.set(10, 15, 7, P('campfire', facing='north', lit=True, signal_fire=False, waterlogged=False))
    # workshop interior (ground): counter, anvil, tools, shelves with 'limbs' (iron blocks/ iron bars)
    for x in range(2, 10): b.set(x, 1, 2, 'dark_oak_planks') if False else None
    for x in range(1, 10): b.slab(x, 1, 3, 'dark_oak_slab', 'top') if False else b.set(x, 1, 3, 'dark_oak_planks')
    for x in range(1, 10): b.slab(x, 2, 3, 'dark_oak_slab', 'bottom')
    b.set(2, 1, 7, P('anvil', facing='north')); b.set(4, 1, 8, P('grindstone', face='floor', facing='north')); b.set(6, 1, 8, 'smithing_table'); b.set(8, 1, 8, P('blast_furnace', facing='north', lit=False))
    b.set(9, 1, 7, 'iron_block'); b.set(9, 2, 7, 'iron_bars'); b.set(1, 1, 8, 'barrel'); b.set(1, 1, 7, 'barrel'); b.chest(10, 1, 8, 'west')
    for z in (4, 5, 6): b.set(10, 1, z, 'bookshelf'); b.set(10, 2, z, 'bookshelf')
    b.fill(2, 1, 4, 5, 1, 5, 'air') if False else None
    for x in range(3, 8):
        for z in range(4, 7): b.set(x, 1, z, 'red_carpet' if (x + z) % 2 else 'brown_carpet')
    b.ladder(1, 1, 5, 5, 'east')
    b.fill(1, 5, 5, 1, 5, 5, 'air')
    # upstairs: bedrooms
    for x in range(3, 9):
        for z in range(3, 8): b.set(x, 6, z, 'brown_carpet')
    b.bed(2, 6, 7, 'red', 'east'); b.bed(2, 6, 2, 'yellow', 'east'); b.set(9, 6, 8, 'bookshelf'); b.set(9, 6, 7, 'barrel'); b.lantern(9, 7, 7)
    b.set(9, 6, 2, 'crafting_table'); b.set(9, 6, 3, 'chest') if False else b.chest(9, 6, 3, 'west')
    b.hang_lantern(5, 9, 5, 1) if False else None
    # fenced front yard with wheat-less planters (flowers) + dirt path
    for z in range(-8, -3):
        for x in (5, 6): b.set(x, 0, z, 'dirt_path')
    for x in range(-3, 15):
        b.set(x, 1, -9, 'dark_oak_fence') if x not in (5, 6) else None
        b.set(x, 0, -9, 'grass_block') if x not in (5, 6) else None
    for (x, z) in [(-2, -6), (13, -6), (-2, 3), (13, 4), (-2, 8), (14, 8)]:
        b.set(x, 0, z, 'grass_block'); b.set(x, 1, z, rnd.choice(['poppy', 'dandelion', 'cornflower', 'oxeye_daisy']))
    for (x, z, h) in [(-6, 6, 7), (17, 3, 8)]:
        tree(b, x, z, h, 'oak', crown=2.8, rnd=rnd)
    return b


def steins_lab():
    b = Build('future_gadget_lab', 'Steins;Gate', 'Лаборатория будущих гаджетов (Акихабара)', foundation='stone_bricks')
    W, D = 10, 9
    b.fill(-3, 0, -6, W + 3, 0, D + 1, 'gray_concrete') if False else None
    for x in range(-3, W + 4):
        for z in range(-6, 0): b.set(x, 0, z, 'gray_concrete' if z != -3 else 'white_concrete') if False else b.set(x, 0, z, 'gray_concrete')
    for x in range(-3, W + 4, 2): b.set(x, 0, -3, 'white_concrete')
    b.fill(0, 0, 0, W, 0, D, 'smooth_stone')
    b.walls(0, 1, 0, W, 14, D, 'light_gray_concrete')
    for y in (5, 10): b.fill(0, y, 0, W, y, D, 'gray_concrete'); b.fill(1, y, 1, W - 1, y, D - 1, 'smooth_stone' if y == 5 else 'spruce_planks')
    for x in (0, W):
        for z in (0, D): b.column(x, 1, 14, z, 'gray_concrete')
    b.fill(-1, 15, -1, W + 1, 15, D + 1, 'gray_concrete'); b.fill(0, 15, 0, W, 15, D, 'gray_concrete')
    # ground floor: TV shop with big display windows and orange awning
    for x in range(1, W):
        if x not in (4, 5, 6): b.fill(x, 2, 0, x, 4, 0, 'light_blue_stained_glass_pane')
    b.carve(4, 1, 0, 6, 3, 0); b.door(4, 1, 0, 'iron_door', 'north', 'left'); b.door(6, 1, 0, 'iron_door', 'north', 'right')
    b.fill(5, 1, 0, 5, 3, 0, 'glass_pane')
    for x in range(-1, W + 2): b.set(x, 5, -1, 'orange_concrete') if False else None
    for x in range(-1, W + 2):
        b.slab(x, 5, -1, 'smooth_red_sandstone_slab' if False else 'orange_terracotta' if False else 'red_sandstone_slab', 'bottom') if False else b.set(x, 5, -1, 'orange_wool' if x % 2 else 'white_wool')
    for x in (-1, W + 1): b.fill(x, 1, -1, x, 4, -1, 'iron_bars')
    # shop interior
    for x in range(2, 9, 2): b.set(x, 1, 2, 'iron_block'); b.set(x, 2, 2, 'light_blue_stained_glass') if False else b.set(x, 2, 2, 'glass')
    for x in range(1, W): b.set(x, 1, 7, 'bookshelf'); b.set(x, 2, 7, 'bookshelf') if x % 2 else None
    b.set(9, 1, 3, 'chest') if False else b.chest(9, 1, 3, 'west')
    # exterior stairs to 2nd floor (iron stairs on the east side)
    for i in range(5):
        b.stair(W + 1, 1 + i, 2 + i if False else 1 + i, 'stone_stairs', 'south') if False else None
    for i, y in enumerate(range(1, 6)):
        b.stair(W + 1 + 0, y, 1 + (0 if False else i - 0) if False else 1 + i, 'stone_stairs', 'south')
        for yy in range(1, y): b.set(W + 1, yy, 1 + i, 'iron_bars')
    b.fill(W + 1, 5, 6, W + 1, 5, 6, 'smooth_stone') if False else None
    b.fill(W + 1, 5, 6, W + 2, 5, 6, 'smooth_stone')
    for z in range(1, 7): b.set(W + 2, 1, z, 'iron_bars') if False else None
    b.carve(W, 6, 6, W, 7, 6); b.door(W, 6, 6, 'iron_door', 'east')
    b.set(W + 2, 6, 6, 'iron_bars')
    # 2nd floor: the lab
    for x in (2, 3, 4, 6, 7, 8): b.fill(x, 7, 0, x, 8, 0, 'light_blue_stained_glass_pane') if x in (3, 4, 6, 7) else None
    b.fill(3, 7, 0, 7, 8, 0, 'light_blue_stained_glass_pane')
    for x in range(1, 5): b.set(x, 6, 8, 'iron_block'); b.set(x, 7, 8, P('observer', facing='south') if x % 2 else 'redstone_lamp')
    b.set(5, 6, 8, 'dispenser'); b.set(6, 6, 8, 'redstone_lamp'); b.set(7, 6, 8, P('observer', facing='south')); b.set(8, 6, 8, 'iron_block'); b.set(8, 7, 8, 'redstone_lamp') if False else None
    for x in range(2, 9, 3): b.set(x, 6, 3, P('lectern', facing='south')); b.set(x, 6, 4, P('oak_stairs', facing='north', half='bottom', shape='straight', waterlogged=False)) if False else None
    b.set(3, 6, 4, P('dark_oak_stairs', facing='north', half='bottom', shape='straight', waterlogged=False)); b.set(7, 6, 4, P('dark_oak_stairs', facing='north', half='bottom', shape='straight', waterlogged=False))
    b.set(2, 6, 2, 'crafting_table') if False else None
    b.set(9, 6, 2, 'brewing_stand'); b.set(9, 6, 3, 'iron_block') if False else None
    b.bed(2, 6, 1, 'white', 'east') if False else b.bed(8, 6, 6, 'blue', 'north') if False else None
    b.set(6, 6, 6, 'blue_carpet'); b.set(5, 6, 6, 'blue_carpet')
    for x in (2, 5, 8): b.set(x, 9, 4, 'sea_lantern') if False else None
    b.hang_lantern(5, 10, 4, 1, soul=True); b.hang_lantern(3, 10, 6, 1, soul=True)
    # 3rd floor: living loft
    b.bed(2, 11, 6, 'red', 'east'); b.set(8, 11, 7, 'bookshelf'); b.set(8, 12, 7, 'bookshelf'); b.set(7, 11, 7, 'barrel'); b.lantern(7, 12, 7)
    for x in (3, 4, 6, 7): b.fill(x, 12, 0, x, 13, 0, 'glass_pane')
    b.fill(2, 11, 2, 7, 11, 4, 'air') if False else None
    # inside ladders (west wall)
    b.fill(1, 5, 2, 1, 5, 2, 'air'); b.fill(1, 10, 2, 1, 10, 2, 'air')
    b.ladder(1, 1, 14, 2, 'east')
    # rooftop: railing, water tank, antenna with dish, AC
    for x in range(-1, W + 2):
        for z in (-1, D + 1): b.set(x, 16, z, 'iron_bars')
    for z in range(-1, D + 2):
        for x in (-1, W + 1): b.set(x, 16, z, 'iron_bars')
    b.fill(1, 16, 2, 3, 19, 4, 'barrel') if False else None
    b.cylinder if False else None
    b.disc(2, 16, 6, 1.6, 'copper_block') if False else None
    b.fill(2, 16, 6, 2, 19, 6, 'iron_bars'); b.set(2, 20, 6, 'lightning_rod')
    b.disc(7, 17, 6, 2.2, 'smooth_quartz_slab') if False else None
    for (x, z) in [(6, 5), (7, 5), (8, 5), (6, 6), (7, 6), (8, 6), (6, 7), (7, 7), (8, 7)]: b.slab(x, 16, z, 'smooth_quartz_slab', 'bottom') if (x, z) != (7, 6) else b.set(x, 16, z, 'smooth_quartz')
    b.fill(7, 17, 6, 7, 18, 6, 'iron_bars'); b.slab(6, 18, 6, 'smooth_quartz_slab', 'bottom') if False else None
    b.set(1, 16, 8, 'barrel'); b.set(2, 16, 8, 'barrel'); b.set(1, 17, 8, 'barrel')
    # AC units + signs (vertical sign boards from wool)
    for y in (7, 12): b.set(W + 1, y, 3, P('iron_trapdoor', facing='east', open=True, half='bottom')) if False else None
    b.fill(-1, 6, 3, -1, 8, 4, 'light_blue_wool') if False else None
    b.fill(-1, 6, 2, -1, 9, 2, 'white_concrete') if False else None
    b.set(-1, 6, 1, 'orange_concrete') if False else None
    # neon sign: vertical sign on the facade
    b.fill(-1, 6, 0, -1, 12, 0, 'orange_concrete'); b.fill(-1, 7, 0, -1, 11, 0, 'orange_concrete')
    for y in range(7, 12): b.set(-1, y, 0, 'glowstone' if y % 2 else 'orange_concrete')
    # street details: lamp posts + vending machines
    for x in (-2, W + 2):
        b.fill(x, 1, -5, x, 5, -5, 'iron_bars'); b.set(x, 6, -5, 'sea_lantern')
    b.fill(-2, 1, -2, -2, 2, -2, 'red_concrete'); b.fill(W + 2, 1, -2, W + 2, 2, -2, 'blue_concrete')
    return b


def all_builds():
    return [totoro_house(), bakery(), forge(), wall_gate(), rockbell(), steins_lab()]
