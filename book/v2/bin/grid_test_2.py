#!/usr/bin/env python3

import sys
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt

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

# Create the plot
plt.figure(figsize=(10, 10))
# Use a colormap that goes from red to blue
plt.imshow(grid, cmap='RdYlBu_r', interpolation='nearest')
plt.title(f'Distribution of ones in {bit_width}-bit binary representation')
plt.xlabel('Lower value')
plt.ylabel('Upper value')
colorbar = plt.colorbar(label='Number of ones')
colorbar.set_ticks(range(bit_width + 1))

# Save the plot
output_file = f'grid_{size}x{size}_all_ones.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
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
