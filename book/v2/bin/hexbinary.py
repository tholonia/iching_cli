#!/bin/env python3

wen_values = {
    1: [1, 63, "111111", 6],
    2: [2, 0, "000000", 0],
    3: [3, 17, "010001", 2],
    4: [4, 34, "100010", 2],
    5: [5, 23, "010111", 4],
    6: [6, 58, "111010", 4],
    7: [7, 2, "000010", 2],
    8: [8, 16, "010000", 1],
    9: [9, 55, "110111", 5],
    10: [10, 59, "111011", 5],
    11: [11, 7, "000111", 3],
    12: [12, 56, "111000", 3],
    13: [13, 61, "111101", 5],
    14: [14, 47, "101111", 5],
    15: [15, 4, "000100", 1],
    16: [16, 8, "001000", 1],
    17: [17, 25, "011001", 3],
    18: [18, 38, "100110", 3],
    19: [19, 3, "000011", 2],
    20: [20, 48, "110000", 2],
    21: [21, 41, "101001", 3],
    22: [22, 37, "100101", 3],
    23: [23, 32, "100000", 1],
    24: [24, 1, "000001", 1],
    25: [25, 57, "111001", 4],
    26: [26, 39, "100111", 4],
    27: [27, 33, "100001", 2],
    28: [28, 30, "011110", 4],
    29: [29, 18, "010010", 2],
    30: [30, 45, "101101", 4],
    31: [31, 28, "011100", 3],
    32: [32, 14, "001110", 3],
    33: [33, 60, "111100", 4],
    34: [34, 15, "001111", 4],
    35: [35, 40, "101000", 2],
    36: [36, 5, "000101", 2],
    37: [37, 53, "110101", 4],
    38: [38, 43, "101011", 4],
    39: [39, 20, "010100", 2],
    40: [40, 10, "001010", 2],
    41: [41, 35, "100011", 3],
    42: [42, 49, "110001", 3],
    43: [43, 31, "011111", 5],
    44: [44, 62, "111110", 5],
    45: [45, 24, "011000", 2],
    46: [46, 6, "000110", 2],
    47: [47, 26, "011010", 3],
    48: [48, 22, "010110", 3],
    49: [49, 29, "011101", 4],
    50: [50, 46, "101110", 4],
    51: [51, 9, "001001", 2],
    52: [52, 36, "100100", 2],
    53: [53, 52, "110100", 3],
    54: [54, 11, "001011", 3],
    55: [55, 13, "001101", 3],
    56: [56, 44, "101100", 3],
    57: [57, 54, "110110", 4],
    58: [58, 27, "011011", 4],
    59: [59, 50, "110010", 3],
    60: [60, 19, "010011", 3],
    61: [61, 51, "110011", 4],
    62: [62, 12, "001100", 2],
    63: [63, 21, "010101", 3],
    64: [64, 42, "101010", 3]
}

# Create dictionary mapping first value to second value from wen_values
wen_ary = {v[0]: v[1] for k, v in wen_values.items()}
# Create dictionary mapping second value to first value from wen_values
bin_ary = {v[1]: v[0] for k, v in wen_values.items()}

width = "50px"
border_color = "#ddd"

html_output = f"""<div style="display: flex; justify-content: space-around; gap: 0;">
    <table style="border-collapse: collapse; border: 1px solid {border_color}; margin: 0;">
        <tr><th style="border: 1px solid {border_color}; width: {width}; text-align: center;">Key</th><th style="border: 1px solid {border_color}; width: {width}; text-align: center;">Value</th></tr>"""
sorted_keys = sorted(wen_ary.keys())
for key in sorted_keys[:32]:
    html_output += f'\n        <tr><td style="border: 1px solid {border_color}; width: {width}; text-align: center;">{key}</td><td style="border: 1px solid {border_color}; width: {width}; text-align: center;">{wen_ary[key]}</td></tr>'
html_output += f"""\n    </table>
    <table style="border-collapse: collapse; border: 1px solid {border_color}; margin: 0;">
        <tr><th style="border: 1px solid {border_color}; width: {width}; text-align: center;">Key</th><th style="border: 1px solid {border_color}; width: {width}; text-align: center;">Value</th></tr>"""
for key in sorted_keys[32:]:
    html_output += f'\n        <tr><td style="border: 1px solid {border_color}; width: {width}; text-align: center;">{key}</td><td style="border: 1px solid {border_color}; width: {width}; text-align: center;">{wen_ary[key]}</td></tr>'
html_output += f"""\n    </table>
</div>"""


html_output2 = f"""<div style="display: flex; justify-content: space-around; gap: 0;">
    <table style="border-collapse: collapse; border: 1px solid {border_color}; margin: 0;">
        <tr><th style="border: 1px solid {border_color}; width: {width}; text-align: center;">Key</th><th style="border: 1px solid {border_color}; width: {width}; text-align: center;">Value</th></tr>"""
sorted_keys = sorted(bin_ary.keys())
for key in sorted_keys[:32]:
    html_output2 += f'\n        <tr><td style="border: 1px solid {border_color}; width: {width}; text-align: center;">{key}</td><td style="border: 1px solid {border_color}; width: {width}; text-align: center;">{bin_ary[key]}</td></tr>'
html_output2 += f"""\n    </table>
    <table style="border-collapse: collapse; border: 1px solid {border_color}; margin: 0;">
        <tr><th style="border: 1px solid {border_color}; width: {width}; text-align: center;">Key</th><th style="border: 1px solid {border_color}; width: {width}; text-align: center;">Value</th></tr>"""
for key in sorted_keys[32:]:
    html_output2 += f'\n        <tr><td style="border: 1px solid {border_color}; width: {width}; text-align: center;">{key}</td><td style="border: 1px solid {border_color}; width: {width}; text-align: center;">{bin_ary[key]}</td></tr>'
html_output2 += """\n    </table>
</div>"""





print(f"""<div style="display: flex; justify-content: space-around; gap: 20px;">
    <div style="flex: 1;">
        <h3 style="text-align: center;">King Wen to Binary</h3>
        <<<<{html_output}
    </div>
    <div style="flex: 1;">
        <h3 style="text-align: center;">Binary to King Wen</h3>
        >>>>{html_output2}
    </div>
</div>""")

