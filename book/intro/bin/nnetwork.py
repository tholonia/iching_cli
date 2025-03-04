#!/bin/env python3

import networkx as nx
import matplotlib
matplotlib.use('TkAgg')  # Use interactive backend if available
import matplotlib.pyplot as plt
import argparse

def generate_bifurcation_graph(levels=5, connect='C'):
    """
    Generate a graph that starts with 1 node and bifurcates at each level.
    connect: 'C' for connecting parent to its 2 children,
             'c' for connecting parent to all children on the next level,
             'a' for connecting each node to every other node at all levels.
    """
    G = nx.DiGraph()
    positions = {}  # Store positions for visualization
    current_nodes = [0]  # Start with a single root node
    positions[0] = (0, 0)  # Initial position of the root node

    node_count = 1  # Node counter

    for level in range(1, levels):
        next_nodes = []
        num_nodes = 2 ** level  # Number of nodes at this level
        # Centered Y positions based on the total number of nodes
        y_positions = [(i - (num_nodes - 1) / 2) * 10 for i in range(num_nodes)]  # Adjusted for centering

        for i, parent in enumerate(current_nodes):
            # Create two child nodes for each parent
            for j in range(2):
                G.add_edge(parent, node_count)  # Connect parent to child
                positions[node_count] = (level, y_positions.pop(0))  # Assign vertical position
                next_nodes.append(node_count)
                node_count += 1

        # Center the root node vertically between its two children
        if level == 1:  # Only do this for the first bifurcation
            child_y_avg = (positions[next_nodes[0]][1] + positions[next_nodes[1]][1]) / 2
            positions[0] = (0, child_y_avg)  # Update root position

        # Connect nodes based on the connect flag
        if connect == 'C':
            for i in range(len(current_nodes)):
                parent = current_nodes[i]
                # Connect only to the two children created for this parent
                G.add_edge(parent, next_nodes[i * 2])  # First child
                G.add_edge(parent, next_nodes[i * 2 + 1])  # Second child
        elif connect == 'c':
            for parent in current_nodes:
                for child in next_nodes:  # Connect to all children at the next level
                    G.add_edge(parent, child)
        elif connect == 'a':
            # Connect each node to every other node at all levels
            all_nodes = list(range(node_count))  # Get all nodes created so far
            for i in range(len(all_nodes)):
                for j in range(i + 1, len(all_nodes)):
                    G.add_edge(all_nodes[i], all_nodes[j])  # Connect every node to every other node

        current_nodes = next_nodes

    return G, positions

def plot_graph(G, positions, output_file="bifurcation_graph.png"):
    plt.figure(figsize=(6, 6))  # Set canvas size to 6 by 6

    # Calculate node sizes based on their level
    node_sizes = [300 / (level + 1) for level in [pos[0] for pos in positions.values()]]  # Smaller for deeper levels

    # Create a subgraph excluding the first node (root)
    G_sub = G.subgraph(list(G.nodes)[1:])  # Exclude the first node

    nx.draw(G_sub, pos={k: v for k, v in positions.items() if k != 0}, with_labels=False,
             node_size=node_sizes[1:], node_color='green', edge_color='gray', arrows=True)  # Set node_color to green
    plt.axis('off')
    plt.savefig(output_file)  # Save the plot to a file
    plt.show()  # Display the plot

# Argument parser to handle command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a bifurcation graph.')
    parser.add_argument('--connect', type=str, choices=['C', 'c', 'a'], default='C',
                        help="Connection type: 'C' for parent to 2 children, 'c' for parent to all next level children, 'a' for all-to-all connections.")
    args = parser.parse_args()

    # Generate and plot the bifurcation graph
    G, positions = generate_bifurcation_graph(connect=args.connect)
    plot_graph(G, positions)
