#!/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")

# Parameter range for the full circle (0 to 2π)
theta = np.linspace(0, 2*np.pi, 1000)

# Radius varying with the sine function
radius = 1.5 + 0.5 * np.sin(6 * theta)  # Changed from 10 to 6 cycles

# Parametric equations
x = radius * np.cos(theta)
y = radius * np.sin(theta)

# Plotting
plt.figure(figsize=(8, 4))
plt.plot(x, y, label="Sine Wave on Circle")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Sine Wave Following a Circle of Radius 1.5")
plt.legend()
plt.axis("equal")
plt.ylim(-2.5, 2.5)
plt.grid(False)
plt.show()
