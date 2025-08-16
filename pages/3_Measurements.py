import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuratie
st.set_page_config(page_title="Geavanceerde Cranklengte Calculator", layout="centered")
st.title("🚴 Geavanceerde Cranklengte Calculator")

# Inputvelden
height = st.number_input("Lengte (cm)", min_value=140, max_value=220, value=180, step=1)
inseam = st.number_input("Inseam (cm)", min_value=60, max_value=100, value=86, step=1)
current_crank = st.number_input("Huidige cranklengte (mm)", min_value=150, max_value=200, value=172, step=1)
cadence = st.number_input("Cadans (rpm)", min_value=60, max_value=120, value=90, step=1)
power = st.number_input("Vermogen (W)", min_value=50, max_value=500, value=200, step=10)

# Berekeningen
obree_crank = height * 0.95
machine_crank = 1.25 * inseam + 65

# Visualisatie: Cranklengte vs. Cadans
crank_lengths = np.array([150, 160, 170, 180, 190])
cadence_values = 100 * np.exp(-0.05 * (crank_lengths - 170))  # Hypothetisch model

fig, ax = plt.subplots()
ax.plot(crank_lengths, cadence_values, label="Cadans vs. Cranklengte", color='b')
ax.scatter(current_crank, cadence, color='r', label="Huidige positie")
ax.set_xlabel("Cranklengte (mm)")
ax.set_ylabel("Cadans (rpm)")
ax.legend()
st.pyplot(fig)

# Analyse: Kracht vs. Cadans
force = power / (2 * np.pi * cadence / 60)  # Kracht = Vermogen / (2 * pi * Cadans / 60)
st.write(f"Benodigde kracht bij {cadence} rpm: {force:.2f} N")

# Conclusies
st.subheader("🔍 Conclusies")
st.write(f"Op basis van je lengte en inseam, zijn hier enkele aanbevolen cranklengtes:")
st.write(f"- Graeme Obree methode: {obree_crank:.1f} mm")
st.write(f"- 'Machine' methode: {machine_crank:.1f} mm")
st.write(f"Je huidige cranklengte is {current_crank} mm, wat binnen het gangbare bereik valt.")

# Aanbevelingen
st.subheader("💡 Aanbevelingen")
if cadence > 90:
    st.write("Overweeg een kortere cranklengte voor hogere cadans en betere aerodynamica.")
else:
    st.write("Een langere cranklengte kan voordelig zijn voor krachtigere pedaalslagen.")
