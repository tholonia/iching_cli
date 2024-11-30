#!/bin/env python
import csv
import json

def load_csv_and_create_dict(csv_file):
    try:
        # Open the CSV file
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)

            # Create a dictionary to store rows with 'asc_bseq' as the key
            rows_dict = {}

            # Loop through each row in the CSV file
            for row in reader:
                # Use the 'asc_bseq' value as the key for the dictionary
                asc_key = row['asc_bseq']

                # Create a list for the row data in format 2
                row_data = {key: value for key, value in row.items()}

                # Add the row data to the dictionary
                rows_dict[asc_key] = row_data

            # Print the resulting dictionary
            for asc_key, row in rows_dict.items():
                print(f"asc_bseq: {asc_key}")
                print(row)
                print("---")

            # Save the resulting dictionary to a JSON file
            with open('pairs.json', mode='w') as json_file:
                json.dump(rows_dict, json_file, indent=4)
                print("Data successfully saved to pairs.json")
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    # CSV file name
    csv_file = "xref_32pairs_202411291606.csv"

    # Load the CSV file and create the dictionary
    load_csv_and_create_dict(csv_file)

if __name__ == "__main__":
    main()
