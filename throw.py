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
    -q, --question      "text"
    -r, --true_random   use true random numbers from Random.ORG
    -b, --binary        show an specific hex by binary value (binary values must be between 0 and 63, inclusive)
    -c, --classic       show an specific hex by classic value (must be between 1 and 64, inclusive)

Examples:

    ./throw.py --binary 0                               # view a hexagram by binary value 0
    ./throw.py --classic 1                              # view a hexagram by classic value 1 (not yet implemented)
    ./throw.py --question "Should I?" --true_random     # ask a question using true random data from RANDOM.ORG (slow)
    ./throw.py --question "Should I?"                   # ask a question using pszxeudo-random numbers (fast)

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

def decimal_to_six_digit_binary(decimal_number):
    if decimal_number < 0 or decimal_number >= 64:
        raise ValueError("Number must be between 0 and 63 inclusive.")
    return format(decimal_number, '06b')

def LineCall(bin=-1,hex=-1,position=0):

    if hex > 0:
        # do a table lookup to convert hexagram number to binary
        bin = c2b_dict[hex]

    binval = str(decimal_to_six_digit_binary(bin))

    if binval[position] == "0":
        DrawLine('weak', False)
        binaryVal = 0
    if binval[position] == "1":
        DrawLine('strong', False)
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

def get_hexagram_val_by_bseq(key, idx):
    global conn_h
    query = f"SELECT {key} FROM hexagrams where bseq = {idx};"
    results = execute_query(conn_h, query)
    stres = str(results[0][0])
    return(stres.lstrip(" ").lstrip("\n").rstrip("\n"))

def get_trigram_val_by_bseq(key, idx):

    # print(key,idx)
    global conn_t
    query = f"SELECT {key} FROM xref_trigrams where bseq = {idx};"
    results = execute_query(conn_t, query)
    stres = str(results[0][0])
    return(stres.lstrip(" ").lstrip("\n").rstrip("\n"))

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
        print(f"{_y}First Hexagram{_re}")
    if hexseq == 2:
        print(f"{_y}Second Hexagram{_re}")

    # this prints the lines
    for i in range(6):
        print(f"{hexlist[i]:10s}")

    hexagram_binary_base10=binary_to_decimal(lst2str(hexnum))

    lower_tri_base10, upper_tri_base10 = hexagram_to_trigrams(hexnum)


    fromstr = _g+f"""
    {_xw}TITLE:    {_g}{get_hexagram_val_by_bseq('title',hexagram_binary_base10)}
    {_xw}TRANS:    {_g}{get_hexagram_val_by_bseq('trans',hexagram_binary_base10)}
    {_xw}SEQUENCE: {_g}{hexagram_binary_base10} ({lst2str(fromhex_binary_lst)})
    {_xw}ORDER:    {_g}{get_hexagram_val_by_bseq('pseq',hexagram_binary_base10)} (I-Ching order)

    {_xw}UPPER_TRIGRAM: {_g}{get_trigram_val_by_bseq('trans',upper_tri_base10)} ({get_trigram_val_by_bseq('title',upper_tri_base10)}), {get_trigram_val_by_bseq('t_element',upper_tri_base10)}, {get_trigram_val_by_bseq('polarity',upper_tri_base10)}, {get_trigram_val_by_bseq('planet',upper_tri_base10)}
    {_xw}LOWER_TRIGRAM: {_g}{get_trigram_val_by_bseq('trans',lower_tri_base10)} ({get_trigram_val_by_bseq('title',lower_tri_base10)}), {get_trigram_val_by_bseq('t_element',lower_tri_base10)}, {get_trigram_val_by_bseq('polarity',lower_tri_base10)}, {get_trigram_val_by_bseq('planet',lower_tri_base10)}

    {_xw}EXPLANATION:
        {_g}{get_hexagram_val_by_bseq('explanation',hexagram_binary_base10)}

    {_xw}JUDGEMENT:
        {_g}{get_hexagram_val_by_bseq('judge_old',hexagram_binary_base10)}

    {_xw}JUDGEMENT EXPLANATION:
        {_g}{get_hexagram_val_by_bseq('judge_exp',hexagram_binary_base10)}

    {_xw}COMMENTS:
        {_r}{get_hexagram_val_by_bseq('comment',hexagram_binary_base10)}

    """
    print(_g+fromstr+_re)

    if hexseq == 1:
        rev_line_vals = list(reversed(line_vals))

        if is_moving_lines(line_vals):
            print(_xw+f"MOVING LINES")
            for i in range(len(rev_line_vals)):
                if rev_line_vals[i] == 9 or rev_line_vals[i] == 6:
                    print(_xm+get_hexagram_val_by_bseq(f'line_{i+1}',hexagram_binary_base10))
                    print(_xb+get_hexagram_val_by_bseq(f'line_{i+1}_org',hexagram_binary_base10))
                    print(_xc+get_hexagram_val_by_bseq(f'line_{i+1}_exp',hexagram_binary_base10))
            print(_re)
        else:
            print(_xw+f"NO MOVING LINES")

def markdown_interp(f,hexlist,hexnum,line_vals,hexseq):


    # this prines the lines
    f.write("```\n")
    for i in range(6):
        f.write(f"{remove_ansi_codes(hexlist[i]):10s}\n")
    f.write("```\n")

    binary_base10=binary_to_decimal(lst2str(hexnum))
    lower_tri_base10, upper_tri_base10 = hexagram_to_trigrams(hexnum)

    fromstr = f"""
**TITLE**:    {get_hexagram_val_by_bseq('title',binary_base10)}
**TRANS**:    {get_hexagram_val_by_bseq('trans',binary_base10)}
**SEQUENCE**: {binary_base10} ({lst2str(fromhex_binary_lst)})
**ORDER**:    {get_hexagram_val_by_bseq('pseq',binary_base10)} (I-Ching order)

**UPPER_TRIGRAM**: {get_trigram_val_by_bseq('trans',upper_tri_base10)} ({get_trigram_val_by_bseq('title',upper_tri_base10)}), {get_trigram_val_by_bseq('t_element',upper_tri_base10)}, {get_trigram_val_by_bseq('polarity',upper_tri_base10)}, {get_trigram_val_by_bseq('planet',upper_tri_base10)}
**LOWER_TRIGRAM**: {get_trigram_val_by_bseq('trans',lower_tri_base10)} ({get_trigram_val_by_bseq('title',lower_tri_base10)}), {get_trigram_val_by_bseq('t_element',lower_tri_base10)}, {get_trigram_val_by_bseq('polarity',lower_tri_base10)}, {get_trigram_val_by_bseq('planet',lower_tri_base10)}

**EXPLANATION**:
> {get_hexagram_val_by_bseq('explanation',binary_base10)}

**JUDGMENT**:
> {get_hexagram_val_by_bseq('judge_old',binary_base10)}

**JUDGMENT EXPLANATION**:
> {get_hexagram_val_by_bseq('judge_exp',binary_base10)}

**COMMENTS**:
> {get_hexagram_val_by_bseq('comment',binary_base10)}



"""
    f.write(fromstr+"\n")

    if hexseq == 1:
        rev_line_vals = list(reversed(line_vals))

        if is_moving_lines(line_vals):
            f.write("**MOVING LINES**\n")

            for i in range(len(rev_line_vals)):
                if rev_line_vals[i] == 9 or rev_line_vals[i] == 6:
                    moving_lines = True
                    f.write("**"+get_hexagram_val_by_bseq(f'line_{i+1}',binary_base10)+"**\n")
                    f.write(">*"+get_hexagram_val_by_bseq(f'line_{i+1}_org',binary_base10)+"*\n")
                    f.write(get_hexagram_val_by_bseq(f'line_{i+1}_exp',binary_base10)+"\n")
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
    return truncated_filename\

def hexagram_to_trigrams(hexlst):
    lower_tri = hexlst[:3]
    upper_tri = hexlst[3:]

    lval = binary_to_decimal(''.join(map(str, lower_tri)))
    uval = binary_to_decimal(''.join(map(str, upper_tri)))

    # print(
    #     f"upper trigram: {lower_tri} ({binary_to_decimal(''.join(map(str, lower_tri)))})\n"
    #     f"lower trigram: {upper_tri} ({binary_to_decimal(''.join(map(str, upper_tri)))}"
    # )
    # exit()
    return lval, uval




#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────


# binary value to classical order

b2c_dict = {
    0: 2, 1: 24, 2: 7, 3: 19, 4: 15, 5: 36, 6: 46, 7: 11, 8: 16, 9: 51,
    10: 40, 11: 54, 12: 62, 13: 55, 14: 32, 15: 34, 16: 8, 17: 3, 18: 29,
    19: 60, 20: 39, 21: 63, 22: 48, 23: 5, 24: 45, 25: 17, 26: 47, 27: 58,
    28: 31, 29: 49, 30: 28, 31: 43, 32: 23, 33: 27, 34: 4, 35: 41, 36: 52,
    37: 22, 38: 18, 39: 26, 40: 35, 41: 21, 42: 64, 43: 38, 44: 56, 45: 30,
    46: 50, 47: 14, 48: 20, 49: 42, 50: 59, 51: 61, 52: 53, 53: 37, 54: 57,
    55: 9, 56: 12, 57: 25, 58: 6, 59: 10, 60: 33, 61: 13, 62: 44, 63: 1
}

# classical order to binary value

c2b_dict = {
    2: 0, 24: 1, 7: 2, 19: 3, 15: 4, 36: 5, 46: 6, 11: 7, 16: 8, 51: 9,
    40: 10, 54: 11, 62: 12, 55: 13, 32: 14, 34: 15, 8: 16, 3: 17, 29: 18,
    60: 19, 39: 20, 63: 21, 48: 22, 5: 23, 45: 24, 17: 25, 47: 26, 58: 27,
    31: 28, 49: 29, 28: 30, 43: 31, 23: 32, 27: 33, 4: 34, 41: 35, 52: 36,
    22: 37, 18: 38, 26: 39, 35: 40, 21: 41, 64: 42, 38: 43, 56: 44, 30: 45,
    50: 46, 14: 47, 20: 48, 42: 49, 59: 50, 61: 51, 53: 52, 37: 53, 57: 54,
    9: 55, 12: 56, 25: 57, 6: 58, 10: 59, 33: 60, 13: 61, 44: 62, 1: 63
}


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
fromhex_binary_lst = []
tohex_binary_lst = []
conn_h = connect_to_database('hexagrams.db')
conn_t = connect_to_database('trigrams.db')
question = "test mode"
true_random = False
question = "test mode"
binary_value = -1
classic_value = -1

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hq:rb:c:",
        [
            "help",
            "question=",
            "binary=",
            "classic=",
        ],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-q", "--question"):
        question = arg
    if opt in ("-r", "--true_random"):
        true_random = True
    if opt in ("-b", "--binary"):
        binary_value = int(arg)
        if binary_value <0 or classic_value >63:
            print("Binary value must be between 0 and 63 (inclusive)")
            showhelp()

    if opt in ("-c", "--classic"):
        classic_value = int(arg)
        if classic_value <1 or classic_value >64:
            print("Classic value must be between 1 and 64m (inclusive)")
            showhelp()


"""
Cast the lines
"""
for i in range(6):
    # print(binary_value,classic_value)
    if binary_value >=0 or classic_value > 0:  # binary strts with 0, classic starts with 1
        LineCall(bin=binary_value,hex=classic_value,position=i)  # this sets all the followings vars: asciipic_fr,asciipic_to,from_val,to_val
    else:
        LineCast()  # this sets all the followings vars: asciipic_fr,asciipic_to,from_val,to_val
    line_vals.append(LineValue)
    visual_from.append(asciipic_fr)
    visual_to.append(asciipic_to)
    fromhex_binary_lst.append(from_val)
    tohex_binary_lst.append(to_val)


"""
print for ANSI screen
"""

ansi_header = f"""
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│{fg.LIGHTWHITE_EX}Question: {fg.LIGHTRED_EX}{question:89s}{fg.RESET}│
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
print(ansi_header)

# print(f"{fg.LIGHTWHITE_EX}Question: {fg.LIGHTRED_EX}{question}{fg.RESET}")
print_interp(visual_from,fromhex_binary_lst,line_vals,1)
if is_moving_lines(line_vals):
    print_interp(visual_to,tohex_binary_lst,line_vals,2)

# print for markdown file screen


filename = "Q_"+string_to_filename(question)+".md"

f = open(filename,"w")
f.write(f"# Question: {question}\n")

markdown_interp(f,visual_from, fromhex_binary_lst, line_vals,1)
if is_moving_lines(line_vals):
    markdown_interp(f,visual_to, tohex_binary_lst, line_vals,2)
f.close


fromhex_bVal = binary_to_decimal(''.join(map(str, fromhex_binary_lst)))
fromhex_cVal = b2c_dict[fromhex_bVal]
tohex_bVal = binary_to_decimal(''.join(map(str, tohex_binary_lst)))
tohex_cVal = b2c_dict[tohex_bVal]


"""
HANDLE THE COMMENTS STUFF
"""

ansi_footer = f"""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""
print(ansi_footer)

print(f"Output written to {filename}")

if is_moving_lines(line_vals):
    addc = f"""

    To add a comment:

    ./update.py -b {fromhex_bVal} --comment '#1 "cause" of the pair b{fromhex_bVal}:b{tohex_bVal} (c{fromhex_cVal}:b{tohex_cVal}) "{get_hexagram_val_by_bseq('trans',fromhex_bVal)}" ⮕ "{get_hexagram_val_by_bseq('trans',tohex_bVal)}"'
    ./update.py -b {fromhex_bVal} --comment '#2 "effect" of the pair b{fromhex_bVal}:b{tohex_bVal} (c{fromhex_cVal}:b{tohex_cVal}) "{get_hexagram_val_by_bseq('trans',fromhex_bVal)}" ⮕ "{get_hexagram_val_by_bseq('trans',tohex_bVal)}"'
    """
else:
    addc = f"""

    To add a comment (from 'latest_comment.txt'):

    ./update.py -b {fromhex_bVal} --comment 'Non-moving hexagram of b{fromhex_bVal} (c{fromhex_cVal}) "{get_hexagram_val_by_bseq('trans',fromhex_bVal)}"'
    """

print(addc)

