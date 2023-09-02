import random
import time
import os

room_desc = {
    'Dark Room': 'You are in a dark room with loud tunes.',
    'Party Room': 'You are in a what looks like a party room.',
    'Boiler Room': 'You are in a small boiler room, you see some loose pipe.',
    'Dining Room': 'You find an angry looking man eating at a table. He looks angry.',
    'Closet Room': 'You find a room containing shelfs.',
    'Basement': 'You wander down into the basement, there are many storage boxes.',
    'Bathroom': 'You walk into a bathroom, it smells like someone died in here.',
    'Hallway': 'You find the front hallway, but see an angry, huge man.',
    'Escape!': 'You are outside.'}

rooms = {
    'Dark Room': {'south': 'Party Room'},
    'Party Room': {'south': 'Boiler Room', 'east': 'Dining Room', 'north': 'Dark Room'},
    'Boiler Room': {'north': 'Party Room'},
    'Dining Room': {'south': 'Closet Room', 'east': 'Bathroom', 'north': 'Hallway',
                    'west': 'Party Room'},
    'Closet Room': {'east': 'Basement', 'north': 'Dining Room'},
    'Basement': {'west': 'Closet Room'},
    'Bathroom': {'west': 'Dining Room'},
    'Hallway': {'west': 'Dining Room', 'east': 'Escape!'},
    'Escape!': 'free man!', }

items = {
    'Dark Room': 'medical supplies',
    'Boiler Room': 'pipe',
    'Closet Room': 'medical supplies',
    'Basement': 'steel file',
    'Bathroom': 'pain meds', }


enemy = {
        'Hallway': 'The Badman',
        'Dining Room': 'The guard', }


def possible_directions(room):
    print(f'Possible choices are: {" or ".join(rooms[room])}.\n')


class players():
    class hero():
        def __init__(self, name):
            self.name = name
            self.d_resistance = 0
            self.hp = 100
            self.max_hp = 150
            self.d_min = 15
            self.d_max = 30
            self.d_mult = 1
            self.current_room = 'Dark Room'
            self.items = []
            self.weapon = False

        def takedamage(self, damage, enemy):
            self.hp -= damage
            os.system('clear')
            print(enemy.name, 'attacks for:', damage, "dp.")


        def calcdam(self):
            dmg = random.randint(self.d_min, self.d_max) * self.d_mult
            return dmg

    class enemy():
        def __init__(self, name, hp, d_min, d_max, current_room):
            self.name = name
            self.hp = hp
            self.d_min = d_min
            self.d_max = d_max
            self.current_room = current_room

        def takedamage(self, damage, enemy):
            self.hp -= damage
            os.system('clear')
            print('You attack', self.name, 'for:', damage, 'dp.')

        def calcdam(self):
            dmg = random.randint(self.d_min, self.d_max)
            return dmg


villan = players.enemy('The badman', 200, 20, 40, 'Hallway')
guard = players.enemy('Dumb Henchman', 50, 0, 15, 'Dining Room')

os.system('clear')
print('Random man: Oh my god you\'re alive! Whats your name?')
playername = input('Enter name: ')
player1 = players.hero(playername)
os.system('clear')
print('Well...', player1.name + '...\nWe\'ve been captured by the a gang')
print('who plan to hold us for randsom...')
action = ''
while action != 'e':
    text = 'Press e to break zipties: '
    action = input("\x1B[3m" + text + "\x1B[0m")
os.system('clear')
print('Don\'t try to escape! They will torture you!')
time.sleep(2)


def status():
    os.system('clear')
    print('current room is:', player1.current_room + '.')
    print('current hp is', str(player1.hp) + '.')
    if player1.items is not None:
        print('current items are:', str(player1.items) + '.')
    elif player1.items is None:
        print('You currently have no items.')
    if player1.weapon is False:
        print('You have no weapon.')
    elif player1.weapon == 'sharpened pipe':
        print('You have a sharpeded pipe.')
    time.sleep(2)


def attack(attacker, attacking, enemy):
    if attacker == player1:
        attacking.takedamage(attacker.calcdam(), attacking)
        time.sleep(2)

    elif attacker == enemy:
        attacking.takedamage(attacking.calcdam(), attacker)
        time.sleep(2)


def use_item():
    os.system('clear')
    text = "\n".join("> [{}] {}".format(n, i) for n, i in enumerate(player1.items, start=1))
    if 'medical supplies' in player1.items or 'pain meds' in player1.items:
        use = input(f'Select an item to use: (1, 2 , 3 etc) \n{text}\n')
        use = int(use) - 1
        if player1.items[use] in player1.items:
            if player1.items[use] == 'medical supplies':
                player1.items.remove(player1.items[use])
                player1.hp += 50
                os.system('clear')
                print('You gain 50 health.')
                time.sleep(2)
            elif player1.items[use] == 'pain meds':
                player1.items.remove(player1.items[use])
                player1.d_resistance += 15
                os.system('clear')
                print('You use pain meds and gain 15 damage resistance.')
                time.sleep(2)
            elif player1.items[use] == 'pipe' or player1.items[use] == 'steel file':
                os.system('clear')
                print('This item can only be used to craft another item.')
                time.sleep(2)
    elif 'medical supplies' not in player1.items or 'pain meds' not in player1.items:
        print('You have no items to use.')
        time.sleep(2)

def fight(hero, enemy, first_move):
    os.system('clear')
    turn = first_move
    print('You are fighting', enemy.name)
    if first_move == hero:
        print('You get to attack first!')
        time.sleep(2)
    elif first_move == enemy:
        print(f'{enemy.name} gets to attack first!')
        time.sleep(2)
    while hero.hp > 0 and enemy.hp > 0:
        os.system('clear')
        if turn == hero:
            print('Your health:', str(hero.hp) + '.')
            print('Enemy health:', str(enemy.hp) + '.')
            print('You can either attack, or use items.')
            move = input('to attack press "a", to use an item press "u".')
            if move == 'a':
                attack(hero, enemy, enemy)
                turn = enemy
                move = ''
            elif move == 'u':
                use_item()
                move = ''
        elif turn == enemy:
            attack(enemy, hero, enemy)
            turn = hero
    if hero.hp < 0:
        os.system('clear')
        print('You died!')
        print('Hint: craft a sharper weapon than your fists.')
        time.sleep(2.3)
    elif enemy.hp < 0:
        print(f'You have defeated {enemy.name}!')
        time.sleep(2)
        os.system('clear')


def craft():
    if 'pipe' in player1.items and 'steel file' in player1.items:
        os.system('clear')
        print('You can craft a sharpened pipe.')
        action = input('Do you wish to craft a sharpened pipe? (y/n)')
        if action == 'y':
            player1.weapon = True
            player1.d_mult = 2
            player1.items.remove('pipe')
            os.system('clear')
            print('You have crafted a sharpened pipe.')
            time.sleep(2)
        elif action == 'n':
            os.system('clear')
            print('You might want to craft this item...')
            choice = input('Do you wish to craft item anyway? (y/n)')
            if choice == 'y':
                player1.weapon = True
                player1.d_mult = 2
                player1.items.pop('pipe')
                os.system('clear')
        else:
            os.system('clear')
            print('Incorrect input.')
            time.sleep(2)
            craft()
    else:
        os.system('clear')
        print('There are no items available to craft. Collect more supplies.')
        time.sleep(2)


def search_room(room):
    os.system('clear')
    if room in items:
        print('Possible items:', items[room])
        choice = input('Do you want to take this item? (y/n) ').lower()
        if choice == 'y':
            try:
                os.system('clear')
                print(f'You have taken the {items[room]}')
                player1.items.append(''.join(items[room]))
                player1.item = items.pop(room)
                time.sleep(1.5)
            except Exception:
                os.system('clear')
                print('There are no items in this room.')
                time.sleep(1.5)
    elif room not in items:
        os.system('clear')
        print('There are no items in this room.')
        time.sleep(1.5)


def show_items():
    os.system('clear')
    print(f'Current items are: {" and ".join(player1.items)}.')
    time.sleep(3)


def possible_actions():
    os.system('clear')
    print('You can either search the room for items or craft an item.')
    print("Type 's' to search, 'c' to craft, 'i' to see items, or", end=" ")
    action = input("'u' to use items. \n")
    if action == 's':
        search_room(player1.current_room)
    elif action == 'c':
        craft()
    elif action == 'i':
        if player1.items == []:
            os.system('clear')
            print('You currently have no items.')
            time.system(3)
        elif player1.items != []:
            show_items()
    elif action == 'u':
        use_item()


def possible_movement(room):
    os.system('clear')
    print(f'\nPossible choices are: {" or ".join(rooms[room])}')


def goto(room):
    os.system('clear')
    possible_movement(player1.current_room)
    move = input('Where do you want to move? ').lower()
    if move == 's':
        move = 'south'
    elif move == 'n':
        move = 'north'
    elif move == 'e':
        move = 'east'
    elif move == 'w':
        move = 'west'
    else:
        pass
    try:
        player1.current_room = rooms[room][move]
        os.system('clear')
        print('You have moved to the', move + '.')
        time.sleep(2)
    except Exception:
        os.system('clear')
        print('You walked into the wall.')
        time.sleep(2)


def instr():
    os.system('clear')
    print(f'{room_desc[player1.current_room]}')
    print('You need to find the exit, but watch out for you\'re captors!')
    print('Make sure to search the rooms and craft items!')
    time.sleep(5)


if __name__ == '__main__':
    instr()
    while player1.current_room != 'Escape!' and player1.hp > 0:
        os.system('clear')
        print(f'{room_desc[player1.current_room]}')
        if player1.current_room == 'Dining Room' and guard.hp > 0:
            choice1 = input('Do you wish to fight the guard? (y/n)')
            if choice1 == 'y':
                fight(player1, guard, player1)
            if choice1 == 'n':
                print('The guard notices you and attacks!')
                attack(player1, guard, guard)
        if player1.current_room == 'Hallway' and villan.hp > 0:
            choice2 = input('Do you wish to fight The Bad Man? (y/n)')
            if choice2 == 'y':
                fight(player1, villan, player1)
            elif choice2 == 'n':
                print('The Bad Man attacks!')
                attack(player1, villan, villan)
        poss = rooms[player1.current_room]
        print('Type "goto" if you wish to move to another room.')
        print('Type "action" if you want to do an action.')
        print('To see status, type status.')
        print("To read instructions again, press 'i'.")
        print("To use an item, press 'u'")
        choice = input('Make a decision. \n').lower()
        if choice == 'a' or choice == 'action':
            possible_actions()
        elif choice == 'g' or choice == 'goto':
            goto(player1.current_room)
        elif choice == 's' or choice == 'status':
            status()
        elif choice == 'i' or choice == 'instructions':
            instr()
        elif choice == 'u' or choice == 'use':
            use_item()
        else:
            print('Invalid choice.')
    if player1.hp > 0 and player1.current_room == 'Escape!':
        os.system('clear')
        print('You have escaped your inevitable demise!')
        print('Do you wish to save the other hostage?')
        choice = input("'y' for yes, 'n' for no: ")
        if choice == 'y':
            os.system('clear')
            print('You both escape into the sunset...')
            time.sleep(2)
        elif choice == 'n':
            os.system('clear')
            print("You're evil for that lol.")
            time.sleep(2)
        os.system('clear')
        print('Game over! Congrats!')
        time.sleep(3)
        os.system('clear')
    elif player1.hp <= 0:
        os.system('clear')
        print('You have DIED!')
        time.sleep(3)
        os.system('clear')
