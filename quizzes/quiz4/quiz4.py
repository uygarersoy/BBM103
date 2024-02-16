
#import sys to extract the name of the input and output files
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

#create temp variable to hold the each line from input file
temp = []

#open file and iterate over each line. append each line to temp
with open(input_file, "r") as inp:
    for line in inp:
        temp.append(line)

#add new line character to the end of the last line.
#because when messages are sorted it can appear in the middle of somewhere
temp[-1] += "\n"
#sort the list by message id and package id
temp = sorted(temp, key=lambda message: (int(message.split("\t")[0]), int(message.split("\t")[1])))

#store each unique message id at message_id starting with the first message's id
message_id = [temp[0].split("\t")[0]]
#initiate start variable by indicating each unique message
result = f"Message\t{len(message_id)}\n"


for message in temp:
    #if new message is reached in temp, append the id of the message to message_id
    if message.split("\t")[0] not in message_id:
        #split the line by \t character to get the message is
        message_id.append(message.split("\t")[0])
        result += f"Message\t{len(message_id)}\n"
    #add each line to the result variable
    result += message
#get rid of the possible new line character at the end
result = result.strip("\n")

#write result to the output file
with open(output_file, "w") as out:
    out.write(result)