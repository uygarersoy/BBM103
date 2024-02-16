
#import sys module to access command-line arguments
import sys

#use try/except in case of an absence of command-line arguments
try:
    #covert string type command-line arguments to integer values and calculate score
    result = int(sys.argv[1]) * 2 + int(sys.argv[2]) * 3 + int(sys.argv[3])
    print(result)

except:
    pass

#define a function with 2 parameters
def healthStatus(height, mass):
    #check to see parameters are positive floats or integers
    if height <= 0 or mass < 0:
        return ""
    else:
        #calculate body mass with given parameters
        BMI = mass / (height**2)

        #return the state of a person according to her/his BMI
        if BMI >= 30:
            return "obese"
        elif BMI >= 24.9 and BMI < 30:
            return "overweight"
        elif BMI >= 18.5 and BMI < 24.9:
            return "healthy"
        else:
            return "underweight"