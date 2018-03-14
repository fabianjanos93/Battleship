import random as idekjnrise
import sys
import time
# Generate boards
size = 6


# Clear Terminal
def clear():
    print("\033[H\033[J")


# clear terminal and a normal screen for player change
def change_player(name):
    input("End turn")
    clear()
    input("\n\n\n\n\n        "+name + "? \n\n\n")
    clear()


# first line creat
def first_line():
    global size
    abc = [" A ", " B ", " C ", " D ", " E ", " F ", " G ", " H ", " I ", " J "]
    first_line_return = "  "
    for i in range(size):
        first_line_return += abc[i]
    return first_line_return


# write out the board state
def print_out(pl_map, enemy_map):
    red = "\033[1;30;41m"
    white = "\033[1;30;47m"
    blue = "\033[1;30;44m"
    cyan = "\033[1;30;46m"
    yellow = "\033[1;30;43m"
    disable = "\033[0m"
    print(" ", first_line(), " " *
          20, " ", first_line())
    for i in range(size):
        enemy_line = ""
        pl_line = ""

        for j in range(size - 1):
            if pl_map[i][j] == "X":
                pl_line += "{}   ".format(red)
            elif pl_map[i][j] == "-":
                pl_line += "{}   ".format(cyan)
            elif pl_map[i][j] == "0":
                pl_line += "{}   ".format(blue)
            else:
                pl_line += "{}   ".format(yellow)
        if pl_map[i][size-1] == "X":
            pl_line += "{}   {}".format(red, disable)
        elif pl_map[i][size-1] == "-":
            pl_line += "{}   {}".format(cyan, disable)
        elif pl_map[i][size-1] == "0":
            pl_line += "{}   {}".format(blue, disable)
        else:
            pl_line += "{}   {}".format(yellow, disable)

        for j in range(size - 1):
            if enemy_map[i][j] == "X":
                enemy_line += "{}   ".format(red)
            elif enemy_map[i][j] == "-":
                enemy_line += "{}   ".format(blue)
            else:
                enemy_line += "{}   ".format(white)
        if enemy_map[i][size-1] == "X":
            enemy_line += "{}   {}".format(red, disable)
        elif enemy_map[i][size-1] == "-":
            enemy_line += "{}   {}".format(blue, disable)
        else:
            enemy_line += "{}   {}".format(white, disable)
        print("{:>2} ".format(i + 1), pl_line, " " * 20, "{:>2} ".format(i + 1), enemy_line)


# write out only your board, for the ship placements
def print_out_Create(pl_map):
    print(" ", ["A", "B", "C", "D", "E", "F"])
    for i in range(size):
        print(i + 1, pl_map[i])


# shoot to the x-y coordinates and return with the table and the boolean if it duable
def shoot(x, y, map, player):
    again = False
    target = map[y][x]
    if target == "X" or target == "-":
        again = True
        if player:
            print("You shot here before!")
    target = map[y][x]
    if target in ["0", "-"]:
        map[y][x] = "-"
    else:
        map[y][x] = "X"
        if player:
            print("hit")
        out = True
        for i in range(size):
            for j in range(size):
                if map[i][j] == target:
                    out = False
        if out and player:
            print("Out!")
    return again, map


# ship placement
def place(x, y, map, rotate, length, number):
    again = False
    for i in range(length):
        if rotate:
            if int(y) + int(i) < len(map):
                if map[int(y) + int(i)][int(x)] == "0":
                    map[int(y) + int(i)][int(x)] = str(number)
                else:
                    print("wrong placement")
                    again = True
            else:
                print("wrong placement")
                again = True
        else:
            if int(x) + int(i) < len(map):
                if map[int(y)][int(x) + int(i)] == "0":
                    map[int(y)][int(x) + int(i)] = str(number)
                else:
                    print("wrong placement")
                    again = True
            else:
                print("wrong placement")
                again = True
    if again:
        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == str(number):
                    map[i][j] = "0"
    return again, map


# ship placement for the player with all the fluff
def place_player(length, map, number):
    again = True
    rotate = False
    while again:
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
            x, y, again = inputcheck(koord)
            if not again:
                again, map = place(x, y, map, rotate, length, number)
    return map


# transfer the input to workeable x and y coordinates
def inputcheck(koord):
    global size
    again = False
    if koord == "EXIT":
        sys.exit
    try:
        x, y = koord.split("-")
        if x in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
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
            elif x == "F":
                x = 5
            elif x == "G":
                x = 6
            elif x == "H":
                x = 7
            elif x == "I":
                x = 8
            else:
                x = 9
            if str(y) in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
                y = int(y) - 1
            else:
                x, y = 11, 11
                again = True
        else:
            x, y = 11, 11
            again = True
        if x > size-1 or y > size-1:
            again = True
    except(ValueError, TypeError, NameError):
        x, y = 11, 11
        again = True
    return x, y, again


# check the coord is in the table and, if it"s a valid target for computer
def isvalidkoord(x, y, map):
    if x in range(size) and y in range(size):
        if (map[y][x] not in ["-", "X"]):
            return True
    return False


def is_valid_to_continue(x, y, map):
    if x in range(size) and y in range(size):
        if (map[y][x] not in ["-"]):
            return True
    return False


# Hard AI "cross shoot" component
def itsahityarrharr(xy, arrayforstuff, map, direc):
    x = int(xy[0])
    y = int(xy[1])
    right = str(x + 1) + str(y) + "r"
    left = str(x - 1) + str(y) + "l"
    down = str(x) + str(y + 1) + "d"
    up = str(x) + str(y - 1) + "u"
    if isvalidkoord(x + 1, y, map) and right not in arrayforstuff and direc in ["0", "r"]:
        arrayforstuff.append(right)
    elif is_valid_to_continue(x + 1, y, map) and right not in arrayforstuff and direc in ["0", "r"]:
        itsahityarrharr(str(x + 1) + str(y), arrayforstuff, map, "r")

    if isvalidkoord(x - 1, y, map) and left not in arrayforstuff and direc in ["0", "l"]:
        arrayforstuff.append(left)
    elif is_valid_to_continue(x - 1, y, map) and left not in arrayforstuff and direc in ["0", "l"]:
        itsahityarrharr(str(x - 1) + str(y), arrayforstuff, map, "l")

    if isvalidkoord(x, y + 1, map) and down not in arrayforstuff and direc in ["0", "d"]:
        arrayforstuff.append(down)
    elif is_valid_to_continue(x, y + 1, map) and down not in arrayforstuff and direc in ["0", "d"]:
        itsahityarrharr(str(x) + str(y + 1), arrayforstuff, map, "d")

    if isvalidkoord(x, y - 1, map) and up not in arrayforstuff and direc in ["0", "u"]:
        arrayforstuff.append(up)
    elif is_valid_to_continue(x, y - 1, map)and up not in arrayforstuff and direc in ["0", "u"]:
        itsahityarrharr(str(x) + str(y - 1), arrayforstuff, map, "u")

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
    difficulty = "nope"
    playmode = "nope"
    streak_option = False
    while playmode not in ["M", "S", "Multi", "Solo"]:
        playmode = input("Choose a play mode ([S]olo/[M]ulti)")
    if playmode in ["S", "Solo"]:
        while difficulty not in ["H", "E", "Hard", "Easy"]:
            name1 = input("Enter your name: ")
            name2 = "SkyNet"
            difficulty = input("Choose a play mode ([E]asy/[H]ard)")
    else:
        name1 = input("Enter First player name: ")
        name2 = input("Enter Second player name: ")
    if input("Streak(Y/N): ") in ["Y", "y", "yes", "YES"]:
        streak_option = True
    return playmode, difficulty, streak_option, name1, name2


# Check if player winned
def check_win(enemy_map):
    win = True
    for i in range(size):
        for j in range(size):
            if not enemy_map[i][j] == "0" and not enemy_map[i][j] == "X" and not enemy_map[i][j] == "-":
                win = False
    return win


# AI place randomly the ships
def ai_placement(pl2map, ship_length, ship_number):
    global size
    again = True
    while again:
        rotate = False
        x = idekjnrise.randint(0, size-1)
        y = idekjnrise.randint(0, size-1)
        R = idekjnrise.randint(0, size-1)
        if R == 1:
            rotate = True
        again, pl2map = place(x, y, pl2map, rotate, ship_length, ship_number)
    return pl2map


# Full player turn
def player_turn(pl_map, enemy_map, name):
    global streak
    again = True
    while again:
        clear()
        print_out(pl_map, enemy_map)
        koord = input("Choose a target (in B-3 format): ")
        x, y, again = inputcheck(koord)
        if not again:
            again, enemy_map = shoot(x, y, enemy_map, True)
            if streak and enemy_map[y][x] == "X" and not again:
                if check_win(enemy_map):
                    clear()
                    print("\n \n \n \n \n        {}  \n \n \n \n \n".format(name))
                    sys.exit
                else:
                    enemy_map = player_turn(pl_map, enemy_map, name)
        clear()
        print_out(pl_map, enemy_map)
    return enemy_map


# generate shooting positions
def generate_hard_positions(x):
    f = 0
    s = x
    global size
    wannabe_filled_up_array = []
    while f < size:
        if s < size:
            wannabe_filled_up_array.append(str(f)+str(s)+"0")
            s += 4
        else:
            x += 1
            s = (x % 4)
            f += 1
            if f < size:
                wannabe_filled_up_array.append(str(f)+str(s)+"0")
    return wannabe_filled_up_array


# generate the shooting pattern for hard ai
def generate_hard_pattern():
    again = True
    mechiteration = 0
    # Declare and generate one of the 2 possible shoot pattern
    rand11 = generate_hard_positions(0)
    rand12 = generate_hard_positions(2)
    rand21 = generate_hard_positions(1)
    rand22 = generate_hard_positions(3)
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


# size input check
def size_input():
    global size
    again = True
    while again:
        try:
            clear()
            size = int(input("Map size(6 to 10): "))
            if size <= 10 and size >= 6:
                again = False
        except(ValueError):
            clear()
            again = True


def main():
    global size
    size_input()
    pl1map = [["0" for x in range(size)] for y in range(size)]
    pl2map = [["0" for x in range(size)] for y in range(size)]
    global streak
    playmode, difficulty, streak, player1, player2 = playmode_and_difficulty()

    pl1map = player_placement(pl1map)
    if playmode in ["M", "Multi"]:
        change_player(player2)

        pl2map = player_placement(pl2map)

        change_player(player1)

    game = True
    while game and playmode in ["M", "Multi"]:
        # First Player
        pl2map = player_turn(pl1map, pl2map, player1)
        win = check_win(pl2map)
        if win:
            clear()
            print("\n \n \n \n \n         {} won \n \n \n \n \n".format(player1))
            break
        # Second player
        change_player(player2)
        pl1map = player_turn(pl2map, pl1map, player2)
        win = check_win(pl1map)
        if win:
            clear()
            print("\n \n \n \n \n         {} won \n \n \n \n \n".format(player2))
            break

        change_player(player1)

    # Computer ship generate part
    if playmode in ["S", "Solo"]:
        pl2map = ai_placement(pl2map, 4, 1)
        pl2map = ai_placement(pl2map, 3, 2)
        pl2map = ai_placement(pl2map, 2, 3)
        pl2map = ai_placement(pl2map, 2, 4)

    # Easy computer game part
    while game and difficulty in ["E", "Easy"]:
        # Player Turn
        pl2map = player_turn(pl1map, pl2map, )
        win = check_win(pl2map)
        if win:
            clear()
            print("\n \n \n \n \n         {} won \n \n \n \n \n".format(player1))
            break
        # Easy Computer turn
        again = True
        while again:
            x = idekjnrise.randint(0, size-1)
            y = idekjnrise.randint(0, size-1)
            again, pl1map = shoot(x, y, pl1map, False)

        win = check_win(pl1map)
        if win:
            clear()
            print("\n \n \n \n \n         {} won \n \n \n \n \n".format(player2))
            break

        clear()

    # Hard computer generate part
    if difficulty in ["H", "Hard"]:
        crosshair = generate_hard_pattern()
        mechiteration = 0
        talalat = []

    # Hard computer game part
    while game and difficulty in ["H", "Hard"]:
        # Player turn
        pl2map = player_turn(pl1map, pl2map, player1)
        win = check_win(pl2map)
        if win:
            clear()
            print("\n \n \n \n \n         {} won \n \n \n \n \n".format(player1))
            break

        # Hard computer turn
        def hard_comp_turn(talalat, mechiteration, crosshair, pl1map):
            if len(talalat) == 0:
                again = True
                while again:
                    target = crosshair[mechiteration]
                    x = int(crosshair[mechiteration][0])
                    y = int(crosshair[mechiteration][1])
                    direction = crosshair[mechiteration][2]
                    mechiteration += 1
                    again, pl1map = shoot(x, y, pl1map, False)
                    if pl1map[y][x] in ["X"]:
                        talalat = itsahityarrharr(target, talalat, pl1map, direction)
                        if streak:
                            clear()
                            print_out(pl1map, pl2map)
                            time.sleep(0.5)
                            talalat, mechiteration, crosshair, pl1map = hard_comp_turn(talalat, mechiteration,
                                                                                       crosshair, pl1map)
                            return talalat, mechiteration, crosshair, pl1map
            else:
                target = talalat[0]
                x = int(talalat[0][1])
                y = int(talalat[0][0])
                direction = talalat[0][2]
                talalat.remove(target)
                again, pl1map = shoot(y, x, pl1map, False)
                if pl1map[x][y] not in ["-"] and not again:
                    talalat = itsahityarrharr(target, talalat, pl1map, direction)
                    if streak:
                        clear()
                        print_out(pl1map, pl2map)
                        time.sleep(0.5)
                        talalat, mechiteration, crosshair, pl1map = hard_comp_turn(talalat, mechiteration,
                                                                                   crosshair, pl1map)
                        return talalat, mechiteration, crosshair, pl1map
            return talalat, mechiteration, crosshair, pl1map

        talalat, mechiteration, crosshair, pl1map = hard_comp_turn(talalat, mechiteration, crosshair, pl1map)
        win = check_win(pl1map)
        if win:
            clear()
            print("\n \n \n \n \n         {} always win \n \n \n \n \n".format(player2))
            break
        time.sleep(1)


main()
