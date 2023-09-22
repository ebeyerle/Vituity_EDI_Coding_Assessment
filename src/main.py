import pandas as pd
import sqlite3
from datetime import date
from backup import make_backups
from hl7_reader import read_hl7
from csv_generator import generate_csv
from bill_amount import get_bill_amount


# Make a copy of the 3 files in a directory Archive/Original
make_backups()

# Initialize an array to hold all hl7 files
hl7_list = []

# Parsed HL7 data is stored on a tuple
data_tuple_ADT = read_hl7('Data/ADT_sample.txt', hl7_list)
data_tuple_ORM = read_hl7('Data/Sample ORU.txt', hl7_list)

# Read the CSV file into a DataFrame
df = pd.read_csv("Data/sampledata.csv")

# If the database doesn't exist, it will create one in the directory
conn = sqlite3.connect("csv_database.db")

# Converted the sampledata.csv file data to SQL table
df.to_sql("csv_table", conn, if_exists="replace", index=False)

# Create a cursor
c = conn.cursor()

# Define the SQL INSERT statement
insert_query = """
INSERT INTO csv_table (
     message_type, patient_first_name, patient_last_name, patient_middle_name,
    patient_address_1, patient_state, account_number, bill_amount
) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

for hl7 in hl7_list:
    if hl7[0] == 'ADT-A03':
        c.execute(insert_query, hl7)
        c.execute("""SELECT message_type, patient_first_name, patient_last_name, patient_middle_name, patient_address_1, patient_state, account_number, bill_amount FROM csv_table 
                  WHERE message_type LIKE 'AD%' """)
        rows = c.fetchall()
        generate_csv(rows, 'ADT')

    if hl7[0] == 'ORU-R01':
        c.execute(insert_query, hl7)
        c.execute("""SELECT message_type, patient_first_name, patient_last_name, patient_middle_name, patient_address_1, patient_state, account_number, bill_amount FROM csv_table 
                  WHERE message_type LIKE 'OR%' """)
        rows = c.fetchall()
        generate_csv(rows, 'ORM')

conn.commit()

# Fetch Table Data
print("Display billing data:")
c.execute("""SELECT patient_state AS 'State', SUM(bill_amount) AS 'Bill Amount' FROM csv_table
          GROUP BY state""")

# Fetch all the rows from the table
rows = c.fetchall()

print("Getting billing report....")

# Get billing info
get_bill_amount(rows)

# Close our connection
conn.close()