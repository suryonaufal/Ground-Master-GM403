# GM403-Inspired S-Band 3D Air Surveillance Radar Simulator

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-green.svg)
![Industry](https://img.shields.io/badge/Industry-Defense%20&%20Aerospace-red.svg)

## 📌 Project Overview
This simulator models the core signal processing chain of an **S-Band AESA 3D Surveillance Radar**, inspired by the **Ground Master 403 (GM403)** Ground Control Interception (GCI) system. 

The project was developed to demonstrate competencies in radar waveform design, target detection algorithms (CFAR), and 3D track visualization—critical components in the collaboration between **PT Len Industri (Persero)** and Thales for the TNI AU's air defense modernization.

## 🛠 Features & Modules

### 1. S-Band Signal Modeling (Module 1)
* **Waveform Generation:** Linear Frequency Modulation (LFM) / Chirp pulse generation (S-band: 2.0 – 4.0 GHz).
* **Radar Range Equation:** Dynamic SNR calculation based on Radar Cross Section (RCS), Peak Power, and System Loss.
* **Matched Filter:** Pulse compression implementation to enhance range resolution and SNR.

### 2. Detection & CFAR (Module 2)
* **CA-CFAR Algorithm:** Cell-Averaging Constant False Alarm Rate implementation to maintain a stable Pfa in the presence of noise and clutter.
* **Threat Scenarios:** Pre-configured models for:
    * **Fighter Jet** (Large RCS, High Altitude)
    * **UAV** (Small RCS, Low Velocity)
    * **Helicopter** (Moderate RCS, Low Altitude)
    * **Cruise Missile** (Small RCS, High Velocity)

### 3. Interactive 3D Visualization (Module 3)
* **Interactive Dashboard:** Built with **Streamlit** for real-time parameter tuning.
* **3D Air Picture:** Spatial visualization of targets using **Plotly** (X, Y, Z coordinates).
* **PPI Display:** Range-Azimuth polar plot for situational awareness.

## 🚀 Quick Start

### Prerequisites
* Python 3.9 or higher
* Pip (Python Package Manager)

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/gm403-radar-simulator.git](https://github.com/yourusername/gm403-radar-simulator.git)
   cd gm403-radar-simulator
2. Install dependencies: pip install -r requirements.txt
3. Run the simulator: streamlit run app.py
   
