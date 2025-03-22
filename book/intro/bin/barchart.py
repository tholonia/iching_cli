#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')

# Increase font sizes globally by 100%
plt.rcParams.update({
    'font.size': 20,  # Default font size is usually around 10
    'axes.titlesize': 24,  # Title font size
    'axes.labelsize': 22,  # Label font size
    'xtick.labelsize': 20,  # X-tick label size
    'ytick.labelsize': 20,  # Y-tick label size
    'legend.fontsize': 20,  # Legend font size
})

# Create the dataframe from the new data
data = [
    {'Pos': 1, 'Qtr SW': 1, 'Qtr NW': 6, 'Qtr NE': 62, 'Qtr SE': 57},
    {'Pos': 2, 'Qtr SW': 2, 'Qtr NW': 5, 'Qtr NE': 61, 'Qtr SE': 58},
    {'Pos': 3, 'Qtr SW': 3, 'Qtr NW': 4, 'Qtr NE': 60, 'Qtr SE': 59},
    {'Pos': 4, 'Qtr SW': 8, 'Qtr NW': 15, 'Qtr NE': 55, 'Qtr SE': 48},
    {'Pos': 5, 'Qtr SW': 9, 'Qtr NW': 14, 'Qtr NE': 54, 'Qtr SE': 49},
    {'Pos': 6, 'Qtr SW': 10, 'Qtr NW': 13, 'Qtr NE': 53, 'Qtr SE': 50},
    {'Pos': 7, 'Qtr SW': 11, 'Qtr NW': 12, 'Qtr NE': 52, 'Qtr SE': 51},
    {'Pos': 8, 'Qtr SW': 16, 'Qtr NW': 23, 'Qtr NE': 47, 'Qtr SE': 40},
    {'Pos': 9, 'Qtr SW': 17, 'Qtr NW': 22, 'Qtr NE': 46, 'Qtr SE': 41},
    {'Pos': 10, 'Qtr SW': 18, 'Qtr NW': 21, 'Qtr NE': 45, 'Qtr SE': 42},
    {'Pos': 11, 'Qtr SW': 19, 'Qtr NW': 20, 'Qtr NE': 44, 'Qtr SE': 43},
    {'Pos': 12, 'Qtr SW': 24, 'Qtr NW': 31, 'Qtr NE': 39, 'Qtr SE': 32},
    {'Pos': 13, 'Qtr SW': 25, 'Qtr NW': 30, 'Qtr NE': 38, 'Qtr SE': 33},
    {'Pos': 14, 'Qtr SW': 26, 'Qtr NW': 29, 'Qtr NE': 37, 'Qtr SE': 34},
    {'Pos': 15, 'Qtr SW': 27, 'Qtr NW': 28, 'Qtr NE': 36, 'Qtr SE': 35}
]

df = pd.DataFrame(data)

# Create the horizontal bar chart with no white space between lines
def create_horizontal_bar_chart(df):
    # Set up the figure with appropriate size - increased to accommodate larger fonts
    plt.figure(figsize=(32, 16))

    # Create a colormap with brighter, more contrasting colors
    colors = {
        'Qtr SE': '#00CC66',  # Bright green
        'Qtr NE': '#3366FF',  # Bright blue
        'Qtr NW': '#FF3333',  # Bright red
        'Qtr SW': '#FF9900'   # Bright orange
    }

    # Use the original dataframe order (no reversal)
    # This will put position 1 at the bottom and 15 at the top

    # Calculate positions
    positions = df['Pos'].values
    num_positions = len(positions)
    y_pos = np.arange(num_positions)
    y_labels = positions  # Use original order

    # Set bar width to exactly 1/4 of the available space
    bar_width = 0.25

    # Plot each quarter as a separate horizontal bar with exact positioning
    for i, col in enumerate(['Qtr SE', 'Qtr NE', 'Qtr NW', 'Qtr SW']):
        # Position each quarter's bar directly next to each other
        offset = i * bar_width - 0.5 + (bar_width / 2)
        # Use negative values to reverse the x-axis direction
        plt.barh(y_pos + offset, -df[col], label=col, color=colors[col],
                 height=bar_width, align='center')

    # Set the y-ticks and labels
    plt.yticks(y_pos, y_labels)
    plt.xlabel('Hex (binary value)')
    plt.ylabel('Position in Quarter')

    # Reverse X-axis labels
    plt.gca().invert_xaxis()

    # Update x-tick labels to show positive values
    current_ticks = plt.gca().get_xticks()
    plt.gca().set_xticklabels([int(abs(x)) for x in current_ticks])

    # Add a title
    plt.title('Position by Hex bVal')

    # Add legend to the right side
    plt.legend(loc='center right', bbox_to_anchor=(1.25, 0.5))

    # Adjust layout
    plt.tight_layout()

    return plt.gcf()

# Create the bar chart
bar_chart = create_horizontal_bar_chart(df)

# Save the figure
bar_chart.savefig('horizontal_bar_chart.png', bbox_inches='tight')

# Show the plot
plt.show()