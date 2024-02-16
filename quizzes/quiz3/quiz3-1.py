import sys

result = int(sys.argv[1]) ** int(sys.argv[2])

if result <= -10:
    print("Enter numbers bigger than zero for base and exponent!")
elif result > -10 and result < 0:
    print(f"{int(sys.argv[1])} ^ {int(sys.argv[2])} = {result}")
else:


    output = f"{int(sys.argv[1])} ^ {int(sys.argv[2])} = {result}"

    if result < 10:
        print(output)
    
    else:

        while True:
            digits = [i for i in str(result)]
            if len(digits) != 1:
                output += " = " + " + ".join(i for i in digits)
                if sum(int(i) for i in digits) > 9:
                    output += " = " + str(sum(int(i) for i in digits))
            elif len(digits) == 1:
                output += " = " + str(sum(int(i) for i in digits))
                break
            result = sum(int(i) for i in digits)
            digits = []
        
        print(output)