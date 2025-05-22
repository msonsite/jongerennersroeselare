# --- Importeren van benodigde libraries ---
import streamlit as st
import plotly.graph_objects as go
import gpxpy
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

# --- Streamlit pagina configuratie en titel ---
st.set_page_config(page_title="Genereer Hoogteprofiel", layout="centered")
st.title("Genereer Hoogteprofiel")

# --- Uitleg en instructies voor de gebruiker ---
with st.expander("ℹ️ Strategisch doel en instructies", expanded=False):
    st.markdown("""
    ### Strategisch doel
    Deze tool ondersteunt bij het tactisch plannen van wedstrijden en trainingen.  
    Met het custom hoogteprofiel krijgen renners en coaches direct inzicht in waar de cruciale klimmetjes, sprintzones en andere belangrijke punten liggen.  
    Zo kunnen race- en trainingsstrategieën beter afgestemd worden op het parcours.  

    De gegenereerde afbeelding is geschikt om als overzichtelijk kaartje op bijvoorbeeld de bovenbuis of het stuur van de fiets te plakken — ideaal voor snelle referentie tijdens de race.

    ---

    ### Instructies
    1. Upload een GPX-bestand van een trainingsrit of wedstrijd.  
    2. Pas kleuren, lijndikte en afmetingen aan naar voorkeur in het *Personaliseer* menu links.
    3. (Optioneel) Gebruik de schuifbalken in het *Profiel instellingen* menu links om de detailgraad en gladheid van het hoogteprofiel aan te passen.
    4. Voeg belangrijke punten toe zoals klim- en sprintlocaties in het linkerpaneel.  
    5. Bekijk onderaan het custom hoogteprofiel met keypoints.  
    6. Download de afbeelding via de "Download" knop en plak deze bijvoorbeeld op de bovenbuis voor een snel tactisch overzicht.
    """)


# --- GPX bestand upload veld ---
uploaded_file = st.file_uploader("Upload een GPX-bestand", type=["gpx"])

# --- Sidebar: Personaliseer sectie met kleur, dikte en afmetingen ---
with st.sidebar.expander("🎨 Personaliseer", expanded=False):
    color_option = st.selectbox(
        "Kleur opties",
        ("Zwart", "Oranje", "Custom")
    )

    if color_option == "Oranje":
        line_color = "#fb5d01"
    elif color_option == "Zwart":
        line_color = "#000000"
    else:
        line_color = st.color_picker("Kies je kleur", "#fb5d01")

    line_width = st.slider("Lijndikte", 1, 8, 2)
    cm_width = st.slider("Breedte afbeelding (cm)", 5.0, 30.0, 10.0)
    cm_height = st.slider("Hoogte afbeelding (cm)", 0.1, 10.0, 1.0)

# --- Berekenen van pixels vanuit centimeters voor printkwaliteit ---
dpi = 300
px_width = int((cm_width / 2.54) * dpi)
px_height = int((cm_height / 2.54) * dpi)

# --- Hoofdlogica: inlezen en verwerken van GPX bestand ---
if uploaded_file is not None:
    gpx = gpxpy.parse(uploaded_file)
    elevations = []
    distances = []
    total_dist = 0

    for track in gpx.tracks:
        for segment in track.segments:
            prev_point = None
            for point in segment.points:
                if prev_point:
                    total_dist += point.distance_3d(prev_point)
                elevations.append(point.elevation)
                distances.append(total_dist / 1000)  # omzetten naar km
                prev_point = point

    df = pd.DataFrame({
        "Afstand (km)": distances,
        "Hoogte (m)": elevations
    })

    # --- Sidebar profiel instellingen (smoothing & detail) ---
    with st.sidebar.expander("⚙️ Profiel instellingen", expanded=False):
        max_points = st.slider(
            "Hoe gedetailleerd het profiel is (meer = fijner)",
            100, 20000, 10000,
            help="Aantal punten waaruit het hoogteprofiel bestaat. Meer punten betekent meer details."
        )

        window_length = st.slider(
            "Hoe vloeiend de lijn is (meer = gladder)",
            5, 501, 101, step=2,
            help="Hoe sterk het hoogteprofiel wordt gladgestreken. Grotere waarde betekent een zachtere, vloeiendere lijn."
        )

    # --- Checkbox om profiel te spiegelen (indien renners verticaal kaartje willen) --- #
    mirror_profile = st.checkbox(
        "Profiel spiegelen (0 km rechts)", value=False
    )

    # --- Data downsamplen en smoothen met Savitzky-Golay filter ---
    step = max(1, len(df) // max_points)
    df_resampled = df.iloc[::step].reset_index(drop=True)

    if window_length % 2 == 0:
        window_length -= 1
    if window_length < 3:
        window_length = 3

    smooth_elev = savgol_filter(df_resampled["Hoogte (m)"], window_length=window_length, polyorder=3)

    # --- Sidebar: Keypoints toevoegen ---
    st.sidebar.header("📍 Voeg keypoints toe")
    keypoint_names = st.sidebar.text_area("Keypoint namen (één per lijn)", "GPM 1\nRAV 1\nSPR 1")
    keypoint_distances = st.sidebar.text_area("Afstanden (in km, evenveel als namen)", "15.3\n42.7\n55.2")

    # Checkbox voor per-keypoint kleuren
    use_custom_colors = st.sidebar.checkbox("Per keypoint een eigen kleur?", False)

    # Parse namen en afstanden netjes
    kp_names = [k.strip() for k in keypoint_names.split("\n") if k.strip()]
    kp_distances = [float(d.strip()) for d in keypoint_distances.split("\n") if d.strip()]

    # Default kleurenpalet voor automatische toewijzing
    default_colors = [
        "#e6194B", "#3cb44b", "#ffe119", "#4363d8",
        "#f58231", "#911eb4", "#46f0f0", "#f032e6",
        "#bcf60c", "#fabebe", "#008080", "#e6beff"
    ]

    if use_custom_colors:
        kp_colors = []
        for i, name in enumerate(kp_names):
            default_col = default_colors[i % len(default_colors)]
            color = st.sidebar.color_picker(f"Kleur voor '{name}'", default_col)
            kp_colors.append(color)
    else:
        default_kp_color = st.sidebar.color_picker("Kleur voor keypoints", "#fb5d01")
        kp_colors = [default_kp_color] * len(kp_names)

    keypoints = []
    for name, km, color in zip(kp_names, kp_distances, kp_colors):
        # Interpoleer hoogte op keypoint afstand
        interpolated_height = np.interp(km, df_resampled["Afstand (km)"], smooth_elev)
        keypoints.append({"name": name, "km": km, "elev": interpolated_height, "color": color})

    # --- Sidebar: Interval tussen afstandlabels op X-as ---
    tick_interval = st.sidebar.slider("Interval afstandlabels (km)", 5, 50, 20)

    # --- Plot bouwen met Plotly ---
    fig = go.Figure()

    # Hoofdhoogteprofiel lijn
    fig.add_trace(go.Scatter(
        x=df_resampled["Afstand (km)"],
        y=smooth_elev,
        mode='lines',
        line=dict(color=line_color, width=line_width),
        hoverinfo='skip',
        showlegend=False
    ))

    # Keypoints als markers + labels
    for kp in keypoints:
        fig.add_trace(go.Scatter(
            x=[kp["km"]],
            y=[kp["elev"]],
            mode='markers',
            marker=dict(size=10, color=kp["color"]),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[kp["km"]],
            y=[kp["elev"] + 100],
            mode='text',
            text=[kp["name"]],
            textfont=dict(size=14, color=kp["color"]),
            showlegend=False
        ))

    # --- X-as ticks en labels instellen ---
    max_dist = df_resampled["Afstand (km)"].max()
    tick_vals = list(np.arange(0, max_dist + tick_interval, tick_interval))
    tick_texts = [f"{int(t)} km" for t in tick_vals]

    # --- Layout aanpassen voor clean look ---
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=tick_vals,
            ticktext=tick_texts,
            ticks="outside",
            showline=False,
            linewidth=0,
            linecolor='rgba(0,0,0,0)',
            title_text=None,
            autorange='reversed' if mirror_profile else True,
            showgrid=False
        ),
        yaxis=dict(
            showline=False,
            linewidth=0,
            linecolor='rgba(0,0,0,0)',
            title_text=None,
            zeroline=False,
            showticklabels=True,
            showgrid=False
        ),
        margin=dict(l=40, r=20, t=20, b=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=px_width,
        height=px_height
    )

    # --- Resultaat tonen ---
    st.subheader("Hoogteprofiel met keypoints")
    st.plotly_chart(fig, use_container_width=False)

    # --- PNG export met transparante achtergrond ---
    img_bytes = fig.to_image(format="png", width=px_width, height=px_height, scale=1)

    st.download_button(
        label=f"Download PNG ({cm_width:.1f} × {cm_height:.1f} cm)",
        data=img_bytes,
        file_name="hoogteprofiel.png",
        mime="image/png"
    )
