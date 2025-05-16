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
    st.markdown("<h1>Wielrennen Performance</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Focus. Analyse. Winnen.</h2>", unsafe_allow_html=True)

    st.image("https://jongerennersroeselare.be/assets/images/logo_jrr.png", width=220)

    st.markdown("""
    <p>
    Website ter analyse van data van de renners.<br>
    De weg naar succes begint met de juiste data.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p>
    Gebruik het menu links om te navigeren naar:
    <ul>
        <li><b>Home</b> – De Home-page</li>
        <li><b>Uitslagen</b> – Bekijk en vergelijk de uitslagen van de renners.</li>
    </ul>
    </p>
    """, unsafe_allow_html=True)

st.markdown("""
<footer>
    Gemaakt door Sander de Lobel | Performance Analyst | 2025 &nbsp;&nbsp;&nbsp;
    <a href="mailto:sanderdelobel@outlook.com">📧 Contact</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
    <a href="https://www.linkedin.com/in/sanderdelobel/" target="_blank">💻 LinkedIn</a>
</footer>
""", unsafe_allow_html=True)
