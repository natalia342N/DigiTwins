# import_csv.py

import csv
from datetime import datetime

def read_csv(file_name):
    """Reads a CSV file and returns a list of lines; Delimiter: ; """
    with open(file_name, 'r',  encoding='Latin-1') as file:
    #     data = file.read()
    # encoding_result = chardet.detect(data)
    # print(encoding_result)
        csv_reader = csv.reader(file, delimiter=';')
        next(csv_reader)  # Skips the header
        return [row for row in csv_reader]

def read_csv_specific_format(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)  # header line
        # TagID from second column onward
        tag_ids = header[1:]

        # List for all results
        data = []
        for row in reader:
            timestamp = row[0]  # Timestamp is in the first column
            # Transform string to datetime
            try:
                timestamp = datetime.strptime(timestamp, "%d.%m.%Y %H:%M")  # Example: 01.01.2018 00:00
            except ValueError:
                continue  # skip error of transforming timestamp values
            # Values of the corresponding tags
            for tag_id, value in zip(tag_ids, row[1:]):
                try:
                # Add tuple (TagID, Timestamp, Value) to the result list
                    data.append((tag_id, timestamp, float(value)))
                except ValueError:
                    continue  # skip error of transforming values

        return data
