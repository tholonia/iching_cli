#!/bin/env python
import random
from colorama import Fore as fg
import requests
import sqlite3
import json
import os, sys, glob, getopt
import re

def showhelp():
    print("help")
    rs = """
    -h, --help          show help

"""
    print(rs)
    exit()


def import_sql_file(db_path, sql_file_path):
    """
    Import an SQL file into an SQLite database.

    Parameters:
    db_path (str): The path to the SQLite database file.
    sql_file_path (str): The path to the SQL file to be imported.


    this sql file was created by

    1) export mysql table to dwl file
    sudo mysqldump iching hexagrams > hexagrams.sql
    sudo mysqldump iching xref_trigrams > trigrams.sql

    2) convert sql file to sqlite file
    mysql2sqlite/mysql2sqlite  hexagrams.sql > hexagrams.sqlite
    mysql2sqlite/mysql2sqlite  trigrams.sql > trigrams.sqlite

    3) create database and import sql file
    mysql2sqlite/mysql2sqlite  hexagrams.sql |sqlite2  hexagrams.db
    mysql2sqlite/mysql2sqlite  trigrams.sql |sqlite3  trigrams.db

To alter the tabes,

    """
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read the SQL file
    with open(sql_file_path, 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute the SQL script
    cursor.executescript(sql_script)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



def connect_to_database(db_file):
    """
    Establish a connection to the specified SQLite3 database.

    This function attempts to create a connection to the SQLite3 database
    specified by the `db_file` path parameter. It returns a connection object
    that can be used to interact with the database.

    Args:
    -----
    db_file : str
        The path to the SQLite3 database file.

    Returns:
    --------
    sqlite3.Connection or None
        A connection object to the SQLite3 database if the connection is
        established successfully, otherwise None.

    Raises:
    -------
    sqlite3.Error
        If there is an issue connecting to the database, an error message
        is printed and the function returns None.

    Examples:
    ---------
    >>> conn = connect_to_database('example.db')
    >>> if conn is not None:
    >>>     print('Connection established.')
    >>> else:
    >>>     print('Connection failed.')
    Connection established.
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []

def get_hexagram_val_by_bseq(idx):
    global conn_h
    # Construct the SQL query to select the desired value based on the column key and binary sequence index
    query = f"SELECT * FROM tbd_asc_positions" # WHERE bseq = {idx};"
    # Execute the query and fetch results
    results = execute_query(conn_h, query)
    # Convert the resulting value to string, remove leading/trailing spaces and newline characters

    print(results)

    stres = str(results[0][0])
    return stres.strip()



#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

conn_h = connect_to_database('hexagrams.db')
conn_t = connect_to_database('trigrams.db')
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "h",
        [
            "help",
        ],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()

rs = get_hexagram_val_by_bseq(0)

print(rs)