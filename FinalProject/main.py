import random
import time
import json
import os

from monster import low_level_monsters, medium_level_monsters, high_level_monsters, boss,clone_monster
from pet import SpiritBeast
from battle_system import BattleSystem


#save file name
SAVE_FILE = "user_data.json"

#save the game
def save_game(player_pet):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:

        #format json file
        json.dump(player_pet.to_dict(), f, indent=4)
    print("💾 Game saved successfully!")

#load the data
def load_game():
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

#random choose the monster in pool
def spawn_monster(level: int):
    """"""
    pool = {
        1: low_level_monsters,
        2: medium_level_monsters,
        3: high_level_monsters,
        4: boss
    }
    template_monster = random.choice(pool[level])

    # avoid monster will get 0 hp after player beat it
    return clone_monster(template_monster)


def gain_exp(player_pet):
    #random experience
    exp = random.randint(50,100 )
    # add exp
    player_pet.exp += exp
    print(f"📈 You gained {exp} EXP from training.")
    player_pet.level_up()

    #30% may drop food
    if random.random() < 0.3:
        item = random.choice(list(player_pet.package.keys()))
        player_pet.package[item] += 1
        print(f"🎁 You found a {item}!")

# mode of battle
def encounter_monster_mode(player_pet):

    # main menu
        print("\n🎮 Choose Difficulty:")
        print("1. 🟢 Simple Mode (5 stages)")
        print("2. 🟡 Medium Mode (10 stages)")
        print("3. 🔴 Hard Mode (15 stages)")
        choice = input("Enter your choice: ")

        #check user input
        if choice == '1':
            difficulty = 'simple'
            stages = 5
        elif choice == '2':
            difficulty = 'medium'
            stages = 10
        elif choice == '3':
            difficulty = 'hard'
            stages = 15
        else:
            print("⚠️ Invalid difficulty. Returning to main menu.")
            return

        #check the num of stage
        for i in range(stages):
            print(f"\n🚶 Entering stage {i + 1}/{stages}...")

            time.sleep(2)

            #probability of monster come out
            chance = random.random()

            #probability of monster come out in simple mode
            if difficulty == 'simple':
                if chance < 0.55:
                    enemy = spawn_monster(1)
                elif chance < 0.1:
                    enemy = spawn_monster(2)
                else:
                    print("🍃 Nothing happened... But you trained.")
                    time.sleep(1)
                    gain_exp(player_pet)
                    time.sleep(1)
                    continue

            #probability of monster come out in medium mode
            elif difficulty == 'medium':
                if chance < 0.55:
                    enemy = spawn_monster(1)
                elif chance < 0.20:
                    enemy = spawn_monster(2)
                elif chance < 0.10:
                    enemy = spawn_monster(3)
                else:
                    print("🍃 Nothing happened... But you trained.")
                    time.sleep(1)
                    gain_exp(player_pet)
                    time.sleep(1)
                    continue

            #probability of monster come out in hard mode
            elif difficulty == 'hard':
                if chance < 0.05:
                    enemy = spawn_monster(1)
                elif chance < 0.25:
                    enemy = spawn_monster(2)
                elif chance < 0.45:
                    enemy = spawn_monster(3)
                elif chance < 0.15:
                    enemy = spawn_monster(4)
                else:
                    print("🍃 Nothing happened... But you trained.")
                    time.sleep(1)
                    gain_exp(player_pet)
                    time.sleep(1)
                    continue

            # Battle
            print("\n🍃End of Training🍃")
            battle = BattleSystem(player_pet,enemy)
            result = battle.start_battle()

            #check player exp can level up
            player_pet.level_up()

            if not result:
                break


def main():
    time.sleep(1)
    print("🎮 Welcome to Spirit Beast Battle Game!")
    time.sleep(1)

    name = input("Please name your Spirit Beast: ")

    # Check if the save file exists
    if not os.path.exists(SAVE_FILE):
        print("🎮 Let's Start New Journey 🎮")
        player_pet = SpiritBeast(name)
        save_game(player_pet)

    else:
        # Load the saved data
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check if the pet name matches
        if data['name'] == name:
            print(f"👋 Welcome back, {name}!")
            player_pet = SpiritBeast.from_dict(data)  # Use from_dict to load the data
        else:
            print("🎮 Let's Start New Journey 🎮")
            player_pet = SpiritBeast(name)
            save_game(player_pet)

    #start game
    while True:
        # mian menu
        print("\n📋 Menu:")
        print("1. 🧟 Start practicing")
        print("2. ❤️ Show Spirit Beast Status")
        print("3. ❌ Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            encounter_monster_mode(player_pet)

        elif choice == '2':
            print(player_pet.__str__())
            continue

        elif choice == '3':
            print("Bye!")
            save_game(player_pet)
            break

        else:
            print("⚠️ Invalid input. Please choose 1, 2 or 3.")


if __name__ == "__main__":
    main()