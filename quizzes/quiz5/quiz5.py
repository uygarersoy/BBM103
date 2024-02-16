
import sys

#define a function to round a given float number to nearest integer
def round_to_nearest(number):
    return int(float(number) + 1) if float(number) - int(float(number)) >= 0.5 else int(float(number))

#try to extract files from command line
try:
    operator_file = sys.argv[1]
    compare_file = sys.argv[2]
    #define list to hold the content of operand file and comparison data file
    operator_lines = []
    compare_lines = []
    
    #open operand file and iterate through each line
    #strip possible whitespaces at the end of the line and get rid of the new line character
    #append each line to a list
    with open(operator_file, "r") as opr:
        for line in opr:
            operator_lines.append(line.strip().strip("\n"))
    #open comparison data and iterate through each line. get rid of new line character at the end
    #append each line to a list
    with open(compare_file, "r") as comp:
        for line in comp:
            compare_lines.append(line.strip("\n"))
#if command line argument is missing raise an error an print a message accordingly
except IndexError:
    print("IndexError: number of input files less than expected.")
#if file cannot be opened for some reason, raise an error and print a message accordingly
#extract the file name from error message and add to error message
except IOError as error:
    error = str(error)
    start_index = error.index("'")
    print(f"IOError: cannot open {error[start_index + 1:-1]}")
#if no error is caught then process accordingly
else:
    #create a variable for iterating over the operands line
    index = 0
    #iterate throughout each line in the operand lines in operator_list
    while index < len(operator_lines):
        #try to execute the desired operations on the operands line
        try:
            #print a separater
            print("-" * 12)
            #create given_input to hold the information of operands as input 
            given_input = operator_lines[index]
            #round numbers in operands to nearest integer and store in a list
            operands = [round_to_nearest(i) for i in operator_lines[index].split(" ")]
            #calculate results by checking divisibility with first item in the operands
            #and non-divisibility with second item in the range between third and fourth item (inclusive)
            result = [str(number) for number in range(operands[2], operands[3] + 1) if number % operands[0] == 0 and number % operands[1] != 0]
            
            #store results in a string
            string_result = " ".join(i for i in result)
            #store results from compare_data file to check equality
            string_compare_result = " ".join(i for i in compare_lines[index].split())
            #print my results and results to compare
            print(f"My Results:\t\t  {string_result}")
            print(f"Results to Compare:\t  {string_compare_result}")
            #assert an expression between calculated results and given results in compare_data files
            assert  [i for i in compare_lines[index].split()] == result
            #if no error related with assertion occured print Goool!!!
            print("Goool!!!") 
        #if non-numeric value is found in operands raise a ValuError and print a message    
        except ValueError:
            print("ValueError: only numeric input is accepted.")
            print(f"Given input: {given_input}")
        #if number of operands is less than 4, raise an IndexError and print a message
        except IndexError:
            print("IndexError: number of operands less than expected.")
            print(f"Given input: {given_input}")
        #if 0 is given as a denominator raise a ZeroDivisionError and print a message
        except ZeroDivisionError:
            print("ZeroDivisionError: You can't divide by 0.")
            print(f"Given input: {given_input}")
        #if assertion expression fails, raise an error and print a message
        except AssertionError:
            print("AssertionError: results don't match.")
        #if an unexpected error occurs, print the following message and raise and error
        except:
            print("kaBOOM: run for your life!")
        #update the index by 1 at each iteration
        index += 1
#at the end of the program, print Game Error and exit the program
finally:
    print("˜ Game Over ˜")