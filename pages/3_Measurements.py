import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

st.set_page_config(page_title="Wetenschappelijke Cranklengte Calculator", layout="centered")
st.title("🔬 Wetenschappelijke Cranklengte Calculator")

# --- Inputs ---
height = st.number_input("Lengte (cm)", 140, 220, 180)
inseam = st.number_input("Inseam (cm)", 60, 100, 86)
current_crank = st.number_input("Huidige cranklengte (mm)", 150, 200, 172)
cadence = st.number_input("Cadans (rpm)", 60, 120, 90)
power = st.number_input("Vermogen (W)", 50, 500, 250)

# Optioneel: merkkeuze voor crank
brand = st.selectbox("Crank merk", ["Shimano", "SRAM", "Andere"])

# --- Berekeningen ---
# Baseline methodes
obree_crank = height * 0.95
machine_crank = 1.25 * inseam + 65

# Cranklengtes voor grafiek
crank_lengths = np.arange(150, 181, 2.5)

# Kracht berekening
torque = power / (2 * np.pi * cadence / 60)  # Nm
force = torque / (crank_lengths / 1000)  # N

# Spieractiviteit simulatie (EMG benadering)
muscle_activity = {
    'Gluteus Maximus': np.exp(-0.01*(crank_lengths-170)**2),
    'Vastus Lateralis': np.exp(-0.015*(crank_lengths-170)**2),
    'Rectus Femoris': np.exp(-0.02*(crank_lengths-170)**2)
}

# --- Optimalisatie ---
def objective(crank_length):
    torque = power / (2*np.pi*cadence/60)
    force = torque / (crank_length/1000)
    efficiency = np.exp(-0.01*(crank_length-170)**2)
    return -efficiency*force

optimal_result = minimize(objective, 170, bounds=[(150,180)])
optimal_crank = optimal_result.x[0]

# --- Grafiek: Kracht vs. Cranklengte ---
st.subheader("📊 Kracht vs. Cranklengte")
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(crank_lengths, force, label='Benodigde kracht (N)')
ax.axvline(x=optimal_crank, color='r', linestyle='--', label=f'Optimaal: {optimal_crank:.1f} mm')
ax.scatter(current_crank, power / (2 * np.pi * cadence / 60) / (current_crank/1000), color='g', label="Huidige crank")
ax.set_xlabel("Cranklengte (mm)")
ax.set_ylabel("Kracht (N)")
ax.legend()
st.pyplot(fig)

# --- Grafiek: Spieractiviteit ---
st.subheader("💪 Gesimuleerde spieractiviteit per cranklengte")
fig2, ax2 = plt.subplots(figsize=(8,5))
for muscle, activity in muscle_activity.items():
    ax2.plot(crank_lengths, activity, label=muscle)
ax2.set_xlabel("Cranklengte (mm)")
ax2.set_ylabel("Relatieve spieractiviteit (gesimuleerd)")
ax2.legend()
st.pyplot(fig2)

# --- Output aanbevolen cranks ---
st.subheader("✅ Aanbevolen cranklengtes")
st.write(f"- Graeme Obree methode: {obree_crank:.1f} mm")
st.write(f"- 'Machine' methode: {machine_crank:.1f} mm")
st.write(f"- Optimalisatie kracht/cadans: {optimal_crank:.1f} mm")
st.write(f"- Huidige crank: {current_crank} mm")

# --- Gangbare cranklengtes per merk ---
st.subheader("🛠️ Gangbare cranklengtes")
cranks = {
    "Shimano": [160, 165, 167.5, 170, 172.5, 175],
    "SRAM": [160, 165, 170, 172.5, 175, 177.5]
}
if brand in cranks:
    st.write(f"{brand} cranklengtes: {cranks[brand]} mm")
else:
    st.write("Voer een cranklengte naar keuze in of gebruik andere merken.")

# --- Aanbeveling op basis cadans ---
st.subheader("💡 Aanbeveling")
if cadence > 95:
    st.write("Overweeg een kortere crank voor hogere cadans en betere aerodynamica.")
elif cadence < 85:
    st.write("Een langere crank kan gunstig zijn voor krachtigere pedaalslagen.")
else:
    st.write("Huidige cadans is neutraal, huidige crank waarschijnlijk geschikt.")
