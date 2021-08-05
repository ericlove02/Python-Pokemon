# --- imports --- #
# from random import randint  import randint to be used as rng
# from math import sqrt       import sqrt to be used in CP calculations

# --- functions --- #


def pokemon_catch():
    """takes no parameters, runs mini game asking looping for guesses input and comparing to random number, if the
    number was guessed in the amount of given tries, add_pokemon() is called and adds to collection, then main_menu(),
    else main_menu() is called to return to main menu with no change"""
    pass


def level_up(lvl):
    """takes in selected pokemon current level, determines if player has the amount of candies needed to level up, adds
    to levels and and CP, rewrites players csv file with new pokemon data. returns to pokemon info screen"""
    pass


def pokemon_battle():
    """takes no parameters, takes user input on which player they would like to fight, shows opponents pokemon options,
    takes input on which pokemon they would like to fight, calculated odds to win based on each pokemons CP level,
    picks random number and decides winner if num is within odds. if player wins, candies are awarded. returns to
    main_menu()"""
    pass


def main_menu():
    """takes no parameters, prints menu options for the user, takes input on which option user would like, calls
    function based on each option"""
    pass


def display_selection_menu():
    """takes no parameters, display current pokemon and grid view of all players pokemon using display_pokemon(), allows
    user to select a new pokemon to be the current pokemon"""
    pass


def display_pokemon_info():
    """prints out current pokemon's info, gives player menu options to level up, view moves, select different pokemon,
    or exit to main menu. calls corresponding function based on selection"""
    pass


def more_pokemon_info():
    """prints out current pokemon and a grid of its moves, including move names, damage or effect, and cooldown. take
    enter as input to return to display_pokemon_info()"""
    pass


def open_player(pl):
    """takes in player number, tries to open csv file for the player, excepts FileExistsError and returns file, else add_
    pokemon() to new players list, create file for candies if not FileExistsError, set playerInfo to csv_to_list() of
    new player list, print welcome message with given pokemon name"""
    pass
    # return csv_to_list(playerNumberCSVFile)


def csv_to_list(file):
    """takes in a csv file, converts the csv into a list, returns list with csv contents as strings"""
    pass
    # return list


def list_to_csv(listInfo, file, write='a'):
    """takes in a list, a target file, and whether to append or write over, breaks up the contents of the list and
    APPENDS or WRITES OVER them to the target file"""
    pass


def update_candies(pl, change):
    """takes in the current player and the amount of change to the candies, opens player candy file, adds change
     to candies and rewrites file"""
    pass


def get_candies(pl):
    """takes in the current player, opens player candy file and reads number of candies, returns the amount of candies
    written in file"""
    pass
    # return candies


def input_int(message):
    """take in a input message, tries to take a value as an int, excpets ValueErrors and asks for an int, repeats until
    value is accepted"""
    pass
    # return valueInput


def add_pokemon():
    """randomly select a pokemon and 4 moves from 'pokemon' and 'moves' lists and APPENDS them to the players file"""
    pass


def display_pokemon(playerList):
    """takes in players list of pokemon, tries to loop through list until IndexError is thrown, prints out pokemon in
    grid with 4 pokemon per row, and Empty slots in last row if number of pokemon not divisible by 4"""
    pass


def pvp():
    """runs player vs player pokemon battle using players moves and cp found in player csv files"""
    pass


def player_turn(pInfo, pPokemon, pHealth, pDmg, pCCd, oInfo, oPokemon, oHealth, oDmg, pNum, oNum, skipped, pCd,
                oPlayerNum):
    """take in all the information for a player to make their move, adjust information based on the move used and
    returns"""
    pass
    # return [pInfo, pPokemon, pHealth, pDmg, pCCd, oInfo, oPokemon, oHealth, oDmg, skipped]


# --- get csv data --- #
# pokemon = csv_to_list('PokeList_v2.csv')  # get pokemon data from csv to list
# moves = csv_to_list('PokemonMoves.csv')  # get pokemon move data from csv to list

# --- setup --- #
# set up vars needs for player data
# currentPlayer = input_int("Enter player number:")  # get the current player account number
# playerInfo = open_player(currentPlayer)  # open the players csv and candies files and create usable lists

# --- main --- #
# while True:
#     main_menu()  # infinitely run the main menu until exit() is called in save and exit option
