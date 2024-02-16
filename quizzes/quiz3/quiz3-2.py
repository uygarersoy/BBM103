import sys

list_of_numbers  = sorted([int(i) for i in sys.argv[1].split(",")])

start = 1
number = list_of_numbers[start]

while number < len(list_of_numbers):
    del(list_of_numbers[number - 1::number])
    
    print(" ".join(str(i) for i in list_of_numbers))

    if number in list_of_numbers:
        start += 1
        number = list_of_numbers[start]
    else:
        number = list_of_numbers[start]   