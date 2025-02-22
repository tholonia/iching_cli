#!/bin/env python3
from funcs_lib import wen_values


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

