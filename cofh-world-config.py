import json

from enum import Enum

class Altitude(Enum):
    LAVA = (0, 12)
    DEEP = (13, 48)
    BURIED = (49, 64)
    SURFACE = (65, 80)
    HILLS = (81, 128)
    MOUNTAINS = (128, 256)

    GRAVEL = (54, 64)

    def __init__(self, min_height=0, max_height=256):
        self.min_height = min_height
        self.max_height = max_height


class Density(Enum):
    DENSE = (12, 12)
    NORMAL = (8, 9)
    TRACE = (4, 12)

    def __init__(self, cluster_size=0, cluster_count=0, chunk_chance=1):
        self.cluster_size = cluster_size
        self.cluster_count = cluster_count
        self.chunk_chance = chunk_chance

    def adjusted_cluster_count(self, altitude):
        altitude_factor = (altitude.max_height - altitude.min_height) / 16
        return round(altitude_factor * self.cluster_count)


class Ore(object):

    def __init__(self, name=None, metadata=0, weight=100):
        self.name = name
        self.metadata = metadata
        self.weight = weight

    def as_json(self):
        if self.metadata == 0 and self.weight == 100:
            return self.name
        else:
            result = {"name": self.name}

            if self.metadata != 0:
                result["metadata"] = self.metadata
            if self.weight != 100:
                result["weight"] = self.weight

            return result


class Vein(object):

    def __init__(self, name=None, *ores):
        self.name = name
        self.ores = ores

    def as_json(self):
        if len(self.ores) == 1:
            return self.ores[0].as_json()
        else:
            return list(o.as_json() for o in self.ores)


class Deposit(object):

    def __init__(self, vein=None, biome_type=None, altitude=Altitude.SURFACE, density=Density.NORMAL):
        self.vein = vein
        self.altitude = altitude
        self.biome_type = biome_type
        self.density = density

        self.material = Vein("stone", Ore("stone", -1))

    @property
    def name(self):
        return f"{self.vein.name.upper()}-{self.altitude.name}-{self.biome_type}"

    def as_json(self):
        result = {
            "enabled": True,
            "generator": {
                "block": self.vein.as_json(),
                "material": self.material.as_json(),
                "type": "cluster",
                "cluster-size": self.density.cluster_size,
            },
            "chunk-chance": self.density.chunk_chance,
            "cluster-count": self.density.adjusted_cluster_count(self.altitude),

            "distribution": "uniform",
            "min-height": self.altitude.min_height,
            "max-height": self.altitude.max_height,

            "biome": {
                "restriction": "whitelist",
                "value": {
                    "type": "dictionary",
                    "entry": [ self.biome_type ]
                }
            },
            "dimension": {
                "restriction": "blacklist",
                "value": [ -1, 1 ]
            }
        }
        if self.altitude is Altitude.GRAVEL:
            result["generator"]["material"] = "gravel"

        return result


class GravelDeposit(Deposit):

    def __init__(self, vein=None, biome_type=None, density=Density.NORMAL):
        super().__init__(vein=vein, biome_type=biome_type, altitude=Altitude.BURIED, density=density)

    @property
    def name(self):
        return f"{self.vein.name.upper()}-{self.biome_type}-GRAVEL"

    def as_json(self):
        result = super().as_json()
        result["generator"]["material"] = [ "gravel" ]
        result["gen-fluid"] = "water"
        result["cluster-count"] *= 2
        result["min-height"] = 0
        result["max-height"] = 65
        return result


# Veins
coal = Vein("coal", Ore("coal_ore"))
iron = Vein("iron", Ore("iron_ore", weight=80), Ore("thermalfoundation:ore", 5, weight=20))
gold = Vein("gold", Ore("gold_ore"))
diamond = Vein("diamond", Ore("diamond_ore", weight=80), Ore("emerald_ore", weight=20))
tin = Vein("tin", Ore("thermalfoundation:ore", 1))
copper = Vein("copper", Ore("thermalfoundation:ore", 0))
apatite = Vein("apatite", Ore("forestry:resources", 0))
aluminum = Vein("aluminum", Ore("thermalfoundation:ore", 4))
lead = Vein("lead", Ore("thermalfoundation:ore", 3, weight=80), Ore("thermalfoundation:ore", 2, weight=20))
lapis = Vein("lapis", Ore("lapis_ore"))
uranium = Vein("uranium", Ore("immersiveengineering:ore", 5, weight=80), Ore("immersiveengineering:ore", 2, weight=20))

tin_gravel = Vein("tin", Ore("gravelores:tin_gravel_ore"))
lapis_gravel = Vein("lapis", Ore("gravelores:lapis_gravel_ore"))
gold_gravel = Vein("gold", Ore("gravelores:gold_gravel_ore"))
iron_gravel = Vein("iron", Ore("gravelores:iron_gravel_ore"))

data = {
    "populate": {d.name: d.as_json() for d in [
        Deposit(coal, "MESA", Altitude.DEEP, Density.TRACE),
        Deposit(coal, "FOREST", Altitude.DEEP, Density.TRACE),
        Deposit(coal, "PLAINS", Altitude.DEEP, Density.DENSE),
        Deposit(coal, "PLAINS", Altitude.BURIED, Density.NORMAL),
        Deposit(coal, "PLAINS", Altitude.SURFACE, Density.TRACE),
        Deposit(coal, "MOUNTAIN", Altitude.DEEP, Density.NORMAL),
        Deposit(coal, "MOUNTAIN", Altitude.BURIED, Density.NORMAL),
        Deposit(coal, "MOUNTAIN", Altitude.SURFACE, Density.DENSE),
        Deposit(coal, "MOUNTAIN", Altitude.HILLS, Density.NORMAL),
        Deposit(coal, "MOUNTAIN", Altitude.MOUNTAINS, Density.TRACE),
        Deposit(coal, "HILLS", Altitude.DEEP, Density.NORMAL),
        Deposit(coal, "HILLS", Altitude.BURIED, Density.NORMAL),
        Deposit(coal, "HILLS", Altitude.SURFACE, Density.DENSE),
        Deposit(coal, "SWAMP", Altitude.DEEP, Density.NORMAL),
        Deposit(coal, "SWAMP", Altitude.BURIED, Density.DENSE),
        Deposit(coal, "SANDY", Altitude.DEEP, Density.TRACE),
        Deposit(coal, "SNOWY", Altitude.DEEP, Density.TRACE),
        Deposit(coal, "WASTELAND", Altitude.DEEP, Density.TRACE),
        Deposit(coal, "BEACH", Altitude.DEEP, Density.TRACE),
        Deposit(coal, "MUSHROOM", Altitude.DEEP, Density.NORMAL),
        Deposit(coal, "MUSHROOM", Altitude.BURIED, Density.TRACE),
        Deposit(coal, "RIVER", Altitude.DEEP, Density.TRACE),
        Deposit(coal, "OCEAN", Altitude.DEEP, Density.TRACE),

        Deposit(iron, "MESA", Altitude.DEEP, Density.TRACE),
        Deposit(iron, "MESA", Altitude.BURIED, Density.TRACE),
        Deposit(iron, "FOREST", Altitude.DEEP, Density.TRACE),
        Deposit(iron, "FOREST", Altitude.BURIED, Density.TRACE),
        Deposit(iron, "PLAINS", Altitude.DEEP, Density.TRACE),
        Deposit(iron, "PLAINS", Altitude.BURIED, Density.TRACE),
        Deposit(iron, "MOUNTAIN", Altitude.LAVA, Density.DENSE),
        Deposit(iron, "MOUNTAIN", Altitude.DEEP, Density.DENSE),
        Deposit(iron, "MOUNTAIN", Altitude.BURIED, Density.NORMAL),
        Deposit(iron, "MOUNTAIN", Altitude.SURFACE, Density.NORMAL),
        Deposit(iron, "MOUNTAIN", Altitude.HILLS, Density.TRACE),
        Deposit(iron, "MOUNTAIN", Altitude.MOUNTAINS, Density.TRACE),
        Deposit(iron, "HILLS", Altitude.LAVA, Density.DENSE),
        Deposit(iron, "HILLS", Altitude.DEEP, Density.NORMAL),
        Deposit(iron, "HILLS", Altitude.BURIED, Density.NORMAL),
        Deposit(iron, "HILLS", Altitude.SURFACE, Density.TRACE),
        Deposit(iron, "HILLS", Altitude.HILLS, Density.TRACE),
        Deposit(iron, "SWAMP", Altitude.DEEP, Density.TRACE),
        Deposit(iron, "SANDY", Altitude.DEEP, Density.TRACE),
        Deposit(iron, "SANDY", Altitude.BURIED, Density.TRACE),
        Deposit(iron, "SNOWY", Altitude.DEEP, Density.TRACE),
        Deposit(iron, "SNOWY", Altitude.BURIED, Density.TRACE),
        Deposit(iron, "WASTELAND", Altitude.DEEP, Density.TRACE),
        Deposit(iron, "WASTELAND", Altitude.BURIED, Density.TRACE),
        Deposit(iron, "BEACH", Altitude.DEEP, Density.TRACE),
        Deposit(iron, "BEACH", Altitude.BURIED, Density.TRACE),
        Deposit(iron, "RIVER", Altitude.DEEP, Density.TRACE),
        Deposit(iron, "OCEAN", Altitude.DEEP, Density.TRACE),

        Deposit(gold, "MESA", Altitude.DEEP, Density.DENSE),
        Deposit(gold, "MESA", Altitude.BURIED, Density.NORMAL),
        Deposit(gold, "MESA", Altitude.SURFACE, Density.TRACE),
        Deposit(gold, "MESA", Altitude.HILLS, Density.TRACE),
        Deposit(gold, "SANDY", Altitude.LAVA, Density.NORMAL),
        Deposit(gold, "SANDY", Altitude.DEEP, Density.NORMAL),
        Deposit(gold, "SANDY", Altitude.BURIED, Density.TRACE),
        Deposit(gold, "WASTELAND", Altitude.DEEP, Density.NORMAL),
        Deposit(gold, "WASTELAND", Altitude.BURIED, Density.TRACE),

        Deposit(diamond, "MESA", Altitude.LAVA, Density.DENSE),
        Deposit(diamond, "FOREST", Altitude.LAVA, Density.TRACE),
        Deposit(diamond, "PLAINS", Altitude.LAVA, Density.TRACE),
        Deposit(diamond, "MOUNTAIN", Altitude.LAVA, Density.DENSE),
        Deposit(diamond, "HILLS", Altitude.LAVA, Density.DENSE),
        Deposit(diamond, "SWAMP", Altitude.LAVA, Density.TRACE),
        Deposit(diamond, "SANDY", Altitude.LAVA, Density.TRACE),
        Deposit(diamond, "SNOWY", Altitude.LAVA, Density.TRACE),
        Deposit(diamond, "WASTELAND", Altitude.LAVA, Density.TRACE),
        Deposit(diamond, "BEACH", Altitude.LAVA, Density.NORMAL),
        Deposit(diamond, "RIVER", Altitude.LAVA, Density.NORMAL),
        Deposit(diamond, "OCEAN", Altitude.LAVA, Density.NORMAL),

        Deposit(tin, "FOREST", Altitude.BURIED, Density.TRACE),
        Deposit(tin, "PLAINS", Altitude.BURIED, Density.TRACE),
        Deposit(tin, "SWAMP", Altitude.BURIED, Density.TRACE),

        Deposit(copper, "FOREST", Altitude.LAVA, Density.NORMAL),
        Deposit(copper, "FOREST", Altitude.DEEP, Density.DENSE),
        Deposit(copper, "FOREST", Altitude.BURIED, Density.NORMAL),
        Deposit(copper, "FOREST", Altitude.SURFACE, Density.TRACE),
        Deposit(copper, "MOUNTAIN", Altitude.DEEP, Density.TRACE),
        Deposit(copper, "MOUNTAIN", Altitude.BURIED, Density.TRACE),
        Deposit(copper, "HILLS", Altitude.DEEP, Density.TRACE),
        Deposit(copper, "RIVER", Altitude.DEEP, Density.TRACE),

        Deposit(apatite, "PLAINS", Altitude.BURIED, Density.NORMAL),
        Deposit(apatite, "PLAINS", Altitude.SURFACE, Density.TRACE),

        Deposit(aluminum, "SANDY", Altitude.LAVA, Density.TRACE),
        Deposit(aluminum, "SANDY", Altitude.DEEP, Density.DENSE),
        Deposit(aluminum, "SANDY", Altitude.BURIED, Density.NORMAL),
        Deposit(aluminum, "SANDY", Altitude.SURFACE, Density.TRACE),

        Deposit(lead, "SNOWY", Altitude.LAVA, Density.TRACE),
        Deposit(lead, "SNOWY", Altitude.DEEP, Density.DENSE),
        Deposit(lead, "SNOWY", Altitude.BURIED, Density.NORMAL),
        Deposit(lead, "SNOWY", Altitude.SURFACE, Density.TRACE),
        Deposit(lead, "SNOWY", Altitude.HILLS, Density.NORMAL),
        Deposit(lead, "SNOWY", Altitude.MOUNTAINS, Density.TRACE),

        Deposit(uranium, "OCEAN", Altitude.LAVA, Density.NORMAL),
        Deposit(uranium, "OCEAN", Altitude.DEEP, Density.NORMAL),
        Deposit(uranium, "WASTELAND", Altitude.LAVA, Density.DENSE),
        Deposit(uranium, "WASTELAND", Altitude.DEEP, Density.NORMAL),
        Deposit(uranium, "WASTELAND", Altitude.BURIED, Density.TRACE),

        GravelDeposit(tin_gravel, "BEACH", Density.NORMAL),

        GravelDeposit(iron_gravel, "RIVER", Density.TRACE),
        GravelDeposit(gold_gravel, "RIVER", Density.TRACE),
        GravelDeposit(lapis_gravel, "RIVER", Density.NORMAL),
        GravelDeposit(tin_gravel, "RIVER", Density.NORMAL),

        GravelDeposit(iron_gravel, "OCEAN", Density.TRACE),
        GravelDeposit(gold_gravel, "OCEAN", Density.TRACE),
        GravelDeposit(lapis_gravel, "OCEAN", Density.TRACE),
        GravelDeposit(tin_gravel, "OCEAN", Density.NORMAL),
    ]}
}

print(json.dumps(data, indent=4))
