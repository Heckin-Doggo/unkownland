# from threading import Timer
# from collections import namedtuple
from time import sleep
import quests
import data
import shop
import inventory
import os
from essentials import add_commas
import world

# latest update: added ryan as a boss
# still need to add burnt popcorn


# naming convention as follows:
# RELEASE.BIGUPDATE.Run (BUILD)
build = data.load_version()
print("Version 0.7.0 (Build {})".format(build))

# uncomment this during development to increase build number. comment for full release
data.save_version(build)

"""
def test():
  print("whats poppin")

t = Timer(5.0, test)
t.start()
print("does it continue tho")
"""


#  we are no longer using namedtuples they gay
# Player = namedtuple("Player", "name weapon quest health max_health defence completed")


# The Player Class
class Player:
    def __init__(self, name, weapon, quest, health, defence, crit_chance=10):
        self.name = name
        self.weapon = weapon
        self.quest = quest
        self.health = health
        self.max_health = health
        self.defence = defence
        self.completed = []
        self.xp = 0
        self.level = 1
        self.inventory = {"Test Item": 100, "bread": 5}  # TODO The actual v.1.0 release should remove this
        self.money = 0
        self.crit_chance = crit_chance
        self.debugEnabled = False
        self.traits = []  # this will hold traits that, if had, activate special things. ex: having "cute" could
        #                   dull an enemy's senses or something. maybe lower attack

    def debug(self):
        self.quest = input("Set new Quest: ")
        self.money += int(input("Set Money: "))
        self.health = 9999
        self.max_health = 9999
        self.level = int(input("Set level: "))
        self.xp = int(input("Set XP:"))
        choice = input("New Item? ")
        amount = int(input("New Value? "))
        self.inventory.update({choice: amount})
        self.debugEnabled = True

    def xp_check(self):
        level_up = 80 * self.level + (100 * .05 * self.level)
        hp_gain = 0
        while self.xp >= level_up:
            self.level += 1
            hp_gain += int(10 + .5*self.level)
            level_up = 80 * self.level + (100 * .05 * self.level)
        self.max_health += hp_gain
        self.health += 5
        print("Level up! You are at level {}. Gained {} HP from leveling!".format(self.level, hp_gain))
        print("{} XP away from next level.".format(level_up - self.xp))


# broken thing below
# quest_dict = {"Clap the Dragon": quests.clap_the_dragon(player), "Mess with Turtles": quests.battle_turtles(player,5 )}
# TODO: optimize how quests are run, bc the current system is not sustainable for long term


def main():
    print_header()
    # player = start_choice()
    player = start()
    if not player:
        player = start_choice()
    info(player)
    sleep(2)
    active = True

    while active:
        option = menu()
        # Quest Option
        if option == "quest":
            if player.quest:  # check that a quest exists
                confirm = input("Start quest?: {} (y/n) \n>>>".format(player.quest))
                if confirm.find("y") != -1:
                    # TODO: make a good system for this, cuz 2 lines of extra elifs per quest cant be great
                    if player.quest == "Clap the Dragon":
                        quests.clap_the_dragon(player)
                    elif player.quest == "Dab on Turtles":
                        quests.battle_turtles(player, 3)
                    elif player.quest == "Beat up the Developer":
                        quests.beat_the_dev(player)
                    elif player.quest == "Mess with Goblins":
                        quests.mess_with_goblins(player)
                    elif player.quest == "Ryan's Battle":  # test battle - only accessable via debug mode
                        quests.ryans_battle(player)
                    elif player.quest == "Defeat Ryan":
                        quests.defeat_ryan(player)
                    else:
                        print("You don't have a quest!")
                else:
                    print("ok then be that way man all this work i do to launch quests and u be that way ok cool")
            else:
                print("You don't have a quest! Go find one before trying to start! There may be some in town...")

        # Inventory Option
        elif option == "inventory":
            inventory.use_item(player)

        # Shop Option
        elif option == "shop":
            shop.shop(player)

        # Player Info
        elif option == "player":
            info(player)

        # Debug mode
        elif option == "debug":
            player.debug()

        # World Option
        elif option == "world":
            selection = world.select_world()
            if selection == "Test World":
                world.test_world(player)
            elif selection == "Start Town":
                world.start_world(player)
            elif selection == "Topshelf":
                world.topshelf(player)

        # Save the game!
        elif option == "save":
            data.save(player)
            print("[!] Saved game!")

        # Exit Option
        elif option == "exit":
            # print("See ya later!")
            data.save(player)
            active = False
            # break


def print_header():
    print("--------------------------------------")
    print("|        The adventure of uh         |")
    print("|             UNKOWNLAND             |")
    print("|   another quality text based rpg   |")
    print("--------------------------------------")


# TODO: rewrite this with better options/dialogue
def start_choice():
    sleep(2)
    name = input("-Wuz yo name, nibba? \n>>>").strip()
    print("-Ah, so it is {}. Sounds pretty dumb but ok".format(name))
    sleep(2)
    print("-These gay ass turtles be dabbin on all the land. deadass get him b")
    answer = input("yes or no \n>>>").lower()
    if answer.find("ye") != -1:
        print("-finna clap these nibbas cheeks")

    else:
        print("-well thats gay but youre doing it anyways slave")

    sleep(2)
    weapon_choice = input("-anyways you need a weapon b. whatchu want a sword or a mf rpg \n>>>").lower().strip()
    if weapon_choice == "sword":
        print("-you have fun with that but ok")
        weapon = "Sword"
    elif weapon_choice == "mf rpg" or weapon_choice == "rpg":
        print("-hell yeah")
        weapon = "RPG"
    else:
        print("-that's not a weapon so you goin barehanded. try actually choosing something next game tho.")
        weapon = "Fists"

    quest = "Dab on Turtles"

    return Player(name, weapon, quest, 100, 10)  # the last 2 numbers are health, defence


def damage(player, dmg):
    player.health -= dmg
    print("{} took {} damage! HP: {}/{}".format(player.name, damage, player.health, player.max_health))


def menu():
    valid = True
    while valid:
        choice = input("\n----{MENU}----\n"
                       "What would you like to do?\n"
                       "[Q]uest [I]nventory [S]hop \n"
                       "[P]layer [W]orld E[X]it\n"
                       "[SAVE]\n"
                       ">>>").lower().strip()
        if choice.find("q") != -1:
            return "quest"
        elif choice == "exit" or choice == "x":
            sure = input("Confirm Quit? (y/n)").lower()
            if sure.find("y") != -1:
                print("Ok, see ya next time bruv.")
                return "exit"
        elif choice == "s" or choice == "shop" or choice == "store":
            return "shop"
        elif choice == "player" or choice == "p":
            return "player"
        elif choice == "world" or choice == "w":
            return "world"
        elif choice == "save":
            return "save"
        elif choice.find("i") != -1:
            return "inventory"
        elif choice == "debug mode":
            return "debug"


def start():
    active = True
    while active:
        print("\n----{START MENU}----\n"
              "[N]ew Game\n"
              "[L]oad Profile")
        ask = input(">>>").lower()
        if ask == "l" or ask == "load":
            saves = data.get_saves()
            for save in saves:
                print("[-] {}".format(save))
            print("Type your username:")
            ask_name = input(">>>").strip()
            filepath = data.get_full_path(ask_name)
            if os.path.exists(filepath):
                loaded = data.load(ask_name)
                if not loaded:  # if loading throws an error
                    return None
                return loaded
            else:
                print("'{}' is not a save file. Did you spell it correctly? Caps matter ya know.".format(ask_name))
        elif ask == "n" or ask == "new" or ask == "new game":
            print("Starting New Game!")
            return None
        else:
            print("'{}' not recognized. Try again.".format(ask))


def info(player):
    print("\n----{INFO}----")
    print("You are {}, wielder of the {}.".format(player.name, player.weapon))
    print("Your current task is to {}".format(player.quest))
    print("You have {}/{} HP and {}G".format(player.health, player.max_health, add_commas(player.money)))
    print("LEVEL {} ({} XP)".format(player.level, player.xp))


if __name__ == "__main__":
    main()
