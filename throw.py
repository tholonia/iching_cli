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
    -q, --question      text
    -r, --true_random   use true random numbers
"""
    print(rs)
    exit()


def import_sql_file(db_path, sql_file_path):
    """
    Import an SQL file into an SQLite database.

    Parameters:
    db_path (str): The path to the SQLite database file.
    sql_file_path (str): The path to the SQL file to be imported.
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

def get_true_random_number(min_val, max_val):
    """
    Get a true random number from random.org.

    Parameters:
    min_val (int): The minimum value of the random number (inclusive).
    max_val (int): The maximum value of the random number (inclusive).

    Returns:
    int: A true random number from random.org.
    """
    url = f"https://www.random.org/integers/?num=1&min={min_val}&max={max_val}&col=1&base=10&format=plain&rnd=new"
    response = requests.get(url)

    if response.status_code == 200:
        return int(response.text.strip())
    else:
        raise Exception(f"Error fetching random number: {response.status_code}")

def binary_to_decimal(binary_str):
    """
    Convert a binary number (as a string) to a decimal number.

    Parameters:
    binary_str (str): The binary number represented as a string of '0's and '1's.

    Returns:
    int: The decimal representation of the binary number.
    """
    decimal_number = int(binary_str, 2)
    return decimal_number

def DivideStalks(YarrowStalks):
    global HandPile, EastPile, WestPile
    global true_random
    # Divide 49 stalks into eastpile westpile
    # Subtract one from westpile and put in handpile
    if true_random:
        WestPile = get_true_random_number(1, YarrowStalks)
    else:
        WestPile = random.randint(1, YarrowStalks)

    EastPile = YarrowStalks - WestPile
    WestPile -= 1
    HandPile = 1

def DivideEastAndWest():
    global EastRemainder, WestRemainder, HandPile
    EastRemainder = EastPile % 4
    WestRemainder = WestPile % 4
    if EastRemainder == 0:
        EastRemainder = 4
    if WestRemainder == 0:
        WestRemainder = 4
    HandPile += EastRemainder + WestRemainder

def LineCast():
    global Stalks, CountValue1, CountValue2, CountValue3, LineValue
    Stalks = 49  # Remove one stalk and set it aside

    DivideStalks(Stalks)
    DivideEastAndWest()
    if EastRemainder + WestRemainder + 1 == 9:
        CountValue1 = 2
    if EastRemainder + WestRemainder + 1 == 5:
        CountValue1 = 3

    Stalks -= HandPile

    DivideStalks(Stalks)
    DivideEastAndWest()
    if EastRemainder + WestRemainder + 1 == 8:
        CountValue2 = 2
    if EastRemainder + WestRemainder + 1 == 4:
        CountValue2 = 3

    Stalks -= HandPile

    DivideStalks(Stalks)
    DivideEastAndWest()
    if EastRemainder + WestRemainder + 1 == 8:
        CountValue3 = 2
    if EastRemainder + WestRemainder + 1 == 4:
        CountValue3 = 3

    LineValue = CountValue1 + CountValue2 + CountValue3

    if LineValue == 6:
        DrawLine('weak', True)
        binaryVal = 0
    if LineValue == 7:
        DrawLine('strong', False)
        binaryVal = 1
    if LineValue == 8:
        DrawLine('weak', False)
        binaryVal = 0
    if LineValue == 9:
        DrawLine('strong', True)
        binaryVal = 1

def DrawLine(line, changing):
    global asciipic_fr
    global asciipic_to
    global from_val
    global to_val
    if changing and line == 'weak':
        asciipic_fr = fg.YELLOW+'━━━   ━━━∘'+fg.RESET
        asciipic_to = fg.MAGENTA+'───────── '+fg.RESET
        from_val=0
        to_val=1
    if changing and line == 'strong':
        asciipic_fr = fg.MAGENTA+'━━━━━━━━━×'+fg.RESET
        asciipic_to = fg.YELLOW+'───   ─── '+fg.RESET
        from_val=1
        to_val=0
    if not changing and line == 'strong':
        asciipic_fr = fg.MAGENTA+'───────── '+fg.RESET
        asciipic_to = fg.MAGENTA+'───────── '+fg.RESET
        from_val=1
        to_val=1
    if not changing and line == 'weak':
        asciipic_fr = fg.YELLOW+'───   ─── '+fg.RESET
        asciipic_to = fg.YELLOW+'───   ─── '+fg.RESET
        from_val=0
        to_val=0

def lst2str(num_list):
    concatenated_string = ''.join(map(str, num_list))
    return concatenated_string

def find_value(json_data, key, value):
    """
    Find all items in a JSON array where a specific key has a specific value.

    Parameters:
    json_data (list): The JSON array to search in.
    key (str): The key to search for.
    value (str): The value to match.

    Returns:
    list: A list of matching items.
    """
    matching_items = [item for item in json_data if item.get(key) == value]
    return matching_items

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
    global conn
    query = f"SELECT {key} FROM hexagrams where bseq = {idx};"
    results = execute_query(conn, query)
    stres = str(results[0][0])
    return(stres.lstrip(" "))

def is_moving_lines(line_vals):
    for i in range(len(line_vals)):
        if line_vals[i] == 9 or line_vals[i] == 6:
            return True
    return False

def print_interp(hexlist,hexnum,line_vals,hexseq):
    # ANSI color shortcuts
    _g = fg.GREEN
    _w = fg.WHITE
    _c = fg.CYAN
    _y = fg.YELLOW
    _b = fg.BLUE
    _m = fg.MAGENTA
    _r = fg.RED

    _xg = fg.LIGHTGREEN_EX
    _xw = fg.LIGHTWHITE_EX
    _xc = fg.LIGHTCYAN_EX
    _xy = fg.LIGHTYELLOW_EX
    _xb = fg.LIGHTBLUE_EX
    _xm = fg.LIGHTMAGENTA_EX
    _xr = fg.LIGHTRED_EX

    _re = fg.RESET


    #! Print the first hexagram
    if hexseq == 1:
        print("#First Hexagram")
    if hexseq == 2:
        print("#Second Hexagram")

    # this prines the lines
    for i in range(6):
        print(f"{hexlist[i]:10s}")

    frdec=binary_to_decimal(lst2str(hexnum))

    fromstr = _g+f"""
    {_xw}TITLE:    {_g}{getval('title',frdec)}
    {_xw}TRANS:    {_g}{getval('trans',frdec)}
    {_xw}SEQUENCE: {_g}{frdec} ({lst2str(fromhex)})
    {_xw}ORDER:    {_g}{getval('pseq',frdec)} (I-Ching order)

    {_xw}EXPLANATION:
        {_g}{getval('explanation',frdec)}

    {_xw}JUDGEMENT:
        {_g}{getval('judge_old',frdec)}

    {_xw}JUDGEMENT EXPLANATION:
        {_g}{getval('judge_exp',frdec)}
    """
    print(_g+fromstr+_re)

    if hexseq == 1:
        rev_line_vals = list(reversed(line_vals))

        if is_moving_lines(line_vals):
            print(_xw+f"MOVING LINES")
            for i in range(len(rev_line_vals)):
                if rev_line_vals[i] == 9 or rev_line_vals[i] == 6:
                    print(_xm+getval(f'line_{i+1}',frdec))
                    print(_xb+getval(f'line_{i+1}_org',frdec))
                    print(_xc+getval(f'line_{i+1}_exp',frdec))
            print(_re)
        else:
            print(_xw+f"NO MOVING LINES")

def markdown_interp(f,hexlist,hexnum,line_vals,hexseq):


    # this prines the lines
    f.write("```\n")
    for i in range(6):
        f.write(f"{remove_ansi_codes(hexlist[i]):10s}\n")
    f.write("```\n")

    frdec=binary_to_decimal(lst2str(hexnum))

    fromstr = f"""
**TITLE**:    {getval('title',frdec)}
**TRANS**:    {getval('trans',frdec)}
**SEQUENCE**: {frdec} ({lst2str(fromhex)})
**ORDER**:    {getval('pseq',frdec)} (I-Ching order)

**EXPLANATION**:
> {getval('explanation',frdec)}

**JUDGMENT**:
> {getval('judge_old',frdec)}

**JUDGMENT EXPLANATION**:
> {getval('judge_exp',frdec)}
"""
    f.write(fromstr+"\n")

    if hexseq == 1:
        rev_line_vals = list(reversed(line_vals))

        if is_moving_lines(line_vals):
            f.write("**MOVING LINES**\n")

            for i in range(len(rev_line_vals)):
                if rev_line_vals[i] == 9 or rev_line_vals[i] == 6:
                    moving_lines = True
                    f.write("**"+getval(f'line_{i+1}',frdec)+"**\n")
                    f.write(">*"+getval(f'line_{i+1}_org',frdec)+"*\n")
                    f.write(getval(f'line_{i+1}_exp',frdec)+"\n")
                    f.write("\n")
        else:
            f.write("**No Moving Lines**\n")

def remove_ansi_codes(input_string):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', input_string)

def string_to_filename(input_string, replace_with='_', max_length=16):
    # Define a regex pattern to match invalid filename characters
    invalid_chars = r'[<>:"/\\|?* ]'
    # Replace invalid characters and spaces with the specified replacement character
    filename = re.sub(invalid_chars, replace_with, input_string)
    # Strip leading and trailing whitespace
    filename = filename.strip()
    # Ensure the filename is not empty
    if not filename:
        raise ValueError("The input string resulted in an empty filename.")
    # Truncate the filename to the maximum length
    truncated_filename = filename[:max_length]
    return truncated_filename

#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────


Stalks = 50
HandPile = 0
EastPile = 0
WestPile = 0
EastRemainder = 0
WestRemainder = 0
CountValue1 = 0
CountValue2 = 0
CountValue3 = 0
LineValue = 0
asciipic_fr = ""
from_val = ""
to_val = ""
asciipic_to = ""
line_vals = []
visual_from = []
visual_to = []
fromhex = []
tohex = []
conn = connect_to_database('hexagrams.db')
question = "test mode"
true_random = False
question = "test mode"

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hq:t",
        [
            "help",
            "question=",
            "true_random",
        ],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-q", "--question"):
        question = arg
    if opt in ("-t", "--true_random"):
        true_random = True


# Cast the line
for i in range(6):
    LineCast()
    line_vals.append(LineValue)
    visual_from.append(asciipic_fr)
    visual_to.append(asciipic_to)
    fromhex.append(from_val)
    tohex.append(to_val)




# print for ANSI screen

print(f"Question: {question}")
print_interp(visual_from,fromhex,line_vals,1)
if is_moving_lines(line_vals):
    print_interp(visual_to,tohex,line_vals,2)

# print for markdown file screen


filename = "Q_"+string_to_filename(question)+".md"

f = open(filename,"w")
f.write(f"# Question: {question}\n")

markdown_interp(f,visual_from, fromhex, line_vals,1)
if is_moving_lines(line_vals):
    markdown_interp(f,visual_to, tohex, line_vals,2)
f.close

print(f"Output written to {filename}")

