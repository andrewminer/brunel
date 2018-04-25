import mods.jei.JEI.removeAndHide;

function removeAll(itemStack as IItemStack, metadata as int[]) {
    val itemDef = itemStack.definition as IItemDefinition;
    for i in metadata {
        removeAndHide(itemDef.makeStack(i));
    }
}

function removeInRange(itemStack as IItemStack, start as int, end as int) {
    val itemDef = itemStack.definition as IItemDefinition;
    for i in start..end {
        removeAndHide(itemDef.makeStack(i));
    }
}

print("Removing banned items...");

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
removeAndHide(<thermalfoundation:rockwool>);
removeAndHide(<thermalfoundation:security>);

removeAll(<thermalfoundation:bait>, [ 0, 1, 2 ]);
removeAll(<thermalfoundation:coin>, [ 0, 65, 67, 68, 69, 70, 71, 72, 96, 97, 98, 99, 100, 101, 102, 103 ]);
removeAll(<thermalfoundation:material>, [ 512, 513, 514, 515, 771, 800, 801 ]);
removeInRange(<thermalfoundation:rockwool>, 0, 15);
removeAll(<thermalfoundation:upgrade>, [ 1, 2, 3, 33, 34, 35, 256 ]);

print("Done.");
