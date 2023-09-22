# Function create a txt file for the billed amount of each state
def get_bill_amount(rows):
  # Define the file name for the output text file
  output_file_name = 'billed_amount.txt'
  total_bill_amount = 0

  # Open the text file in append mode
  with open(output_file_name, 'a') as file:
      file.write(f"State :: Bill Amount\n")
      # Iterate through fetched data and write it to the file
      for row in rows:
          file.write(f"{row[0]} - {row[1]}\n")
          # Check if row[1] is not None before adding
          if row[1] is not None:
            total_bill_amount += float(row[1])

      # Append the row with the sum of "Bill Amount"
      file.write(f"Total Bill Amount: {total_bill_amount}\n")

  print("Bill report generated")