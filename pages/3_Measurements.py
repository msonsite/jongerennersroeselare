import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize

# Configuratie
sns.set(style="whitegrid")
np.random.seed(42)

# Inputparameters
height = 180  # cm
inseam = 86  # cm
cadence = 90  # rpm
power = 250  # W
crank_lengths = np.array([150, 155, 160, 165, 170, 172.5, 175, 177.5, 180])  # mm

# Fysieke eigenschappen
leg_length = inseam * 0.9  # schatting van beenlengte
hip_angle = 90  # graden
knee_angle = 30  # graden

# Biomechanische parameters
torque = power / (2 * np.pi * cadence / 60)  # Nm
force = torque / (crank_lengths / 1000)  # N

# Spieractiviteit (EMG) - benaderingen gebaseerd op literatuur
muscle_activity = {
    'gluteus_maximus': 0.8,
    'vastus_lateralis': 0.7,
    'rectus_femoris': 0.6,
    'biceps_femoris': 0.5,
    'gastrocnemius': 0.4
}

# Optimalisatie van cranklengte op basis van kracht en cadans
def objective(crank_length):
    torque = power / (2 * np.pi * cadence / 60)
    force = torque / (crank_length / 1000)
    efficiency = np.exp(-0.01 * (crank_length - 170)**2)  # hypothetische efficiëntiefunctie
    return -efficiency * force  # negatief voor minimalisatie

optimal_result = minimize(objective, 170, bounds=[(150, 180)])
optimal_crank_length = optimal_result.x[0]

# Visualisatie van kracht vs. cranklengte
plt.figure(figsize=(10, 6))
plt.plot(crank_lengths, force, label='Kracht (N)', color='b')
plt.axvline(x=optimal_crank_length, color='r', linestyle='--', label=f'Optimaal: {optimal_crank_length:.1f} mm')
plt.title('Kracht vs. Cranklengte')
plt.xlabel('Cranklengte (mm)')
plt.ylabel('Kracht (N)')
plt.legend()
plt.grid(True)
plt.show()

# Visualisatie van spieractiviteit
plt.figure(figsize=(10, 6))
plt.bar(muscle_activity.keys(), muscle_activity.values(), color='g')
plt.title('Gesimuleerde Spieractiviteit bij Verschillende Cranklengtes')
plt.ylabel('Spieractiviteit (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
