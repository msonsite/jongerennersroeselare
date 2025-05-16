import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.image("https://jongerennersroeselare.be/assets/images/logo_jrr.png", width=150)

st.markdown("""
<h1 style='color:#fb5d01;'>Uitslagen Men Juniors</h1>
<h2 style='color:#0000000;'>Seizoen 2025</h2>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

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
    else:
        st.info("Selecteer minstens een renner om de grafiek te zien.")
else:
    st.info("Upload een Excel file die een uitslagen tabblad bevat.")
