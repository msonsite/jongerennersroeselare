# streamlit_crank_calc.py
from imports import *

st.set_page_config(page_title="Cranklengte Calculator", layout="centered")
st.title("🚴 Cranklengte Calculator")

st.markdown("Vul hieronder je gegevens in en krijg automatisch advies voor optimale cranklengte:")

# --- Input ---
inseam = st.number_input("Inseam (mm)", min_value=600, max_value=1000, value=860)
current_crank = st.number_input("Huidige cranklengte (mm)", min_value=150, max_value=200, value=172.5)
threshold_cadence = st.number_input("Threshold cadence (rpm)", min_value=60, max_value=130, value=85)
sprint_cadence = st.number_input("Sprint cadence (rpm)", min_value=80, max_value=150, value=125)
femur = st.number_input("Femur lengte (mm)", min_value=200, max_value=500, value=400)
tibia = st.number_input("Tibia lengte (mm)", min_value=200, max_value=500, value=360)
mobility_issue = st.selectbox("Mobility issues?", ["No", "Yes"])
discipline = st.selectbox("Bike discipline", ["Road", "TT", "Track", "Climbing", "MTB", "Gravel"])
stack = st.number_input("Shoe–pedal stack (mm)", min_value=0.0, max_value=30.0, value=8.5)

# --- Baseline crank range ---
baseline_min = round(inseam * 0.200, 1)
baseline_neutral = round(inseam * 0.205, 1)
baseline_max = round(inseam * 0.210, 1)

# --- Cadence interpretatie ---
if threshold_cadence < 85:
    cadence_note = "Krachtgeoriënteerd → langere crank gunstig"
elif threshold_cadence > 95:
    cadence_note = "Cadansgericht → kortere crank gunstig"
else:
    cadence_note = "Neutraal → huidige crank waarschijnlijk oké"

# --- Femur/Tibia interpretatie ---
if femur > tibia * 1.05:
    ratio_note = "Femur dominant → langere crank kan voordeel geven"
elif tibia > femur * 1.05:
    ratio_note = "Tibia dominant → kortere crank vaak comfortabeler"
else:
    ratio_note = "Neutraal → geen sterke voorkeur"

# --- Mobiliteit interpretatie ---
mobility_note = "Mobiliteit beperkt → kortere crank aanbevolen" if mobility_issue == "Yes" else "Geen mobiliteitsissues → alle lengtes mogelijk"

# --- Discipline interpretatie ---
discipline_lower = discipline.lower()
if discipline_lower in ["tt", "track"]:
    discipline_note = "Kortere cranks vaak beter (aero, hoge cadans, kniehoek beperken)"
elif discipline_lower == "climbing":
    discipline_note = "Langere cranks mogelijk (meer hefboom), mits mobiliteit toelaat"
elif discipline_lower in ["mtb", "gravel"]:
    discipline_note = "Kortere cranks vaak beter (clearance/controle)"
else:
    discipline_note = "Neutraal tot iets langer; balans cadans/kracht afhankelijk van stijl"

# --- Stack invloed ---
stack_note = "Hoge stack → comfort kan beperken bij lange cranks, overweeg iets korter" if stack > 15 else "Stack laag → vrij om langere cranks te gebruiken"

# --- Berekening aanbevolen crank ---
recommended_crank = baseline_neutral

# Aanpassing op cadans
if threshold_cadence < 85:
    recommended_crank += 2.5
elif threshold_cadence > 95:
    recommended_crank -= 2.5

# Aanpassing op femur/tibia ratio
if femur > tibia * 1.05:
    recommended_crank += 2.5
elif tibia > femur * 1.05:
    recommended_crank -= 2.5

# Aanpassing op mobiliteit
if mobility_issue == "Yes":
    recommended_crank -= 2.5

# Limiteer binnen baseline range
recommended_crank = max(baseline_min, min(recommended_crank, baseline_max))

# Bereken saddle adjustment
saddle_adjustment = recommended_crank - current_crank

# --- Output ---
st.subheader("📊 Analyse per parameter")
st.markdown(f"- **Cadansprofiel:** {cadence_note}")
st.markdown(f"- **Femur/Tibia ratio:** {ratio_note}")
st.markdown(f"- **Mobiliteit:** {mobility_note}")
st.markdown(f"- **Discipline:** {discipline_note}")
st.markdown(f"- **Stack invloed:** {stack_note}")

st.subheader("✅ Aanbevolen cranklengte")
st.markdown(f"- **Cranklengte:** {recommended_crank} mm")
st.markdown(f"- **Saddle aanpassen:** {saddle_adjustment:+.1f} mm om beenhoek gelijk te houden")
st.markdown(f"- **Baseline range:** {baseline_min} – {baseline_max} mm")
