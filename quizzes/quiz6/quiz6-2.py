import sys
try:
    #check the argument validity
    number = int(sys.argv[1])
    assert number >= 0
    #get the max possible number of stars
    max_val = 2 * number - 1
    #using list comprehension, form the upper body of the pattern
    result1 = [((max_val - (2 * i - 1)) // 2) * " " + ((2 * i) - 1) * "*" + ((max_val - (2 * i - 1)) // 2) * " " for i in range(1, number + 1)]
    #using list comprehension, form the bottom part of the pattern
    result2 = [((max_val - (2 * i - 1)) // 2) * " " + ((2 * i) - 1) * "*" + ((max_val - (2 * i - 1)) // 2) * " " for i in range(number -1, 0, -1)]
    #check if there is a pattern to print
    if len(result1 + result2) == 0:
        pass
    else:
        #print the complete pattern as a whole using join expression
        print("\n".join(i for i in result1 + result2))
except:
    #if given argument is invalid, print a message
    print("Given argument is not an integer or a negative integer")