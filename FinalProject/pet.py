import random
import monster
import json

class SpiritBeast:
    element_weakness = {
        "Fire": {"Metal": 1.5, "Water": 0.8},  # Metal afraid to fire
        "Water": {"Fire": 1.5, "Earth": 0.8},  # Fire afraid to Water
        "Wood": {"Earth": 1.5, "Metal": 0.8},  # Earth afraid to Wood
        "Metal": {"Wood": 1.5, "Metal": 0.8},  # wood afraid to Metal
        "Earth": {"Water": 1.5, "Wood": 0.8}  # Water afraid to Earth
    }
    elements = ["Metal", "Wood", "Water", "Fire", "Earth"]
    def __init__(self, name: str):
        """
        Initialise the spirit beast attribute
        name:
        level:
        exp:
        HP:
        attack:
        defense:
        element:
        stage:
        skills:
        energy:
        :param name:
        """
        self.name = name
        self.level = 0
        self.exp = 0
        self.HP = 100
        self.max_HP = 100
        self.attack = 10
        self.defense = 5
        self.element = "Unawakened"  # Metal, Wood, Water, Fire, Earth
        self.stage = "child stage"  # grow-up stage/ maturity stage/ Complete stage
        self.skills = []
        self.energy = 100 # set maximum energy is 100, and min is 0.
        self.package = {
            "Devil Fruits" : 0,
            "Energy Fruit" : 0,
            "Recovery pills" : 0,
            "Strength pills" : 0
        } # food

        self.skills_map = {
            20: {
                'Metal': ['Metal Impact', 'Steel Aegis'],
                'Wood': ['Entangling Vines', "Nature's Cure"],
                'Water': ['Aqua Barrier', 'Frost Bolt'],
                'Fire': ['Fireball', 'Inferno Charge'],
                'Earth': ['Stone Armor', 'Spike Burst']
            },

            30: {
                'Metal': ['Magnetic Storm', 'Wolfram Claws'],
                'Wood': ["Forest's Wrath", 'Life Blossom'],
                'Water': ['Blizzard', 'Hydro Tornado'],
                'Fire': ['Inferno Storm', 'Inferno Storm'],
                'Earth': ['Seismic Wave', 'Sandstorm']
            },

            50: {
                'Metal': ['Supernova Detonation'],
                'Wood': ["Yggdrasil's Descent"],
                'Water': ['Abyssal Maelstrom'],
                'Fire': ['Karmic Blaze'],
                'Earth': ['Primordial Cataclysm']
            }
        }

    def level_up(self):
        """
        handle the continuous level_up
        """
        upgraded = False
        while True:
            current_level = self.level
            # calculate current_level's exp needed
            required_exp = 50 * (2 ** (current_level // 5))

            # check if required
            if self.exp >= required_exp:
                # cost exp
                self.exp -= required_exp
                # level up
                self.level += 1
                # attribute grow
                self.attack += 5 + random.randint(0, 2)
                self.defense += 3 + random.randint(0, 1)
                self.max_HP += 20
                self.HP = self.max_HP  # recovery full of hp

                # print info
                print(f"\n✨ {self.name} Level up to Lv.{self.level}!")
                # evolve check
                self.evolve()
                self.learn_skill()
                upgraded = True
                if self.level >= 50:
                    self.maximum_level()
            else:
                break
        return upgraded

    def maximum_level(self):
        """
        if level are 50
        :return: you are already maximum_level
        """
        if self.level >= 50:
            self.level = 50
            self.exp = 0

        print(f"""
        🔥🔥🔥 {self.name} are already maximum_level！
        ▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞
        ⚔️  attack:{self.attack}
        🛡️  defense:{self.defense}
        ❤️  HP: {self.max_HP}
        ▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚
        🔥🔥🔥
        """)

    def evolve(self):
        """
        check evolve stage
        :return:
        """
        evolution_map = {
            10: 'Grow-up Stage',
            20: 'Maturity Stage',
            35: 'Complete Stage'
        }

        for lv in sorted(evolution_map.keys(),reverse=True):
            if self.level == lv:
                self.stage = evolution_map[lv]
                self.awaken_element()
                print(f"🌌 {self.name} evolve to {evolution_map[lv]}!\n")


    def awaken_element(self):
        """awaken_five element"""
        if self.element == "Unawakened":
            self.element = random.choice(self.elements)
            print(f"💫 awaken {self.element} element!\n")


    def feed(self, food: str):
        """
        if nothing in package then print noting in the package,
            "Devil Fruits" : every thing growth 5.
            "Energy Fruit" : energy increase 20 max energy is 100,if 100 print energy is full
            "Recovery pills" : Hp recover full
            "Strength pills" : attack increase 5
        :param food: string with food
        :return:
        """
        if food not in self.package:
            print(f"\n⚠️ Invalid item: {food}")
            return False

        if self.package[food] == 0:
            print("\n⚠️ You don't have this item!\n")
            return False

        if food == "Energy Fruit" and self.energy == 100:
            print("\n⚡ full of energy don't need to use!")
            return False

        if food == "Recovery pills" and self.HP == self.max_HP:
            print("\n❤️ Your HP is full don't need to use!")
            return False


        #used food
        self.package[food] -= 1

        if food == "Devil Fruits":
            self.defense += 5
            self.attack += 5
            self.max_HP += 5
            self.HP = min(self.HP + 5, self.max_HP)
            print(f"\n🍖 used {food}!, All attributes +5!\n")

        elif food == "Energy Fruit":
            self.energy = min(self.energy + 20 , 100)
            print(f"\n🍖 used {food}!, energy increase 20! current energy is {self.energy}/100 \n")

        elif food == "Recovery pills":
            self.HP = self.max_HP
            print(f"\n🍖 used{food}!, your HP are full\n")

        elif food == "Strength pills":
            self.attack += 5
            print(f"\n🍖 used{food}!, your attack increased 5!\n")


    def take_damage(self, damage):
        """calculate damage"""
        #damage
        actual_damage = max(1, damage - self.defense * 0.5)

        # take the damage
        self.HP = max(0, self.HP - actual_damage)
        print(f"\n💢 {self.name} got {actual_damage:0.2f} damage!!")

        if self.HP <= 0:
            print("\n💀 your Spirit Beast dead!")
        return actual_damage

    def attack_target(self, target) -> float:
        """attack damage"""
        # calculate damage
        base_damage = self.attack
        base_damage = max(1, base_damage)  # make sure min damage is 1

        # calculate element boots
        element_multiplier = 1.0
        if self.element in SpiritBeast.element_weakness:
            if target.element in SpiritBeast.element_weakness[self.element]:
                element_multiplier = SpiritBeast.element_weakness[self.element][target.element]

        return base_damage * element_multiplier

    def heal(self, amount: float):
        """heal system"""
        if self.energy >= 50 and self.HP != self.max_HP:
            self.energy = min(self.energy - amount, 100)
            #1 energy  = 10 hp
            self.HP = min(self.HP + amount * 10, self.max_HP)
            print(f"\n⚡ spend {amount} energy! current energy:{self.energy}/100")
            print(f"\n💚 heal {amount * 10} HP! current HP: {self.HP}/{self.max_HP}")

    def learn_skill(self):
        """learn_skill"""
        #check the lv in skills map
        for lv in sorted(self.skills_map.keys(),reverse=True):
            #if level equal to lv
            if self.level == lv:
                    #append skills in skills
                    for element in self.skills_map[lv]:
                        # check element is correct
                        if element == self.element:
                            skill = random.choice(self.skills_map[lv][element])
                            print(f"📚 study new skills {skill}!\n")
                            self.skills.append(skill)

    def use_skill(self, skill_name):
        if skill_name not in self.skills:
            print(f"⚠️⚠️⚠️ You don't have {skill_name} skills:(\n")
            return 0
        if self.energy < 10:
            print(f"⚠️⚠️⚠️ You don't have enough energy!\n")
            return 0

        skill_level = None
        for lv, elements in self.skills_map.items():
            for element, skills in elements.items():
                if skill_name in skills:
                    skill_level = lv
                    break
            if skill_level:
                break

        if not skill_level:
            print(f"⚠️ {skill_name} is not a valid skill")
            return 0

        #skills effect
        skill_effects = {
            20: {"damage_bonus": 25, "energy_cost": 10},
            30: {"damage_bonus": 100, "energy_cost": 15},
            50: {"damage_bonus": 999, "energy_cost": 80}
        }

        # if skill_level in effects
        if skill_level not in skill_effects:
            print(f"\n⚠️ No effect defined for level {skill_level}")
            return 0
        effect = skill_effects[skill_level]

        # if effect in effect
        if "energy_cost" not in effect or "damage_bonus" not in effect:
            print(f"\n⚠️ Missing effect parameters for level {skill_level}")
            return 0

        energy_cost = effect["energy_cost"]
        damage_bonus = effect["damage_bonus"]

        # check enough energy
        if self.energy < energy_cost:
            print("\n⚠️ Not enough energy")
            return 0

        # cost energy
        else:
            self.energy -= energy_cost

            print(f"\n✨ {skill_name} used! (⚔️{damage_bonus + self.attack} damage, -{energy_cost} energy)")
            return damage_bonus + self.attack

    #show the package
    def package_show(self):
        package_items = []
        for item, num in self.package.items():
            if num > 0:
                package_items.append(f"📦 {item}: {num}")

        if package_items:
            package_list = " ".join(package_items)
        else:
            package_list = "no items!"
        return  f"🎒 Package: {package_list}"

    def show_skills(self):
        #skills check
        if self.skills:
            skills_list = " ".join([f"📚 {skill}" for skill in self.skills])
        else:
            skills_list = "🎯 no skills!"
        return f"🎯 Skill: {skills_list}"


    def __str__(self):
        """show the attribute"""

        status = f"""
    🐉[{self.name}]---[{self.stage}]
    🔰 level: Lv.{self.level} ({self.exp}/{(50 * (2 ** (self.level // 5))):.0f})
    ❤️ HP: {self.HP}/{self.max_HP}
    ⚔️ Attack: {self.attack} 🛡️ Defence: {self.defense}
    🌈 Element:{self.element}
    🔋 Energy: {self.energy}/100
    {self.show_skills()}
    {self.package_show()}
        """
        return status

    def to_dict(self):
        """turn SpiritBeast to dict"""
        return {
            "name": self.name,
            "level": self.level,
            "exp": self.exp,
            "HP": self.HP,
            "max_HP": self.max_HP,
            "attack": self.attack,
            "defense": self.defense,
            "element": self.element,
            "stage": self.stage,
            "skills": self.skills,
            "energy": self.energy,
            "package": self.package
        }

    @classmethod
    def from_dict(cls, data):
        """turn dict into data"""
        pet = cls(data["name"])
        pet.level = data["level"]
        pet.exp = data["exp"]
        pet.HP = data["HP"]
        pet.max_HP = data["max_HP"]
        pet.attack = data["attack"]
        pet.defense = data["defense"]
        pet.element = data["element"]
        pet.stage = data["stage"]
        pet.skills = data["skills"]
        pet.energy = data["energy"]
        pet.package = data["package"]
        return pet

if __name__ == '__main__':
    pass
    # name = input("enter your name: ")
    # monster = main.spawn_monster(4)
    # while True:
    #
    #     pet = SpiritBeast(name)
    #     show_off = input("Do you want to show off all element? (y/n): ")
    #
    #
    #     if show_off.lower() == 'y':
    #         print(pet)
    #     else:
    #         print("back to main")
    #
    #
    #     fight = input("Do you want to fight? (y/n): ")
    #     if fight.lower() == 'y':
    #
    #         pet.learn_skill()
    #         pet.exp += 400000
    #         pet.level_up()
    #         pet.package["Energy Fruit"] = 1
    #         pet.package["Strength pills"] = 1
    #         print(f"choose your skills{pet.show_skills()}:")
    #         skill = input("input skill: ")
    #         pet.use_skill(skill)
    #         print("you win and gain 500 exp")
    #         print(pet)
    #
    #     else:
    #         pet.take_damage(monster.attack_target(pet))
    #         heal = input("Do you want to heal? (y/n): ")
    #         if heal.lower() == 'y':
    #             hp = int(input("How many HP?: "))
    #             pet.heal(hp)
    #         else:
    #             print(pet.HP)
    #
    #     feed = input("Do you want to feed? (y/n): ")
    #     if feed.lower() == 'y':
    #         print(f"choose your food{pet.package_show()}\n:")
    #         food = input("what food you want to use?: ")
    #         pet.feed(food)
    #         print(pet)
    #









