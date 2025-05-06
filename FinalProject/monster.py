import random

class Monster:
    element_weakness = {
        "Fire": {"Metal": 1.5, "Water": 0.8},  # Metal afraid to fire
        "Water": {"Fire": 1.5, "Earth": 0.8},  # Fire afraid to Water
        "Wood": {"Earth": 1.5, "Metal": 0.8},  # Earth afraid to Wood
        "Metal": {"Wood": 1.5, "Metal": 0.8},  # wood afraid to Metal
        "Earth": {"Water": 1.5, "Wood": 0.8}  # Water afraid to Earth
    }

    def __init__(self, name, level, hp, attack, defense,element):
        self.name = f"{name}---<{element}> Element"
        self.level = level # decide level ( 1=low level，2=medium level, 3=high level, 4=Boss)
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.element = element

    def attack_target(self, target) -> float:
        """attack damage"""
        # calculate damage
        base_damage = self.attack + random.randint(1,2)
        base_damage = max(1, base_damage)  # make sure min damage is 1

        # calculate element boots
        element_multiplier = 1.0
        if self.element in Monster.element_weakness:
            if target.element in Monster.element_weakness[self.element]:
                element_multiplier = Monster.element_weakness[self.element][target.element]

        return base_damage * element_multiplier

    def take_damage(self, damage: int):
        """calculate damage take"""
        #damage
        actual_damage = max(1, damage - self.defense * 0.5)

        # take the damage
        self.hp = max(0, self.hp - actual_damage)
        print(f"💢 {self.name} got {actual_damage:0.2f} damage!!")

        if self.hp <= 0:
            print("💀 You beat monster")
        return actual_damage




low_level_monsters = [
    Monster("Goblin", level=1, hp=50, attack=10, defense=2.5, element="Wood"),
    Monster("Slime", level=1, hp=30, attack=5, defense=3.9, element="Earth")
]

medium_level_monsters = [
    Monster("Dragon", level=2, hp=146, attack=35, defense=4.2, element="Fire"),
    Monster("Demon", level=2, hp=120, attack=30, defense=6.5, element="Fire")
]

high_level_monsters = [
    Monster("Flash Wolf", level=3, hp=200, attack=46, defense=10, element="Metal"),
    Monster("Judgment Angle", level=3, hp=150, attack=57, defense=25, element="Metal")
]

boss = [
    Monster("Frost Banshee", level=4, hp=600, attack=80, defense=44, element="Water"),
    Monster("Flame King", level=4, hp=359, attack=100, defense=16, element="Fire")
]


def clone_monster(monster):
    return Monster(
        name=monster.name.split("---")[0],  # 去掉元素后缀
        level=monster.level,
        hp=monster.hp,
        attack=monster.attack,
        defense=monster.defense,
        element=monster.element
    )

if __name__ == '__main__':
    pass