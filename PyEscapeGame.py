import random
import time


def clear():
    print("\x1B[2J")
# using random to calculate random integers for attack damage.
# using time and clear() to clear terminal and make script sleep breifly to
# make the script easier to follow, allowing the screen to show only
# updated game data.
# \ used to continue lines where strings are too long.
map = '''
start         exit
-----         -----
| * |         |   |
-----         -----
  |             |
-----  -----  -----
|   |--|   |  |   |
-----  -----  -----
  |      |      |
-----  -----  -----
|   |  |   |--|   |
-----  -----  -----
'''
# map codes are the indexes of where '*' appear on map, indicating the room you're in relative to the other rooms.
map_code = {
    'Dark Room': 42,
    'Hallway': 56,
    'Party Room': 120,
    'Dining Room': 127,
    'Bathroom': 134,
    'Boiler Room': 198,
    'Closet Room': 205,
    'Living Room': 212
    }


# define room descriptions.
room_desc = {
    'Dark Room': 'You are in a dark room with loud tunes.',
    'Party Room': 'You are in a what looks like a party room.',
    'Boiler Room': 'You are in a small boiler room, you see some loose pipe.',
    'Dining Room': 'You find an angry looking man eating at a table. He looks angry.',

    'Closet Room': 'You find a room containing shelfs.',
    'Living Room': 'You wander down into the Living Room, there are many storage boxes.',

    'Bathroom': 'You walk into a bathroom, it smells like someone died in here.',

    'Hallway': 'You find the front hallway, but see an angry, huge man.',
    'Escape!': 'You are outside.'}

# define room layout.
rooms = {
    'Dark Room': {'south': 'Party Room'},
    'Party Room': {'south': 'Boiler Room', 'east': 'Dining Room', 'north': 'Dark Room'},
    'Boiler Room': {'north': 'Party Room'},
    'Dining Room': {'south': 'Closet Room', 'west': 'Party Room'},
    'Closet Room': {'east': 'Living Room', 'north': 'Dining Room'},
    'Living Room': {'west': 'Closet Room', 'north': 'Bathroom'},
    'Bathroom': {'north': 'Hallway', 'south': 'Living room'},
    'Hallway': {'south': 'Dining Room', 'north': 'Escape!'},
    'Escape!': 'free man!', }

# define items and coresponding rooms.
items = {
    'Dark Room': 'healing potion',
    'Dining Room': 'magic stone',
    'Party Room': 'cloth',
    'Boiler Room': 'pipe',
    'Closet Room': 'healing potion',
    'Living Room': 'steel file',
    'Bathroom': 'resistance potion', }


# Creates classes for the player and enemy.
class players():
    class hero():
        # defines player stats.
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
            self.weapon = None
            self.map = map

        # defines function repsponsible for applying damage to player.
        def takedamage(self, damage, enemy):
            self.hp -= damage - self.d_resistance
            clear()
            print(enemy.name, 'attacks for:', damage, "dp.")

        # defines function to calculate how much damage is delt.
        def calcdam(self):
            dmg = random.randint(self.d_min, self.d_max) * self.d_mult
            return dmg


    # defines enemy character stats.
    class enemy():
        def __init__(self, name, hp, d_min, d_max, current_room):
            self.name = name
            self.hp = hp
            self.d_min = d_min
            self.d_max = d_max
            self.current_room = current_room

        # defines function for enemy damage delt.
        def takedamage(self, damage, enemy):
            self.hp -= damage
            clear()
            print('You attack', self.name, 'for:', damage, 'dp.')

        # defines function to calculate damage of enemy attacks.
        def calcdam(self):
            dmg = random.randint(self.d_min, self.d_max)
            return dmg


# creates enemy objects and sets hp and minimum/maximum attack damage.
villan = players.enemy('The badman', 250, 20, 40, 'Hallway')
guard = players.enemy('Dumb Henchman', 50, 0, 15, 'Dining Room')

# small introduction into the game, allows you to give yourself a name,
clear()
print('\nRandom man: Finally you\'re awake! Whats your name?')
playername = input('Enter username: ') # allowing user to input a username. You could use this to make a leaderboard.
player = players.hero(playername) # initialize player object.
clear()
print('\nWell...', player.name + '...\nWe\'ve been captured by the a group')
print('of raiders who plan to hold us for randsom...')
action = ''
while action != 'e':  # using while loop to make sure program won't crash.
    text = 'Press e to break zipties: '
    action = input("\x1B[3m" + text + "\x1B[0m")
clear()
print('\nDon\'t try to escape! They will torture you!')
time.sleep(2)

# defines a function to show current room, hp, inventory, and weapon.
def status():
    print('Current room is:', player.current_room + '.')
    print('Current hp is', str(player.hp) + '.')
    if player.items is not None:
        print('Current items are:', str(player.items) + '.')
    elif player.items is None:
        print('You currently have no items.')
    if player.weapon is False:
        print('You have no weapon.')
    elif player.weapon == 'sharpened pipe':
        print('You have a sharpeded pipe.')


# defines a function to handle attack sequences.
def attack(attacker, attacking, enemy):
    if attacker == player:
        attacking.takedamage(attacker.calcdam(), attacking)
        time.sleep(2)
    elif attacker == enemy:
        attacking.takedamage(attacker.calcdam(), attacker)
        time.sleep(2)


# defines a function that allows the player to use an item.
def use_item():
    clear()
    # enumerates through player.items, shows enumerating number next to each item making it easier to select an item.
    text = "\n".join("> [{}] {}".format(n, i) for n, i in enumerate(player.items, start=1))
    
    
    if 'healing potion' in player.items or 'resistance potion' in player.items or 'magic stone' in player.items:
        print('Select an item to use: (1, 2 , 3 etc).')
        use = input(f'Type \'exit\' to exit menu \n{text}\n')
        if use == 'e' or use == 'exit':
            return
        elif player.items[int(use) - 1] in player.items:
            if player.items[int(use) - 1] == 'healing potion':
                player.items.remove(player.items[int(use) - 1])
                player.hp += 50
                clear()
                print('You gain 50 health.')
                time.sleep(2)
            elif player.items[int(use) - 1] == 'resistance potion':
                player.items.remove(player.items[int(use) - 1])
                player.d_resistance += 15
                clear()
                print('-1 Resistance Potion')
                print('+15 damage resistance.')
                time.sleep(2)
            elif player.items[int(use) - 1] == 'pipe'\
                    or player.items[int(use) - 1] == 'steel file':

                clear()
                print('This item can only be used to craft another item.')
                time.sleep(2)

            else:
                clear()
                print('Invalid entree')
                time.sleep(1.5)
                use_item()

    elif 'healing potion' not in player.items or 'resistance potion' not in\
            player.items:

        print('You have no items to use.')
        time.sleep(2)


# defines function for player and enemy to fight until either wins.
def fight(hero, enemy, first_move):
    clear()
    turn = first_move
    print('You are fighting', enemy.name)
    if first_move == hero:
        print('You get to attack first!')
        time.sleep(2)
    elif first_move == enemy:
        print(f'{enemy.name} gets to attack first!')
        time.sleep(2)
    while hero.hp > 0 and enemy.hp > 0:
        clear()
        if turn == hero:
            print('Your health:', str(hero.hp) + '.')
            print('Enemy health:', str(enemy.hp) + '.')
            print('You can either attack, or use items.')
            move = input('to attack press "a", to use an item press "u".\n')
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
        clear()
        print('You died!')
        print('Hint: craft a sharper weapon than your fists.')
        time.sleep(2.3)
    elif enemy.hp < 0:
        clear()
        enemy.current_room = 'dead'
        print(f'You have defeated {enemy.name}!')
        time.sleep(2)
        clear()


# defines the function to craft the weapon needed to beat the main villan.
def craft():
    if 'pipe' in player.items and 'steel file' in player.items\
            and 'cloth' in player.items:
        clear()
        print('You can craft a sharpened pipe.')
        action = input('Do you wish to craft a sharpened pipe? (y/n)\n')
        if action == 'y':
            player.d_mult = 2
            player.items.remove('pipe')
            player.items.remove('cloth')
            
            clear()
            print('You have crafted a sharpened pipe.')
            time.sleep(2)
        elif action == 'n':
            clear()
            print('You might want to craft this item...')
            choice = input('Do you wish to craft item anyway? (y/n)\n')
            if choice == 'y':
                player.d_mult = 2
                player.items.pop('pipe')
                clear()
        else:
            clear()
            print('Incorrect input.')
            time.sleep(2)
            craft()
    else:
        clear()
        print('There are no items available to craft. Collect more supplies.')
        time.sleep(2)


# defines function for searching the rooms, and obtaining items.
def search_room(room):
    clear()
    if room in items:
        print('Possible items:', items[room])
        choice = input('Do you want to take this item? (y/n) ').lower()
        if choice == 'y':
            try:
                clear()
                if items[room] == 'magic stone':
                    print(f'+ 10% resistance.')
                    player.d_resistance += 10
                print(f'You have taken the {items[room]}')
                player.items.append(''.join(items[room]))
                player.item = items.pop(room)
                time.sleep(1.5)
            except Exception:
                clear()
                print('There are no items in this room.')
                time.sleep(1.5)
    elif room not in items:
        clear()
        print('There are no items in this room.')
        time.sleep(1.5)


# defines function to show current items in inventory.
def show_items():
    clear()
    print(f'Current items are: {" and ".join(player.items)}.')
    time.sleep(3)


# defines function to show possible actions
def possible_actions():
    while True:
        clear()
        print('You can either search the room for items or craft an item.')
        print("Type 's' to search, 'c' to craft, 'i' to see items,", end=" ")
        action = input("'u' to use items.\n'Q' to quit.\n").lower()
        if action == 's' or action == 'search':
            search_room(player.current_room)
        elif action == 'c' or action == 'craft':
            craft()
        elif action == 'i' or action == 'items':
            if player.items == []:
                clear()
                print('You currently have no items.')
                time.system(1.5)
            elif player.items != []:
                show_items()
        elif action == 'u' or action == 'use':
            use_item()
        elif action == 'q' or action == 'quit':
            return None
        else:
            clear()
            print('Invalid input.')
            time.sleep(1.5)
            continue


# defines function that shows the direction of conqurent rooms.
def possible_movement(room):
    return (f'Possible directions are: {" or ".join(rooms[room])}')


# defines function for navigating through conqurent rooms.
def goto(room, dir):
    clear()
    while True:
        move = dir
        if move == 's':
            move = 'south'
            break
        elif move == 'n':
            move = 'north'
            break
        elif move == 'e':
            move = 'east'
            break
        elif move == 'w':
            move = 'west'
            break
        else:
            clear()
            print('Invalid choice.')
            time.sleep(1.5)
            clear()
            return None
    # this if statement makes sure that the movement direction is possible before erasing current position in map.
    if move not in rooms[room]:
        print('You have walked into a wall.')
        time.sleep(2)
        return
    try:
        player.map = player.map[:map_code[player.current_room]] + ' ' + player.map[map_code[player.current_room]+1:]
        player.current_room = rooms[room][move]  # changes current room.
        player.map = player.map[:map_code[player.current_room]] + '*' + player.map[map_code[player.current_room]+1:]
        clear()
        print('You have moved to the', move + '.')
        time.sleep(2)
    except Exception:
        clear()
        print('You walked into the wall.')
        print(Exception)
        time.sleep(2)

'''
come back to this --VV

def changeRoom(room, move):
    player.map = player.map[:map_code[player.current_room]] + ' ' + player.map[map_code[player.current_room]+1:]
    player.current_room = rooms[room][move]  # changes current room.
    player.map = player.map[:map_code[player.current_room]] + '*' + player.map[map_code[player.current_room]+1:]
^^^
'''    
# allows player to see instructions whenever needed.
def instr():
    clear()
    print(f'\n{room_desc[player.current_room]}')
    print('You need to find the exit, but watch out for you\'re captors!')
    print('Make sure to search the rooms and craft items!')
    time.sleep(5)


# function to check if player in an enemy room and initiates fight sequence.
def if_fight():
    while True:
        if player.current_room == guard.current_room:
            print(f'{room_desc[player.current_room]}')
            choice1 = input('Do you wish to fight the theif? (y/n)\n')
            if choice1 == 'y':
                fight(player, guard, player)
            elif choice1 == 'n':
                print('the thief notices you and attacks!')
                fight(player, guard, guard)
            else:
                clear()
                print('Invalid choice.')
                time.sleep(1.5)
                clear()
                continue

        elif player.current_room == villan.current_room:
            print(f'{room_desc[player.current_room]}')
            choice2 = input('Do you wish to fight The theif leader? (y/n)\n')
            if choice2 == 'y':
                fight(player, villan, player)
            elif choice2 == 'n':
                print('The theif leader attacks!')
                fight(player, villan, villan)
            else:
                clear()
                print('Invalid choice.')
                time.sleep('1.5')
                clear()
                continue
        else:
            return None


def main():
    clear()
    while player.hp > 0 and villan.hp > 0:
        clear()
        if_fight()
        print(player.map)
        status()
        print(f'\n{possible_movement(player.current_room)}.\n')
        print('Command prefixes: ')
        print("'goto (n, s, e or w)' to navigate rooms,\n'search' \
to search room,")

        print("'craft' to craft,\n'use' to use items,")
        print("'items' to show items,")
        print("'help' for help.\n")
        choice = input('Enter move: ').lower()
        choice = choice.split(' ')
        try:
            if choice[0][0] == 'g':
                goto(player.current_room, choice[1][0])
            elif choice[0][0] == 's':
                search_room(player.current_room)
            elif choice[0][0] == 'c':
                craft()
            elif choice[0][0] == 'u':
                use_item()
            elif choice[0][0] == 'i':
                show_items()
            elif choice[0][0] == 'h':
                instr()
        except Exception:
            clear()
            print('Invalid command.')
            time.sleep(1.5)


def winning_sequence():
    if player.hp > 0 and villan.hp <= 0:
        clear()
        print('You have escaped your inevitable demise!')
        print('Do you wish to save the other hostage?')
        choice = input("'y' for yes, 'n' for no: ")
        if choice == 'y':
            clear()
            print('You both escape into the sunset...')
            time.sleep(2)
        elif choice == 'n':
            clear()
            print("You're evil for that lol.")
            time.sleep(2)
        clear()
        print('Game over! Congrats!')
        time.sleep(3)
        clear()
    elif player.hp <= 0:
        clear()
        print('You have DIED!')
        time.sleep(3)
        clear()


# function containing main loop.
if __name__ == '__main__':
    instr()
    while villan.hp > 0 and player.hp > 0:
        clear()
        main()
    winning_sequence()
