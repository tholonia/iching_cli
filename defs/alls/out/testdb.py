#!/bin/env python
import json
import sqlite3
import argparse
from typing import Dict, Any

def import_json_to_db(json_file_path: str, database_path: str, table_name: str):
    """
    Import data from a JSON file into an SQLite database.
    
    Args:
        json_file_path (str): Path to the JSON file
        database_path (str): Path to the SQLite database
        table_name (str): Name of the table to create/insert into
    """
    # Read JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Ensure data is a list of dictionaries
    if isinstance(data, dict):
        data = [data]
    elif not isinstance(data, list):
        raise ValueError("JSON data must be a dictionary or list of dictionaries")
    
    if not data:
        raise ValueError("JSON data is empty")
    
    # Connect to database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        # Create table based on the first object's structure
        columns = list(data[0].keys())
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {', '.join(f'{col} TEXT' for col in columns)}
        )
        """
        cursor.execute(create_table_sql)
        
        # Prepare INSERT statement
        placeholders = ','.join(['?' for _ in columns])
        insert_sql = f"""
        INSERT INTO {table_name} ({','.join(columns)})
        VALUES ({placeholders})
        """
        
        # Insert data
        for item in data:
            values = [str(item.get(col, '')) for col in columns]
            cursor.execute(insert_sql, values)
        
        # Commit changes
        conn.commit()
        print(f"Successfully imported {len(data)} records into {table_name}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Import JSON data into SQLite database')
    parser.add_argument('json_file', help='Path to the JSON file to import')
    parser.add_argument('--database', '-d', default='database.db',
                        help='Path to the SQLite database (default: database.db)')
    parser.add_argument('--table', '-t', default='data',
                        help='Name of the table to create/insert into (default: data)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Import the data
    try:
        import_json_to_db(
            json_file_path=args.json_file,
            database_path="out.db",
            table_name="ichingcli"
        )
    except FileNotFoundError:
        print(f"Error: Could not find JSON file '{args.json_file}'")
    except json.JSONDecodeError:
        print(f"Error: '{args.json_file}' is not a valid JSON file")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()