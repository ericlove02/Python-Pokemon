# --- imports --- #
from random import randint
from math import sqrt


# --- functions --- #


def pokemon_catch():
    """takes no input, runs mini game, returns boolean for whether or not catch was successful"""
    print('\n')
    print("A wild pokemon has appeared!")
    print("Guess the number 1 - 10 correct in under 3 guesses!")
    success = False
    num = randint(1, 10)
    for k in range(3):
        guess = input_int("Enter your guess:")
        if not guess == num:
            if guess > num:
                print("A little too high")
            elif guess < num:
                print("A little too low")
        else:
            print("You got it right!\n")
            success = True
            break
        if k == 2 and not success:
            print("Dang! The number was " + str(num) + ". Better luck next time")
    if success:
        add_pokemon()
        global playerInfo
        playerInfo = csv_to_list('player' + str(currentPlayer) + '.csv')
        print("You caught a " + playerInfo[-21] + "!")
        rand = randint(1, 3)
        addedCandy = 0
        if rand == 1:
            addedCandy = 3
        elif rand == 2:
            addedCandy = 5
        elif rand == 3:
            addedCandy = 10
        update_candies(currentPlayer, addedCandy)
        print(playerInfo[-21], "and", addedCandy, "candies have been added to your collection!\n")
    main_menu()


def level_up(lvl):
    """takes in current pokemon level, allows user to spend candies to level up, returns new level"""
    global currentPokemon, playerInfo, currentPlayer
    if int(lvl) >= 40:
        print(playerInfo[currentPokemon * 22 + 1], "is already max level!")
    elif 1 <= int(lvl) <= 30:
        if get_candies(currentPlayer) - 1 >= 0:
            update_candies(currentPlayer, -1)
            playerInfo[currentPokemon * 22 + 4] = int(float(playerInfo[currentPokemon * 22 + 4]) +
                                                      float(playerInfo[currentPokemon * 22 + 4]) * .0094 /
                                                      (.095 * sqrt(int(lvl))))
            '''if int(playerInfo[currentPokemon * 6 + 4]) > int(playerInfo[currentPokemon * 6 + 3]):  # if cp > max cp
                playerInfo[currentPokemon * 6 + 4] = int(playerInfo[currentPokemon * 6 + 3])
                print("Pokemon has reached its max CP")'''
            playerInfo[currentPokemon * 22 + 5] = int(playerInfo[currentPokemon * 22 + 5]) + 1
            print(str(playerInfo[currentPokemon * 22 + 1]) + " has been leveled up to level " +
                  str(playerInfo[currentPokemon * 22 + 5]) + ". Their CP has increased to " +
                  str(playerInfo[currentPokemon * 22 + 4]))
            list_to_csv(playerInfo, 'player' + str(currentPlayer) + '.csv', 'w')
        else:
            print("You don't have enough candies to level up")
    elif 31 <= int(lvl) < 40:
        if get_candies(currentPlayer) - 2 >= 0:
            update_candies(currentPlayer, -2)
            playerInfo[currentPokemon * 22 + 4] = int(float(playerInfo[currentPokemon * 22 + 4]) +
                                                      float(playerInfo[currentPokemon * 22 + 4]) *
                                                      .0045 / (.095 * sqrt(int(lvl))))
            '''if int(playerInfo[currentPokemon * 6 + 4]) > int(playerInfo[currentPlayer * 6 + 3]):  # if cp > max cp
                playerInfo[currentPokemon * 6 + 4] = int(playerInfo[currentPlayer * 6 + 3])
                print("Pokemon has reached its max CP")'''
            playerInfo[currentPokemon * 22 + 5] = int(playerInfo[currentPokemon * 22 + 5]) + 1
            print(playerInfo[currentPokemon * 22 + 1] + " has been leveled up to level " +
                  str(playerInfo[currentPokemon * 22 + 5]) + ". Their CP has increased to " +
                  str(playerInfo[currentPokemon * 22 + 4]))
            list_to_csv(playerInfo, 'player' + str(currentPlayer) + '.csv', 'w')
        else:
            print("You don't have enough candies to level up")
    display_pokemon_info()


def pokemon_battle():
    """determines winning pokemon, prints winner"""
    while True:
        try:
            opponent = input("\nWhat player would you like to fight (type exit to return to main menu):")
            if opponent == 'exit':
                main_menu()
            opponent = int(opponent)
            open('player' + str(opponent) + '.csv')
            break
        except FileNotFoundError:
            print("That player does not exist")
        except ValueError:
            print("Enter an integer")
    opponentList = csv_to_list('player' + str(opponent) + '.csv')

    global playerInfo
    print('\n' + " You are battling with: ".center(40, "-"))
    print(playerInfo[currentPokemon * 22 + 1])
    print("CP: ", playerInfo[currentPokemon * 22 + 4])

    print(" Opponent Pokemon ".center(80, '-'))
    oppPokemon = []
    numOpponentPokemon = 0
    for i in range(152 // 4):
        try:
            oppPokemon.append(opponentList[i * 22 + 1])
            oppPokemon.append(opponentList[i * 22 + 4])
        except IndexError:
            if numOpponentPokemon == 0:
                numOpponentPokemon = i
            oppPokemon.append("Empty")
            oppPokemon.append("N/A")
    index = 0
    for i in range(1, 152 // 4):
        for k in range(1, 5):
            print(str(index + 1) + ". {:<20}".format(oppPokemon[index * 2]), end='')
            index += 1
        index -= 4
        print()
        for k in range(1, 5):
            print("   CP: " + "{:<16}".format(oppPokemon[index * 2 + 1]), end='')
            index += 1
        print('\n')
        if oppPokemon[(index - 1) * 2] == 'Empty' or oppPokemon[index * 2] == 'Empty':
            break
    print((" Opponent has 1 - " + str(numOpponentPokemon) + " to choose from ").center(80, '-'))

    while True:
        try:
            opponentPokemon = input_int("Which would you like to fight:") - 1
            opponentList[opponentPokemon * 22]
            break
        except IndexError:
            print("Invalid selection")

    # fight odds calculations
    # if player better than opp, .5 + (cp diff/player cp). if opp better than player, .5 + (cp diff/player cp). else .5
    if int(playerInfo[currentPokemon * 22 + 4]) > int(opponentList[opponentPokemon * 22 + 4]):
        odds = .5 + ((int(playerInfo[currentPokemon * 22 + 4]) - int(opponentList[opponentPokemon * 22 + 4])) /
                     int(playerInfo[currentPokemon * 22 + 4])) / 2
    elif int(playerInfo[currentPokemon * 22 + 4]) < int(opponentList[opponentPokemon * 22 + 4]):
        odds = .5 - (abs((int(playerInfo[currentPokemon * 22 + 4]) - int(opponentList[opponentPokemon * 22 + 4])) /
                         int(playerInfo[currentPokemon * 22 + 4]))) / 2
    else:
        odds = .5
    odds *= 100
    odds = 10 if odds <= 10 else 90 if odds >= 90 else odds  # balance odds if extremely high or low

    if randint(0, 100) <= odds:
        print("\nYour pokemon, " + str(playerInfo[currentPokemon * 22 + 1]) + ", won the fight against " +
              str(opponentList[opponentPokemon * 22 + 1]))
        print("Your CP was " + str(playerInfo[currentPokemon * 22 + 4]) + " and theirs was " +
              str(opponentList[opponentPokemon * 22 + 4]) + ". Your odds to win were " + str(round(odds, 2)) + "%")
        print("You have been rewarded with 2 candies")
        update_candies(currentPlayer, 2)
    else:
        print("\nYour pokemon, " + str(playerInfo[currentPokemon * 22 + 1]) + ", lost the fight against " +
              str(opponentList[opponentPokemon * 22 + 1]))
        print("Your CP was " + str(playerInfo[currentPokemon * 22 + 4]) + " and theirs was " +
              str(opponentList[opponentPokemon * 22 + 4]) + ". Your odds to win were " + str(round(odds, 2)) + "%")
        print("Better luck next time")
    main_menu()


def main_menu():
    """takes no input, prints out main menu and takes input from user"""
    global currentPlayer, currentPokemon, playerInfo
    print('\n' + " MAIN MENU ".center(80, '-'))
    print("1 - View current pokemon\n2 - Catch a new pokemon\n3 - Quick battle pokemon\n4 - Battle Player vs. Player\n5"
          " - Select player\n6 - Save and Exit\n")
    select = input_int("Enter your selection: ")
    if select == 1:
        display_pokemon_info()
    elif select == 2:
        pokemon_catch()
    elif select == 3:
        pokemon_battle()
    elif select == 4:
        pvp()
    elif select == 5:
        newPlayer = input_int("\nEnter player: ")
        currentPlayer = newPlayer
        currentPokemon = 0
        playerInfo = open_player(currentPlayer)
        main_menu()
    elif select == 6:
        list_to_csv(playerInfo, 'player' + str(currentPlayer) + '.csv', 'w')
        exit()
    else:
        print("Invalid selection")


def display_selection_menu():
    """Print list of pokemon and their info"""
    global playerInfo, currentPokemon, playerPokemon
    playerInfo = csv_to_list('player' + str(currentPlayer) + '.csv')
    print('\n' + " Pokemon Selection Menu ".center(80, "-"))
    print(playerInfo[currentPokemon * 22 + 1] + '\n')
    print("Current CP: ", playerInfo[currentPokemon * 22 + 4])
    print("Current Level: ", playerInfo[currentPokemon * 22 + 5])
    print("Candies: ", get_candies(currentPlayer))
    print("-" * 80)
    display_pokemon(playerInfo)
    print("-" * 80)
    while True:
        currentPokemon = input_int("Enter which pokemon you would like to select:") - 1
        if playerPokemon[currentPokemon * 2] == "Empty":
            print("Invalid pokemon, select a filled slot")
        else:
            break
    display_pokemon_info()


def display_pokemon_info():
    """Print pokemon name, cp, level, candies, and user options"""
    global playerInfo, currentPokemon
    playerInfo = open_player(currentPlayer)
    currentPokemon = currentPokemon
    print('\n' + " Current Pokemon ".center(80, "-"))
    print(playerInfo[currentPokemon * 22 + 1] + '\n')
    print("Current CP: ", playerInfo[currentPokemon * 22 + 4])
    print("Current Level: ", playerInfo[currentPokemon * 22 + 5])
    print("Candies: ", get_candies(currentPlayer))
    print("\n1 - Use Candy to Level-Up\n2 - View Pokemon's moves\n3 - Select different Pokemon\n4 - Exit to Main Menu")
    while True:
        select = input_int("Enter your selection:")
        if select == 1:
            level_up(playerInfo[currentPokemon * 22 + 5])
        elif select == 2:
            more_pokemon_info()
        elif select == 3:
            display_selection_menu()
        elif select == 4:
            main_menu()
        else:
            print("Invalid selection")


def more_pokemon_info():
    print('\n' + "Pokemon's Moves".center(80, "-"))
    print(playerInfo[currentPokemon * 18 + 1], "\n")
    print("Current CP: ", playerInfo[currentPokemon * 22 + 4])
    print("Current Level: ", playerInfo[currentPokemon * 22 + 5] + '\n')
    print("{:<30}".format(playerInfo[currentPokemon * 22 + 7]), end='')
    print("{:<30}".format(playerInfo[currentPokemon * 22 + 11]), end='')
    print("{:<30}".format(playerInfo[currentPokemon * 22 + 15]), end='')
    print("{:<30}".format(playerInfo[currentPokemon * 22 + 19]))
    for i in range(9, 22, 4):
        if playerInfo[currentPokemon * 22 + i - 1] == 'Damage':
            print("Dmg: {:<25}".format(playerInfo[currentPokemon * 18 + i]), end='')
        elif playerInfo[currentPokemon * 22 + i - 1] == 'Skip':
            print("{:<30}".format("Skip opponents move"), end='')
        elif playerInfo[currentPokemon * 22 + i - 1] == 'Down':
            print("{:<30}".format("Reduce opp dmg by " + str(playerInfo[currentPokemon * 22 + i])), end='')
        elif playerInfo[currentPokemon * 22 + i - 1] == 'Up':
            print("{:<30}".format("Increase self dmg by " + str(playerInfo[currentPokemon * 22 + i])), end='')
        elif playerInfo[currentPokemon * 22 + i - 1] == 'Heal':
            print("{:<30}".format("Increase health by " + str(playerInfo[currentPokemon * 22 + i])), end='')
    print()
    print("{:<30}".format("Cooldown: " + str(playerInfo[currentPokemon * 22 + 6])), end='')
    print("{:<30}".format("Cooldown: " + str(playerInfo[currentPokemon * 22 + 10])), end='')
    print("{:<30}".format("Cooldown: " + str(playerInfo[currentPokemon * 22 + 14])), end='')
    print("{:<30}".format("Cooldown: " + str(playerInfo[currentPokemon * 22 + 18])))
    input("\n\nPress enter to return")
    display_pokemon_info()


def open_player(pl):
    """takes in player number, create a csv specific to player if new player, add player number to existing players,
    else open player file """
    if pl not in players:
        players.append(pl)
        try:
            open('player' + str(pl) + '.csv', 'x')
        except FileExistsError:
            return csv_to_list('player' + str(pl) + '.csv')
        add_pokemon()
        try:
            open('candies' + str(currentPlayer) + '.txt', 'x')
            candiesFile = open('candies' + str(currentPlayer) + '.txt', 'r+')
            candiesFile.write('0')
        except FileExistsError:
            candiesFile = open('candies' + str(currentPlayer) + '.txt', 'r+')
        candiesFile.close()
        global playerInfo
        playerInfo = csv_to_list('player' + str(pl) + '.csv')
        print("Welcome new player! You were randomly given", playerInfo[-21])
        return csv_to_list('player' + str(pl) + '.csv')
    else:
        return csv_to_list('player' + str(pl) + '.csv')


def csv_to_list(file):
    """takes in a csv file, returns the contents of the file as a list"""
    from csv import reader
    with open(file, 'r', newline='') as csvfile:
        reader = reader(csvfile, delimiter=',')
        listInfo = []
        for row in reader:
            listInfo += row
    return listInfo


def list_to_csv(listInfo, file, write='a'):
    """takes in a list, a target file, and whether to append or write over, breaks up the contents of the list and
    APPENDS or WRITES OVER them to the target file"""
    from csv import writer, QUOTE_MINIMAL
    with open(file, write, newline='') as csvfile:
        writer = writer(csvfile, delimiter=',', quotechar='|', quoting=QUOTE_MINIMAL)
        writer.writerow(listInfo)


def update_candies(pl, change):
    """takes in the current player and the amount of change to the candies, opens player candy file, adds change
     to candies and rewrites"""
    file = open('candies' + str(pl) + '.txt', 'r+')
    candy = get_candies(pl)
    file.truncate(0)
    file.write(str(int(candy) + int(change)))
    file.close()


def get_candies(pl):
    """takes in the current player, opens player candy file, returns the amount of candies written in file"""
    file = open('candies' + str(pl) + '.txt')
    candy = int(file.read())
    file.close()
    return candy


def input_int(message):
    """take in a message, tries to take a value, if the value is not an int print message"""
    while True:
        try:
            value = int(input(message))
            break
        except ValueError:
            print("Enter an integer")
    return value


def add_pokemon():
    """randomly select a pokemon and moves from the csv files and add them to the players file"""
    pokemonMoves = []
    added = []
    for i in range(4):
        k = randint(0, 40)
        added.append(k)
        while k in added:
            k = randint(0, 40)
        pokemonMoves.append(moves[k * 4])
        pokemonMoves.append(moves[k * 4 + 1])
        pokemonMoves.append(moves[k * 4 + 2])
        pokemonMoves.append(moves[k * 4 + 3])
    i = randint(1, 152) * 4
    list_to_csv([pokemon[i], pokemon[i + 1], pokemon[i + 2], pokemon[i + 3], randint(int(pokemon[i + 2]),
                                                                                     int(pokemon[i + 3])), 1,
                 pokemonMoves[0], pokemonMoves[1], pokemonMoves[2], pokemonMoves[3],
                 pokemonMoves[4], pokemonMoves[5], pokemonMoves[6], pokemonMoves[7], pokemonMoves[8], pokemonMoves[9],
                 pokemonMoves[10], pokemonMoves[11], pokemonMoves[12], pokemonMoves[13],
                 pokemonMoves[14], pokemonMoves[15]], 'player' + str(currentPlayer) + '.csv')


def display_pokemon(playerList):
    """take in players list of pokemon and print out formatted list"""
    global playerPokemon
    playerPokemon = []
    for i in range(152 // 4):
        try:
            playerPokemon.append(playerList[i * 22 + 1])
            playerPokemon.append(playerList[i * 22 + 4])
        except IndexError:
            playerPokemon.append("Empty")
            playerPokemon.append("N/A")
    index = 0
    for i in range(1, 152 // 4):
        for k in range(1, 5):
            print("{:<20}".format(str(index + 1) + ". " + str(playerPokemon[index * 2])), end='')
            index += 1
        index -= 4
        print()
        for k in range(1, 5):
            print("{:<20}".format("   CP: " + str(playerPokemon[index * 2 + 1])), end='')
            index += 1
        print('\n')
        if playerPokemon[(index - 1) * 2] == 'Empty' or playerPokemon[index * 2] == 'Empty':
            break  # will display all of your collection until a row ends or starts with an 'Empty'


def pvp():
    """runs player vs player pokemon battle using players moves and cp found in player csv files"""
    # setup
    print("\nTwo players will now be able to player against each other, decide who is player 1 and player 2\n")
    print("PLAYER 1".center(40, '-'))
    while True:
        try:
            player1 = input("\nEnter the first player (type exit to return to main menu):")
            if player1 == 'exit':
                main_menu()
            player1 = int(player1)
            open('player' + str(player1) + '.csv')
            break
        except FileNotFoundError:
            print("That player does not exist")
        except ValueError:
            print("Enter an integer")
    player1Info = csv_to_list('player' + str(player1) + '.csv')
    print()
    display_pokemon(player1Info)
    print("-" * 80)
    while True:
        player1Pokemon = input_int("Enter which pokemon you would like to select:") - 1
        if playerPokemon[player1Pokemon * 2] == "Empty":
            print("Invalid pokemon, select a filled slot")
        else:
            break
    print("Player 1 has selected a level " + player1Info[player1Pokemon * 22 + 5] + " " +
          player1Info[player1Pokemon * 22 + 1] + " with a CP of " + player1Info[player1Pokemon * 22 + 4] + '\n')

    print("PLAYER 2".center(40, '-'))
    while True:
        try:
            player2 = input("\nEnter the second player (type exit to return to main menu):")
            if player2 == 'exit':
                main_menu()
            player2 = int(player2)
            open('player' + str(player2) + '.csv')
            break
        except FileNotFoundError:
            print("That player does not exist")
        except ValueError:
            print("Enter an integer")
    player2Info = csv_to_list('player' + str(player2) + '.csv')
    print()
    display_pokemon(player2Info)
    print("-" * 80)
    while True:
        player2Pokemon = input_int("Enter which pokemon you would like to select:") - 1
        if playerPokemon[player2Pokemon * 2] == "Empty":
            print("Invalid pokemon, select a filled slot")
        else:
            break
    print("Player 2 has selected a level " + player2Info[player2Pokemon * 22 + 5] + " " +
          player2Info[player2Pokemon * 22 + 1] + " with a CP of " + player2Info[player2Pokemon * 22 + 4] + '\n')

    print(player1Info[player1Pokemon * 22 + 1] + " vs. " + player2Info[player2Pokemon * 22 + 1])
    print("Let the fight begin!" + "\n" + '-' * 50)

    print("Players will take turns using moves to deal damage or affect the match. Pokemon's CP will be their health\n")

    # players pokemon vars setup
    player1Health = int(player1Info[player1Pokemon * 22 + 4])  # set cp to health
    player2Health = int(player2Info[player2Pokemon * 22 + 4])
    player1Dmg = [int(player1Info[player1Pokemon * 22 + 9]), int(player1Info[player1Pokemon * 22 + 13]),
                  int(player1Info[player1Pokemon * 22 + 17]), int(player1Info[player1Pokemon * 22 + 21])]
    player2Dmg = [int(player2Info[player2Pokemon * 22 + 9]), int(player2Info[player2Pokemon * 22 + 13]),
                  int(player2Info[player2Pokemon * 22 + 17]), int(player2Info[player2Pokemon * 22 + 21])]
    player1Cooldowns = [int(player1Info[player1Pokemon * 22 + 6]), int(player1Info[player1Pokemon * 22 + 10]),
                        int(player1Info[player1Pokemon * 22 + 14]), int(player1Info[player1Pokemon * 22 + 18])]
    player2Cooldowns = [int(player2Info[player2Pokemon * 22 + 6]), int(player2Info[player2Pokemon * 22 + 10]),
                        int(player2Info[player2Pokemon * 22 + 14]), int(player2Info[player2Pokemon * 22 + 18])]
    player1CurrentCooldown = [0, 0, 0, 0]
    player2CurrentCooldown = [0, 0, 0, 0]
    skip = False

    # fight
    while player1Health > 0 and player2Health > 0:
        [player1Info, player1Pokemon, player1Health, player1Dmg, player1CurrentCooldown, player2Info, player2Pokemon,
         player2Health, player2Dmg, skip] = player_turn(player1Info, player1Pokemon, player1Health, player1Dmg,
                                                        player1CurrentCooldown, player2Info, player2Pokemon,
                                                        player2Health, player2Dmg, '1', '2', skip, player1Cooldowns,
                                                        player2)
        [player2Info, player2Pokemon, player2Health, player2Dmg, player2CurrentCooldown, player1Info, player1Pokemon,
         player1Health, player1Dmg, skip] = player_turn(player2Info, player2Pokemon, player2Health, player2Dmg,
                                                        player2CurrentCooldown, player1Info, player1Pokemon,
                                                        player1Health, player1Dmg, '2', '1', skip, player2Cooldowns,
                                                        player1)


def player_turn(pInfo, pPokemon, pHealth, pDmg, pCCd, oInfo, oPokemon, oHealth, oDmg, pNum, oNum, skipped, pCd,
                oPlayerNum):
    if pHealth > 0 and not skipped and not (pCCd[0] != 0 and pCCd[1] != 0 and pCCd[2] != 0 and pCCd[3] != 0):
        print(("PLAYER " + pNum).center(50, '-'))
        print("{:>47}".format("P" + oNum + ": " + str(oInfo[oPokemon * 22 + 1])) + "\n" +
              "{:>43}".format("HP: " + "{:>3}".format(str(oHealth))))
        print("{:>22}".format("P" + pNum + ": " + str(pInfo[pPokemon * 22 + 1])) + "\n" +
              "{:>18}".format("HP: " + "{:>3}".format(str(pHealth))))
        print()
        print("{:<30}".format("1. " + pInfo[pPokemon * 22 + 7]), end='')
        print("{:<30}".format("2. " + pInfo[pPokemon * 22 + 11]), end='')
        print("{:<30}".format("3. " + pInfo[pPokemon * 22 + 15]), end='')
        print("{:<30}".format("4. " + pInfo[pPokemon * 22 + 19]))
        k = 0
        for i in range(9, 22, 4):
            if pInfo[pPokemon * 22 + i - 1] == 'Damage':
                print("Dmg: {:<25}".format(pDmg[k]), end='')
            elif pInfo[pPokemon * 22 + i - 1] == 'Skip':
                print("{:<30}".format("Skip opponents move"), end='')
            elif pInfo[pPokemon * 22 + i - 1] == 'Down':
                print("{:<30}".format("Reduce opp dmg by " + str(pInfo[pPokemon * 22 + i])), end='')
            elif pInfo[pPokemon * 22 + i - 1] == 'Up':
                print("{:<30}".format("Increase self dmg by " + str(pInfo[pPokemon * 22 + i])), end='')
            elif pInfo[pPokemon * 22 + i - 1] == 'Heal':
                print("{:<30}".format("Increase health by " + str(pInfo[pPokemon * 22 + i])), end='')
            k += 1
        print()
        print("{:<30}".format("Cooldown: " + str(pCCd[0])), end='')
        print("{:<30}".format("Cooldown: " + str(pCCd[1])), end='')
        print("{:<30}".format("Cooldown: " + str(pCCd[2])), end='')
        print("{:<30}".format("Cooldown: " + str(pCCd[3])))
        print('\n')
        while True:
            pMove = input_int("Select your move:")
            if 1 <= pMove <= 4 and pCCd[pMove - 1] == 0:
                pMoveDmg = pMove - 1
                pMove = 9 if pMove == 1 else 13 if pMove == 2 else 17 if pMove == 3 else 21 if pMove == 4 else 0
                break
            elif not pCCd[pMove - 1] == 0:
                pMove = 9 if pMove == 1 else 13 if pMove == 2 else 17 if pMove == 3 else 21 if pMove == 4 else 0
                print(str(pInfo[pPokemon * 22 + pMove - 2]) + " still has a cooldown of " +
                      str(pCCd[pMove // 4 - 2]))
            else:
                print("Invalid selection")
        print("\n")

        # apply damage and changes from player move
        if pInfo[pPokemon * 22 + pMove - 1] == 'Damage':
            num = randint(0, 100)
            if num < 20:
                print(str(pInfo[pPokemon * 22 + 1]) + " has used " + str(
                    pInfo[pPokemon * 22 + pMove - 2]) + ", but has missed!")
            elif num > 90:
                oHealth -= int(1.2 * (int(pDmg[pMoveDmg])))
                print(str(pInfo[pPokemon * 22 + 1]) + " has used " + str(
                    pInfo[pPokemon * 22 + pMoveDmg - 2]) + ", hitting a CRITICAL HIT for " + str(
                    int(1.2 * (int(pDmg[pMoveDmg])))) + " damage!")
            else:
                oHealth -= int(pDmg[pMoveDmg])
                print(str(pInfo[pPokemon * 22 + 1]) + " has used " + str(
                    pInfo[pPokemon * 22 + pMove - 2]) + ", hitting " + str(
                    oInfo[oPokemon * 22 + 1]) + " for " + str(pDmg[pMoveDmg]) + " damage!")
        elif pInfo[pPokemon * 22 + pMove - 1] == 'Skip':
            skipped = True
            print(str(pInfo[pPokemon * 22 + 1]) + " has used " + str(
                pInfo[pPokemon * 22 + pMove - 2]) + " causing " + str(
                oInfo[oPokemon * 22 + 1]) + " to skip their move!")
        elif pInfo[pPokemon * 22 + pMove - 1] == 'Heal':
            pHealth += int(pInfo[pPokemon * 22 + pMove])
            print(str(pInfo[pPokemon * 22 + 1]) + " has used " + str(
                pInfo[pPokemon * 22 + pMove - 2]) + " increasing their health by " + str(pInfo[pPokemon * 22 + pMove]))
        elif pInfo[pPokemon * 22 + pMove - 1] == 'Down':
            for i in range(len(oDmg)):
                oDmg[i] -= int(pInfo[pPokemon * 22 + pMove])
                if oDmg[i] <= 5:
                    oDmg[i] = 5
            print(str(pInfo[pPokemon * 22 + 1]) + " has used " + str(
                pInfo[pPokemon * 22 + pMove - 2]) + " taking " + str(
                pInfo[pPokemon * 22 + pMove]) + " damage from all of " + str(
                oInfo[oPokemon * 22 + 1]) + "\'s moves!")
        elif pInfo[pPokemon * 18 + pMove - 1] == 'Up':
            for i in range(len(pDmg)):
                pDmg[i] += int(pInfo[pPokemon * 22 + pMove])
            print(
                str(pInfo[pPokemon * 22 + 1]) + " has used " + str(pInfo[pPokemon * 22 + pMove - 2]) + " adding " + str(
                    pInfo[pPokemon * 22 + pMove]) + " damage to all of their moves!")
        pMove = 1 if pMove == 9 else 2 if pMove == 13 else 3 if pMove == 17 else 4 if pMove == 21 else 0
        for move in range(len(pCCd)):
            if move == pMove - 1:
                pCCd[pMove - 1] = pCd[pMove - 1]
            elif not pCCd[move] <= 0:
                pCCd[move] -= 1
    elif pHealth < 0:
        print("Player " + str(oNum) + " and " + str(oInfo[oPokemon * 22 + 1]) + " have won the fight!")
        update_candies(oPlayerNum, 10)
        print("Player " + str(oNum) + " has been awarded 10 candies!")
        main_menu()
    elif pCCd[0] != 0 and pCCd[1] != 0 and pCCd[2] != 0 and pCCd[3] != 0:
        print('\n' + str(pInfo[pPokemon * 22 + 1]) + " has no moves ready and has been skipped!")
        for move in range(len(pCCd)):
            if not pCCd[move] <= 0:
                pCCd[move] -= 1
    else:
        skipped = False
    return [pInfo, pPokemon, pHealth, pDmg, pCCd, oInfo, oPokemon, oHealth, oDmg, skipped]


# --- get csv data --- #
pokemon = csv_to_list('PokeList_v2.csv')
moves = csv_to_list('PokemonMoves.csv')
moves[0] = 1  # FIXME : correct file item error

# --- setup --- #
players = []
playerPokemon = []
currentPokemon = 0
currentPlayer = input_int("Enter player number:")
playerInfo = open_player(currentPlayer)

# --- main --- #
while True:
    main_menu()
