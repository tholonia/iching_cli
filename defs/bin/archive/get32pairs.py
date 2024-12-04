#!/bin/env python
import sqlite3

def connect_to_db(db_name):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_name)
        print(f"Successfully connected to database: {db_name}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def fetch_data(conn, table_name):
    try:
        # Create a cursor object to interact with the database
        cursor = conn.cursor()
        
        # Execute a query to fetch all data from the specified table
        cursor.execute(f"SELECT * FROM {table_name}")
        
        # Fetch all rows from the result of the query
        rows = cursor.fetchall()
        
        # Get column names from the table
        column_names = [description[0] for description in cursor.description]
        
        # Print each row as key-value pairs
        for row in rows:
            row_dict = dict(zip(column_names, row))
            for key, value in row_dict.items():
                print(f"{key}: {value}")
            print("---")
    except sqlite3.Error as e:
        print(f"Error fetching data from table: {e}")

def main():
    # Database name
    db_name = "ichibala.db"
    
    # Connect to the SQLite database
    conn = connect_to_db(db_name)
    
    # If connection is successful, fetch data from the specified table
    if conn:
        table_name = "iching_xref_32pairs"
        fetch_data(conn, table_name)
        
        # Close the database connection
        conn.close()

if __name__ == "__main__":
    main()
