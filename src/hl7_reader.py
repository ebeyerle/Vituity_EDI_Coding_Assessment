# Function to split a field using the '^' delimiter
def split_field(field):
    return field.split('^')

def read_hl7(hl7_file_path, hl7_list):

    # Read the HL7 file content
    with open(hl7_file_path, 'r') as file:
      hl7_message = file.read()

    # Split the HL7 message into lines using '\r' as the delimiter
    lines = hl7_message.split('\r')

    # Initialize variables to store parsed data
    patient_last_name = None
    patient_first_name = None
    patient_middle_name = None
    patient_address_street = None
    patient_address_state = None
    account_number = None
    bill_amount = None

    # Iterate through lines
    for line in lines:
        # Split each line into segments using '\n' as the segment delimiter
        segments = line.split('\n')

        for segment in segments:
            fields = segment.split('|')
            segment_name = fields[0]

            if segment_name == 'MSH':
                message_type = fields[8]
                message_type = message_type.replace('^', '-')

            if segment_name == 'PID':
                # PID segment: Patient Identification
                patient_name_field = fields[5]
                patient_address_field = fields[11]

                # Split the patient name field using the split_field function
                name_parts = split_field(patient_name_field)

                address_parts = split_field(patient_address_field)

                # Assign name parts to variables
                if len(name_parts) >= 1:
                    patient_last_name = name_parts[0]
                if len(name_parts) >= 2:
                    patient_first_name = name_parts[1]
                if len(name_parts) >= 3:
                    patient_middle_name= name_parts[2]

                if len(address_parts) >= 1:
                    patient_address_street = address_parts[0]
                if len(address_parts) >= 4:
                    patient_address_state = address_parts[3]

            if segment_name == 'IN1':
                insurance_account_field = fields[2]

                account_parts = split_field(insurance_account_field)

                if len(account_parts) >= 1:
                    account_number = account_parts[0]

            if segment_name == 'PV1':
                if len(fields) >= 47:
                    bill_amount = fields[47]


    # Store HL7 data in a tuple
    parsed_data = (message_type, patient_last_name, patient_first_name, patient_middle_name, patient_address_street, patient_address_state, account_number, bill_amount)
    hl7_list.append(parsed_data)
    return parsed_data

