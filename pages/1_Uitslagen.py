import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

st.image("https://jongerennersroeselare.be/assets/images/logo_jrr.png", width=200)

current_year = datetime.now().year

st.markdown(f"""
<h1 style='color:#fb5d01;'>Uitslagen Men Juniors</h1>
<h2 style='color:#000000;'>Seizoen {current_year}</h2>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("\n\nDownload hieronder de input template indien nodig.")

try:
    with open("standardized_template.xlsx", "rb") as template_file:
        st.download_button(
            label="Download standaard Excel-template",
            data=template_file,
            file_name="standardized_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
except FileNotFoundError:
    pass

st.markdown("---")

uploaded_file = st.file_uploader("Upload het Excel bestand:", type=["xlsx"])

if uploaded_file:
    raw_df = pd.read_excel(uploaded_file, sheet_name="Uitslagen", header=None)

    race_dates = raw_df.iloc[1, 3:].tolist()

    names = raw_df.iloc[2:, 1].tolist()
    results = raw_df.iloc[2:, 3:].reset_index(drop=True)

    df = pd.DataFrame(results.values, columns=race_dates)

    df.insert(0, 'NAME', names)
    df.set_index('NAME', inplace=True)

    df = df.astype(str)
    df = df.replace(to_replace=["", "nan", "NaN"], value=pd.NA)
    df = df.mask(df == "DNF", pd.NA)

    df = df.apply(pd.to_numeric, errors='coerce')

    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    riders = df.index.tolist()

# --- Vergelijken van verschillende renners ---
    st.markdown("---")
    st.subheader("Vergelijk de prestaties van één of meerdere renners.")

    selected_riders = st.multiselect("Selecteer renners om te vergelijken", riders, default=[riders[0]] if riders else [])

    if selected_riders:
        fig = go.Figure()

        for rider in selected_riders:
            results = df.loc[rider]
            fig.add_trace(go.Scatter(
                x=results.index,
                y=results.values,
                mode='lines+markers',
                name=rider,
                connectgaps=True,
                line_shape='spline'
            ))

        fig.update_layout(
            title="Resultaten over de tijd",
            xaxis_title="Koers (chronologisch)",
            yaxis_title="Uitslag",
            yaxis=dict(autorange="reversed"),
            height=500
        )

        st.plotly_chart(fig)

# --- Extra wedstrijd-filter en vergelijkende grafiek ---
        st.markdown("---")
        st.subheader("Vergelijk de teamprestaties in één specifieke wedstrijd.")

        valid_races = [col for col in df.columns if pd.notna(col)]
        selected_race = st.selectbox("Selecteer een koers om te vergelijken", options=valid_races)

        if selected_race:
            race_column = df[selected_race].dropna()
            sorted_race = race_column.sort_values()

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=sorted_race.index,
                y=sorted_race.values,
                text=sorted_race.values,
                textposition='auto',
                marker_color='#fb5d01'
            ))

            fig_bar.update_layout(
                title=f"Uitslagen voor {selected_race}",
                xaxis_title="Renner",
                yaxis_title="Uitslag",
                yaxis=dict(autorange="reversed"),
                height=500
            )

            st.plotly_chart(fig_bar)


    else:
        st.info("Selecteer minstens een renner om de grafiek te zien.")
else:
    st.info("Upload de Excel template die een ingevuld uitslagen tabblad bevat.")