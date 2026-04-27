import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="GM403 Radar Simulator", layout="wide")

# --- CSS CUSTOM UNTUK LOOK & FEEL MILITER ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1a1c24; padding: 10px; border-radius: 5px; border-left: 5px solid #00b0f0; }
    </style>
    """, unsafe_allow_html=True)

# --- DISCLAIMER ---
st.title("📡 GM403-Inspired S-Band Radar Simulator")
st.caption("Modelling Engineer Portfolio: Naufal Suryo Saputro (UGM)")
st.warning("⚠️ EDUCATIONAL SIMULATION — Not based on classified GM403 specifications. Based on public radar engineering principles.")

# --- SIDEBAR PARAMETERS ---
with st.sidebar:
    st.header("🕹️ Radar Control")
    fc = st.slider("Center Frequency (GHz)", 2.0, 4.0, 3.0) * 1e9
    P_tx = st.number_input("Peak Power (W)", value=10000)
    bw = st.slider("Bandwidth (MHz)", 1, 10, 2) * 1e6
    pfa = st.select_slider("Prob. False Alarm (Pfa)", options=[1e-4, 1e-5, 1e-6, 1e-7, 1e-8], value=1e-6)
    
    st.header("🎯 Target Scenario")
    target_type = st.selectbox("Select Focus Target", ["Fighter Jet", "UAV", "Helicopter", "Cruise Missile"])

# --- CONSTANTS ---
C = 3e8
R_MAX = 470e3
FS = 20e6
TAU = 10e-6

# --- RADAR MATH FUNCTIONS ---
def db(x): return 10 * np.log10(np.maximum(x, 1e-30))
def idb(x): return 10 ** (x / 10)

def generate_signal(target_range, rcs):
    # LFM Pulse
    t = np.linspace(0, TAU, int(TAU * FS))
    k = bw / TAU
    lfm = np.exp(1j * np.pi * k * t**2)
    
    # Range Profile
    n_samples = int(2 * R_MAX / C * FS)
    rx = np.zeros(n_samples, dtype=complex)
    n_del = int((2 * target_range / C) * FS)
    
    # SNR Calculation (Simplified)
    snr_lin = (P_tx * (idb(35)**2) * (C/fc)**2 * rcs) / ((4*np.pi)**3 * target_range**4 * 1.38e-23 * 290 * bw * idb(4))
    
    # Insert target if within range
    if n_del + len(lfm) < n_samples:
        rx[n_del : n_del + len(lfm)] = np.sqrt(snr_lin) * lfm
        
    # Noise
    noise = (np.random.randn(n_samples) + 1j*np.random.randn(n_samples)) / np.sqrt(2)
    rx += noise
    
    # Matched Filter
    mf = np.conj(lfm[::-1])
    rx_mf = np.convolve(rx, mf, mode='same')
    
    return np.abs(rx_mf), db(snr_lin)

# --- SIMULATION DATA ---
targets = {
    "Fighter Jet": {"R": 120e3, "az": 45, "el": 8, "RCS": 5.0, "color": "cyan"},
    "UAV": {"R": 80e3, "az": 120, "el": 3, "RCS": 0.05, "color": "orange"},
    "Helicopter": {"R": 60e3, "az": 200, "el": 1.5, "RCS": 3.0, "color": "purple"},
    "Cruise Missile": {"R": 200e3, "az": 310, "el": 0.5, "RCS": 0.1, "color": "red"}
}

# --- UI LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📦 Module 1 & 2: Signal Processing")
    tgt = targets[target_type]
    mag, snr_val = generate_signal(tgt["R"], tgt["RCS"])
    
    # CA-CFAR
    n_ref = 16
    n_guard = 4
    alpha = n_ref * (pfa**(-1/n_ref) - 1)
    
    # Optimasi CFAR sederhana untuk visualisasi
    threshold = np.convolve(mag, np.ones(n_ref+n_guard)/n_ref, mode='same') * alpha
    
    fig_sig, ax_sig = plt.subplots(figsize=(10, 4), facecolor='#0e1117')
    ax_sig.set_facecolor('#0e1117')
    r_km = np.linspace(0, R_MAX/1e3, len(mag))
    
    # Zoom ke area target
    zoom_range = [tgt["R"]/1e3 - 20, tgt["R"]/1e3 + 20]
    mask = (r_km > zoom_range[0]) & (r_km < zoom_range[1])
    
    ax_sig.plot(r_km[mask], mag[mask], color='#00b0f0', label="Matched Filter Output")
    ax_sig.plot(r_km[mask], threshold[mask], color='red', linestyle='--', label="CFAR Threshold")
    ax_sig.set_xlabel("Range (km)", color="white")
    ax_sig.set_ylabel("Magnitude", color="white")
    ax_sig.tick_params(colors='white')
    ax_sig.legend()
    st.pyplot(fig_sig)
    
    st.metric("Estimated SNR", f"{snr_val:.2f} dB", delta="Optimal" if snr_val > 13 else "Low")

with col2:
    st.subheader("🌐 Module 3: 3D Air Picture")
    
    fig_3d = go.Figure()
    
    # Plot Tracks
    for name, t_data in targets.items():
        # Generate dummy track points
        z = t_data["R"] * np.sin(np.radians(t_data["el"])) / 1e3
        x = t_data["R"] * np.cos(np.radians(t_data["el"])) * np.sin(np.radians(t_data["az"])) / 1e3
        y = t_data["R"] * np.cos(np.radians(t_data["el"])) * np.cos(np.radians(t_data["az"])) / 1e3
        
        fig_3d.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers+text',
            marker=dict(size=8, color=t_data["color"]),
            name=name,
            text=[name],
            textposition="top center"
        ))
    
    # Radar Center
    fig_3d.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], marker=dict(size=10, color='white', symbol='diamond'), name="GM403 Site"))

    fig_3d.update_layout(
        scene=dict(
            xaxis_title="East (km)", yaxis_title="North (km)", zaxis_title="Alt (km)",
            bgcolor="#0e1117"
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        template="plotly_dark"
    )
    st.plotly_chart(fig_3d, use_container_width=True)

# --- BOTTOM TABLE ---
st.subheader("📋 Detection Log (Real-time)")
df = pd.DataFrame([
    {"Target": k, "Range (km)": v["R"]/1e3, "RCS (m2)": v["RCS"], "Azimuth": v["az"]} 
    for k, v in targets.items()
])
st.table(df)
