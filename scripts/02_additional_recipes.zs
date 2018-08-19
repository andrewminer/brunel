val hammer = <immersiveengineering:tool:0>.reuse();

recipes.addShapeless(<rtfm:book_manual>, [<minecraft:book>,<minecraft:book>]);
recipes.addShapeless(<thermalfoundation:coin:1>, [<ore:nuggetGold>,hammer]);
recipes.addShapeless(<thermalfoundation:coin:64>, [<ore:nuggetCopper>,hammer]);
recipes.addShapeless(<thermalfoundation:coin:66>, [<ore:nuggetSilver>,hammer]);

recipes.addShaped(<wearablebackpacks:backpack>, [[<ore:leather>, <ore:ingotBronze>, <minecraft:leather>],[<minecraft:leather>, <ore:blockWool>, <minecraft:leather>], [<minecraft:leather>, <minecraft:leather>, <minecraft:leather>]]);
recipes.addShaped(<wearablebackpacks:backpack>, [[<ore:leather>, <ore:ingotCopper>, <minecraft:leather>],[<minecraft:leather>, <ore:blockWool>, <minecraft:leather>], [<minecraft:leather>, <minecraft:leather>, <minecraft:leather>]]);
