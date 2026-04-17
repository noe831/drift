import numpy as np
import time
import matplotlib.pyplot as plt

# Define parameters   
L1, L2 = 100.0, 100.0  # Length in mm
EPSILON = 0.05         # Determinant threshold for halt  

def planar_2dof_fk(q):
    """
    Forward kinematics for a 2-DOF planar manipulator
    """
    x = L1 * np.cos(q[0]) + L2 * np.cos(q[0] + q[1])
    y = L1 * np.sin(q[0]) + L2 * np.sin(q[0] + q[1])
    return np.array([x, y])

def get_det_j_numerical(q1, q2):
    q = np.array([q1, q2])
    eps = 1e-6
    x0 = planar_2dof_fk(q)
    J = np.zeros((2, 2))
    for i in range(2):
        q_eps = np.copy(q)
        q_eps[i] += eps
        J[:, i] = (planar_2dof_fk(q_eps) - x0) / eps
    return np.linalg.det(J)


def get_jacobian(q, forward_kinematics_func, epsilon=1e-6):
    """
    Numerically compute Jacobian J(theta)
    """
    n = len(q)
    x0 = forward_kinematics_func(q)
    J = np.zeros((len(x0), n))
    eps = 1e-6

    for i in range(n):
        q_eps = np.copy(q)
        q_eps[i] += eps
        J[:, i] = (forward_kinematics_func(q_eps) - x0) / eps
    return J

def sovereign_observer(q, fk_func):
    """
    The observer performs real-time auditing
    Returns safety status, manipulability index, and latency
    """
    start_time = time.perf_counter()
    
    J = get_jacobian(q, fk_func)
    det_J = np.linalg.det(J) if J.shape[0] == J.shape[1] else np.linalg.norm(J)
    
    # Singularity stress test
    epsilon = 0.05
    is_safe = np.abs(det_J) > epsilon    
    latency = (time.perf_counter() - start_time) * 1000  # in ms
    
    return is_safe, det_J, latency

# Simulation
for t in range(100):
    simulated_q = np.array([0.5, np.sin(t * 0.1)])
    safe, metric, dt = sovereign_observer(simulated_q, planar_2dof_fk)
    
    if not safe:
        print(f"DETERMINISTIC HALT TRIGGERED: metric={metric:.4f}, dt={dt:.4f}ms")
        break

# Create Grid
t1 = np.linspace(-np.pi, np.pi, 100)
t2 = np.linspace(-np.pi, np.pi, 100)
T1, T2 = np.meshgrid(t1, t2)
Z = np.vectorize(get_det_j_numerical)(T1, T2)

plt.rcParams.update({'font.size': 10, 'font.family': 'serif'})
plt.figure(figsize=(8, 6))

cp = plt.contourf(T1, T2, np.abs(Z), cmap='viridis', levels=20)
cbar = plt.colorbar(cp)
cbar.set_label(r'$|\det(J)|$ - Dexterity Metric', fontsize=10)

plt.title(r'Safe Operating Envelope ($\Omega$)')
plt.xlabel(r'Joint 1 Angle $\theta_1$ (rad)')
plt.ylabel(r'Joint 2 Angle $\theta_2$ (rad)')

plt.contour(T1, T2, np.abs(Z), levels=[EPSILON], colors='red', linestyles='dashed')
plt.text(0.1, 0.1, 'Halt Boundary', color='red', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('PRISM_Fig1_Envelope.png', dpi=300)
plt.show()
