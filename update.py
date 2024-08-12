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
    -c, --comment       bool flag
    -b, --bin           binary-ID
    -d. --dump          bool flag
    -r. --reload        <sql_dump_file>


Examples:
    ./update.py --bin 0 --comment                   # add a new comment to bID=0
    ./update.py --reload hexagrams_08_12_2024.sql   # reload database from specific backup
    ./update.py --dump                              # make dump backupsd of all databases (hexagrams.db and trigrams.db)


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


def execute_query(conn, query):
    """
    Execute a query on the SQLite database.

    Parameters:
    conn (sqlite3.Connection): The connection object to the SQLite database.
    query (str): The SQL query to be executed.

    Returns:
    list: The results of the query.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []

def getval(key, idx):
    global conn_h
    query = f"SELECT {key} FROM hexagrams where bseq = {idx};"
    results = execute_query(conn_h, query)
    stres = str(results[0][0])
    return(stres.lstrip(" "))

def connect_to_database(db_file):
    """
    Connect to an SQLite3 database.

    Parameters:
    db_file (str): The path to the SQLite3 database file.

    Returns:
    sqlite3.Connection: The connection object to the SQLite database.
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def generate_file_name(title):
    import datetime
    # Get the current date
    current_date = datetime.datetime.now()

    # Format the date as month_day_year
    formatted_date = current_date.strftime("%m_%d_%Y")

    # Create the file name
    file_name = f"{title}_{formatted_date}.sql"

    return file_name


def reload_database_from_sql_file(database_path, sql_file_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    drop_all_tables(conn)

    # Read the SQL file
    with open(sql_file_path, 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute the SQL script
    cursor.executescript(sql_script)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def drop_all_tables(conn):
    """Drop all tables in the connected database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]};")
    conn.commit()

conn_h = connect_to_database('hexagrams.db')
conn_t = connect_to_database('trigrams.db')

comment = False
bin = False
dump = False
reload = False

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hcb:dr:",
        [
            "help",
            "comment",
            "bin=",
            "dump",
            "reload=",
        ],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-c", "--comment"):
        comment = True
    if opt in ("-b", "--bin"):
        bin = int(arg)
    if opt in ("-d", "--dump"):
        dump = True
    if opt in ("-r", "--reload"):
        reload = arg



if comment:
    existing_comment = getval("comment", bin)

    # print for ANSI screen
    print(fg.GREEN + existing_comment + fg.RESET)

    new_comment = input("Enter new comment: ")

    all_comments = existing_comment + "\n\n" + new_comment

    print(fg.RED + all_comments + fg.RESET)

    ok = "n"
    ok = input("Is this OK? (y/[n]): ")
    if ok == "y":

        update_query = "UPDATE hexagrams SET comment = ? WHERE bseq = ?"
        conn_h.execute(update_query, (all_comments, bin))


        # query = f"UPDATE hexagrams SET comment = '{all_comments}' WHERE bseq = {bin};"
        # print(query)
        # exit()
        # conn_h.execute(query)
        conn_h.commit()
        print("Updated")

if dump:

    # Define the name of the dump file
    hex_dump_file = generate_file_name("hexagrams")
    tri_dump_file = generate_file_name("trigrams")
    dump_file_path = 'example_dump.sql'

    # Open the dump file in write mode
    with open(hex_dump_file, 'w') as dump_file:
        # Use the .dump command to get the SQL dump
        for line in conn_h.iterdump():
            dump_file.write('%s\n' % line)
    print(f"'hexagrams' SQL dump created successfully at {hex_dump_file}")

    with open(tri_dump_file, 'w') as dump_file:
        # Use the .dump command to get the SQL dump
        for line in conn_t.iterdump():
            dump_file.write('%s\n' % line)
    print(f"'trigrams' SQL dump created successfully at {tri_dump_file}")

    # Close the connection
    conn_h.close()
    conn_t.close()

if reload:

    if "hex" in reload:
        database_path = 'hexagrams.db'
        sql_file_path = reload
        reload_database_from_sql_file(database_path, sql_file_path)
        print(f"Database {database_path} reloaded successfully from {sql_file_path}")
    if "tri" in reload:
        database_path = 'trigrams.db'
        sql_file_path = reload
        reload_database_from_sql_file(database_path, sql_file_path)
        print(f"Database {database_path} reloaded successfully from {sql_file_path}")
