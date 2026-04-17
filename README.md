# The `Drift` Framework 

### Nothing Personal: Integrity for Medical Robotics

*Architecting the Independent Observer Pattern*

> In safety-critical systems, software intent is a promise; physical reality is the truth. The gap between them is where integrity fails.

This repository contains the `drift` framework, a decoupled **independent observer** system designed to bridge a reality gap in robotics. While traditional systems rely on self-reporting, this framework implements a *nothing personal* philosophy: an objective, impartial auditor that reconciles software commands with raw physical telemetry.

<details>
<summary><b>Why <i>Nothing Personal</i>? (The Architectural Philosophy)</b>
</summary>
<br>In systems engineering, <i>nothing personal</i> is a philosophy of architectural impartiality.<br><br>

We often assume a system's internal state is a source of truth, but in high-stakes robotics, a controller can be sincere but wrong. It executes a command and believes it is on target, while physical forces (drift) pull it off course. <i>Nothing personal</i> means the system refuses to trust its own internal story. <br><br>By decoupling the observer (the auditor) from the controllter (the actor), we ensure that the audit of the machine is objective and separated from the machine's intent. It's not just about data privacy - it's about data integrity.
</details>

### Problem: Reality Gap

In medical robotics, **state desynchronization** occurs when a system's internal logic and its physical position drift apart. 
* **Controller** assumes the arm is at position $P_1$
* **Actual Data** (due to jitter, latency, or mechanical wear) records the arm at position $P_2$
* **Risk:** In surgery, a 2mm drift is the difference between a successful biopsy and a clinical catastrophe

** Technical Glossary: The Blueprint of Trust**
To bridge the reality gap, `drift` implements a formal verification architecture based on the core pillars:

| Term | Definition | Metric of Success |
| :--- | :--- | :--- |
| **Safe Operating Envelope ($\Omega$)** | Bounded manifold where the system maintains kinematic integrity | $\|det(J)\|>\epsilon$ |
| **Stewardship Ratio ($\mathbb{K}$)** | Ratio of physical states verified by the independent auditor | $\mathbb{K} = 1.00$ (Target) |
| **Deterministic Halt** | An inhibitor that intercepts commands | $\Delta t < 1ms$ |

### Solution: Independent Observer Pattern

We solve this by decoupling the monitoring layer from the control layer. This ensures that the system's truth is never compromised by the complexity of its commands.

1. **Controller:** Implements high-level paths and logic
2. **Actual Data Stream:** Ingests raw hardware telemetry directly from the physical sensors
3. **Observer:** A decoupled node that reconciles the two in real-time and flags system drift before it becomes a failure

### Implementation

The core of this project is a telemetry auditor built in Python.

<details>
<summary><b>View Technical Proofs (SVD & Jacobian Analysis)</b></summary>
<br>

To ensure objective oversight in highly regulated environments, the audit engine utilizes:
* **Singular Value Decomposition (SVD):** Monitor the condition number $\kappa(J)$ of the system to ensure numerical stability
* **Jacobian Determinant Analysis:** The observer calculates $|det(J)|$ in real-time to identify state desynchronization before physical drift manifests
* **Deterministic Determinism:** By decoupling the hardware clock, achieve a reaction time ($\Delta t$) of **0.08ms**, fulfilling the safety-critical requirements of the independent observer pattern.
</details>


#### **Logic: Drift Formula**

The observer calculates the Jacobian determinant $|det(J)|$ of the system in real-time. This metric represents the safe operating envelope. If the determinant approaches zero, indicating a singularity or state desynchronization, the system triggers a deterministic halt.

#### Audit Trail: The Verifiable Receipt

The framework provides a high-frequency audit log. In recent stress tests, the system achieved a Stewardship Ratio $(K)$ of 1.00, meaning every move was successfully audited against physical truth.

```bash
# Validated Test Output:
[AUDIT] DETERMINISTIC HALT TRIGGERED: metric=0.0000, dt=0.0868ms
[AUDIT] Stewardship Ratio (K): 1.00
```

# Getting Started

Built for the **Your Next Win IWD Virtual Summit 2026**, this project aims to empower engineers to build safer, more resilient systems.

**Core Components**
* **`kinematic_verification_n.py` (The Trust-Core):** The primary logic for the observer
* **`simulation.py` (The Demo):** The test harness used to simulate the reality gap and trigger a halt signal
* **`drift_results_visual.png` (The Receipt):** The visual of sub-millisecond determinism

## Prerequisites
* Python 3.12+
* GCP Account (Recommended for rendering on `viz-engine`)
* FFmpeg (For video stitching)

## Installation
```bash
git clone https://github.com/noe831/drift.git
cd drift
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
