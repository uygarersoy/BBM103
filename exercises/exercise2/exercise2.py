number = int(input("Enter a number: "))

check = abs(number)
binary_repr = ""

while True:
    if check == 0:
        binary_repr += "0"
        break
    else:
        binary_repr += str(check % 2)
        check = check // 2
if number >= 0:
    print(binary_repr[::-1])
else:
    print("-" + binary_repr[::-1])