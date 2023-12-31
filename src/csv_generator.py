import csv
import os
from datetime import date
import pandas as pd
import sqlite3


# Function to ensure a directory exists and create it if needed
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Creates a database for all final modified CSV ADT messages.
def create_adt_table(output_file):
    # Create a connection to the SQLite database
    conn = sqlite3.connect("csv_database.db")

    # Read the CSV file into a DataFrame
    df = pd.read_csv(output_file)

    # Use the to_sql method to insert the DataFrame into an SQL table
    # Replace 'my_table' with the name of your SQL table
    df.to_sql("adt_table", conn, if_exists="replace", index=False)

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()

# Format the date to 'm-d-yyyy'
def format_date(date):
    date = date.strftime("%m-%d-%Y")
    return date

# Created the modified csv files for eith ORU or ADT
def generate_csv(rows, hl7_type):
    # Specify the base output directory
    base_output_dir = 'Archive/Modified/'

    # Ensure that the base output directory exists
    ensure_directory_exists(base_output_dir)

    # Set the output file path based on the HL7 message type and current date
    if hl7_type == 'ADT':
        output_file = os.path.join(base_output_dir, f'ADT_{date.today()}_Modified_file.csv')
    elif hl7_type == 'ORM':
        output_file = os.path.join(base_output_dir, f'ORU_{date.today()}_Modified_file.csv')
    else:
        output_file = 'Error.txt'

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
            
        print("Data saved to output csv - " + output_file)
    else:
        print("No data found in csv_table")

    # After creating the csv file for ADT messages, a database is created that mimics the final modified data in the csv
    if hl7_type == 'ADT':
        create_adt_table(output_file)