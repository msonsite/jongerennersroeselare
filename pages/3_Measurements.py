import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

st.set_page_config(page_title="Wetenschappelijke Cranklengte Tool", layout="wide")
st.title("🔬 Wetenschappelijke Cranklengte Calculator")

# --- Input ---
st.sidebar.header("🚴‍♂️ Fietsersgegevens")
height = st.sidebar.number_input("Lengte (cm)", 140, 220, 180)
inseam = st.sidebar.number_input("Inseam (cm)", 60, 100, 86)
femur = st.sidebar.number_input("Femur lengte (cm)", 35, 60, 40)
tibia = st.sidebar.number_input("Tibia lengte (cm)", 30, 50, 36)
current_crank = st.sidebar.number_input("Huidige cranklengte (mm)", 150.0, 200.0, 172.5, step=0.5)
cadence = st.sidebar.number_input("Threshold cadans (rpm)", 60, 120, 90)
sprint_cadence = st.sidebar.number_input("Sprint cadans (rpm)", 80, 150, 120)
power = st.sidebar.number_input("Vermogen (W)", 50, 500, 250)
mobility_issue = st.sidebar.selectbox("Mobiliteitsbeperkingen", ["Nee", "Ja"])
discipline = st.sidebar.selectbox("Discipline / Bike type", ["Road", "TT/Track", "Climbing", "MTB/Gravel"])
saddle_height = st.sidebar.number_input("Saddle height BB→saddle (mm)", 600, 900, 750)
kops_status = st.sidebar.selectbox("KOPS status", ["Neutraal", "Forward", "Back"])
shoe_stack = st.sidebar.number_input("Shoe–pedal stack (mm)", 0, 25, 8.5)

# --- Berekeningen: binnenbeenlengte methodes ---
conservatief = inseam * 0.200
neutraal = inseam * 0.205
kracht = inseam * 0.210

st.subheader("1️⃣ Binnenbeenlengte richtlijnen")
st.write(f"- Conservatief: {conservatief:.1f} mm → korte, cadansvriendelijke crank")
st.write(f"- Neutraal: {neutraal:.1f} mm → balans cadans/kracht")
st.write(f"- Krachtgeoriënteerd: {kracht:.1f} mm → lange crank, meer hefboom")

if current_crank < conservatief:
    st.warning("Huidige crank is erg kort: snelle cadans, minder hefboom")
elif current_crank > kracht:
    st.warning("Huidige crank is erg lang: meer koppel, risico knie/heup")
else:
    st.info("Huidige crank ligt in veilige middenrange")

# --- Cadansprofiel analyse ---
st.subheader("2️⃣ Cadansprofiel interpretatie")
if cadence < 85:
    st.write("Threshold cadans krachtgeoriënteerd → langere crank vaak gunstig")
elif 85 <= cadence <= 95:
    st.write("Neutraal → huidige crank waarschijnlijk oké")
else:
    st.write("Cadansgericht → kortere crank vaak gunstig")

if sprint_cadence >= 120:
    st.write("Sprint cadans hoog → korte crank helpt cadans hoog te houden")
elif 100 <= sprint_cadence < 120:
    st.write("Sprint cadans neutraal → huidige crank oké")
else:
    st.write("Sprint cadans laag → langere crank kan helpen hefboom te behouden")

# --- Femur/Tibia ratio ---
st.subheader("3️⃣ Femur / Tibia ratio")
ratio = femur / tibia
if ratio > 1:
    st.write("Femur dominant → langere crank kan voordeel geven bij krachtinspanningen")
elif 0.95 <= ratio <= 1.05:
    st.write("Neutraal → geen sterke voorkeur")
else:
    st.write("Tibia dominant → kortere crank vaak comfortabeler")

# --- Mobiliteit / blessures ---
st.subheader("4️⃣ Mobiliteit / blessures")
if mobility_issue == "Ja":
    st.write("Kortere crank aanbevolen voor comfort en beperking van beweging")
else:
    st.write("Alle cranklengtes binnen range mogelijk")

# --- Discipline / Bike type ---
st.subheader("5️⃣ Discipline / Bike type")
if discipline == "TT/Track":
    st.write("Kortere cranks gunstig voor aerodynamica en hoge cadans")
elif discipline == "Road":
    st.write("Neutraal tot iets langer, afhankelijk van stijl")
elif discipline == "Climbing":
    st.write("Langere crank mogelijk, mits mobiliteit toelaat")
else:
    st.write("Kortere cranks voor clearance en controle")

# --- Saddle & KOPS ---
st.subheader("6️⃣ Saddle height & KOPS")
st.write(f"- Saddle height: {saddle_height} mm (pas aan bij extreme cranklengtes)")
st.write(f"- KOPS status: {kops_status}")

# --- Shoe-pedal stack ---
st.subheader("7️⃣ Shoe–pedal stack")
if shoe_stack > 15:
    st.write("Hoge stack → comfort kan beperkt zijn bij lange cranks")
else:
    st.write("Stack laag → vrijheid om langere cranks te gebruiken")

# --- Wetenschappelijke optimalisatie ---
st.subheader("📊 Wetenschappelijke optimalisatie")
crank_lengths = np.arange(150, 181, 2.5)
torque = power / (2 * np.pi * cadence / 60)
force = torque / (crank_lengths / 1000)
efficiency = np.exp(-0.01 * (crank_lengths - 170)**2)
score = force * efficiency

# Optimalisatie
def objective(crank):
    torque = power / (2 * np.pi * cadence / 60)
    force = torque / (crank/1000)
    eff = np.exp(-0.01 * (crank-170)**2)
    return -force*eff

from scipy.optimize import minimize
opt_result = minimize(objective, 170, bounds=[(150,180)])
optimal_crank = opt_result.x[0]

# --- Visualisatie ---
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(crank_lengths, score, label="Force x Efficiëntie")
ax.axvline(optimal_crank, color='r', linestyle='--', label=f'Optimaal: {optimal_crank:.1f} mm')
ax.scatter(current_crank, torque/(current_crank/1000)*np.exp(-0.01*(current_crank-170)**2), color='g', label="Huidige crank")
ax.set_xlabel("Cranklengte (mm)")
ax.set_ylabel("Force x Efficiëntie")
ax.legend()
st.pyplot(fig)

st.subheader("✅ Aanbevolen cranklengtes")
st.write(f"- Graeme Obree methode: {height*0.95:.1f} mm")
st.write(f"- 'Machine' methode: {1.25*inseam+65:.1f} mm")
st.write(f"- Wetenschappelijke optimalisatie: {optimal_crank:.1f} mm")
st.write(f"- Huidige crank: {current_crank} mm")
