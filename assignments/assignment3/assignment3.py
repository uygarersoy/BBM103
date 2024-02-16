

#import sys to extract command line arguments, and string to obtain all uppercase letters in Eglish alphabet
import sys
import string
#define a function to read lines from a file, with given parameters as the name of the input file
def read_file(input_file):

    #open the file in "r" mode to be able to read it
    with open(input_file, "r") as input_file:        
        #iterate over each line in the file
        for line in input_file:
            #get rid of the new line character by replacing it with empty string and strip any whitespaces
            #and split the line by " " character to process it in the future
            #this results with a list containing command name and its arguments
            command = line.strip().replace("\n", "").split(" ")
            
            #check if the first item in command list is 'CREATECATEGORY' or not
            if "CREATECATEGORY" == command[0]:
                #extract the category name
                category_name = command[1]
                #split the last item in the list by 'x' character to extract row and column numbers
                number_of_rows, number_of_columns = command[-1].split("x")
                
                #check if category name is suitable or not
                if category_name[:10] not in ["category-1", "category-2"]:
                    #if not append a message to the output_lines list
                    output_lines.append(f"Error: The category name '{category_name}' is not a suitable category name.\n")
                    
                #check if given row number is greater than the number of letters in the alphabet
                elif int(number_of_rows) > 26:
                    #if so, append a message to the output_lines list
                    output_lines.append(f"Error: The given row number {number_of_rows} is bigger than maximum available row number 26.\n")
                    
                else:
                    #if no error found above, call create_category function to process the data           
                    create_category(category_name, number_of_rows, number_of_columns)
            #check if the first item in the command list is equal to 'SELLTICKET' or not
            elif "SELLTICKET" == command[0]:
                #extract customer name and ticket type from command list and turn them to lowercase
                customer = command[1].lower()
                ticket_type = command[2].lower()
                #extract category name and possible seat arguments
                category_name = command[3]
                seats = command[4:]
                #check if the given arguments has the minimum number
                #SELLTICKET customer_name full|student|season category_name seat* <- at least 1 command name and 4 arguments
                if len(command) < 5:
                    #if it has less command argument append a message to the output_lines list
                    output_lines.append(f"Error: Missing command arguments in SELLTICKET command.\n")
                    
                #check if the category name exist already
                elif category_name not in categories.keys():
                    #if not, append a message to the output_lines list
                    output_lines.append(f"Error: The category {category_name} does not exist to sell tickets.\n")
                #check if the given ticket type is an allowed ticket type
                elif ticket_type not in ["student", "season", "full"]:
                    #if not, append a message to the output_lines list
                    output_lines.append(f"Error: Incorrect type of ticket.\n")
                else:
                    #if no error found above, call sell_ticket function with suitable parameters to process them
                    sell_ticket(customer, ticket_type, category_name, seats)
            
            #check if the first item in the command list is equal to 'CANCELTICKET' or not
            elif "CANCELTICKET" == command[0]:
                #extract category name and seats from command list
                category_name = command[1]
                seats = command[2:]
                #check whether or not command list has at least 3 items
                #CANCELTICKET, category_name, seats*
                if len(command) < 3:
                    #if not, append a message to the output_lines list
                    output_lines.append(f"Error: Missing command arguments in CANCELTICKET command.\n")
                #check if the category name already exists
                elif category_name not in categories.keys():
                    #if not append a message to the output_lines list
                    output_lines.append(f"Error: The category '{category_name}' does not exist to cancel tickets.\n")


                else:
                    #if no error has found above,call cancel_ticket function with suitable parameters to process them
                    cancel_ticket(category_name, seats)
            #check if the first item in the command list is equal to "BALANCE" or not
            elif "BALANCE" == command[0]:
                #extract category name
                category_name = command[1]
                #check if the category name already exists
                if category_name not in categories.keys():
                    #if not, append a message to the output_lines list
                    output_lines.append(f"Error: The category '{category_name}' does not exist to show balance.\n")

                else:
                    #if no error found above, call the balance function with suitable paramater to process it
                    balance(category_name)
            #check if the first item in the command list is equal to "SHOWCATEGORY" or not
            elif "SHOWCATEGORY" == command[0]:
                #extract category name from command list
                category_name = command[1]
                #check if category name already exist or not
                if category_name not in categories.keys():
                    #if not, append a message to the output_lines list
                    output_lines.append(f"Error: The category {category_name} does not exist to show current layout of it.\n")
                else:
                    #if no error found above, call show_category function with suitable parameter to process it
                    show_category(category_name)

#define a function to create category with given parameters as category name, number of rows and columns
def create_category(category_name, rows, columns):
    #check if it is already exist or not
    if category_name not in categories.keys():
        #if not, convert rowns and columns to integer values
        row, col = int(rows), int(columns)
        #using string module, extract row names according to the given number of rows by list slicing
        column_name = string.ascii_uppercase[:row]
        #reverse the column_name to make it easier to print in descending order
        seats_name = column_name[::-1]
        #create an empty list to hold all the rows and columns data
        seats = []
        #iterate over the given number of rows
        for index in range(0,row):
            #append to the seats list 2 another list
            #first list is the row name and second one is the seats data, which is given as 'X' to imply it is empty
            #["X"] is multiplied by the number of rows to get the seating right
            seats.append([[seats_name[index]], ["X"]*col])
        #add category name as a key and seats list as a value to global categories dictionary
        categories[category_name] = seats
        #append a message to the output_lines list to indicate process went successful
        output_lines.append(f"The category '{category_name}' having {row * col} seats has been created\n")
    else:
        #category already created before. append a message to the output_lines list
        output_lines.append(f"Warning: Cannot create the category for the second time. The stadium has already {category_name}\n")

#define a function to sell ticket, with given parameters as customer name, ticket type, category name and seats
def sell_ticket(customer, ticket_type, category_name, seats):
    #create a dictionary to hold valid ticket types
    tickets = {
        "student": "S",
        "full": "F",
        "season": "T"
    }
    #iterate over the list of seats
    for seat in seats:
        #check if the seats list contain seats with seat ranges
        if "-" not in seat:
            #if no seat ranges found, check if the row name exist in the given category using string module
            #and length of the given category's row. Also check if the index of the seat exceeds the category's index or not
            #by comparing it the length of the first row in the category
            if seat[0] not in string.ascii_uppercase[:len(categories[category_name])] and int(seat[1:]) >= len(categories[category_name][0][1]):
                #if both exceeds their valid range, append a message to the output_lines list
                output_lines.append(f"Error: The category '{category_name}' has less row and column than the specified index {seat}!\n")
            #check if the row name exist in the given category name and if the given seat number exceeds the allowed range or not
            elif seat[0] not in string.ascii_uppercase[:len(categories[category_name])] and int(seat[1:]) < len(categories[category_name][0][1]):
                #if row name is invalid, and column number is valid, append a message to the output_lines list
                output_lines.append(f"Error: The category '{category_name}' has less row than the specified index {seat}!\n")
            #check if the row name is valid and column number is invalid or not
            elif seat[0] in string.ascii_uppercase[:len(categories[category_name])] and int(seat[1:]) >= len(categories[category_name][0][1]):
                #if so, append a message to the output_lines list
                output_lines.append(f"Error: The category '{category_name}' has less column than the specified index {seat}!\n")
            else:
                #both row name and column number is valid
                #rows are descending order. in string.ascii_uppercase "A" has 0 as its index
                #in descending order it has -1. Implementing the following algorithm outputs the desired row name
                #check if the given seat is empty or not
                if categories[category_name][- 1 * string.ascii_uppercase.index(seat[0]) - 1][1][int(seat[1:])] == "X":
                    #if so, append a message to the output_lines list
                    output_lines.append(f"Success: {customer} has bought {seat} at {category_name}\n")
                    #update the seat status to given ticket type
                    categories[category_name][- 1 * string.ascii_uppercase.index(seat[0]) - 1][1][int(seat[1:])] = tickets[ticket_type]
                else:
                    #if seat is unavailable, append a message to the output_lines list
                    output_lines.append(f"Warning: The seat {seat} cannot be sold to {customer} since it was already sold!\n")
        #seat contains seat ranges
        else:
            #split the given seat by "-" character to obtain the start and end index of the seat
            start, end = seat[1:].split("-")
            #consider the unordered start and end ranges
            start, end = min(int(start), int(end)), max(int(start), int(end))
            #extract row name
            seat_letter = seat[0]
            #check if the rown name is in the given category and if start or end index exceeds the maximum column number
            #by looking the length of the column number of the seating area
            if seat_letter not in string.ascii_uppercase[:len(categories[category_name])] and (start >= len(categories[category_name][0][1]) or end >= len(categories[category_name][0][1])):
                #if both row name and column numbers exceeds their allowed range, append a message to the output_lines list
                output_lines.append(f"Error: category '{category_name}' has less row and column than the specified index {seat}!\n")
            #check if the row name is invalid but seat ranges are valid
            elif seat_letter not in string.ascii_uppercase[:len(categories[category_name])] and not (start >= len(categories[category_name][0][1]) or end >= len(categories[category_name][0][1])):
                #if so, append a message to the output_lines list
                output_lines.append(f"Error: The category '{category_name}' has less row than the specified index {seat}!\n")
            #check if the row name is valid and column numbers are invalid
            elif seat_letter in string.ascii_uppercase[:len(categories[category_name])] and (start >= len(categories[category_name][0][1]) or end >= len(categories[category_name][0][1])):
                #if so, append a message to the output_lines list
                output_lines.append(f"Error: The category '{category_name}' has less column than the specified index {seat}!\n")
            #both row name and column numbers are valid
            else:
                #set the value of count variable to 0
                count = 0
                #iterate over from the start range to end range
                for seat_range in range(start, end + 1):
                    #if the given seat at the given index is empty, add 1 to the value of count
                    if categories[category_name][- 1 * string.ascii_uppercase.index(seat[0]) - 1][1][seat_range] == "X":
                        count += 1
                #if the value of count equal to the total number of seats in the given range, then it means all seats are empty
                if count == end - start + 1:
                    #iterate over the given range to update the values of empty seats to given ticket type
                    for seat_range in range(start, end + 1):
                        categories[category_name][- 1 * string.ascii_uppercase.index(seat[0]) - 1][1][seat_range] = tickets[ticket_type]
                    #append a message to the output_lines list to indicate the process is successful
                    output_lines.append(f"Success: {customer} has bought {seat} at {category_name}\n")

                else:
                    #if the count value is not equal to the given seat range, this means at least 1 seat is unavailable
                    #append a message to the output_lines list to indicate the process is unsuccessful
                    output_lines.append(f"Warning: The seats {seat} cannot be sold to {customer} due some of them have already been sold\n")


#define a function to cancel ticket with given parameters as category name and seats
def cancel_ticket(category_name, seats):
    #iterate over the list of seats
    for seat in seats:
        #check if the row name and column number are invalid or not
        if seat[0] not in string.ascii_uppercase[:len(categories[category_name])] and int(seat[1:]) >= len(categories[category_name][0][1]):
            #if both of them are invalid, append a message to the output_lines list
            output_lines.append(f"Error: The category '{category_name}' has less row and column than the specified index {seat}!\n")
        #check if the row name is invalid and column number is valid
        elif seat[0] not in string.ascii_uppercase[:len(categories[category_name])] and int(seat[1:]) < len(categories[category_name][0][1]):
            #if so, append a message to the output_lines list
            output_lines.append(f"Error: The category '{category_name}' has less row than the specified index {seat}!\n")
        #check if the row name is valid but column number is invalid
        elif seat[0] in string.ascii_uppercase[:len(categories[category_name])] and int(seat[1:]) >= len(categories[category_name][0][1]):
            #if so, append a message to the output_lines list
            output_lines.append(f"Error: The category '{category_name}' has less column than the specified index {seat}!\n")
        #both row name and column number is valid
        else:
            #check if the seat is free or not
            if categories[category_name][- 1 * string.ascii_uppercase.index(seat[0]) - 1][1][int(seat[1:])] == "X":
                #if it is free, append a message to the output_lines list to indicate that the seat is already free
                output_lines.append(f"Error: The seat {seat} at '{category_name}' has already been free! Nothing to cancel\n")
            #seat is not free
            else:
                #append a message to the output_lines list to indicate cancellation is successful
                #update the seat status to "X" to indicate it has been freed
                output_lines.append(f"Success: The seat {seat} at '{category_name}' has been canceled and now ready to sell again\n")
                categories[category_name][- 1 * string.ascii_uppercase.index(seat[0]) - 1][1][int(seat[1:])] = "X"
#define a function to show the balance of the category with given parameters as the category name
def balance(category_name):
    #set the initial values of students, full, and season tickets to 0
    students, full, season = 0, 0, 0
    #iterate over the given category in categories dictionary as category name as a key
    for category in categories[category_name]:
        #iterate over the seats in the given category
        for seats in category[1]:
            #check if the given seat has student, full, or season ticket currently
            #given the situation add to the values of students, full, and season variables by 1
            if seats == "S":
                students += 1
            elif seats == "F":
                full += 1
            elif seats == "T":
                season += 1
    #calculate the total revenue
    revenue = students * 10 + full * 20 + season * 250
    
    #set the headers of the output message as info and dashes
    info = f"category report of '{category_name}'\n"
    dashes = len(info) * "-"
    output = f"Sum of students = {students}, Sum of full pay = {full}, Sum of season ticket = {season}, and Revenues = {revenue} Dollars"
    #combine the values of info and dashes and add a new line.
    #concatenate this with output string and append it to the output_lines list
    output_lines.append(info + dashes + "\n" + output + "\n")

#define a function to show the layout of the given category, with parameters given as the category name
def show_category(category_name):
    #set the initial value of result to empty string
    result = ""
    #iterate over the given category in categories dictionary
    for category in categories[category_name]:
        #concatenate result with the row name of the category
        #add 1 empty space and for each seat, concatenate them to result with 2 empty spaces between them and add a new line
        result += category[0][0] + " " + "  ".join(seat for seat in category[1]) + "\n"

    #for bottom of the categories, iterate over the column number of the given category
    #if column number is less than ten, put 2 empty spaces between them
    #if column number is less than hundred but greater than 10, put 1 empty spaces between them 
    #else convert the column number to string and concatenate with result
    for index in range(len(categories[category_name][0][1])):
        if index < 10:
            result += "  " + str(index)
        elif index < 100:
            result += " " + str(index)
        else:
            result += str(index)
    #add new line character at the end of the result 
    result += "\n"
    #add necessary outline and concatenate it with result
    #append a message to the output_lines list
    message = f"Printing category layout of {category_name}\n"
    output_lines.append(message + result)
#define a function to write the outputs to a .txt file
def write_file(output_file, output_results):
    #print output_results to console
    print(output_results)
    #open the file in write mode to be able to write onto it
    with open(output_file, "w") as out:
        #write output_results to the output file
        out.write(output_results)

#extract the name of the input file from command line using sys.argv
input_file = sys.argv[1]
#set the name of the output file to output_file variable
output_file = "output.txt"
#create a dictionary named categories to hold category names as keys and status of the category as values
categories = {}
#create a list named output_lines to hold the outputs of each operation
output_lines = []
#call read_file function with input file name to kick-start the whole process
read_file(input_file)
#join all elements of the output_lines to a string named final_output
final_output = "".join(line for line in output_lines)
#call write_file function with the outputs and output file name parameters
#to print the output to both console and the file
write_file(output_file, final_output)