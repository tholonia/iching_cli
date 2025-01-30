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
    """
    Divide a given number of Yarrow Stalks into two piles, EastPile and WestPile,
    optionally using true random numbers from random.org. The remainder of the
    west pile is added to the HandPile.

    Parameters:
    YarrowStalks (int): The total number of Yarrow Stalks to be divided.

    Returns:
    None
    Updates global vars
    """
    global HandPile, EastPile, WestPile
    global true_random
    # Divide YarrowStalks into EastPile and WestPile
    if true_random:
        WestPile = get_true_random_number(1, YarrowStalks)
    else:
        WestPile = random.randint(1, YarrowStalks)

    EastPile = YarrowStalks - WestPile

    # Subtract one from WestPile and add it to HandPile
    WestPile -= 1
    HandPile = 1

def DivideEastAndWest():
    """
    Calculate the remainders of the EastPile and WestPile when divided by 4,
    and update the HandPile with these remainders. If the remainders are 0,
    they are set to 4, per the rules of the Yarrow Stalk method.

    This function is used as a part of the Yarrow Stalk method to generate
    hexagrams according to I Ching divination. The piles and hands are divided
    and aggregated to determine the resulting hexagram line values.

    Returns:
    None
    Updates global vars

    """
    global EastRemainder, WestRemainder, HandPile
    EastRemainder = EastPile % 4
    WestRemainder = WestPile % 4
    if EastRemainder == 0:
        EastRemainder = 4
    if WestRemainder == 0:
        WestRemainder = 4
    HandPile += EastRemainder + WestRemainder

def LineCast():
    """
    Cast a line using the Yarrow Stalk method according to I Ching divination.

    This function performs the Yarrow Stalk method to determine the value of a
    line in a hexagram. It involves dividing stalks into piles and calculating
    specific remainders iteratively to derive the line's value. The final line
    value is then used to decide whether the line is 'weak' or 'strong' and whether
    it is a changing line.

    Updates global variables:
    Stalks, CountValue1, CountValue2, CountValue3, LineValue

    Returns:
    None
    """
    global Stalks, CountValue1, CountValue2, CountValue3, LineValue
    # Initial setup: remove one stalk and set it aside
    Stalks = 49

    # First division cycle
    DivideStalks(Stalks)
    DivideEastAndWest()

    # Determine CountValue1 based on remainders
    if EastRemainder + WestRemainder + 1 == 9:
        CountValue1 = 2
    elif EastRemainder + WestRemainder + 1 == 5:
        CountValue1 = 3

    # Reduce remaining stalks
    Stalks -= HandPile

    # Second division cycle
    DivideStalks(Stalks)
    DivideEastAndWest()

    # Determine CountValue2 based on remainders
    if EastRemainder + WestRemainder + 1 == 8:
        CountValue2 = 2
    elif EastRemainder + WestRemainder + 1 == 4:
        CountValue2 = 3

    # Further reduce remaining stalks
    Stalks -= HandPile

    # Third division cycle
    DivideStalks(Stalks)
    DivideEastAndWest()

    # Determine CountValue3 based on remainders
    if EastRemainder + WestRemainder + 1 == 8:
        CountValue3 = 2
    elif EastRemainder + WestRemainder + 1 == 4:
        CountValue3 = 3

    # Sum of count values to determine the line value
    LineValue = CountValue1 + CountValue2 + CountValue3

    # Determine the type and state of the line
    if LineValue == 6:
        DrawLine('weak', True)
        binaryVal = 0
    elif LineValue == 7:
        DrawLine('strong', False)
        binaryVal = 1
    elif LineValue == 8:
        DrawLine('weak', False)
        binaryVal = 0
    elif LineValue == 9:
        DrawLine('strong', True)
        binaryVal = 1

def decimal_to_six_digit_binary(decimal_number):
    """
    Convert a decimal number to a six-digit binary string.

    Parameters:
    decimal_number (int): The decimal number to convert, must be between 0 and 63 inclusive.

    Returns:
    str: A binary string representation of the decimal number, padded to six digits.

    Raises:
    ValueError: If the input decimal_number is not between 0 and 63 inclusive.
    """
    if decimal_number < 0 or decimal_number >= 64:
        raise ValueError("Number must be between 0 and 63 inclusive.")
    return format(decimal_number, '06b')

def LineCall(bin=-1, hex=-1, position=0):
    """
    Set the line representation based on the provided binary or hexadecimal values and the position.

    This function sets the global variables `asciipic_fr`, `asciipic_to`, `from_val`, and `to_val`
    to their corresponding line representations. If a classical hexagram value is provided, it is
    first converted to its binary representation.

    Parameters:
    bin (int): The binary value representing the hexagram (default: -1).
    hex (int): The classical hexagram value (default: -1).
    position (int): The position of the line in the hexagram (0-5).

    Returns:
    None
    """

    if hex > 0:
        # Convert classical hexagram number to binary if hex value is provided
        bin = c2b_dict[hex]

    # Convert the decimal (binary) value to a six-digit binary string
    binval = str(decimal_to_six_digit_binary(bin))

    # Determine the line type ('weak' or 'strong') based on the binary digit at the given position
    if binval[position] == "0":
        DrawLine('weak', False)
        binaryVal = 0
    if binval[position] == "1":
        DrawLine('strong', False)
        binaryVal = 1

def DrawLine(line, changing):
    """
    Draw a line for I Ching hexagrams with ANSI color codes, updating global variables for
    ASCII line representation and line transition states.

    This function updates the following global variables:
    - `asciipic_fr`: The initial ASCII representation of the line.
    - `asciipic_to`: The resulting ASCII representation of the line after the transition.
    - `from_val`: The initial value (0 for weak, 1 for strong) of the line.
    - `to_val`: The resulting value (0 for weak, 1 for strong) of the line after the transition.

    Parameters:
    line (str): The type of the line, either 'weak' or 'strong'.
    changing (bool): Whether the line is changing (True) or not (False).

    """
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
    """
    Convert a list of integers to a concatenated string of digits.

    Parameters:
    num_list (list of int): The list of integers to be converted.

    Returns:
    str: A string consisting of all the integers in the list concatenated together.

    Example:
    >>> lst2str([1, 2, 3])
    '123'
    >>> lst2str([9, 0, 8, 7])
    '9087'
    """
    concatenated_string = ''.join(map(str, num_list))
    return concatenated_string


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
    """
    Retrieve a specific value from the 'hexagrams' table in the database based on the given
    key and binary sequence index (bseq).

    This function queries the 'hexagrams' table for a particular column (specified by 'key')
    and binary sequence index (specified by 'idx'). It fetches the corresponding value,
    removes leading and trailing whitespace, and returns the cleaned string.

    Parameters:
    -----------
    key : str
        The column name in the 'hexagrams' table from which the value should be retrieved.
    idx : int
        The binary sequence index (bseq) used to filter the query.

    Returns:
    --------
    str
        The cleaned string value retrieved from the specified column of the 'hexagrams' table.

    Example:
    --------
    >>> value = get_hexagram_val_by_bseq('title', 42)
    >>> print(value)
    'Grace (R)'

    Notes:
    ------
    - Ensure that the global variable `conn_h` is an active connection object to the database.
    - The function strips any leading or trailing whitespace and newline characters from the result.

    Raises:
    -------
    IndexError
        If the query returns no results or the index is out of range.
    sqlite3.Error
        If there is an error executing the SQL query.
    """
    global conn_h
    # Construct the SQL query to select the desired value based on the column key and binary sequence index
    query = f"SELECT {key} FROM hexagrams WHERE bseq = {idx};"
    # Execute the query and fetch results
    results = execute_query(conn_h, query)
    # Convert the resulting value to string, remove leading/trailing spaces and newline characters
    stres = str(results[0][0])
    return stres.strip()

def get_trigram_val_by_bseq(key, idx):
    """
    Retrieves a specific value from the 'xref_trigrams' table in the database based on the given
    key and binary sequence index (bseq).

    This function queries the 'xref_trigrams' table for a particular column (specified by 'key')
    and binary sequence index (specified by 'idx'). It fetches the corresponding value,
    removes leading and trailing whitespace and newline characters, and returns the cleaned string.

    Parameters:
    -----------
    key : str
        The column name in the 'xref_trigrams' table from which the value should be retrieved.
    idx : int
        The binary sequence index (bseq) used to filter the query.

    Returns:
    --------
    str
        The cleaned string value retrieved from the specified column of the 'xref_trigrams' table.

    Example:
    --------
    >>> value = get_trigram_val_by_bseq('title', 3)
    >>> print(value)
    'The Abysmal Water'

    Notes:
    ------
    - Ensure that the global variable `conn_t` is an active connection object to the database.
    - The function strips any leading or trailing whitespace and newline characters from the result.

    Raises:
    -------
    IndexError
        If the query returns no results or the index is out of range.
    sqlite3.Error
        If there is an error executing the SQL query.
    """
    global conn_t
    # Construct the SQL query to select the desired value based on the column key and binary sequence index
    query = f"SELECT {key} FROM xref_trigrams WHERE bseq = {idx};"
    # Execute the query and fetch results
    results = execute_query(conn_t, query)
    # Convert the resulting value to string, remove leading/trailing spaces and newline characters
    cleaned_result = str(results[0][0]).strip()
    return cleaned_result

def is_moving_lines(line_vals):
    """
    Determine if there are any moving lines in the list of line values.

    In I Ching divination, a line value of 6 or 9 indicates a moving line.
    This function checks the given list of line values to see if any of
    them are moving lines.

    Parameters:
    -----------
    line_vals : list of int
        A list of integers representing the values of lines in a hexagram.
        The values are typically between 6 and 9 inclusive.

    Returns:
    --------
    bool
        True if there is at least one moving line (value of 6 or 9) in the list,
        otherwise False.

    Example:
    --------
    >>> line_vals = [7, 6, 8, 9, 7, 8]
    >>> has_moving_lines = is_moving_lines(line_vals)
    >>> print(has_moving_lines)
    True
    """
    return any(line_val in (6, 9) for line_val in line_vals)

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

def markdown_interp(f, hexlist, hexnum, line_vals, hexseq):
    """
    Outputs the hexagram and its details to a markdown file.

    Parameters:
    -----------
    f : file object
        The markdown file to write the hexagram details to.
    hexlist : list of str
        The list containing the ASCII representations of the hexagram lines.
    hexnum : list of int
        The list containing binary values (0 or 1) representing the hexagram.
    line_vals : list of int
        The list containing the numerical values (6, 7, 8, 9) of the hexagram lines.
    hexseq : int
        The sequence number (1 or 2) indicating whether it is the first or second hexagram.

    Returns:
    --------
    None
    """
    # Write the hexagram lines
    f.write("```\n")
    for line in hexlist:
        f.write(f"{remove_ansi_codes(line):10s}\n")
    f.write("```\n")

    # Get base 10 representation of hexagram and respective trigrams
    binary_base10 = binary_to_decimal(lst2str(hexnum))
    lower_tri_base10, upper_tri_base10 = hexagram_to_trigrams(hexnum)

    # Construct hexagram details
    hexagram_details = f"""
**TITLE**:    {get_hexagram_val_by_bseq('title', binary_base10)}
**TRANS**:    {get_hexagram_val_by_bseq('trans', binary_base10)}
**SEQUENCE**: {binary_base10} ({lst2str(fromhex_binary_lst)})
**ORDER**:    {get_hexagram_val_by_bseq('pseq', binary_base10)} (I-Ching order)

**UPPER_TRIGRAM**: {get_trigram_val_by_bseq('trans', upper_tri_base10)} ({get_trigram_val_by_bseq('title', upper_tri_base10)}), {get_trigram_val_by_bseq('t_element', upper_tri_base10)}, {get_trigram_val_by_bseq('polarity', upper_tri_base10)}, {get_trigram_val_by_bseq('planet', upper_tri_base10)}
**LOWER_TRIGRAM**: {get_trigram_val_by_bseq('trans', lower_tri_base10)} ({get_trigram_val_by_bseq('title', lower_tri_base10)}), {get_trigram_val_by_bseq('t_element', lower_tri_base10)}, {get_trigram_val_by_bseq('polarity', lower_tri_base10)}, {get_trigram_val_by_bseq('planet', lower_tri_base10)}

**EXPLANATION**:
> {get_hexagram_val_by_bseq('explanation', binary_base10)}

**JUDGMENT**:
> {get_hexagram_val_by_bseq('judge_old', binary_base10)}

**JUDGMENT EXPLANATION**:
> {get_hexagram_val_by_bseq('judge_exp', binary_base10)}

**COMMENTS**:
> {get_hexagram_val_by_bseq('comment', binary_base10)}
"""
    f.write(hexagram_details)

    if hexseq == 1:
        reversed_line_vals = list(reversed(line_vals))
        if is_moving_lines(line_vals):
            f.write("**MOVING LINES**\n")
            for index, value in enumerate(reversed_line_vals):
                if value in (6, 9):
                    f.write(f"**{get_hexagram_val_by_bseq(f'line_{index + 1}', binary_base10)}**\n")
                    f.write(f">*{get_hexagram_val_by_bseq(f'line_{index + 1}_org', binary_base10)}*\n")
                    f.write(f"{get_hexagram_val_by_bseq(f'line_{index + 1}_exp', binary_base10)}\n\n")
        else:
            f.write("**No Moving Lines**\n")


def remove_ansi_codes(input_string):
    """
    Remove ANSI escape codes from a given string.

    ANSI escape codes are used in terminal and console outputs to style text with colors, bolding, etc.
    These codes are not desirable in certain contexts, such as when processing or storing plain text.

    Parameters:
    -----------
    input_string : str
        The string from which to remove ANSI escape codes.

    Returns:
    --------
    str
        The input string with all ANSI escape codes removed.

    Example:
    --------
    >>> text_with_ansi = "\x1B[31mThis is red text\x1B[0m"
    >>> cleaned_text = remove_ansi_codes(text_with_ansi)
    >>> print(cleaned_text)
    'This is red text'
    """
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', input_string)


def string_to_filename(input_string, replace_with='_', max_length=16):
    """
    Convert a given string into a valid filename by replacing invalid characters and truncating to a specified length.

    This function replaces characters that are not allowed in filenames (e.g., < > : " / \\ | ? *) with a specified replacement character.
    It also trims leading and trailing whitespace from the resulting filename and ensures it does not exceed a given maximum length.

    Parameters:
    -----------
    input_string : str
        The original string to be converted into a valid filename.
    replace_with : str, optional
        The character to replace invalid filename characters with. Default is '_'.
    max_length : int, optional
        The maximum length of the resulting filename. Default is 16.

    Returns:
    --------
    str
        A valid filename string.

    Raises:
    -------
    ValueError
        If the input string results in an empty filename after replacing invalid characters.

    Example:
    --------
    >>> string_to_filename("Invalid:/Filename*Example", replace_with='_', max_length=20)
    'Invalid__Filename_Exa'
    """
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


def hexagram_to_trigrams(hexlst):
    """
    Split a hexagram into its lower and upper trigrams, returning their decimal values.

    In the I Ching divination system, a hexagram is a figure composed of six stacked horizontal lines,
    which can be broken down into two separate trigrams of three lines each. This function takes a
    list of binary values representing the hexagram lines and computes the decimal values for the
    lower and upper trigrams.

    Parameters:
    -----------
    hexlst : list of int
        A list containing six integers (0 or 1) representing the binary values of the hexagram lines.

    Returns:
    --------
    tuple of int
        A tuple containing two integers:
        - The decimal value of the lower trigram.
        - The decimal value of the upper trigram.

    Example:
    --------
    >>> hexlst = [1, 0, 1, 0, 1, 0]
    >>> lower, upper = hexagram_to_trigrams(hexlst)
    >>> print(lower, upper)
    5, 2

    Notes:
    ------
    - The first three values of the input list constitute the lower trigram.
    - The last three values of the input list constitute the upper trigram.

    Raises:
    -------
    ValueError
        If the input list does not contain exactly six elements or if any element is not 0 or 1.
    """

    # Validate input
    if len(hexlst) != 6:
        raise ValueError("Input list must contain exactly six elements.")
    if not all(x in (0, 1) for x in hexlst):
        raise ValueError("All elements in the input list must be either 0 or 1.")

    # Split into lower and upper trigrams
    lower_tri = hexlst[:3]
    upper_tri = hexlst[3:]

    # Convert binary trigrams to decimal values
    lval = binary_to_decimal(''.join(map(str, lower_tri)))
    uval = binary_to_decimal(''.join(map(str, upper_tri)))

    return lval, uval


#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#! ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

"""
These dictionaries ...

maps binary values (0 to 63) to their corresponding classical hexagram values (1 to 64)
used in the I Ching divination system. The keys represent the binary sequence index (bseq), and the values
represent the classical hexagram number (cseq).

maps classical hexagram values (1 to 64) to their corresponding binary values (0 to 63)
used in the I Ching divination system. The keys represent the classical sequence index (cseq), and the values
represent the binary hexagram number (bseq).

Each key-value pair in the dictionary allows for quick conversion from a binary representation, used for
internal computations and lookups, to the classical hexagram numbering system, which is often preferred in
traditional forms of I Ching interpretation.

# To get the classical hexagram number for the binary value 10:
classical_hexagram = b2c_dict[10]  # Returns 40

# To get the binary hexagram number for the classical value 40:
binary_hexagram = c2b_dict[40]  # Returns 10

"""
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
            "true_random",
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

Process each of the 6 lines of a hexagram, determining their visual and numerical representations.

This function determines whether to use a user-provided binary or classical hexagram value, or to cast lines
to generate the hexagrams. It updates the global variables `line_vals`, `visual_from`, `visual_to`,
`fromhex_binary_lst`, and `tohex_binary_lst` based on the outcome.

Depending on the chosen method (user-provided or random/casted), the function:
- Calls `LineCall` to set the line representations based on a provided binary or classical value.
- Calls `LineCast` to randomly determine the line representations using the Yarrow Stalk or similar method.

The global variables (`LineValue`, `asciipic_fr`, `asciipic_to`, `from_val`, and `to_val`) are updated
by these functions and appended to their respective lists.
"""
for i in range(6):
    if binary_value >= 0 or classic_value > 0:  # binary starts with 0, classic starts with 1
        LineCall(bin=binary_value, hex=classic_value, position=i)  # sets vars: asciipic_fr, asciipic_to, from_val, to_val
    else:
        LineCast()  # sets vars: asciipic_fr, asciipic_to, from_val, to_val
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

"""
example comment format:

    <comment> - CAUSE b50⮕b48 (c59⮕b20) "DISPERSION [DISSOLUTION]" ⮕ "CONTEMPLATION (VIEW)"
    <comment> - EFFECT b50⮕b48 (c59⮕b20) "DISPERSION [DISSOLUTION]" ⮕ "CONTEMPLATION (VIEW)"'
"""

if is_moving_lines(line_vals):
    addc = f"""jwmilton@protonmail.com

    To add a comment:

    ./update.py -b {fromhex_bVal} --comment '<comment>  - CAUSE b{fromhex_bVal}⮕b{tohex_bVal} (c{fromhex_cVal}⮕b{tohex_cVal}) "{get_hexagram_val_by_bseq('trans',fromhex_bVal)}" ⮕ "{get_hexagram_val_by_bseq('trans',tohex_bVal)}"'
    ./update.py -b {tohex_bVal} --comment '<comment> - EFFECT b{fromhex_bVal}⮕b{tohex_bVal} (c{fromhex_cVal}⮕b{tohex_cVal}) "{get_hexagram_val_by_bseq('trans',tohex_bVal)}" ⮕ "{get_hexagram_val_by_bseq('trans',tohex_bVal)}"'
    """
else:
    addc = f"""
    ./update.py -b {fromhex_bVal} --comment '<comment> - STATIC b{fromhex_bVal} (c{fromhex_cVal}) "{get_hexagram_val_by_bseq('trans',fromhex_bVal)}"'
    """

print(addc)

