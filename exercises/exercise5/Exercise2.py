my_list = input("My list: ").split(",")
nth_largest = int(input("nth largest element: "))
number = sorted(my_list, reverse=True)[nth_largest-1]
print(number.strip(" "))