import time
from time import sleep


import pet
from pet import *
from monster import *

class BattleSystem:
    def __init__(self, player_pet, enemy: monster.Monster):
        self.player_pet = player_pet  # player spririt beast
        self.enemy = enemy  # monster
        self.turn_count = 0  # turn count
        self.battle_over = False  # check battle is over or not
        self.escaped_success = False

    # === main flow check ===
    def start_battle(self) -> bool:
        """battle flow check True of false"""
        print(f"\n🆚You met {self.enemy.name}, Level: {self.enemy.level}, Hp:{self.enemy.hp}!")
        time.sleep(1)
        print("🆚Battle started!!🆚")
        time.sleep(1)
        print("3!")
        time.sleep(1)
        print("2!")
        time.sleep(1)
        print("1!")
        time.sleep(1)

        if self.player_pet.element in self.enemy.element_weakness:
            print("\n✨Element weakness are activated")
            time.sleep(1)
        else:
            print("\n✨This battle don't have Element weakness Scenario✨")
            time.sleep(1)
        while self.player_pet.HP > 0 and self.enemy.hp > 0:

            self.show_battle_ui()
            time.sleep(1)

            self.player_turn()
            time.sleep(1)

            #if escaped break
            if self.escaped_success:
                break

            #if enemy dead break
            if self.enemy.hp <= 0:
                break
            self.enemy_turn()

            self.turn_count += 1
        return self.end_battle()

    #player flow check
    def player_turn(self):
        """handle the player turn"""
        print("\n=====  Your Turn =====")
        while True:
            print("\n1. ⚔️Normal attack")
            print("2. ✨Use skills")
            print("3. 💊Use package")
            print("4. 🏃Escape (Only 30%) and (Spend 10 Energy)")
            print("5. ❤️Heal (use Energy to heal)\n")
            choice = input("Choose your action 1 | 2 | 3 | 4 | 5 :")

            if choice == '1':  # Normal attack
                self.enemy.take_damage(self.player_pet.attack_target(self.enemy))
                break

            elif choice == '2':  # Use skills

                if self.player_pet.skills:
                    print(f"\nChoose the skills you want to use{self.player_pet.show_skills()}")
                    player_skill = input("Input your skill: ")

                    if player_skill in self.player_pet.skills:
                        #monster take damage from user skills
                        self.enemy.take_damage(self.player_pet.use_skill(player_skill))
                    else:
                        print("invalid input skill")
                        continue

                else:
                    print("⚠️You don't have skills yet :(")
                    continue
                break

            elif choice == '3':  # Use package
                # check is empty
                if all(value == 0 for value in self.player_pet.package.values()):
                    print("⚠️You don't have any food yet :(")
                    continue
                else:
                    # if have choose
                    print(f"\nChoose the package you want to use{self.player_pet.package_show()}")
                    food_choice = input("\nChoose the food you want to use:")
                    if food_choice == "Recovery pills" and self.player_pet.HP == self.player_pet.max_HP:
                        self.player_pet.feed(food_choice)
                        continue
                    else:
                        self.player_pet.feed(food_choice)
                break

            elif choice == '4':  # Escape
                return self.escaped()

            # heal
            elif choice == '5':  # Escape
                try:
                    if self.player_pet.HP == self.player_pet.max_HP:
                        print("\n❤️❤️❤️Your Hp is full no need to heal!")
                        continue
                    else:
                        heal_hp = float(input("\n❤️❤️❤️How many HP do you want to heal? "))
                        return  self.player_pet.heal(heal_hp)

                except ValueError:
                    print("Please enter a valid number.")
                    continue

            else:
                print("\n⚠️ Invalid Choice!")
                continue
            # return False

    def escaped(self):
        """check escape condition"""
        if self.player_pet.energy <= 0:
            print("\n⚠️You don't have energy yet :(")
            return False

        elif random.random() < 0.3:
            print("\n🚀 Escape Success!")
            self.escaped_success = True  # success
            return True
        else:
            print("\n❌ Escape Failed!")
            sleep(1)
            print("\nYou spend 10 energy to escape")
            self.player_pet.energy -= 10
            return False


    def enemy_turn(self):
        """enemy tern"""
        print("\n=====  Enemy Turn =====")
        print("\n⚠️⚠️Waiting the Enemy action!!⚠️⚠️")
        time.sleep(3.5)
        self.player_pet.take_damage(self.enemy.attack_target(self.player_pet))


    # === UI ===
    def show_battle_ui(self):
        """show the battle ui"""
        print(f"\n==== Round {self.turn_count+1} ====")
        print(f"<{self.player_pet.name}> ❤️HP {self.player_pet.HP:0.2f}/{self.player_pet.max_HP:0.2f} | ⚡Energy {self.player_pet.energy}")
        print(f"💀<{self.enemy.name}>💀 ❤️HP {self.enemy.hp:0.2f}")
        print("▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞")

    def end_battle(self):
        """end battle flow check True of false"""
        if self.player_pet.HP <= 0:
            print("\n💀 Battle Failed...")
            return False

        elif self.escaped_success:  # 优先判断逃跑成功
            print("🎉 No exp gain and No Awards")
            return True

        elif self.enemy.hp <= 0:
            print(f"\n🎉 Congrats！You beat {self.enemy.name}!")

            # price
            exp = self.enemy.level * 50
            self.player_pet.exp += exp
            print(f"\n✨ You gain {exp} experience！")

            # awards
            if random.random() < 0.4:
                item = random.choice(list(self.player_pet.package.keys()))
                self.player_pet.package[item] += 1
                print(f"\n📦 {self.enemy.name} become a {item}!")
            return True
        return True


if __name__ == '__main__':
    pass
    #
    # level = random.randint(1, 4)
    # monster = main.spawn_monster(level)
    #
    #
    # player = SpiritBeast(name="Lier")
    #
    #
    # player.HP = 120
    # player.attack = 15
    # player.level = 0
    # player.exp = 0
    # player.HP = 100
    # player.max_HP = 100
    # player.attack = 10
    # player.defense = 5
    # player.element = "Metal"  # Metal, Wood, Water, Fire, Earth
    # player.stage = "child stage"  # grow-up stage/ maturity stage/ Complete stage
    # player.skills = ["Supernova Detonation"]
    # player.energy = 100
    #
    #
    # battle = BattleSystem(player, enemy=monster)
    # battle.start_battle()