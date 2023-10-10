# Kameron Coolong
import random  # using random to calculate random integers for attack damage.
import time  # using time to make the script sleep for a specified amount of seconds.

# using time and clear() to clear terminal, and make script sleep breifly to
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
    'Barracks': 'You see a raider eating at a table.',
    'Medical Room': 'You find a room containing shelfs.',
    'Storage Room': 'You wander down into the Storage Room, there are many storage boxes.',
    'Armory': 'You walk into a Armory, it smells like someone died in here.',
    'Cave Opening': 'You find the front Cave Opening, but see the raider leader.'}

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

# create item objects and assign them to indavidual rooms.
class Items():
    _registry: list[object] = []
    # set item attributes. Accounting for things like consumable vs non-consumable, location, hp, damage, resistance and name.
    def __init__(self, name, hpAdd, resistAdd, damAdd, useable, location, effects):
        self._registry.append(self) # appends to registry for searching for items in rooms. this makes the item objects iterable.
        self.name = name
        self.hpAdd = hpAdd
        self.resistAdd = resistAdd
        self.damAdd = damAdd
        self.useable = useable
        self.location = location
        self.effects = effects
    # this function handles adding items to the player inventory. if item grants passive effects, they will be applied.
    def addItem(self, player):
        if self.useable == False:
            player.items1.append(self.name)
            player.hp += int(self.hpAdd)
            player.resistance += int(self.resistAdd)
            player.min_damage += int(self.damAdd/2)
            player.max_damage += int(self.damAdd)
            self._registry.remove(self)
            if self.effects is not None:
                print(self.effects) # prints to screen the effect given to player.
            self.location = player.items1
        else:
            player.items2.append({self: self.name})
            self.location = player.items2
    def useItem(self, player):
        if self.useable == True:
            player.hp += int(self.hpAdd)
            player.resistance += int(self.resistAdd)
            player.min_damage += int(self.damAdd/2)
            player.max_damage += int(self.damAdd)
            print(f'You have used: {self.name}')
            print(f'{self.effects}')

# Creates classes for the player and enemy objects.
class Players():
    class Hero():
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
        # below are functions used to make gameplay functionality work as expected
        # defines function repsponsible for applying damage to player.
        def takedamage(self, damage, enemy):
            clear()
            self.hp -= int(damage - ((self.resistance / 100) * damage))
            print(enemy.name, 'attacks for:', damage, "dp.")
            time.sleep(1.75)
        # defines function to calculate how much damage the player deals.
        def calcdam(self):
            dmg = random.randint(self.min_damage, self.max_damage) * self.damage_mult
            return dmg
        def useItem(self):
                clear()
                # enumerates through player.items, shows enumerating number next to each item making it easier to select an item.
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
                    time.sleep(.5)
                    self.items2[:] = [i for i in self.items2 if str(keys[use-1]) not in str(i.keys())]
                elif 'healing potion' not in out or 'resistance potion' not in\
                        out:
                    print('You have no items to use.')
                    time.sleep(.5)
        # defines a function to show current room, hp, inventory.
        def status(self):
            print('Current room is:', self.current_room + '.')
            print('Current hp is', str(self.hp) + '.')
            if self.items1 != None or self.items2 != None:
                self.show_items()
            elif self.items1 is None and self.items2 is None:
                print('You currently have no items.')
        # defines the function to craft the weapon needed to beat the main villan. this weapon makes you far stronger than the villan.
        def craft(self):
            if 'iron' in self.items1 and 'steel file' in self.items1\
                    and 'cloth' in self.items1:
                clear()
                print('You can craft a sword.')
                action = input('Do you want to craft a sword? (y/n)\n')
                if action == 'y':
                    self.damage_mult = 2
                    self.items1.remove('iron')
                    self.items1.remove('cloth')
                    self.items1.remove('steel file')
                    sword = Items('sword', 0, 0, 20, False, self.items1, effects='+20 damage')
                    sword.addItem(self)
                    clear()
                    print('You have crafted a sword.')
                    time.sleep(.5)
                elif action == 'n':
                    pass
                else:
                    clear()
                    print('Incorrect input.')
                    time.sleep(.5)
                    craft()
            else:
                clear()
                print('There are no items available to craft. Collect more supplies.')
                time.sleep(.5)
        # function to search current room.
        def search_room(self):
            room_items = None
            for i in Items._registry:
                if i.location == self.current_room:
                    room_items = i
            if room_items == None:
                clear()
                print('There are no items in this room.')
                time.sleep(1.5)
                return
            while True:
                clear()
                print('Items in room:', room_items.name)
                choice = input('Do you want to take this item? (y/n)\n\nchoice: ').lower()
                if choice == 'y':
                    clear()
                    room_items.addItem(self)
                    print(f'You have taken the {room_items.name}.')
                    time.sleep(1.5)
                    break
                elif choice == 'n':
                    break
                else:
                    clear()
                    print('Invalid choice.')
                    time.sleep(1.5)
                    choice = None
                    continue
        # defines function to show current inventory.
        def show_items(self):
            inventory = self.items1
            item2keys = []
            for i in range(0, len(self.items2)):
                item2keys += list(self.items2[i].values())
            inventory = self.items1 + item2keys
            print('Current items are:', inventory)
        # defines function that shows the direction of conqurent rooms.
        def possible_movement(self):
            return (f'Possible directions are: {" or ".join(rooms[self.current_room])}')
        # allows player to see instructions whenever needed.
        def instr(self):
            clear()
            print(f'\n{room_desc[self.current_room]}')
            print('You need to find the exit, but watch out for you\'re captors!')
            print('Make sure to search the rooms and craft items!')
            time.sleep(5)
        # function to check if player in an enemy room and initiates fight sequence.
        def if_fight(self):
            enemy = None
            for i in Players.Enemy._eregistry:
                if i.current_room == self.current_room:
                    enemy = i
            while True:
                if not enemy == None:
                    print(f'{room_desc[self.current_room]}')
                    choice1 = input(f'Do you wish to fight the {enemy.name}? (y/n)\n')
                    if choice1 == 'y':
                        loser = fight(self, enemy, self)
                    elif choice1 == 'n':
                        print(f'the {enemy.name} notices you and attacks!')
                        loser = fight(self, enemy, enemy)
                    else:
                        clear()
                        print('Invalid choice.')
                        time.sleep(1.5)
                        clear()
                        continue
                    if loser == self:
                        return 'lose'
                    elif loser == villan:
                        return 'win'
                return None
        # defines function for navigating through conqurent rooms.
        def goto(self, move):
            clear()
            dirs = {'s': 'south', 'e': 'east', 'w': 'west', 'n': 'north'}
            while True:
                try:
                    move = dirs[move]
                    break
                except Exception:
                    print('Invalid input.')
                    time.sleep(1.5)
                    clear()
                    return None
            # this if statement makes sure that the movement direction is possible before erasing current position in map.
            if move not in rooms[self.current_room]:
                print('You have walked into a wall.')
                time.sleep(2)
                return
            # using map codes to update map and changing current room
            self.map = self.map[:map_code[self.current_room]] + ' ' + self.map[map_code[self.current_room]+1:]
            self.current_room = rooms[self.current_room][move]  # changes current room.
            self.map = self.map[:map_code[self.current_room]] + '*' + self.map[map_code[self.current_room]+1:]
            clear()
            print('You have moved to the', move + '.')
            time.sleep(2)

    # defines enemy character stats.
    class Enemy():
        _eregistry: list[object] = []
        def __init__(self, name, hp, min_damage, max_damage, current_room):
            self._eregistry.append(self)
            self.name = name
            self.hp = hp
            self.min_damage = min_damage
            self.max_damage = max_damage
            self.current_room = current_room
        # defines function for enemy damage delt.
        def takedamage(self, damage):
            clear()
            self.hp -= damage
            print('You attack', self.name, 'for:', damage, 'dp.')
            time.sleep(1.75)
        # defines function to calculate damage of enemy attacks.
        def calcdam(self):
            dmg = random.randint(self.min_damage, self.max_damage)
            if self.name == 'Raider Leader':
                if random.randint(1,100) == random.randint(1,100):
                    print('Critical hit!')
                    dmg += random.randint(30,50)
            return dmg

# creates items and sets atributes and room location.
item1 = Items('healing potion', 75, 0, 0, True, 'Medical Room', '+75 HP.')
item2 = Items('magic necklace', 0, 15, 0, False, 'Barracks', f'+15% resistance.')
item3 = Items('cloth', 0, 0, 0, False, 'Cave Hallway', None)
item4 = Items('iron', 0, 0, 0, False, 'Torture Room', None)
item5 = Items('resistance potion', 0, 15, 0, True, 'Armory', '+15 Resistance.')
item6 = Items('steel file', 0, 0, 0, False, 'Storage Room', None)

clear()
print('\nRandom man: Finally you\'re awake! Whats your name?') # start of intro. must initialize player and enemy objects globally for this to work.
playername = input('Enter username: ') # allowing user to input a username.
player = Players.Hero(playername) # initialize player object.
villan = Players.Enemy('Raider Leader', 250, 35, 65, 'Cave Opening') # creates enemy objects and sets hp and minimum/maximum attack damage.
guard = Players.Enemy('Raider Henchman', 50, 5, 20, 'Barracks')

# defines function for player and enemy to fight until either wins.
def fight(hero, enemy, first_move):
    clear()
    turn = first_move
    print(f'{hero.name} VS {enemy.name}')
    print(f'{first_move.name} attacks first!')
    time.sleep(3)
    while hero.hp > 0 and enemy.hp > 0:
        clear()
        if turn == hero:
            print(f'{hero.name} health:', str(hero.hp) + '.')
            print(f'{enemy.name} health:', str(enemy.hp) + '.')
            print(f'You can either use \'a\' attack, or \'u\' use items.')
            move = input('choice: ')
            if move == 'a':
                enemy.takedamage(hero.calcdam())
                turn = enemy
                move = ''
            elif move == 'u':
                use_item()
                move = ''
        elif turn == enemy:
            hero.takedamage(enemy.calcdam(), enemy)
            turn = hero
    if hero.hp < 0:
        clear()
        print('You died!')
        print('Hint: craft a sharper weapon than your fists.')
        time.sleep(2.3)
        return player
    elif enemy.hp < 0:
        clear()
        enemy.current_room = 'dead'
        print(f'You have defeated {enemy.name}!')
        time.sleep(2)
        clear()
        if enemy == villan:
            return villan

def introdec(function): # decorator for main function. packs intro before main and ending sequence after main.
    def ending_sequence(result): # sequence that happens when you win or lose.
        if result == 'win':
            clear()
            print('You have escaped!')
            print('Winner!')
        elif result == 'lose':
            clear()
            print('Collect items and craft a weapon to become stronger.')
            print('Game Over!')
    def wrapper():
        # small introduction into the game, allows you to give yourself a name,
        clear()
        print('\nWell...', player.name + '...\nWe\'ve been captured by the a group')
        print('of raiders who plan to hold us for randsom...')
        action = ''
        while action == '':  # using while loop to make sure program won't crash.
            text = 'enter anything to break chains on rocks: '
            action = input("\x1B[3m" + text + "\x1B[0m")
        clear()
        print('\nDon\'t try to escape! They will torture you!')
        time.sleep(2)
        player.instr()
        result = function() # saving result for ending sequence, if win or lose sequences.
        ending_sequence(result)
    return wrapper 

@introdec
def main():
    clear()
    choices = {'g': player.goto, 's': player.search_room, 'c': player.craft, 'u': player.useItem, 'i': player.show_items, 'h':  player.instr}
    while player.hp > 0 and villan.current_room == 'Cave Opening':
        result = player.if_fight()
        if result != None:  # check for game ending scenareo.
            return result
        clear()
        print(player.map)
        player.status()
        print(f'\n{player.possible_movement()}.\n')
        print('Command prefixes: ')
        print("'goto (n, s, e or w)' to navigate rooms,\n'search' to search room,")
        print("'craft' to craft,\n'use' to use items,")
        print("'items' to show items,")
        print("'help' for help.\n")
        choice = []
        if choice == []:
            choice = [i for i in input('Enter move: ').lower() if i != ' ']
            try:
                if choice[0][0] == 'g':
                    choices[choice[0][0]](choice[1][0])
                else:
                    clear()
                    choices[choice[0][0]]()
                    time.sleep(2)
            except Exception:
                clear()
                print('Invalid choice.')
                time.sleep(1)
                
if __name__ == '__main__':        
    main()