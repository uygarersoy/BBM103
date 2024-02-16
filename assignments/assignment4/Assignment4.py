
import sys

#reads inputs from the files that have been as command line arguments
def read_file(input_file):
    lines = []
    with open(input_file, "r") as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines
#create a table that shows the current attack, player, state of player grids, grid info and round number
def print_table(grid1, grid2, count, player, shot_index):
    #set the header for each table printing
    header = f"Player{player}'s Move\n\nRound : {count+1}\t\t\t\t\tGrid Size : 10x10\n\n"


    info = "Player1's Hidden Board\t\tPLayer2's Hidden Board\n"
    column_names = "ABCDEFGHIJ"
    #combine header, info, and column_names with appropriate spacing  
    table = header + info + "  " + " ".join(column_names) + "\t\t  " + " ".join(column_names) + "\n"

    #loop over the range of column length of grids and print concatenate them to table variable with suitable spacing
    for index in range(1,11):
        if index < 10:
            table += str(index) + " " + " ".join(grid1[index-1]) + "\t\t" + str(index) + " " + " ".join(grid2[index-1]) + "\n"
        else:
            table += str(index) + " ".join(grid1[index-1]) + "\t\t" + str(index) + " ".join(grid2[index-1]) + "\n\n"
    #add current state of ships to table variable
    table += ship_state() + "\n"
    #according to the current player, extract their next attack position from player1_shots
    if player == 1:
        table += f"Enter your move: {player1_shots[shot_index]}\n\n"
    else:
        table += f"Enter your move: {player2_shots[shot_index]}\n\n"
    #append the table string to file_messages list for further printing and writing to a file or console
    file_messages.append(table)

#places ships to table for each player
def place_ships(ships):
    #create a 10X10 empty matrix using nested lists
    grid = [["-"] * 10 for i in range(10)] 
    #iterate over each line of ship placement for each given player
    for index, placement in enumerate(ships):
        #iterate over each row of the ship placement
        for i in range(len(placement)):
            #if the value at the current position is not ';' character, place the ship at the given position accordingly
            if placement[i] != ";":
                grid[index][placement[:i].count(";")] = placement[i]
    #return grid with positioned ships
    return grid

#initiate the attack and guessing of each player against each other
def play():
    #set round_count, count1, and count2 variables to zero initially
    #round_count represents round number, count1 and count2 will retrieve information from
    #their shot selections continuously if they enter invalid attack positions
    round_count = 0
    count1 = 0
    count2 = 0
    #as long as each player have shots left to attack, keep the game going
    while count1 < len(player1_shots) and count2 < len(player2_shots):
        
        while True:
            try:
                #get the attack of first player. check if the index of the shot is in the correct range in shots list 
                if count1 < len(player1_shots):
                    shot_positions = player1_shots[count1]
                else:
                    break
                #check if it is valid or not
                is_index = index_error(shot_positions)
                #if not raise an IndexError to indicate the absence of row or column value (or both)
                if is_index != 0:
                    raise IndexError(is_index)
                shot_positions = shot_positions.split(",")
                #check if the given operands are interpretable or not. If not raise a ValueError
                is_value = value_error(shot_positions)
                if is_value != 0:
                    raise ValueError(is_value)
                #extract row and column
                row, column = int(shot_positions[0]) - 1, shot_positions[1]
                #check if the values of row and column are in the suitable range. If not raise an AssertionError
                assert row < 10 and column in columns
                column = columns[column]
            #if ValueError got caught, print table with informative message and increment count1 by 1 to keep reading
            except ValueError as err:
                print_table(player1_hidden, player2_hidden, round_count, 1, count1)
                file_messages.append(str(err))
                count1 += 1
            #if IndexError got caught, print table with informative message and increment count1 by 1 to keep reading            
            except IndexError as err:
                print_table(player1_hidden, player2_hidden, round_count, 1, count1)
                file_messages.append(str(err))
                count1 += 1
            #if AssertionError got caught, print table with informative message and increment count1 by 1 to keep reading
            except AssertionError:
                message = "AssertionError: Invalid Operation.\n\n"
                print_table(player1_hidden, player2_hidden, round_count, 1, count1)
                file_messages.append(message)
                count1 += 1
            #if anything unexpected happens, print a message to both console and file and exit the program
            except:
                message = "kaBOOM: run for your life!"
                file_messages.append(message)
                final_output = "".join(line for line in file_messages)
                write_file(output_file, final_output)
                print(final_output)
                sys.exit(1)
            #if no exception is happened, check if the attack was a hit or a miss and update the oppent's grid
            else:
                #if attack is successful, print the table of current situtation and increment count1 by 1
                print_table(player1_hidden, player2_hidden, round_count, 1, count1)
                count1 += 1
                if player2_table[row][column] != "-":
                    player2_hidden[row][column] = "X"
                else:
                    player2_hidden[row][column] = "O"
                #break from while loop for opponent to attack
                break
        #check if the ships are sunk or alive at the end of each attack
        if ships2["Carrier"] != "X":
            check_single_ships(player2_table, player2_hidden, 2, "Carrier", 5)
        if ships2["Destroyer"] != "X":
            check_single_ships(player2_table, player2_hidden, 2, "Destroyer", 3)
        if ships2["Submarine"] != "X":
            check_single_ships(player2_table, player2_hidden, 2, "Submarine", 3)
        if ships2["Battleship"] != "X X":
            check_multiple_ships("Battleship", 2, 4)
        if ships2["Patrol Boat"] != "X X X X":
            check_multiple_ships("Patrol Boat", 2, 2)
          
        
        while True:
            try:
                #get the attack of second player. check if the index of the shot is in the correct range in shots list
                if count2 < len(player2_shots):
                    shot_positions = player2_shots[count2]
                else:
                    break
                #check if it is valid or not
                is_index = index_error(shot_positions)
                #if not raise an IndexError to indicate the absence of row or column value (or both)
                if is_index != 0:
                    raise IndexError(is_index)
                shot_positions = shot_positions.split(",")
                #check if the given operands are interpretable or not. If not raise a ValueError
                is_value = value_error(shot_positions)
                if is_value != 0:
                    raise ValueError(is_value)
                #extract row and column. apply required optimization to them
                row, column = int(shot_positions[0]) - 1, shot_positions[1]
                #check if the values of row and column are in the suitable range. If not raise an AssertionError
                assert row < 10 and column in columns
                #extract integer value from dictionary
                column = columns[column]
            #if ValueError got caught, print table with informative message and increment count2 by 1 to keep reading
            except ValueError as err:
                print_table(player1_hidden, player2_hidden, round_count, 2, count2)
                file_messages.append(str(err))
                count2 += 1
            #if IndexError got caught, print table with informative message and increment count2 by 1 to keep reading
            except IndexError as err:
                print_table(player1_hidden, player2_hidden, round_count, 2, count2)
                file_messages.append(str(err))
                count2 += 1
            #if AssertionError got caught, print table with informative message and increment count2 by 1 to keep reading
            except AssertionError:
                message = "AssertionError: Invalid Operation.\n\n"
                print_table(player1_hidden, player2_hidden, round_count, 2, count2)
                file_messages.append(message)
                count2 += 1
            #if anything unexpected happens, print a message to both console and file and exit the program
            except:
                message = "kaBOOM: run for your life!"
                file_messages.append(message)
                final_output = "".join(line for line in file_messages)
                write_file(output_file, final_output)
                print(final_output)
                sys.exit(1)
            #if no exception is happened, check if the attack was a hit or a miss and update the oppent's grid   
            else: 
                #if attack is successful, print the table of current situtation and increment count2 by 1
                print_table(player1_hidden, player2_hidden, round_count, 2, count2)
                count2 += 1
                if player1_table[row][column] != "-":
                    player1_hidden[row][column] = "X"
                else:
                    player1_hidden[row][column] = "O"
                #break from while loop for opponent to attack
                break
        #check if the ships are sunk or alive at the end of each attack
        if ships1["Carrier"] != "X":
            check_single_ships(player1_table, player1_hidden, 1, "Carrier", 5)
        if ships1["Destroyer"] != "X":
            check_single_ships(player1_table, player1_hidden, 1, "Destroyer", 3)
        if ships1["Submarine"] != "X":
            check_single_ships(player1_table, player1_hidden, 1, "Submarine", 3)
        if ships1["Battleship"] != "X X":
            check_multiple_ships("Battleship", 1, 4)  
        if ships1["Patrol Boat"] != "X X X X":
            check_multiple_ships("Patrol Boat", 1, 2)
        #at the end of each round, check if one of the players won the game or not, namely, if their opponents ships are all sunk
        result = is_won(player1_hidden, player2_hidden)
        #if one of them has won, append a message to file_messages and finish the game
        if result != None:
            file_messages.append(f"{result}\n\n")
            break
        #update round_count by 1 at the end of each round if the game still is on
        round_count += 1

#check if any of two players has won the game
def is_won(player1_grid, player2_grid):
    #convert each position form respective grid of players into single string 
    positions1 = "".join(column for row in player1_grid for column in row)
    positions2 = "".join(column for row in player2_grid for column in row)
    #count the number of ship parts that have been hit
    player1_count = positions1.count("X")
    player2_count = positions2.count("X")
    #if total number equal to 27 for any of them or both of them, return the following messages
    if player1_count == 27 and player2_count != 27:
        return "Player2 Wins!"
    elif player1_count != 27 and player2_count == 27:
        return "Player1 Wins!"
    elif player1_count == 27 and player2_count == 27:
        return "It is a Draw!"
#print the final state of the grids after the game has ended
def final_tables(player1_grid, player2_grid):
    #iterate over the original grid that contains ship placements
    for row in range(10):
        for column in range(10):
            #if the position at the original one contains a ship part and target grid has this part as unhit
            #update the target grid by changing "-" to respective symbol of the ship part for both of players
            if player1_table[row][column] != "-" and player1_grid[row][column] == "-":
                player1_grid[row][column] = player1_table[row][column]

            if player2_table[row][column] != "-" and player2_grid[row][column] == "-":
                player2_grid[row][column] = player2_table[row][column]
    #set the heading and information about the table for final results
    table = "Final Information\n\n" + "Player1's Board\t\t\t\tPLayer2's Board\n"
    table += "  " + " ".join("ABCDEFGHIJ") + "\t\t  " + " ".join("ABCDEFGHIJ") + "\n"
    #iterate over columns and concatenate table with grid parts and suitable spacing
    for index in range(1,11):
        if index < 10:
            table += str(index) + " " + " ".join(player1_grid[index-1]) + "\t\t" + str(index) + " " + " ".join(player2_grid[index-1]) + "\n"
        else:
            table += str(index) + " ".join(player1_grid[index-1]) + "\t\t" + str(index) + " ".join(player2_grid[index-1]) + "\n"
    #append the resultant table to file_messages for further printing and writing operations
    file_messages.append(table + "\n" + ship_state())

#get the ship states of each player for the state of being sunk or alive for each ship
def ship_state():
    state = ""
    state += f"Carrier\t\t{ships1['Carrier']}\t\t\t\tCarrier\t\t{ships2['Carrier']}\n"
    state += f"Battleship\t{ships1['Battleship']}\t\t\t\tBattleship\t{ships2['Battleship']}\n"
    state += f"Destroyer\t{ships1['Destroyer']}\t\t\t\tDestroyer\t{ships2['Destroyer']}\n"
    state += f"Submarine\t{ships1['Submarine']}\t\t\t\tSubmarine\t{ships2['Submarine']}\n"
    state += f"Patrol Boat\t{ships1['Patrol Boat']}\t\t\tPatrol Boat\t{ships2['Patrol Boat']}\n"
    return state

#check if the given ship for given player is sunk, aka, got hitten from its all part
def check_single_ships(player_grid, player_grid_hidden, player, ship, length):
    #set count to zero to check the ship has been hit completely
    count = 0
    #iterate over grid
    for row in range(10):
        for column in range(10):
            #if the respective position contains the given ship and at that position, if the ship took a shot, increment count
            if player_grid[row][column] == ship[0] and player_grid_hidden[row][column] == "X" :
                count += 1
    #update the state of ship to sunk if hit count is equal to lenght of the ship for given player
    if player == 1:
        if length == count:
            ships1[ship] = "X"
    if player == 2:
        if length == count:
            ships2[ship] = "X"
#extract the positions of battleship and patrol ships
def battleship_and_patrol_positions(positions, player):

    #set the general variables according to the given player
    if player == 1:
        battleship = battleship_positions1
        patrol_boat = patrol_positions1

    if player == 2:
        battleship = battleship_positions2
        patrol_boat = patrol_positions2

    #iterate over the lines of input file
    for position in positions:
        position = position.split(";")
        #extract the row and column information from each line
        row = int(position[0].split(":")[-1].split(",")[0]) - 1
        column = "ABCDEFGHIJ".index(position[0].split(":")[-1][-1])
        #if the ship continues to the right, append its starting row and column values and add a boolean value for further usage
        #if the ship continues to downward, add rows according to the length of the ship as a list and the column value
        #to the list with boolean value at the end
        if position[-1] == "right" and position[0][0] == "B":
            battleship.append([row, column, True])
        if position[-1] == "down" and position[0][0] == "B":
            battleship.append([[row, row + 1, row + 2, row + 3], column, True])
        if position[-1] == "right" and position[0][0] == "P":
            patrol_boat.append([row, column, True])
        if position[-1] == "down" and position[0][0] == "P":
            patrol_boat.append([[row, row + 1], column, True])

#check if the battleships and patrol boats are sunk or not
def check_multiple_ships(ship, player, length):
    #set the general variables according to given player
    if player == 1:
        battleship = battleship_positions1
        hidden = player1_hidden
        ships_ = ships1
        patrol_boat = patrol_positions1
    
    if player == 2:
        battleship = battleship_positions2
        hidden = player2_hidden
        ships_ = ships2
        patrol_boat = patrol_positions2
    
    if ship[0] == "B":
        main_ship = battleship

    if ship[0] == "P":
        main_ship = patrol_boat

    #iterate over ship positions that have been obtained from battleship_and_patrol_positions function
    for position in main_ship:
        #set count to compare the state of sinkage of a ship
        count = 0
        #if first argument is a list, this means the ship goes downward
        #if boolean value is True, that means the ship was swimming before last check
        if type(position[0]) == list and position[-1] != False:
            #iterate over ship parts and update the count if a part of the sink has been hit
            for row in position[0]:
                if hidden[row][position[1]] == "X":
                    count += 1
            #if count is equal to the length of the ship, that means the ship has been sunk
            if count == length:
                #update the swimming state of the ship to sunk by replacing "-" with "X"
                if "-" in ships_[ship]:
                    place = ships_[ship].index("-")
                    ships_[ship] = ships_[ship][:place] + "X" + ships_[ship][place + 1:]
                #update the boolean to False to indicate that the ship is not swimming anymore
                position[-1] = False
        #if the first argument is an int, that means the ship is going right direction
        elif type(position[0]) == int and position[-1] != False:
            #iterate over ship parts and update the count if a part of the sink has been hit
            for column in range(position[1], position[1] + length):
                if hidden[position[0]][column] == "X":
                    count += 1
            #if count is equal to the length of the ship, that means the ship has been sunk
            if count == length:
                #update the swimming state of the ship to sunk by replacing "-" with "X"
                if "-" in ships_[ship]:
                    place = ships_[ship].index("-")
                    ships_[ship] = ships_[ship][:place] + "X" + ships_[ship][place + 1:]
                #update the boolean to False to indicate that the ship is not swimming anymore
                position[-1] = False
#write messages to the ouput file
def write_file(output_file, message):
    with open(output_file, "w") as out:
        out.write(message)
#check if the given command line arguments are valid to process or not
def io_error():
    #iterate over the command line arguments
    index = 1
    while index < 5:
        #try to open them
        try:        
            with open(sys.argv[index], "r") as inp:
                pass
        #if index error is caught, that means at least one of the file is missing at the command line as an argument
        except IndexError:
            #print the message to console and output file and terminate the program
            message = "IndexError: Less command line argument than expected.\nUsage: python3 Assignment4.py Player1.txt Player2.txt Player1.in Player2.in"
            print(message)
            write_file(output_file, message)
            sys.exit(1)
        #if FileNotFoundError is found, the file can't be processed for some reason. append the file name to fails list
        except FileNotFoundError:
                fails.append(sys.argv[index])
        index += 1
    #if fails list contains more than 1 file name, print a message to console and file. afterwards terminate the program
    if len(fails) > 1:
        message = f"IOError: input files {', '.join(file_name for file_name in fails)} are not reachable."
        print(message)
        write_file(output_file, message)
        sys.exit(1)
    #if only 1 file failed to open, print a message to console and file. then terminate the program
    if len(fails) == 1:
        message = f"IOError: input file {fails[0]} is not reachable."
        print(message)
        write_file(output_file, message)
        sys.exit(1)
#check index error of the shots of the each player
def index_error(shot):
    #evaluate each possible scenario and return a suitable message to caller
    if "," not in shot:
        return f"IndexError: Missing comma to separate possible row and column values! Given value: '{shot}'\n\n"
    elif "" == shot.split(",")[0] and shot.split(",")[1] == "":
        return f"IndexError: Missing row and column values! Given value: '{shot}'\n\n"
    elif "" != shot.split(",")[0] and shot.split(",")[1] == "":
        return f"IndexError: Missing column value! Given value: '{shot}'\n\n"
    elif "" == shot.split(",")[0] and shot.split(",")[1] != "":
        return f"IndexError: Missing row value! Given value: '{shot}'\n\n"
    else:
        return 0
#check if a value eror occurs from shots of the each player
def value_error(positions):
    #if fails list contains more than 1 file name, print a message to console and file. afterwards terminate the program
    if len(positions) > 2:
        return f"ValueError: Too many values were given as rows and columns! Given input: '{' '.join(pos for pos in positions)}'\n\n"
    elif positions[0] in "12345678910" and positions[1] in "12345678910":
        return f"ValueError: Invalid column value: Given value: '{' '.join(pos for pos in positions)}'\n\n"
    elif positions[0] in "ABCDEFGHIJ" and positions[1] in "ABCDEFGHIJ":
        return f"ValueError: Invalid row value: Given value: '{' '.join(pos for pos in positions)}'\n\n"
    elif positions[0] in "ABCDEFGHIJ" and positions[1] in "12345678910":
        return f"ValueError: Invalid row and column values: Given value: '{' '.join(pos for pos in positions)}'\n\n"
    else:
        return 0
#check possible overlap scenario in ship positioning of each player
def check_overlap_and_correctness(positions, player):
    #iterate over their ship positioning
    for pos in positions:
        #extract each square
        pos = pos.split(";")
        #iterate over each square
        for square in pos:
            #if any oen of the squares have length greater than 1, this means possible overlaping scenario
            if len(square) > 1:
                #check if any of the characters are unknown and print a message accordingly. raise an error afterwards
                if not set(square).issubset(set("PBSCD")):
                    message = f"There is multiple characters to represent singular ship. Possible overlap and unidentified character: '{square}' at Player{player}.txt"
                else:
                    message = f"There is multiple characters to represent singular ship. Possible overlap: '{square}' at Player{player}.txt"
                raise Exception(message)
            #check if the current character is unknown to represent given ships. If so, raise an error
            else:
                char = "PBSCD"
                if square not in char and square != "":
                    message = f"Unidentified character is found: '{square}' at Player{player}.txt"
                    raise Exception(message)

#create a list called fails to hold the file names of possible failed file's from trying to open them
fails = []
#set the output name of the file
output_file = "Battleship.out"
#check firstly the correctness of the files. If no problem occurs continue, else terminate the program
io_error()
#try possible overlap situation in each ship positioning
try:
    check_overlap_and_correctness(read_file(sys.argv[1]), 1)
    check_overlap_and_correctness(read_file(sys.argv[2]), 2)
#if overlap occurs in one of the files, print a message to console and file. Then quit the program
except Exception as err:
    print(f"kaBOOM: run for your life! {err}")
    write_file(output_file, f"kaBOOM: run for your life! {err}")
    sys.exit(1)
#if placing of ships goes smoothly, continue with the process to kick-start the game of battleship
else:
    #obtain ship placements and shots selection of each player
    player1_table = place_ships(read_file(sys.argv[1]))
    player2_table = place_ships(read_file(sys.argv[2]))
    player1_shots = read_file(sys.argv[3])[0].split(";")[:-1]
    player2_shots = read_file(sys.argv[4])[0].split(";")[:-1]


    #create empty grids to hold the information of each attack
    player1_hidden = [["-"] * 10 for i in range(10)]
    player2_hidden = [["-"] * 10 for i in range(10)]
    #set the welcoming message of the game
    message = "Battle of Ships Game\n\n"
    #initialize the list to hold the all outcomes of each operation
    file_messages = [message]
    #get the ship positions of battleship and patrol boats 
    player1_optional = [position[:-1] for position in read_file("OptionalPlayer1.txt")]
    player2_optional = [position[:-1] for position in read_file("OptionalPlayer2.txt")]

    #initialize empty list to hold the row and column informaiton of battleships and patrol boats
    battleship_positions1 = []
    battleship_positions2 = []

    patrol_positions1 = []
    patrol_positions2 = []

    #set the column names as following and put values as following to make indexing easier
    columns = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "G": 6,
        "H": 7,
        "I": 8,
        "J": 9
    }
    #initialize dictionaries to hold the state of ships for each player
    ships1 = {
        "Carrier": "-",
        "Battleship": "- -",
        "Destroyer": "-",
        "Submarine": "-",
        "Patrol Boat": "- - - -"
    }

    ships2 = {
        "Carrier": "-",
        "Battleship": "- -",
        "Destroyer": "-",
        "Submarine": "-",
        "Patrol Boat": "- - - -"
    }

    #extract the row and column info of battleships and patrol boats
    battleship_and_patrol_positions(player1_optional, 1)
    battleship_and_patrol_positions(player2_optional, 2)
    #initialize the guessing and attacking process of each player against each other
    play()
    #after one of them won, or a possible draw, print the final state of grids of each player
    final_tables(player1_hidden, player2_hidden)
    #get rid of the new line charachter at the end of the final message in file_messages
    file_messages[-1] = file_messages[-1].strip("\n")
    #create a final string to hold all of the outcomes of all processes that happened
    final_message = "".join(line for line in file_messages)
    #write the final_message to both console and file
    write_file(output_file, final_message)
    print(final_message)
