#!/usr/bin/env python3

"""
Binary Pattern Target Analyzer and Visualizer

This script generates and visualizes a 2D grid highlighting positions where binary
numbers have a specific number of '1' bits. For a given grid size NxN and a target
number of ones, it:

1. Creates a grid where each cell represents a composite number formed by combining
   two values (upper and lower) into a single binary number
2. Marks cells (1/0) based on whether their binary representation contains exactly
   the target number of '1' bits
3. Generates a binary heatmap visualization showing matching positions
4. Outputs statistics about the overall distribution of '1' bits

Usage:
    ./grid_test.py <grid_size> <target_ones>

Arguments:
    grid_size:    Integer specifying the dimensions of the square grid (NxN)
    target_ones:  Integer specifying the desired number of '1' bits to match

Output:
    - Generates a binary plot saved as 'grid_<size>x<size>_ones_<target>.png'
    - Prints the distribution of '1' bits across all numbers in the grid
    - Uses binary colormap (black and white) for visualization

Example:
    ./grid_test.py 64 10  # Creates a 64x64 grid, highlighting numbers with 10 ones

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

# Check if both arguments are provided
if len(sys.argv) != 3:
    print("Usage: ./grid_test_2.py <grid_size> <target_ones>")
    print("Example: ./grid_test_2.py 64 10")
    sys.exit(1)

# Get parameters and validate
try:
    size = int(sys.argv[1])
    target_ones = int(sys.argv[2])
    if size <= 0:
        raise ValueError("Grid size must be positive")

    # Calculate required bits based on grid size
    max_value = (size - 1) * size  # Maximum possible value in grid
    bit_width = math.ceil(math.log2(max_value + 1))  # Number of bits needed

    if target_ones < 0 or target_ones > bit_width:
        raise ValueError(f"Target ones must be between 0 and {bit_width}")
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
        grid[upper, lower] = 1 if ones_count == target_ones else 0

# Create the plot
plt.figure(figsize=(10, 10))
plt.imshow(grid, cmap='binary')
plt.title(f'Grid showing positions with {target_ones} ones\nin {bit_width}-bit binary representation')
plt.xlabel('Lower value')
plt.ylabel('Upper value')
plt.colorbar(label='Has target number of ones')

# Save the plot to a file
output_file = f'grid_{size}x{size}_ones_{target_ones}.png'
plt.savefig(output_file)
plt.close()

print(f"\nPlot saved as: {output_file}")

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
