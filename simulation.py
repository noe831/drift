import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from kinematic_verification_n import sovereign_observer, planar_2dof_fk

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'mathtext.fontset': 'stix'
})

def generate_telemetry_load(n_joints, duration_sec=10, frequency_hz=100):
    """
    Simulate real-time telemetry with noise
    """
    timestamps = np.linspace(0, duration_sec, duration_sec * frequency_hz)
    data = []
    
    for t in timestamps:
        q_sim = np.array([0.5 * np.cos(t)] * n_joints) 
        
        is_safe, det_J, dt = sovereign_observer(q_sim, planar_2dof_fk)
        
        data.append({
            "timestamp": t,
            "det_J": det_J,
            "latency_ms": dt,
            "status": "SAFE" if is_safe else "HALT"
        })
    return pd.DataFrame(data)

df = generate_telemetry_load(n_joints=2)
stewardship_ratio = len(df[df['status'] == 'SAFE']) / len(df)
print(f"Stewardship Ratio (K): {stewardship_ratio:.2f}")


def plot_results(df):
    plt.figure(figsize=(10, 6))
    
    # Plot Determinism Latency (Delta t)
    plt.subplot(2, 1, 1)
    plt.plot(df['timestamp'], df['latency_ms'], color='blue', label='Latency (ms)')
    plt.axhline(y=0.85, color='red', linestyle='--', label='Target (0.85ms)')
    plt.ylabel('Latency (ms)')
    plt.title('Real-Time Audit')
    plt.legend()

    # Plot Manipulability Index
    plt.subplot(2, 1, 2)
    plt.plot(df['timestamp'], df['det_J'], color='green', label='|det(J)|')
    plt.axhline(y=0.05, color='orange', linestyle='--', label='Halt Threshold (epsilon)')
    plt.ylabel(r'|\det(J)| - Dexterity Metric')
    plt.xlabel('Time (s)')
    plt.legend()

    plt.tight_layout()
    
    plt.xlabel('Time (s)', fontsize=10)
    plt.ylabel('Latency (ms)', fontsize=10)

    plt.savefig('prism_results_visual.png')
    print("SUCCESS: Graphic saved as drift_results_visual_1.png")

# After generating the dataframe
plot_results(df)
