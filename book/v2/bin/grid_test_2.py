#!/usr/bin/env python3

"""
Grid Binary Pattern Analyzer and Visualizer

This script generates and visualizes a 2D grid showing the distribution of '1' bits
in binary numbers. For a given grid size NxN, it:

1. Creates a grid where each cell represents a composite number formed by combining
   two values (upper and lower) into a single binary number
2. Counts the number of '1' bits in each resulting binary representation
3. Generates a heatmap visualization of the distribution
4. Outputs statistics about the frequency of different bit counts

Usage:
    ./grid_test_2.py <grid_size>

Arguments:
    grid_size: Integer specifying the dimensions of the square grid (NxN)

Output:
    - Generates a heatmap plot saved as 'grid_<size>x<size>_all_ones.png'
    - Prints the distribution of '1' bits across all numbers in the grid
    - Uses RdYlBu_r colormap (red to blue) for visualization

Example:
    ./grid_test_2.py 8  # Creates an 8x8 grid analysis

Note:
    The script automatically calculates the required bit width based on the
    maximum possible value in the grid ((size-1) * size).
"""

import sys
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from fractions import Fraction

def decimal_to_fraction(decimal):
    """Convert a decimal number to a simplified fraction string."""
    if math.isinf(decimal):
        return "∞"
    fraction = Fraction(decimal).limit_denominator()
    return f"{fraction.numerator}/{fraction.denominator}"

# Check if both arguments are provided
if len(sys.argv) != 2:  # Now only need grid size
    print("Usage: ./grid_test_2.py <grid_size>")
    print("Example: ./grid_test_2.py 8")
    sys.exit(1)

# Get parameters and validate
try:
    size = int(sys.argv[1])
    if size <= 0:
        raise ValueError("Grid size must be positive")

    # Calculate required bits based on grid size
    max_value = (size - 1) * size
    bit_width = math.ceil(math.log2(max_value + 1))

except ValueError as e:
    print(f"Error: {e}")
    print("Please provide valid integers")
    sys.exit(1)

print(f"Grid size: {size}x{size}, using {bit_width} bits for values")

# Initialize grid array
grid = np.zeros((size, size))

# Create the grid
for upper in range(size):
    for lower in range(size):
        value = (upper << (bit_width//2)) + lower
        binary = format(value, f'0{bit_width}b')
        ones_count = binary.count('1')
        grid[upper, lower] = ones_count

# Print the matrix of values that determine the colors
print("\nMatrix of '1' bit counts (determines color spectrum from red to blue):")
print("     " + "".join(f"{i:4}" for i in range(size)))  # Column headers
print("    " + "----" * size)  # Separator line
for i in range(size):
    print(f"{i:2d} |", end=" ")  # Row header
    for j in range(size):
        print(f"{int(grid[i,j]):3d}", end=" ")
    print()  # New line
print()  # Extra line for spacing

# Calculate and print Yin, Center, and Yang totals and their ratio
bit_width = math.ceil(math.log2(max_value + 1))  # Number of bits needed
threshold = bit_width / 2  # Center point for bit counts

# Center all values around zero by subtracting threshold
centered_grid = grid - threshold
yang_values = centered_grid[centered_grid > 0]
yin_values = centered_grid[centered_grid < 0]

# Print debug information about the values
# print(f"\nDebug information:")
# print(f"Grid shape: {grid.shape}")
# print(f"Unique values in grid: {np.unique(grid)}")
# print(f"Number of Yang values: {len(yang_values)}")
# print(f"Number of Yin values: {len(yin_values)}")
# print(f"Yang values: {sorted(yang_values)}")
# print(f"Yin values: {sorted(yin_values)}")

# Calculate average values to normalize the comparison
yang_avg = np.mean(yang_values) if len(yang_values) > 0 else 0
yin_avg = abs(np.mean(yin_values)) if len(yin_values) > 0 else 0  # Take absolute of average
total_avg = yang_avg + yin_avg

# Calculate normalized ratio
yang_ratio = yang_avg / total_avg if total_avg > 0 else 0
yin_ratio = yin_avg / total_avg if total_avg > 0 else 0

print(f"\nBit width: {bit_width}, threshold: {threshold:.1f}")
print(f"Average YANG value: {yang_avg:.3f} (count: {len(yang_values)})")
print(f"Average YIN value: {yin_avg:.3f} (count: {len(yin_values)})")
print(f"!!, {yang_ratio:.3f},{decimal_to_fraction(yang_ratio)},{yin_ratio:.3f},{decimal_to_fraction(yin_ratio)},{size}")
print()

# Create the plot
# plt.figure(figsize=(10, 10))
# # Use a colormap that goes from red to blue
# plt.imshow(grid, cmap='RdYlBu_r', interpolation='nearest')
# plt.title(f'Distribution of ones in {bit_width}-bit binary representation')
# plt.xlabel('Lower value')
# plt.ylabel('Upper value')
# colorbar = plt.colorbar(label='Number of ones')
# colorbar.set_ticks(range(bit_width + 1))

# # Save the plot
# output_file = f'grid_{size}x{size}_all_ones.png'
# plt.savefig(output_file, dpi=300, bbox_inches='tight')
# plt.close()

# print(f"\nPlot saved as: {output_file}")

# Calculate and print distribution
ones_distribution = [0] * (bit_width + 1)
for upper in range(size):
    for lower in range(size):
        value = (upper << (bit_width//2)) + lower
        binary = format(value, f'0{bit_width}b')
        ones_count = binary.count('1')
        ones_distribution[ones_count] += 1

print("\nDistribution of ones in binary representations:")
for i in range(bit_width + 1):
    if ones_distribution[i] > 0:
        print(f"Numbers with {i:2d} ones: {ones_distribution[i]:4d}")
