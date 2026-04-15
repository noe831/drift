# The `Drift` Framework 

### Nothing Personal: Integrity for Medical Robotics

*Architecting the Independent Observer Pattern*

> In safety-critical systems, software intent is a promise; physical reality is the truth. The gap between them is where integrity fails.

This repository contains the `drift` framework, a decoupled **independent observer** system designed to bridge a reality gap in robotics. While traditional systems rely on self-reporting, this framework implements a *nothing personal* philosophy: an objective, impartial auditor that reconciles software commands with raw physical telemetry.

<details>
<summary><b>Why *Nothing Personal*? (The Architectural Philosophy)</b>
</summary>
In systems engineering, *nothing personal* is a philosophy of architectural impartiality. The system should never "trust" its own control loop.

We often assume a system's internal state is a source of truth, but in high-stakes robotics, a controller can be sincere but wrong. It executes a command and believes it is on target, while physical forces (drift) pull it off course. *Nothing personal* means the system refuses to trust its own internal story. By decoupling the observer, we ensure that the audit of the machine is objective and separated from the machine's intent. It's not just about data privacy - it's about data integrity.
</details>

### Problem: Reality Gap

In medical robotics, **state desynchronization** occurs when a system's internal logic and its physical position drift apart. 
* **Controller** assumes the arm is at position $P_1$
* **Actual Data** (due to jitter, latency, or mechanical wear) records the arm at position $P_2$
* **Risk:** In surgery, a 2mm drift is the difference between a successful biopsy and a clinical catastrophe

### Solution: Independent Observer Pattern

We solve this by decoupling the monitoring layer from the control layer. This ensures that the system's truth is never compromised by the complexity of its commands.

1. **Controller:** Implements high-level paths and logic
2. **Actual Data Stream:** Ingests raw hardware telemetry directly from the physical sensors
3. **Observer:** A decoupled node that reconciles the two in real-time and flags system drift before it becomes a failure

### Implementation

The core of this project is a telemetry auditor built in Python and rendered via a distributed GCP pipeline.

#### **Logic: Drift Formula**

The observer calculates the distance ($\Delta$) between the software intent vector ($\vec{I}$) and the physical truth vector ($\vec{T}$):

$$\Delta = \sqrt{(x_I - x_T)^2 + (y_I - y_T)^2 + (z_I - z_T)^2}$$

#### Audit Trail

The system provides a terminal output designed for human oversight:
* `[AUDIT] DRIFT DETECTED: 1.14mm | STATUS: NOMINAL`
* `[AUDIT] DRIFT DETECTED: 2.05mm | STATUS: CRITICAL - INTERVENTION REQUIRED`

# Getting Started

Built for the **Your Next Win IWD Virtual Summit 2026**, this project aims to empower engineers to build safer, more resilient systems.

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
