import crafttweaker.item.IItemDefinition;
import crafttweaker.item.IItemStack;
import mods.jei.JEI.removeAndHide;

function removeAll(itemStack as IItemStack, metadata as int[]) {
    for index in metadata {
        removeAndHide(itemStack.definition.makeStack(index));
    }
}

function removeInRange(itemStack as IItemStack, start as int, end as int) {
    for i in start..end {
        removeAndHide(itemStack.definition.makeStack(i));
    }
}

print("Removing banned items...");

removeAndHide(<agricraft:debugger>);
removeAndHide(<agricraft:peripheral>);
removeAndHide(<biomesoplenty:biome_finder>);
removeAndHide(<dynamictrees:staff>);
removeAndHide(<forestry:analyzer>);
removeAndHide(<forestry:genetic_filter>);
removeAndHide(<forestry:rainmaker>);
removeAndHide(<harvestcraft:apiary>);
removeAndHide(<harvestcraft:market>);
removeAndHide(<malisisdoors:forcefielditem>);
removeAndHide(<minecraft:beacon>);
removeAndHide(<minecraft:barrier>);
removeAndHide(<minecraft:brewing_stand>);
removeAndHide(<minecraft:chain_command_block>);
removeAndHide(<minecraft:command_block>);
removeAndHide(<minecraft:command_block_minecart>);
removeAndHide(<minecraft:knowledge_book>);
removeAndHide(<minecraft:repeating_command_block>);
removeAndHide(<minecraft:structure_block>);
removeAndHide(<minecraft:structure_void>);
removeAndHide(<minecraft:totem_of_undying>);
removeAndHide(<thermalfoundation:glass>);
removeAndHide(<thermalfoundation:meter>);
removeAndHide(<thermalfoundation:security>);
removeAndHide(<twilightforest:ore_meter>);

removeAll(<thermalfoundation:bait>, [ 0, 1, 2 ] as int[]);
removeAll(<thermalfoundation:coin>, [ 0, 65, 67, 68, 69, 70, 71, 72, 96, 97, 98, 99, 100, 101, 102, 103 ] as int[]);
removeAll(<thermalfoundation:material>, [ 512, 513, 514, 515, 771, 800, 801 ] as int[]);
removeInRange(<thermalfoundation:rockwool>, 0, 15);
removeInRange(<davincisvessels:balloon>, 0, 15);
removeAll(<thermalfoundation:upgrade>, [ 0, 1, 2, 3, 33, 34, 35, 256 ] as int[]);

print("Done.");
