# Kameron Coolong.

import random  # using random to calculate random integers for attack damage.
import time  # using time to make the script sleep for a specified amount of seconds.

# using time and clear() to clear terminal and make script sleep breifly to
# allow the script to be easier to follow. this makes the screen show only updated game data.
def clear():
    print("\x1B[2J")

# uses this map to visuale current player room for user.
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

# uses "map_code" to slice at specified indexes of string map for each room.
# "*" = current room on the map. 
map_code = {
    'Cell': 42,
    'Cave Opening': 56,
    'Cave Hallway': 120,
    'Barracks': 127,
    'Armory': 134,
    'Torture Room': 198,
    'Medical Room': 205,
    'Storage Room': 212}

# define room descriptions.
room_desc = {
    'Cell': 'You are in a dark cell.',
    'Cave Hallway': 'You are in a what looks like a Cave Hallway.',
    'Torture Room': 'You are in a small torture room, you see some loose scrap metal.',
    'Barracks': 'You find an angry looking man eating at a table.',
    'Medical Room': 'You find a room containing shelfs.',
    'Storage Room': 'You wander down into the Storage Room, there are many storage boxes.',
    'Armory': 'You walk into a Armory, it smells like someone died in here.',
    'Cave Opening': 'You find the front Cave Opening, but see an angry, huge man.'}

# defines room layout.
rooms = {
    'Cell': {'south': 'Cave Hallway'},
    'Cave Hallway': {'south': 'Torture Room', 'east': 'Barracks', 'north': 'Cell'},
    'Torture Room': {'north': 'Cave Hallway'},
    'Barracks': {'south': 'Medical Room', 'west': 'Cave Hallway'},
    'Medical Room': {'east': 'Storage Room', 'north': 'Barracks'},
    'Storage Room': {'west': 'Medical Room', 'north': 'Armory'},
    'Armory': {'north': 'Cave Opening', 'south': 'Storage Room'},
    'Cave Opening': {'south': 'Armory'}}

# Creates classes for the player and enemy objects.
class players():
    class hero():
        # defines player stats. as player moves around, takes damage, and uses items,
        # these stats will change and the data will be persistent until program is over, or objects are destroyed.
        def __init__(self, name):
            self.name = name
            self.resistance = 0
            self.hp = 100
            self.max_hp = 150
            self.min_damage = 15
            self.max_damage = 30
            self.damage_mult = 1
            self.current_room = 'Cell' # starts player in the start room.
            self.items1 = [] # using 2 items lists for usable and non usable items. will still show in inventory the same.
            self.items2 = []
            self.map = map

        # defines function repsponsible for applying damage to player.
        def takedamage(self, damage, enemy):
            self.hp -= int(damage - ((self.resistance / 100) * damage))
            print(enemy.name, 'attacks for:', damage, "dp.")

        # defines function to calculate how much damage the player deals.
        def calcdam(self):
            dmg = random.randint(self.min_damage, self.max_damage) * self.damage_mult
            return dmg
        
        def useItem(self):
                clear()
                # enumerates through player.items, shows enumerating number next to each item making it easier to select an item.
                print(self.items2)
                out = []
                keys = []
                for i in self.items2:
                    out += list(self.items2[self.items2.index(i)].values())
                    keys += list(self.items2[self.items2.index(i)].keys())
                text = "\n".join("> [{}] {}".format(n, i) for n, i in enumerate(out, start=1))
                if 'healing potion' in out or 'resistance potion' in out:
                    print('Select an item to use: (1, 2 , 3 etc).')
                    use = int(input(f'Type \'exit\' to exit menu \n{text}\n'))
                    out = keys[use-1]
                    clear()
                    out.useItem(self)
                    time.sleep(2)
                    self.items2[:] = [i for i in self.items2 if str(keys[use-1]) not in str(i.keys())]
                elif 'healing potion' not in out or 'resistance potion' not in\
                        out:
                    print('You have no items to use.')
                    time.sleep(2)

    # defines enemy character stats.
    class enemy():
        def __init__(self, name, hp, min_damage, max_damage, current_room):
            self.name = name
            self.hp = hp
            self.min_damage = min_damage
            self.max_damage = max_damage
            self.current_room = current_room

        # defines function for enemy damage delt.
        def takedamage(self, damage):
            self.hp -= damage
            print('You attack', self.name, 'for:', damage, 'dp.')

        # defines function to calculate damage of enemy attacks.
        def calcdam(self):
            dmg = random.randint(self.min_damage, self.max_damage)
            if self.name == 'Raider Leader':
                if random.randint(1,100) == random.randint(1,100):
                    print('Critical hit!')
                    dmg += random.randint(30,50)
            return dmg

# creates enemy objects and sets hp and minimum/maximum attack damage.
villan = players.enemy('Raider Leader', 250, 20, 40, 'Cave Opening')
guard = players.enemy('Raider Henchman', 50, 0, 15, 'Barracks')

# small introduction into the game, allows you to give yourself a name,
clear()
print('\nRandom man: Finally you\'re awake! Whats your name?')
playername = input('Enter username: ') # allowing user to input a username.
player = players.hero(playername) # initialize player object.

clear()
print('\nWell...', player.name + '...\nWe\'ve been captured by the a group')
print('of raiders who plan to hold us for randsom...')
action = ''
while action != 'e':  # using while loop to make sure program won't crash.
    text = 'Press e to break chains on rocks: '
    action = input("\x1B[3m" + text + "\x1B[0m")

clear()
print('\nDon\'t try to escape! They will torture you!')
time.sleep(2)

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

def status():
    print('Current room is:', player.current_room + '.')
    print('Current hp is', str(player.hp) + '.')

# defines function that shows the direction of conqurent rooms.
def possible_movement(room):
    return (f'Possible directions are: {" or ".join(rooms[room])}')

def main():
    clear()
    while player.hp > 0 and villan.current_room == 'Cave Opening':
        # commented out, but this is what would eventrually trigger game ending sequence. The fight sequence and item handling are code intensive.
        # result = if_fight()
        # if result != None:  # check for game ending scenareo.
        #     return result
        clear()
        print('--MOVEMENT DEMO--')
        print(player.map)
        status()
        print(f'\n{possible_movement(player.current_room)}.\n')
        print('Command prefixes: ')
        print("'goto (n, s, e or w)' to navigate rooms,\n'search' to search room,")
        print("'craft' to craft,\n'use' to use items,")
        print("'items' to show items,")
        print("'help' for help.\n")
        choice = input('Enter move: ').lower()
        choice = choice.split(' ')
        try:
            # uses nested list to read user commands, user can use goto, go or g etc, for each ccommand prefix. any additional arugments will be passes based on the command prefix.
            if choice[0][0] == 'g':
                goto(player.current_room, choice[1][0]) # calls function that handles movement between rooms.
            elif choice[0][0] == 's':
                search_room(player.current_room) # calls function that searches the room that the player is currently in.
            elif choice[0][0] == 'c':
                craft() # calls a function that checks if player can craft an item
            elif choice[0][0] == 'u':
                player.useItem() # calls a function that handles using consumable items
            elif choice[0][0] == 'i':
                show_items() # calls a function that handles 
            elif choice[0][0] == 'h':
                instr()
        except Exception: # catches an error if the user inputs an invalid command prefix.
            clear()
            print('Invalid command.')
            time.sleep(1.5)

# sequence that happens when you win or lose.
def ending_sequence(result):
    if result == 'win':
        clear()
        print('You have escaped!')
        print('Winner!')
        time.sleep(3)
        clear()
    elif result == 'lose':
        clear()
        print('Collect items and craft a weapon to become stronger.')
        print('Game Over!')
        time.sleep(3)
        clear()

# function containing main loop.
if __name__ == '__main__':
    while villan.hp > 0 and player.hp > 0:
        clear()
        result = main()
    ending_sequence(result)