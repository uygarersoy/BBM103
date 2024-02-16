
#define a function to read lines from .txt file
def read_file(input_file):

    #open the file in "r" mode to be able to read it
    with open(input_file, "r") as input_file:
        
        #iterate over each line in the file
        for line in input_file:
            #get rid of the new line character and split the line by "," character to process it in the future
            command = line.replace("\n", "").split(", ")
            
            #check whether or not the desired keyword is in the first item of variable command
            #replace the keyword with an empty string for further use
            #call the desired function with the required or additional parameters
            if "create" in command[0]:
                command[0] = command[0].replace("create ", "")
                create(command)
            
            #second argument in probability function states where the function is called
            elif "probability" in command[0]:
                command[0] = command[0].replace("probability ", "")
                probability(command[0], 1)
            
            elif "recommendation" in command[0]:
                command[0] = command[0].replace("recommendation ", "")
                recommendation(command[0])

            elif "remove" in command[0]:
                command[0] = command[0].replace("remove ", "")
                remove(command)
            
            elif "list" in command[0]:
                get_list()


         
#define a function to write the outputs to a .txt file
def write_file(output_file, message):

    #open the file in append mode to keep adding new lines to file
    with open(output_file, "a") as out:
        #write the message to the output file
        out.write(f"{message}\n")

#define a function to add patient info to patient list
def create(patient):

    #check whether or not the person is alreay recorded
    if is_recorded(patient[0]):
        #if person already exist, call write_file function with a suitable message
        message = f"Patient {patient[0]} cannot be recorded due to duplication."
        write_file(outputs_file, message)
    else:
        #if person is not recorded yet, do some altercations to person's data for further use
        #record the patient to patient_list and call write_file function to indicate recording is succesfull        
        message = f"Patient {patient[0]} is recorded."
        patient[1] = float(patient[1])
        patient[-1] = float(patient[-1])
        patient_list.append(patient)
        write_file(outputs_file, message)
        
#define a function to calculate the person's probability of having the disease
def probability(patient_name, check):
    
    #set is_found variable to check if person is recorded or not 
    is_found = False

    #iterate over records of patients
    for patient in patient_list:
        #check if the person's name is in the record
        if patient_name == patient[0]:
            #if person's name is in records set is_found variable to True
            is_found = True
            #extract the values of accuracy of results and disease_incidence from person's record
            accuracy, disease_incidence = patient[1], patient[3]
            #split the disease_incidence by "/" character to enable calculations on it
            disease_incidence = disease_incidence.split("/")

            #calculate the true_positive value accordingly
            true_positive = int(disease_incidence[0]) * accuracy * 100
            #calculate the false_positive value accordingly
            false_positive = (int(disease_incidence[1]) - int(disease_incidence[0])) * (1 - accuracy) * 100
            #calculate the value of probability according to the formula
            probability = f"{((true_positive / (true_positive + false_positive)) * 100):.2f}"

            #check if the value of probability is an integer
            if int(float(probability)) - float(probability) == 0:
                #if it is an integer, get rid of the precision of the decimal points and convert it to string for further use
                probability = str(int(float(probability)))

            #check if the probability function is called from read_file function
            if check == 1:
                #if it is called from read_file function, call write_file function with the appropriate message
                message = f"Patient {patient_name} has a probability of {probability}% of having {patient[2].lower()}."
                write_file(outputs_file, message)
            #check if the probability function is called from recommendation function
            if check == 0:
                #if it is called from recommendation function, return probability value to be used in the recommendation function
                return probability
    #if personn is not found, call write_file function to state person was not found                
    if not is_found:
        write_file(outputs_file, f"Probability for {patient_name} cannot be calculated due to absence.")
    
#define a function to recommend to patient whether to take the treatment or not
def recommendation(patient_name):
    #set is_found to False to check person is recorded or not
    is_found = False

    #iterate over patients in patients_list
    for patient in patient_list:
        #check if person's name is in records
        if patient_name == patient[0]:
            #if person is in records, set is_found to True to indicate person is recorded
            is_found = True
            #get the value of probability of having the disease from probability function
            prob = float(probability(patient_name, 0))
            # check if treatment risk is higher than having the disease probability
            if prob < patient[-1] * 100:
                #if it is higher, call write_file function to indicate treatment is risky
                write_file(outputs_file, f"System suggests {patient[0]} NOT to have the treatment.")
            else:
                #if it is not higher, call write_file function to indicate treatment can be appliable
                write_file(outputs_file, f"System suggests {patient[0]} to have the treatment.")
    #if person is not in records, call write_file function to state person was not found        
    if not is_found:
        write_file(outputs_file, f"Recommendation for {patient_name} cannot be calculated due to absence.")

#define a function to tabulate the records in patients_list
def get_list():

    #import built-in math library
    import math

    #set the table headers and rows accordingly
    header_top = "Patient\tDiagnosis\tDisease\t\t\tDisease\t\tTreatment\t\tTreatment"
    header_bottom = "Name\tAccuracy\tName\t\t\tIncidence\tName\t\t\tRisk"
    dashes = "-" * 73
    
    #put them all in a list to ease the further usage
    headers = [header_top, header_bottom, dashes]
    
    #call write_file function to output the headers of the table
    for _ in range(len(headers)):
        write_file(outputs_file, headers[_])
    
    #set the spaces between each column according to longest value for each column to align all records
    max_word_spaces = [8, 12, 16, 12, 16, 0]
    
    #initiate a variable to hold patients' records
    patient_data = ""
    
    #iterate over records in patient_list
    for patient in patient_list:
        #iterate over each patient's own records
        for index in range(len(patient)):
            #multiply the value of diagnosis accuracy by 100 to get the percent value with two point decimal precision
            #concatenate patient data with diagnosis_accuracy and add percent symbol
            #convert it to string and add necessary "\t" values by calculating left-over spacing
            if index == 1:    
                diagnosis_accuracy = f"{(patient[index] * 100):.2f}%"            
                patient_data += diagnosis_accuracy + int(math.ceil((max_word_spaces[index] - len(diagnosis_accuracy)) / 4)) * "\t" 
            #check the information of patient is treatment risk or not
            elif index == len(patient) - 1:
                #multiply the float value by 100 to get percent value by two percent decimal precision
                #if precision part is all zeros, drop the zeros and concatenate with patient_data
                if int(patient[index] * 100) - (patient[index] * 100) == 0:
                    patient_data += f"{int(patient[index] * 100)}%"
                else:
                    #if precision points not all zero, drop the ones at the right-side if possible
                    #concatenate with the patient_data
                    risk = f"{(patient[index] * 100):.2f}".rstrip("0")
                    patient_data += f"{risk}%"
            else:
                #concatenate the patient_data with the informations of the patient
                #add required "\t" characters according to the left-over spacing
                patient_data += patient[index] + int(math.ceil((max_word_spaces[index] - len(patient[index])) / 4)) * "\t" 
        #call write_file function to write the patient info to the file
        write_file(outputs_file, patient_data)
        #reset the patient_data value to empty string for next patient
        patient_data = ""
        
   

#define a function to remove a patient from records
def remove(patient_name):

    #set is_deleted to False to to search the records to find patient in it
    is_deleted = False

    #iterate over records to look for patient
    for index, patient in enumerate(patient_list):
        #check if patient's name is in the records
        if patient[0] == patient_name[0]:
            #delete the person's record from the patient_list
            del(patient_list[index])
            #set the is_deleted to True to indicate person is deleted
            is_deleted = True
    #if person is deleted, call the wrtite_file function to state the situation
    if is_deleted:
        message = f"Patient {patient_name[0]} is removed."
        write_file(outputs_file, message)
    #if is_deleted is False, then person was not in the list
    #call write_message function to indicate the situation
    else:
        message = f"Patient {patient_name[0]} cannot be removed due to absence."
        write_file(outputs_file, message)

#define a function to check if the person is in the recordings already or not
def is_recorded(patient_name):
    #check if the records are empty or not
    if len(patient_list) != 0:
        #iterate over the records
        for record in patient_list:
            #if person is in records, return True to state he/she is already recorded
            if record[0] == patient_name:
                return True
        #return False to state that person is not in the records
        return False
    #return False to state that list is empty, therefore person is not in the records
    else:
        return False

#create a patient_list to hold all the patient patients' records
patient_list = []

#set the input and output files name
inputs_file = "doctors_aid_inputs.txt"
outputs_file = "doctors_aid_outputs.txt"

#call the read_file function to kick-start the whole process
read_file(inputs_file)