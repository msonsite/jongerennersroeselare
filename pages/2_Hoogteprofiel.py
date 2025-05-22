import streamlit as st
import plotly.graph_objects as go
import gpxpy
import pandas as pd
import io

st.set_page_config(page_title="GPX Hoogteprofiel", layout="centered")

st.title("🏔️ GPX Hoogteprofiel Generator (Plotly)")

uploaded_file = st.file_uploader("📤 Upload een GPX-bestand", type=["gpx"])

st.sidebar.header("🎨 Personaliseer")

line_color = st.sidebar.color_picker("Lijnkleur", "#1f77b4")
line_width = st.sidebar.slider("Lijndikte", 1, 8, 3)
img_width = st.sidebar.slider("Breedte afbeelding (px)", 600, 2000, 1000)
img_height = st.sidebar.slider("Hoogte afbeelding (px)", 200, 800, 300)

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

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Afstand (km)"],
        y=df["Hoogte (m)"],
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
        height=img_height,
        width=img_width
    )

    st.subheader("📈 Voorbeeld hoogteprofiel")
    st.plotly_chart(fig, use_container_width=True)

    # Opslaan als PNG
    img_bytes = fig.to_image(format="png", width=img_width, height=img_height, scale=1)

    st.download_button(
        label="📥 Download PNG (transparant)",
        data=img_bytes,
        file_name="hoogteprofiel.png",
        mime="image/png"
    )

