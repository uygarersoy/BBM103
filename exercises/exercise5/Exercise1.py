number = int(input("Enter the number N value: "))
dictionary = {i : ["*"] * i for i in range(1, number + 1)}
print(dictionary)