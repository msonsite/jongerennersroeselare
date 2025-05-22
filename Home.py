import streamlit as st

st.markdown("""
<style>
body {
    background-color: #fafafa;
}

h1 {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
        Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    font-weight: 700;
    font-size: 3.5rem;
    color: #111;
    margin-bottom: 0.3rem;
}

h2 {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
        Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    font-weight: 400;
    font-size: 1.5rem;
    color: #666;
    margin-top: 0;
    margin-bottom: 3rem;
    letter-spacing: 0.05em;
}

p {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
        Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    font-weight: 300;
    font-size: 1.125rem;
    line-height: 1.6;
    color: #444;
    max-width: 600px;
}

a {
    color: #fb5d01;  /* jouw accentkleur */
    text-decoration: none;
    font-weight: 600;
}

a:hover {
    text-decoration: underline;
}

footer {
    margin-top: 5rem;
    font-size: 0.875rem;
    color: #999;
}

header, footer, .css-18e3th9 {
    visibility: hidden;
    height: 0px;
    margin: 0;
    padding: 0;
}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div style='text-align: center; padding-top: 30px; padding-bottom: 20px;'>
        <h1 style='color: #fb5d01; font-size: 3em; margin-bottom: 5px;'>Wielrennen Performance</h1>
        <h2 style='color: #333; font-weight: 300; margin-top: 0;'>Focus. Analyse. Winnen.</h2>
        <img src='https://jongerennersroeselare.be/assets/images/logo_jrr.png' width='200' style='margin-top: 20px;'/>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; font-size: 1.1em; margin-top: 20px; color: #444;'>
        <p>Deze website helpt bij het analyseren van rennerdata.<br>
        De weg naar succes begint met de juiste inzichten.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='padding: 20px 40px; font-size: 1.05em; color: #222;'>
        <p><b>Gebruik het menu links om te navigeren naar:</b></p>
        <ul>
            <li><b>🏠 Home</b> – Overzicht en introductie.</li>
            <li><b>🏁 Uitslagen</b> – Bekijk en vergelijk de prestaties van de renners.</li>
            <li><b>⛰️ GPX Hoogteprofiel Generator</b> – Maak een afdrukbaar profiel van een GPX-bestand.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with st.container():
    st.markdown("<hr style='border:1px solid #ccc; margin-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: gray; padding-bottom: 20px;'>
        💻 Ontwikkeld door <strong>Sander de Lobel</strong>
    </div>
    """, unsafe_allow_html=True)
