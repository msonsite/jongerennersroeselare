import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
import numpy as np
import plotly.express as px

# --- HEADER & INTRODUCTIE ---

# Toon logo bovenaan
st.image("https://jongerennersroeselare.be/assets/images/logo_jrr.png", width=200)

# Dynamisch huidig jaar bepalen en weergeven
current_year = datetime.now().year

st.markdown(
    f"""
    <h1 style='color:#fb5d01;'>Uitslagen Men Juniors</h1>
    <h2 style='color:#000000;'>Seizoen {current_year}</h2>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown("\n\nDownload hieronder de input template indien nodig.")

# --- DOWNLOAD TEMPLATE BUTTON ---

try:
    with open("standardized_template.xlsx", "rb") as template_file:
        st.download_button(
            label="Download standaard Excel-template",
            data=template_file,
            file_name="standardized_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
except FileNotFoundError:
    # Template bestand niet gevonden, geen download-knop tonen
    pass

st.markdown("---")

# --- FILE UPLOADER ---

uploaded_file = st.file_uploader("Upload het Excel bestand:", type=["xlsx"])

if uploaded_file:

    # --- DATA INLADEN ---

    raw_df = pd.read_excel(uploaded_file, sheet_name="Uitslagen", header=None)

    # Haal kolomnamen (racedata) uit tweede rij, vanaf kolom 4 (index 3)
    race_dates = raw_df.iloc[1, 3:].tolist()

    # Haal rennersnamen uit derde rij en verder, kolom 2 (index 1)
    names = raw_df.iloc[2:, 1].tolist()

    # Resultaten vanaf derde rij, kolom 4 en verder, reset index om makkelijker te werken
    results = raw_df.iloc[2:, 3:].reset_index(drop=True)

    # Dataframe maken met resultaten, kolomnamen = race_dates
    df = pd.DataFrame(results.values, columns=race_dates)

    # Voeg 'NAME' kolom toe met rennersnamen, zet als index
    df.insert(0, "NAME", names)
    df.set_index("NAME", inplace=True)

    # --- DATA CLEANING ---

    df = df.astype(str)  # Eerst alles string maken voor vervangingen
    df = df.replace(to_replace=["", "nan", "NaN"], value=pd.NA)  # lege cellen vervangen door NA
    df = df.mask(df == "DNF", pd.NA)  # 'DNF' vervangen door NA
    df = df.apply(pd.to_numeric, errors="coerce")  # Probeer alles om te zetten naar numeriek

    # Verwijder rijen en kolommen die helemaal leeg zijn
    df.dropna(how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)

    riders = df.index.tolist()  # lijst met renners

    # --- GRAFIEKEN EN INTERACTIEVE COMPONENTEN ---

    # 1) Vergelijk prestaties van meerdere renners over tijd
    st.markdown("---")
    st.subheader("Vergelijk de prestaties van één of meerdere renners.")

    selected_riders = st.multiselect(
        "Selecteer renners om te vergelijken",
        riders,
        default=[riders[0]] if riders else [],
    )

    if selected_riders:

        # Lijngrafiek met prestaties per renner
        fig = go.Figure()

        for rider in selected_riders:
            results = df.loc[rider]
            fig.add_trace(
                go.Scatter(
                    x=results.index,
                    y=results.values,
                    mode="lines+markers",
                    name=rider,
                    connectgaps=True,
                    line_shape="spline",
                    hovertemplate="Koers: %{x}<br>Uitslag: %{y}<extra></extra>",
                )
            )

        fig.update_layout(
            title="Resultaten over de tijd",
            xaxis_title="Koers (chronologisch)",
            yaxis_title="Uitslag",
            yaxis=dict(autorange="reversed"),  # beter resultaat bovenaan
            height=500,
        )

        st.plotly_chart(fig)

        # 2) Vergelijk prestaties in één specifieke wedstrijd (bar chart)
        st.markdown("---")
        st.subheader("Vergelijk de teamprestaties in één specifieke wedstrijd.")

        valid_races = [col for col in df.columns if pd.notna(col)]
        selected_race = st.selectbox(
            "Selecteer een koers om te vergelijken", options=valid_races
        )

        if selected_race:
            race_column = df[selected_race].dropna()
            sorted_race = race_column.sort_values()

            fig_bar = go.Figure()
            fig_bar.add_trace(
                go.Bar(
                    x=sorted_race.index,
                    y=sorted_race.values,
                    text=sorted_race.values,
                    textposition="auto",
                    marker_color="#fb5d01",
                )
            )

            fig_bar.update_layout(
                title=f"Uitslagen voor {selected_race}",
                xaxis_title="Renner",
                yaxis_title="Uitslag",
                yaxis=dict(autorange="reversed"),
                height=500,
            )

            st.plotly_chart(fig_bar)

        # 3) Consistentie van prestaties vergelijken (standaarddeviatie)
        st.markdown("---")
        st.subheader("Vergelijk consistentie van prestaties")

        selected_riders_consistency = st.multiselect(
            "Selecteer renners om consistentie te vergelijken",
            options=riders,
            default=selected_riders
            if "selected_riders" in locals()
            else ([riders[0]] if riders else []),
        )

        if selected_riders_consistency:
            consistency_series = (
                df.loc[selected_riders_consistency].std(axis=1, skipna=True).dropna()
            )
            consistency_sorted = consistency_series.sort_values()

            fig_consistency = go.Figure()
            fig_consistency.add_trace(
                go.Bar(
                    x=consistency_sorted.index,
                    y=consistency_sorted.values,
                    text=consistency_sorted.round(2),
                    textposition="auto",
                    marker_color="#fb5d01",
                )
            )

            fig_consistency.update_layout(
                title="Consistentie van prestaties (lagere waarde = stabieler)",
                xaxis_title="Renner",
                yaxis_title="Standaarddeviatie Uitslag",
                yaxis=dict(autorange="reversed"),  # optioneel, kan ook zonder
                height=500,
            )

            st.plotly_chart(fig_consistency)

        else:
            st.info("Selecteer minstens één renner om consistentie te vergelijken.")

    else:
        st.info("Selecteer minstens een renner om de grafiek te zien.")

else:
    st.info("Upload de Excel template die een ingevuld uitslagen tabblad bevat.")
