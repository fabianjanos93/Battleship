import random as idekjnrise
# Generate boards
meret = 6
pl1map = [["0" for x in range(meret)] for y in range(meret)]
pl2map = [["0" for x in range(meret)] for y in range(meret)]


# clear terminal and a normal screen for player change
def change_player(name):
    input('End turn')
    print("\033[H\033[J")
    input('\n\n\n\n\n        '+name + '? \n\n\n')
    print("\033[H\033[J")


# write out the board state
def print_out(pl_map, enemy_map):
    print(' ', ["A", "B", "C", "D", "E", "F"], ' ' *
          20, ' ', ["A", "B", "C", "D", "E", "F"])
    for i in range(meret):
        rajz = str(i + 1) + " ["
        for j in range(meret - 1):
            if enemy_map[i][j] == "X":
                rajz += "'X', "
            elif enemy_map[i][j] == "-":
                rajz += "'-', "
            else:
                rajz += "'0', "
        if enemy_map[i][5] == "X":
            rajz += "'X']"
        elif enemy_map[i][5] == "-":
            rajz += "'-']"
        else:
            rajz += "'0']"
        print(i + 1, pl_map[i], ' ' * 20, rajz)


# write out only your board, for the ship placements
def print_out_Create(pl_map):
    print(' ', ["A", "B", "C", "D", "E", "F"])
    for i in range(meret):
        print(i + 1, pl_map[i])


# shoot to the x-y coordinates and return with the table and the boolean if it duable
def shoot(x, y, map, player):
    helyes = False
    target = map[y][x]
    if target == "X" or target == "-":
        helyes = True
        if player:
            print('You shot here before!')
    target = map[y][x]
    if target in ['0', '-']:
        map[y][x] = '-'
    else:
        map[y][x] = 'X'
        if player:
            print('hit')
        out = True
        for i in range(meret):
            for j in range(meret):
                if map[i][j] == target:
                    out = False
        if out and player:
            print('Out!')
    return helyes, map


# ship placement
def place(x, y, map, rotate, length, number):
    helyes = False
    for i in range(length):
        if rotate:
            if int(y) + int(i) < len(map):
                if map[int(y) + int(i)][int(x)] == "0":
                    map[int(y) + int(i)][int(x)] = str(number)
                else:
                    print('rossz elhelyezés')
                    helyes = True
            else:
                print('rossz elhelyezés')
                helyes = True
        else:
            if int(x) + int(i) < len(map):
                if map[int(y)][int(x) + int(i)] == "0":
                    map[int(y)][int(x) + int(i)] = str(number)
                else:
                    print('rossz elhelyezés')
                    helyes = True
            else:
                print('rossz elhelyezés')
                helyes = True
    if helyes:
        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == str(number):
                    map[i][j] = "0"
    return helyes, map


# ship placement for the player with all the fluff
def place_player(length, map, number):
    helyes = True
    rotate = False
    while helyes:
        print("\033[H\033[J")
        print("Where whould you like to place the " + str(length) + " length ship?")
        print("(set O point in the B-4 form)")
        print("(R in case of rotate)")
        print_out_Create(map)
        if rotate:
            print("ship: O")
            for x in range(length - 1):
                print("      X")
        else:
            utotag = ""
            for x in range(length - 1):
                utotag += "X"
            print("ship: O" + utotag)
        koord = input()
        if len(koord) == 1 and koord == "R":
            rotate = not rotate
        else:
            x, y, helyes = inputcheck(koord)
            if not helyes:
                helyes, map = place(x, y, map, rotate, length, number)
    return map


# transfer the input to workeable x and y coordinates
def inputcheck(koord):
    helyes = False
    if len(koord) == 3 and "-" in koord:
        x, y = koord.split("-")
        if x in ["A", "B", "C", "D", "E", "F"]:
            if x == "A":
                x = 0
            elif x == "B":
                x = 1
            elif x == "C":
                x = 2
            elif x == "D":
                x = 3
            elif x == "E":
                x = 4
            else:
                x = 5
            if str(y) in["1", "2", "3", "4", "5", "6", ]:
                y = int(y) - 1
            else:
                x, y = 7, 7
                helyes = True
        else:
            x, y = 7, 7
            helyes = True
    else:
        x, y = 7, 7
        helyes = True

    return x, y, helyes


# check the coord is in the table and, if it's a valid target for computer
def isvalidkoord(x, y, map):
    if x in [0, 1, 2, 3, 4, 5] and y in [0, 1, 2, 3, 4, 5]:
        if (map[y][x] not in ['X', '-']):
            return True
    return False


# Hard AI 'cross shoot' component
def itsahityarrharr(xy, arrayforstuff, map, direc):
    x = int(xy[0])
    y = int(xy[1])
    if isvalidkoord(x + 1, y, map) and str(x + 1) + str(y) + \
            'r' not in arrayforstuff and direc in ['0', 'r']:
        if map[x + 1][y] == 'X':
            itsahityarrharr(str(x + 1) + str(y), arrayforstuff, map, direc)
        else:
            arrayforstuff.append(str(x + 1) + str(y) + 'r')

    if isvalidkoord(x - 1, y, map) and str(x - 1) + str(y) + \
            'l' not in arrayforstuff and direc in ['0', 'l']:
        if map[x + 1][y] == 'X':
            itsahityarrharr(str(x - 1) + str(y), arrayforstuff, map, direc)
        else:
            arrayforstuff.append(str(x - 1) + str(y) + 'l')

    if isvalidkoord(x, y + 1, map) and str(x) + str(y + 1) + \
            'd' not in arrayforstuff and direc in ['0', 'd']:
        if map[x + 1][y] == 'X':
            itsahityarrharr(str(x) + str(y + 1), arrayforstuff, map, direc)
        else:
            arrayforstuff.append(str(x) + str(y + 1) + 'd')

    if isvalidkoord(x, y - 1, map) and str(x) + str(y - 1) + \
            'u' not in arrayforstuff and direc in ['0', 'u']:
        if map[x + 1][y] == 'X':
            itsahityarrharr(str(x) + str(y - 1), arrayforstuff, map, direc)
        else:
            arrayforstuff.append(str(x) + str(y - 1) + 'u')

    return arrayforstuff


# Player place the 4 ship (ship number changeable here)
def player_placement(pl_map):
    pl1map = place_player(4, pl_map, 1)
    pl1map = place_player(3, pl_map, 2)
    pl1map = place_player(2, pl_map, 3)
    pl1map = place_player(2, pl_map, 4)
    clear()
    print_out_Create(pl_map)
    return pl_map


# Ask player for playmode(Multi or Solo) and Difficulti in case of Solo
def playmode_and_difficulty():
    difficulty = 'nope'
    playmode = 'nope'
    while playmode not in ['M', 'S', 'Multi', 'Solo']:
        playmode = input('Choose a play mode ([S]olo/[M]ulti)')
    if playmode in ['S', 'Solo']:
        while difficulty not in ['H', 'E', 'Hard', 'Easy']:
            difficulty = input('Choose a play mode ([E]asy/[H]ard)')
    return playmode, difficulty


# Check if player winned
def check_win(enemy_map):
    win = True
    for i in range(meret):
        for j in range(meret):
            if not enemy_map[i][j] == '0' and not enemy_map[i][j] == 'X' and not enemy_map[i][j] == '-':
                win = False
    return win


# Clear Terminal
def clear():
    print("\033[H\033[J")


# AI place randomly the ships
def ai_placement(pl2map, ship_length, ship_number):
    helyes = True
    while helyes:
        rotate = False
        x = idekjnrise.randint(0, 5)
        y = idekjnrise.randint(0, 5)
        R = idekjnrise.randint(0, 1)
        if R == 1:
            rotate = True
        helyes, pl2map = place(x, y, pl2map, rotate, ship_length, ship_number)
    return pl2map


# Full player turn
def player_turn(pl_map, enemy_map):
    helyes = True
    while helyes:
        clear()
        print_out(pl_map, enemy_map)
        koord = input('Choose a target (in B-3 format): ')
        x, y, helyes = inputcheck(koord)
        if not helyes:
            helyes, pl2map = shoot(x, y, enemy_map, True)
    return enemy_map


# generate the shooting pattern for hard ai
def generate_hard_pattern():
    helyes = True
    mechiteration = 0
    # Declare and generate one of the 2 possible shoot pattern
    rand11 = ['000', '040', '110', '150', '220', '330', '400', '440', '510', '550']
    rand12 = ['020', '130', '200', '240', '310', '350', '420', '530']
    rand21 = ['010', '050', '120', '230', '300', '340', '410', '450', '520']
    rand22 = ['030', '100', '140', '210', '250', '320', '430', '500', '540']
    rand1 = []
    rand2 = []
    # Choose one of the 4
    if idekjnrise.randint(0, 1) == 1:
        if idekjnrise.randint(0, 1) == 1:
            rand1 = rand11
            rand2 = rand12
        else:
            rand1 = rand12
            rand2 = rand11
    else:
        if idekjnrise.randint(0, 1) == 1:
            rand1 = rand21
            rand2 = rand22
        else:
            rand1 = rand22
            rand2 = rand21
    # Ugly Calculations
    for i in range(100):
        randomnumber1 = idekjnrise.randint(0, len(rand1)-1)
        randomnumber2 = idekjnrise.randint(0, len(rand1)-1)
        temp = rand1[randomnumber1]
        rand1[randomnumber1] = rand1[randomnumber2]
        rand1[randomnumber2] = temp
        randomnumber3 = idekjnrise.randint(0, len(rand2)-1)
        randomnumber4 = idekjnrise.randint(0, len(rand2)-1)
        temp = rand2[randomnumber3]
        rand2[randomnumber3] = rand2[randomnumber4]
        rand2[randomnumber4] = temp
    crosshair = []
    for i in rand1:
        crosshair.append(i)
    for i in rand2:
        crosshair.append(i)
    return crosshair


def main():
    playmode, difficulty = playmode_and_difficulty()

    pl1map = player_placement(pl1map)
    if playmode in ['M', 'Multi']:
        change_player('Player 2')

        pl2map = player_placement(pl2map)

        change_player('Player 1')

    game = True
    while game and playmode in ['M', 'Multi']:
        # First Player
        pl2map = player_turn(pl1map, pl2map)
        win = check_win(pl2map)
        if win:
            clear()
            print("\n \n \n \n \n         Player 1 won \n \n \n \n \n")
            break
        # Secound player
        change_player('Player 2')
        pl1map = player_turn(pl2map, pl1map)
        win = check_win(pl1map)
        if win:
            clear()
            print("\n \n \n \n \n         Player 2 won \n \n \n \n \n")
            break

        change_player('Player 1')

    # Computer ship generate part
    if playmode in ['S', 'Solo']:
        pl2map = ai_placement(pl2map, 4, 1)
        pl2map = ai_placement(pl2map, 3, 2)
        pl2map = ai_placement(pl2map, 2, 3)
        pl2map = ai_placement(pl2map, 2, 4)

    # Easy computer game part
    while game and difficulty in ['E', 'Easy']:
        # Player Turn
        pl2map = player_turn(pl1map, pl2map)
        win = check_win(pl2map)
        if win:
            clear()
            print("\n \n \n \n \n         Player 1 won \n \n \n \n \n")
            break
        # Easy Computer turn
        helyes = True
        while helyes:
            x = idekjnrise.randint(0, 5)
            y = idekjnrise.randint(0, 5)
            helyes, pl1map = shoot(x, y, pl1map, False)

        win = check_win(pl1map)
        if win:
            clear()
            print("\n \n \n \n \n         Computer won \n \n \n \n \n")
            break

        clear()

    # Hard computer generate part
    if difficulty in ['H', 'Hard']:
        crosshair = generate_hard_pattern()
        mechiteration = 0
        talalat = []

    # Hard computer game part
    while game and difficulty in ['H', 'Hard']:
        # Player turn
        pl2map = player_turn(pl1map, pl2map)
        win = check_win(pl2map)
        if win:
            clear()
            print("\n \n \n \n \n         Player 1 won \n \n \n \n \n")
            break
        # Hard computer turn
        if len(talalat) == 0:
            helyes = True
            while helyes:
                target = crosshair[mechiteration]
                x = int(crosshair[mechiteration][0])
                y = int(crosshair[mechiteration][1])
                direction = crosshair[mechiteration][2]
                helyes, pl1map = shoot(x, y, pl1map, False)
                if pl1map[y][x] in ['X']:
                    talalat = itsahityarrharr(target, talalat, pl1map, direction)
                mechiteration += 1
        else:
            target = talalat[0]
            x = int(talalat[0][1])
            y = int(talalat[0][0])
            direction = talalat[0][2]
            shoot(y, x, pl1map, False)
            if pl1map[x][y] in ['X']:
                talalat = itsahityarrharr(target, talalat, pl1map, direction)
            talalat.remove(target)

        win = check_win(pl1map)
        if win:
            clear()
            print("\n \n \n \n \n         Computer won \n \n \n \n \n")
            break


main()
