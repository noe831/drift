import numpy as np
import matplotlib.pyplot as plt

# Define parameters for first case
l1, l2 = 100.0, 100.0  # Lengths of segments  
epsilon = 0.05 # Threshold for action, safety halt  

def calculate_det_j(theta1, theta2):
    return l1 * l2 * np.sin(theta2)

t1 = np.linspace(-np.pi, np.pi, 100)
t2 = np.linspace(-np.pi, np.pi, 100)
T1, T2 = np.meshgrid(t1, t2)
Z = calculate_det_j(T1, T2)

# Plot the safe operating envelope
plt.figure(figsize=(10, 8))
cp = plt.contourf(T1, T2, np.abs(Z), cmap='viridis', levels=20)
plt.colorbar(cp, label='|det(J)| - Dexterity Metric')
plt.title(r'Safe Operating Envelope ($\Omega$)')
plt.xlabel('Joint 1 Angle (rad)')
plt.ylabel('Joint 2 Angle (rad)')

# Draw the boundary (deterministic halt)
plt.contour(T1, T2, np.abs(Z), levels=[epsilon], colors='red', linestyles='dashed')
plt.text(0, 0, 'Singularity Line', color='red', fontweight='bold')

plt.show()
