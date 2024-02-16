number = int(input("Write a number N: "))

sum_of_odd, num_of_even, sum_of_even = 0, 0, 0

if number <= 1:
    print("Enter a number bigger than 1!")
else:
    for num in range(1, number + 1):
        if num % 2 == 1:
            sum_of_odd += num
        else:
            num_of_even += 1
            sum_of_even += num


        
    print(f"Sum of odds: {sum_of_odd}")
    print(f"Average of evens: {sum_of_even / num_of_even}")