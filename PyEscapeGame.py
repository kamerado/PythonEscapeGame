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
    'Hallway': 56,
    'Study': 120,
    'Dining Room': 127,
    'Armory': 134,
    'Torture Room': 198,
    'Storage Room': 205,
    'Living Quarters': 212}

# define room descriptions.
room_desc = {
    'Cell': 'You are in a dark cell.',
    'Study': 'You are in a what looks like a Study.',
    'Torture Room': 'You are in a small torture room, you see some loose scrap metal.',
    'Dining Room': 'You find an angry looking man eating at a table.',
    'Storage Room': 'You find a room containing shelfs.',
    'Living Quarters': 'You wander down into the Living Quarters, there are many storage boxes.',
    'Armory': 'You walk into a Armory, it smells like someone died in here.',
    'Hallway': 'You find the front hallway, but see an angry, huge man.'}

# defines room layout.
rooms = {
    'Cell': {'south': 'Study'},
    'Study': {'south': 'Torture Room', 'east': 'Dining Room', 'north': 'Cell'},
    'Torture Room': {'north': 'Study'},
    'Dining Room': {'south': 'Storage Room', 'west': 'Study'},
    'Storage Room': {'east': 'Living Quarters', 'north': 'Dining Room'},
    'Living Quarters': {'west': 'Storage Room', 'north': 'Armory'},
    'Armory': {'north': 'Hallway', 'south': 'Living Quarters'},
    'Hallway': {'south': 'Dining Room'}}

# define items and coresponding rooms.
items = {
    'Dining Room': 'magic necklace',
    'Study': 'cloth',
    'Torture Room': 'iron',
    'Storage Room': 'healing potion',
    'Living Quarters': 'steel file',
    'Armory': 'resistance potion'}

# Creates classes for the player and enemy objects.
class players():
    class hero():
        # defines player stats.
        def __init__(self, name):
            self.name = name
            self.resistance = 0
            self.hp = 100
            self.max_hp = 150
            self.min_damage = 15
            self.max_damage = 30
            self.damage_mult = 1
            self.current_room = 'Cell'
            self.items = []
            self.map = map

        # defines function repsponsible for applying damage to player.
        def takedamage(self, damage, enemy):
            self.hp -= int(damage - ((self.resistance / 100) * damage))
            print(enemy.name, 'attacks for:', damage, "dp.")

        # defines function to calculate how much damage the player deals.
        def calcdam(self):
            dmg = random.randint(self.min_damage, self.max_damage) * self.damage_mult
            return dmg

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
            if self.name == 'The badman':
                if random.randint(1,100) == random.randint(1,100):
                    print('Critical hit!')
                    dmg += random.randint(20,50)
            return dmg

# creates enemy objects and sets hp and minimum/maximum attack damage.
villan = players.enemy('The badman', 250, 20, 40, 'Hallway')
guard = players.enemy('Dumb Henchman', 50, 0, 15, 'Dining Room')

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

# defines a function to show current room, hp, inventory.
def status():
    print('Current room is:', player.current_room + '.')
    print('Current hp is', str(player.hp) + '.')
    if player.items is not None:
        print('Current items are:', str(player.items) + '.')
    elif player.items is None:
        print('You currently have no items.')

# defines a function to handle attack sequences.
def attack(attacker, attacking, enemy):
    if attacker == player:
        clear()
        attacking.takedamage(attacker.calcdam())
        time.sleep(2)
    elif attacker == enemy:
        clear()
        attacking.takedamage(attacker.calcdam(), enemy)
        time.sleep(2)

# defines a function that allows the player to use an item.
def use_item():
    clear()
    # enumerates through player.items, shows enumerating number next to each item making it easier to select an item.
    text = "\n".join("> [{}] {}".format(n, i) for n, i in enumerate(player.items, start=1))
    if 'healing potion' in player.items or 'resistance potion' in player.items or 'magic necklace' in player.items:
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
                player.resistance += 15
                clear()
                print('-1 Resistance Potion')
                print('+15 damage resistance.')
                time.sleep(2)
            elif player.items[int(use) - 1] == 'iron'\
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
        return player
    elif enemy.hp < 0:
        clear()
        enemy.current_room = 'dead'
        print(f'You have defeated {enemy.name}!')
        time.sleep(2)
        clear()
        if enemy == villan:
            return villan
        

# defines the function to craft the weapon needed to beat the main villan.
def craft():
    if 'iron' in player.items and 'steel file' in player.items\
            and 'cloth' in player.items:
        clear()
        print('You can craft a sharpened iron.')
        action = input('Do you wish to craft a sharpened iron? (y/n)\n')
        if action == 'y':
            player.damage_mult = 2
            player.items.remove('iron')
            player.items.remove('cloth')
            
            clear()
            print('You have crafted a sharpened iron.')
            time.sleep(2)
        elif action == 'n':
            clear()
            print('You might want to craft this item...')
            choice = input('Do you wish to craft item anyway? (y/n)\n')
            if choice == 'y':
                player.damage_mult = 2
                player.items.pop('iron')
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
                if items[room] == 'magic necklace':
                    print(f'+ 15% resistance.')
                    player.resistance += 15
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
            return None

        elif player.current_room == villan.current_room:
            print(f'{room_desc[player.current_room]}')
            choice2 = input('Do you wish to fight The theif leader? (y/n)\n')
            if choice2 == 'y':
                loser = fight(player, villan, player)
            elif choice2 == 'n':
                print('The theif leader attacks!')
                loser = fight(player, villan, villan)
            else:
                clear()
                print('Invalid choice.')
                time.sleep('1.5')
                clear()
                continue
            if loser == player:
                return 'lose'
            elif loser == villan:
                return 'win'
        else:
            return None

def main():
    clear()
    while player.hp > 0 and villan.current_room == 'Hallway':
        clear()
        result = if_fight()
        print(result)
        if result != None:  # check for game ending scenareo.
            return result
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

# sequence that happens when you win or lose.
def ending_sequence(result):
    if result == 'win':
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
            print("You lose karma.")
            time.sleep(2)
        clear()
        print(winner)
        time.sleep(3)
        clear()
    elif result == 'lose':
        clear()
        print(gameover)
        time.sleep(3)
        clear()
winner = '''
 _     _  ___   __    _  __    _  __    _  _______  ______    __  
| | _ | ||   | |  |  | ||  |  | ||  |  | ||       ||    _ |  |  | 
| || || ||   | |   |_| ||   |_| ||   |_| ||    ___||   | ||  |  | 
|       ||   | |       ||       ||       ||   |___ |   |_||_ |  | 
|       ||   | |  _    ||  _    ||  _    ||    ___||    __  ||__| 
|   _   ||   | | | |   || | |   || | |   ||   |___ |   |  | | __  
|__| |__||___| |_|  |__||_|  |__||_|  |__||_______||___|  |_||__| 
'''
gameover = '''
 ___      _______  _______  _______  ______    __  
|   |    |       ||       ||       ||    _ |  |  | 
|   |    |   _   ||  _____||    ___||   | ||  |  | 
|   |    |  | |  || |_____ |   |___ |   |_||_ |  | 
|   |___ |  |_|  ||_____  ||    ___||    __  ||__| 
|       ||       | _____| ||   |___ |   |  | | __  
|_______||_______||_______||_______||___|  |_||__| 
'''

# function containing main loop.
if __name__ == '__main__':
    instr()
    while villan.hp > 0 and player.hp > 0:
        clear()
        result = main()
    ending_sequence(result)
