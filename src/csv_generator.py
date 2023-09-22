import csv
from datetime import date

# Format the date to 'm-d-yyyy'
def format_date(date):
    date = date.strftime("%m-%d-%Y")
    return date

# Created the modified csv files for eith ORU or ADT
def generate_csv(rows, hl7_type):
    output_file = 'Error.txt'

    # check to see what type hl7 message is being sent through
    if hl7_type == 'ADT':
        output_file = 'Archive/Modified/ADT_{}_Modified_file.csv'.format(date.today())

    if hl7_type == 'ORM':
        output_file = 'Archive/Modified/ORU_{}_Modified_file.csv'.format(date.today())

    # Check if any rows were returned
    if len(rows) > 0:
        
        # Create a list to hold the modified rows
        modified_rows = []
        
        for row in rows:
            message_type, first_name, last_name, middle_name, address, state, account_number, bill_amount = row
            
            # Combine the three columns into one column called "patient_name"
            patient_name = f"{last_name}, {first_name} {middle_name}"

            # Set date of service to the current date
            date_of_service = date.today()
            date_of_service = format_date(date_of_service)
            
            # Append the modified row to the list
            modified_row = (message_type, patient_name, address, state, account_number, bill_amount, date_of_service)
            modified_rows.append(modified_row)
            
        
        # Create a CSV file and write the modified data to it
        with open(output_file, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Write the header row
            header = ["message_type", "patient_name", "patient_address", "patient_state", "account_number", "bill_amount", "date_of_service"]
            csv_writer.writerow(header)
            
            # Write the modified data rows
            csv_writer.writerows(modified_rows)
            
        print("Data saved to output csv")
    else:
        print("No data found in csv_table")