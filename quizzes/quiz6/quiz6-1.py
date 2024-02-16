import sys

#if num is equal to zero return 0, else print a pattern with current values and call the function by updating given values
def upper_recursive(num, i=0):
    if num == 0:
        return 0
    else:
        print((num-1) * " " + ((2 * i) + 1) * "*" + (num-1) * " ")
        return upper_recursive(num - 1, i + 1)
#this function will print the result of first n - 1 lines upside down with the same logic
def bottom_recursive(num, i=1):
    if num <= 0:
        return 0
    else:
        print(i * " " + ((2 * num) - 1) * "*" + i * " ")
        return bottom_recursive(num - 1, i+1)

try:
    #check argument validity and call functions if no exceptions occur
    num = int(sys.argv[1])
    assert num >= 0
    upper_recursive(num)
    bottom_recursive(num-1)
except:
    #if an exception occurs, print a message about it
    print("Given argument is not an integer or a negative integer")