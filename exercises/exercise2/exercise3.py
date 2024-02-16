b = int(input("Enter a number: "))
c = int(input("Enter a number: "))

delta = b**2 - 4 * c

if delta < 0:
    print("There are no real roots to this equation.")
else:
    print(f"First root is: {(-b + delta**0.5) / 2}")
    print(f"Second root is: {(-b - delta**0.5) / 2}")