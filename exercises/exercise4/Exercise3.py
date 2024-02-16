import random

number = random.randint(1,50)

print("Guess a number between 1 and 50")
guess = int(input("Please enter a number: "))

while True:
    if guess == number:
        print("You won!")
        break
    elif guess > number:
        guess = int(input("Decrease your number: "))
    else:
        guess = int(input("Increase your number: "))