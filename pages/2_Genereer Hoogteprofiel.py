from imports import *

# --- Pagina config en titel ---
st.set_page_config(page_title="Genereer Hoogteprofiel", layout="centered")
st.image("https://jongerennersroeselare.be/assets/images/logo_jrr.png", width=200)
st.markdown(
    f"""
    <h1 style='color:#fb5d01;'>Genereer Hoogteprofiel</h1>
    """,
    unsafe_allow_html=True,
)

# --- Uitleg en instructies ---
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
    2. Pas alle instellingen aan in de sidebar links:

    <ul style="list-style:none; padding-left:0;">
      <li><span style="font-weight:bold; background:#fb5d01; color:#fff; padding:3px 8px; border-radius:5px;">🎨 Personaliseer</span> — kleur, lijndikte en afmetingen aanpassen</li>
      <li><span style="font-weight:bold; background:#fb5d01; color:#fff; padding:3px 8px; border-radius:5px;">⚙️ Profiel instellingen</span> — detailgraad en gladheid van het hoogteprofiel instellen</li>
      <li><span style="font-weight:bold; background:#fb5d01; color:#fff; padding:3px 8px; border-radius:5px;">📍 Keypoints toevoegen</span> — belangrijke punten zoals klim- en sprintlocaties toevoegen</li>
    </ul>

    3. Bekijk het aangepaste hoogteprofiel met keypoints onderaan de pagina.  
    4. Download de afbeelding en gebruik deze bijvoorbeeld als tactisch overzicht op de fiets.
    """, unsafe_allow_html=True)

# --- GPX-file upload veld ---
uploaded_file = st.file_uploader("Upload een GPX-bestand", type=["gpx"])

# --- Sidebar: Personaliseer sectie ---
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

    line_width = st.number_input("Lijndikte", min_value=1, max_value=8, value=2, step=1)
    cm_width = st.number_input("Breedte hoogteprofiel (cm)", min_value=5.0, max_value=30.0, value=10.0, step=0.1)
    cm_height = st.number_input("Hoogte hoogteprofiel (cm)", min_value=0.1, max_value=20.0, value=1.0, step=0.1)


# --- Pixels cm conversie ---
dpi = 300
px_width = int((cm_width / 2.54) * dpi)
px_height = int((cm_height / 2.54) * dpi)

# --- Hoofdlogica: verwerken van GPX-file ---
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

    # --- Data downsamplen en smoothen ---
    step = max(1, len(df) // max_points)
    df_resampled = df.iloc[::step].reset_index(drop=True)

    if window_length % 2 == 0:
        window_length -= 1
    if window_length < 3:
        window_length = 3

    smooth_elev = savgol_filter(df_resampled["Hoogte (m)"], window_length=window_length, polyorder=3)

    # --- Sidebar: keypoints toevoegen ---
    with st.sidebar.expander("📍 Keypoints toevoegen", expanded=True):
        st.warning("⚠️ Gebruik een punt (.) als decimaalteken, geen komma (,).")
        
        keypoint_names = st.text_area("Keypoint namen (één per lijn)", "GPM 1\nRAV 1\nSPR 1")
        keypoint_distances = st.text_area("Afstanden (in km, evenveel als namen)", "15.3\n42.7\n55.2")

        use_custom_colors = st.checkbox("Per keypoint een eigen kleur?", False)

        kp_names = [k.strip() for k in keypoint_names.split("\n") if k.strip()]
        try:
            kp_distances = [float(d.strip()) for d in keypoint_distances.split("\n") if d.strip()]
        except ValueError:
            st.error("Zorg dat alle afstanden correcte getallen zijn met een punt als decimaalteken.")

        default_colors = [
            "#e6194B", "#3cb44b", "#ffe119", "#4363d8",
            "#f58231", "#911eb4", "#46f0f0", "#f032e6",
            "#bcf60c", "#fabebe", "#008080", "#e6beff"
        ]

        if use_custom_colors:
            kp_colors = []
            for i, name in enumerate(kp_names):
                default_col = default_colors[i % len(default_colors)]
                color = st.color_picker(f"Kleur voor '{name}'", default_col)
                kp_colors.append(color)
        else:
            default_kp_color = st.color_picker("Kleur voor keypoints", "#fb5d01")
            kp_colors = [default_kp_color] * len(kp_names)

        keypoints = []
        for name, km, color in zip(kp_names, kp_distances, kp_colors):
            interpolated_height = np.interp(km, df_resampled["Afstand (km)"], smooth_elev)
            keypoints.append({"name": name, "km": km, "elev": interpolated_height, "color": color})


    # --- Sidebar: interval tussen X-as marks ---
    tick_interval = st.sidebar.slider("Interval afstandlabels (km)", 5, 50, 20)

    # --- Plot bouwen met Plotly ---
    fig = go.Figure()

    # --- Hoofdhoogteprofiel lijn ---
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
            mode='markers+text',
            marker=dict(size=10, color=kp["color"]),
            text=[kp["name"]],
            textposition="top center",
            showlegend=False,
            textfont=dict(size=14, color=kp["color"])
        ))

    # --- X-as ticks en labels ---
    max_dist = df_resampled["Afstand (km)"].max()
    tick_vals = list(np.arange(0, max_dist + tick_interval, tick_interval))
    tick_texts = [f"{int(t)} km" for t in tick_vals]

    # --- Layout aanpassingen ---
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

    # --- Plot tonen ---
    st.subheader("Hoogteprofiel met keypoints")
    st.plotly_chart(fig, use_container_width=False)

    # --- Transparante PNG export ---
    img_bytes = fig.to_image(format="png", width=px_width, height=px_height, scale=3)

    st.download_button(
        label=f"Download PNG ({cm_width:.1f} × {cm_height:.1f} cm)",
        data=img_bytes,
        file_name="hoogteprofiel.png",
        mime="image/png"
    )
