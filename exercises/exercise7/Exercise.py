
import sys

#create empty dictionary to hold students data
students = {}
#extract name of the input file
input_file = sys.argv[1]

with open(input_file, "r") as inp:
    for line in inp:
        #extract name and education info of each student by splitting each line
        name, education = line.split(":")
        #add record to students dictionary by adding names as a key and education information as value
        #strip the new line character at the end of each line
        students[name] = education.strip("\n")

#iterate over names in command line
for name in sys.argv[2].split(","):
    #try to print the name of student and education of her/his by looking at dictionary
    try:
        #if s/he recorded print accordingly
        print(f"Name: {name}, University: {students[name]}")
    except:
        #otherwise throw an exception and print the following message 
        print(f"No record of '{name}' was found!")