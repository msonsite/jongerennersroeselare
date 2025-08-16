import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

st.set_page_config(page_title="Wetenschappelijke Cranklengte Tool", layout="wide")
st.title("🔬 Wetenschappelijke Cranklengte Calculator")

# --- Input ---
st.sidebar.header("🚴‍♂️ Fietsersgegevens (float inputs)")
height = st.sidebar.number_input("Lengte (cm)", 140.0, 220.0, 180.0, step=0.5)
inseam = st.sidebar.number_input("Inseam (cm)", 60.0, 100.0, 86.0, step=0.5)
femur = st.sidebar.number_input("Femur lengte (cm)", 35.0, 60.0, 40.0, step=0.5)
tibia = st.sidebar.number_input("Tibia lengte (cm)", 30.0, 50.0, 36.0, step=0.5)
current_crank = st.sidebar.number_input("Huidige cranklengte (mm)", 150.0, 200.0, 172.5, step=0.5)
cadence = st.sidebar.number_input("Threshold cadans (rpm)", 60.0, 120.0, 90.0, step=1.0)
sprint_cadence = st.sidebar.number_input("Sprint cadans (rpm)", 80.0, 150.0, 120.0, step=1.0)
power = st.sidebar.number_input("Vermogen (W)", 50.0, 500.0, 250.0, step=5.0)
mobility_issue = st.sidebar.selectbox("Mobiliteitsbeperkingen", ["Nee", "Ja"])
discipline = st.sidebar.selectbox("Discipline / Bike type", ["Road", "TT/Track", "Climbing", "MTB/Gravel"])
saddle_height = st.sidebar.number_input("Saddle height BB→saddle (mm)", 600.0, 900.0, 750.0, step=1.0)
kops_status = st.sidebar.selectbox("KOPS status", ["Neutraal", "Forward", "Back"])

# --- Pedalen ---
st.sidebar.subheader("Pedaal type")
pedal_type = st.sidebar.selectbox("Selecteer pedaal", 
    ["Shimano SPD-SL", "Shimano SPD", "Look Keo", "Look Keo Blade", 
     "Speedplay Zero/Nano", "Time ATAC", "Crankbrothers Eggbeater"]
)

# Stack hoogte per pedaal
pedal_stack_dict = {
    "Shimano SPD-SL": 12.5,
    "Shimano SPD": 7.0,
    "Look Keo": 12.0,
    "Look Keo Blade": 13.0,
    "Speedplay Zero/Nano": 5.5,
    "Time ATAC": 9.5,
    "Crankbrothers Eggbeater": 8.0
}

shoe_stack = pedal_stack_dict[pedal_type]

st.write(f"📏 Stack hoogte van gekozen pedaal ({pedal_type}): {shoe_stack} mm")

# --- Binnenbeenlengte methodes ---
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

# --- Cadansprofiel ---
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

# --- Wetenschappelijke optimalisatie ---
st.subheader("📊 Wetenschappelijke optimalisatie")
crank_lengths = np.arange(150.0, 181.0, 2.5)
torque = power / (2 * np.pi * cadence / 60.0)
# Pas stackhoogte aan voor effectieve crank
effective_crank_lengths = crank_lengths + shoe_stack
force = torque / (effective_crank_lengths / 1000.0)
efficiency = np.exp(-0.01 * (effective_crank_lengths - 170.0)**2)
score = force * efficiency

# Optimalisatie functie
def objective(crank):
    crank_eff = crank + shoe_stack
    torque = power / (2 * np.pi * cadence / 60.0)
    force = torque / (crank_eff / 1000.0)
    eff = np.exp(-0.01 * (crank_eff - 170.0)**2)
    return -force * eff

opt_result = minimize(objective, 170.0, bounds=[(150.0, 180.0)])
optimal_crank = opt_result.x[0]

# --- Visualisatie ---
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(effective_crank_lengths, score, label="Force x Efficiëntie")
ax.axvline(optimal_crank + shoe_stack, color='r', linestyle='--', label=f'Optimaal: {optimal_crank:.1f} mm (excl. stack)')
ax.scatter(current_crank + shoe_stack, torque/( (current_crank + shoe_stack)/1000.0)*np.exp(-0.01*((current_crank + shoe_stack)-170.0)**2), color='g', label="Huidige crank")
ax.set_xlabel("Effectieve cranklengte (mm)")
ax.set_ylabel("Force x Efficiëntie")
ax.legend()
st.pyplot(fig)

# --- Aanbevolen cranklengtes ---
st.subheader("✅ Aanbevolen cranklengtes")
st.write(f"- Graeme Obree methode: {height*0.95:.1f} mm")
st.write(f"- 'Machine' methode: {1.25*inseam+65:.1f} mm")
st.write(f"- Wetenschappelijke optimalisatie: {optimal_crank:.1f} mm (excl. stack)")
st.write(f"- Huidige crank: {current_crank} mm")
st.write(f"- Effectieve crank incl. stack: {current_crank + shoe_stack:.1f} mm")
