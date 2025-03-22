#!/usr/bin/env python3

import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import networkx as nx
import pandas as pd

# Try to import ace_tools, but provide a fallback if it's not available
try:
    import ace_tools as tools
except ModuleNotFoundError:
    # Create a simple replacement for the display_dataframe_to_user function
    class ToolsReplacement:
        def display_dataframe_to_user(self, name, dataframe):
            print(f"\n{name}:")
            print(dataframe)

    tools = ToolsReplacement()
    print("Note: Using fallback for ace_tools module")

# Define vertices for a tetrahedron
tetrahedron_vertices = np.array([
    [1, 1, 1],    # Vertex 0
    [-1, -1, 1],  # Vertex 1
    [-1, 1, -1],  # Vertex 2
    [1, -1, -1]   # Vertex 3
])

# Create an inverted tetrahedron by reflecting it
inverted_tetrahedron_vertices = tetrahedron_vertices * -1

# Assign new values to the tetrahedra
tetra_values = [7, 6, 5, 4]  # Upper tetrahedron
inverted_tetra_values = [0, 1, 2, 3]  # Lower tetrahedron

# Create figure and 3D axis
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot original tetrahedron (7,6,5,4)
ax.scatter(*zip(*tetrahedron_vertices), color='blue', s=200)
ax.add_collection3d(Poly3DCollection([tetrahedron_vertices[[0, 1, 2]],
                                      tetrahedron_vertices[[0, 1, 3]],
                                      tetrahedron_vertices[[0, 2, 3]],
                                      tetrahedron_vertices[[1, 2, 3]]],
                                      alpha=0.3, linewidths=1.5, edgecolors='blue', facecolors='lightblue'))

# Plot inverted tetrahedron (0,1,2,3)
ax.scatter(*zip(*inverted_tetrahedron_vertices), color='red', s=200)
ax.add_collection3d(Poly3DCollection([inverted_tetrahedron_vertices[[0, 1, 2]],
                                      inverted_tetrahedron_vertices[[0, 1, 3]],
                                      inverted_tetrahedron_vertices[[0, 2, 3]],
                                      inverted_tetrahedron_vertices[[1, 2, 3]]],
                                      alpha=0.3, linewidths=1.5, edgecolors='red', facecolors='salmon'))

# Calculate offset for text labels - INCREASED to add more space around numbers
offset_factor = 0.5  # Increased from previous value

# Annotate vertices with large numbers - move text away from vertices
for i, value in enumerate(tetra_values):
    # Move label away from origin (center of the cube)
    direction = tetrahedron_vertices[i] / np.linalg.norm(tetrahedron_vertices[i])
    offset_pos = tetrahedron_vertices[i] + direction * offset_factor
    ax.text(*offset_pos, str(value), fontsize=24, color='black', ha='center', weight='bold')

for i, value in enumerate(inverted_tetra_values):
    # Move label away from origin (center of the cube)
    direction = inverted_tetrahedron_vertices[i] / np.linalg.norm(inverted_tetrahedron_vertices[i])
    offset_pos = inverted_tetrahedron_vertices[i] + direction * offset_factor
    ax.text(*offset_pos, str(value), fontsize=24, color='black', ha='center', weight='bold')

# Set plot limits and labels - expanded to accommodate larger offsets
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-2.0, 2.0)
ax.set_zlim(-2.0, 2.0)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_title("Dual Tetrahedral Mapping of VI Values", fontsize=14)

# Show the plot
plt.show()

# Define the OI and VI values based on the chart (example structure from the original image)
oi_values = np.array([7, 6, 5, 4, 3, 2, 1, 0])
vi_values = np.array([7, 0, 6, 1, 5, 2, 4, 3])  # The VI mapping from OI

# Create a mapping from OI to VI
oi_to_vi_mapping = dict(zip(oi_values, vi_values))

# Create a new structured layout for the VI values
# We attempt to position them in a way that reveals order (e.g., sorting, clustering transformations)
sorted_vi_indices = np.argsort(vi_values)  # Sort by VI values
reordered_vi = vi_values[sorted_vi_indices]  # Get ordered VI values

# Create a graph to show OI to VI transformation in a network
G = nx.DiGraph()

for oi, vi in oi_to_vi_mapping.items():
    G.add_edge(f"OI {oi}", f"VI {vi}")

# Draw the network to visualize relationships
plt.figure(figsize=(12, 10))  # Larger figure size
pos = nx.spring_layout(G, seed=42, k=1.5)  # Increased k value for more spacing

# Scale the positions to spread them out more
for p in pos:
    pos[p] = pos[p] * 1.5  # Scale positions by 1.5

nx.draw(G, pos,
       with_labels=True,
       node_color="lightblue",
       edge_color="gray",
       node_size=5000,  # Even larger nodes to accommodate bigger text
       font_size=30,    # Increased to 30 as requested
       font_weight='bold',  # Make font bold
       width=1.5,       # Thicker edges
       arrowsize=15,    # Larger arrows
       connectionstyle='arc3,rad=0.1')  # Curved edges for better visibility

plt.title("OI to VI Transformation Network", fontsize=18)
plt.tight_layout()
plt.show()

# Display a table to compare OI and VI values in an organized way
df = pd.DataFrame({"OI": oi_values, "VI": reordered_vi})
tools.display_dataframe_to_user(name="Reordered VI Chart", dataframe=df)
