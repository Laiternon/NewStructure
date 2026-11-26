package com.animebuilder.build;

import com.animebuilder.structure.Structure;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.Container;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.*;

public final class BuildService {
    private BuildService() {}

    public static final int MAX_DISTANCE = 160;
    private static final int MAX_FOUNDATION_DEPTH = 14;

    public static void tryBuild(ServerPlayer player, Structure s, BlockPos origin, int rot) {
        ServerLevel level = player.serverLevel();
        Structure.Placement pl = s.get(rot);
        boolean creative = player.getAbilities().instabuild;

        if (origin.getY() + s.minY < level.getMinBuildHeight() || origin.getY() + s.minY + s.sizeY >= level.getMaxBuildHeight()) {
            player.sendSystemMessage(Component.literal("§cПостройка не помещается по высоте."));
            return;
        }

        // 1) what really has to be placed
        List<Structure.Entry> todo = new ArrayList<>();
        List<BlockPos> targets = new ArrayList<>();
        int skipped = 0;
        for (Structure.Entry e : pl.all()) {
            BlockPos pos = origin.offset(e.x(), e.y(), e.z());
            BlockState cur = level.getBlockState(pos);           // loads the chunk if needed
            if (cur == e.state()) continue;
            if (e.state().isAir() && cur.isAir()) continue;
            if (!level.mayInteract(player, pos) || !player.mayBuild()) { skipped++; continue; }
            if (cur.getDestroySpeed(level, pos) < 0) { skipped++; continue; }
            if (level.getBlockEntity(pos) != null) { skipped++; continue; }   // never overwrite chests etc.
            todo.add(e);
            targets.add(pos);
        }
        if (todo.isEmpty()) {
            player.sendSystemMessage(Component.literal("§eНечего строить: всё уже на месте или место защищено."));
            return;
        }

        // 2) resources
        Map<Item, Integer> need = Structure.computeMaterials(todo);
        List<Container> sources = ResourceScanner.sources(player);
        if (!creative) {
            Map<Item, Integer> have = ResourceScanner.count(sources, need.keySet());
            List<String> missing = new ArrayList<>();
            for (Map.Entry<Item, Integer> e : need.entrySet()) {
                int h = have.getOrDefault(e.getKey(), 0);
                if (h < e.getValue()) missing.add(e.getKey().getDescription().getString() + " ×" + (e.getValue() - h));
            }
            if (!missing.isEmpty()) {
                player.sendSystemMessage(Component.literal("§cНе хватает ресурсов (инвентарь + сундуки в радиусе " + ResourceScanner.RADIUS + "): §f"
                        + String.join(", ", missing.subList(0, Math.min(8, missing.size())))
                        + (missing.size() > 8 ? " …и ещё " + (missing.size() - 8) : "")));
                return;
            }
            ResourceScanner.take(sources, need);
        }

        // 3) order: ground fill first, then solid blocks bottom-up, fluids LAST (so basins are sealed before water/lava appears)
        List<Integer> order = new ArrayList<>();
        for (int i = 0; i < todo.size(); i++) order.add(i);
        order.sort(Comparator.comparingInt((Integer i) -> isFluid(todo.get(i).state()) ? 1 : 0));
        List<Structure.Entry> entries = new ArrayList<>();
        List<BlockPos> poss = new ArrayList<>();

        int filled = 0;
        for (int[] col : pl.foundation()) {            // free ground fill below every column that touches the ground plane
            for (int d = 1; d <= MAX_FOUNDATION_DEPTH; d++) {
                BlockPos pos = origin.offset(col[0], -d, col[1]);
                BlockState cur = level.getBlockState(pos);
                boolean replaceable = cur.isAir() || cur.canBeReplaced() || !cur.getFluidState().isEmpty();
                if (!replaceable) break;
                if (!level.mayInteract(player, pos)) break;
                entries.add(new Structure.Entry(col[0], -d, col[1], s.foundationState));
                poss.add(pos);
                filled++;
            }
        }
        for (int i : order) { entries.add(todo.get(i)); poss.add(targets.get(i)); }

        BuildManager.add(new BuildJob(level, player.getUUID(), entries, poss));
        player.sendSystemMessage(Component.literal("§aСтроительство «" + s.name.getString() + "» началось: " + todo.size() + " блоков"
                + (filled > 0 ? " + фундамент " + filled : "") + (skipped > 0 ? " (пропущено защищённых/занятых: " + skipped + ")" : "") + "."));
    }

    private static boolean isFluid(BlockState st) { return !st.getFluidState().isEmpty() && st.getBlock() instanceof net.minecraft.world.level.block.LiquidBlock; }

    /** Used by the scan packet. */
    public static Map<Item, Integer> scan(ServerPlayer player, Structure s) {
        return ResourceScanner.count(ResourceScanner.sources(player), s.materials().keySet());
    }

    public static String keyOf(Item i) {
        var k = ForgeRegistries.ITEMS.getKey(i);
        return k == null ? "minecraft:air" : k.toString();
    }
}
