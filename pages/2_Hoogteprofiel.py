import streamlit as st
import plotly.graph_objects as go
import gpxpy
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

st.set_page_config(page_title="GPX Hoogteprofiel Generator", layout="centered")
st.title("GPX Hoogteprofiel Generator")

st.markdown(
    """
    **Upload hieronder een GPX-bestand** om een helder en printbaar hoogteprofiel te genereren.  
    Pas de lijnkleur, dikte en afmetingen aan in de sidebar links.  
    Download daarna het resultaat als een transparante PNG, perfect om toe te voegen op de rennerskaartjes.  
    """
)

uploaded_file = st.file_uploader("Upload een GPX-bestand", type=["gpx"])

st.sidebar.header("Personaliseer")

color_option = st.sidebar.selectbox(
    "Kleur opties",
    ("Oranje (#fb5d01)", "Zwart (#000000)", "Custom")
)

if color_option == "Oranje":
    line_color = "#fb5d01"
elif color_option == "Zwart":
    line_color = "#000000"
else:
    line_color = st.sidebar.color_picker("Kies je kleur", "#fb5d01")

# Gebruiker kiest kleur, dikte, formaat
line_width = st.sidebar.slider("Lijndikte", 1, 8, 3)
cm_width = st.sidebar.slider("Breedte afbeelding (cm)", 5.0, 30.0, 15.0)
cm_height = st.sidebar.slider("Hoogte afbeelding (cm)", 1.0, 10.0, 3.0)

# DPI voor printkwaliteit
dpi = 300
px_width = int((cm_width / 2.54) * dpi)
px_height = int((cm_height / 2.54) * dpi)

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
                distances.append(total_dist / 1000)  # km
                prev_point = point

    df = pd.DataFrame({
        "Afstand (km)": distances,
        "Hoogte (m)": elevations
    })

    # Smoothing
    window_length = min(51, len(df)) if len(df) % 2 == 1 else max(3, len(df) - 1)  # moet oneven zijn
    smooth_elev = savgol_filter(df["Hoogte (m)"], window_length=window_length, polyorder=3)

    # Plotly plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Afstand (km)"],
        y=smooth_elev,
        mode='lines',
        line=dict(color=line_color, width=line_width),
        hoverinfo='skip'
    ))

    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=px_width,
        height=px_height
    )

    st.subheader("Hoogteprofiel")
    st.plotly_chart(fig, use_container_width=False)

    # Export naar PNG (transparant)
    img_bytes = fig.to_image(format="png", width=px_width, height=px_height, scale=1)

    st.download_button(
        label=f"Download PNG ({cm_width:.1f} × {cm_height:.1f} cm)",
        data=img_bytes,
        file_name="hoogteprofiel.png",
        mime="image/png"
    )
