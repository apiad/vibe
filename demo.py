import streamlit as st
import vibe as vb

# Define a custom style
my_style = (
    vb.Style(background_color="#f0f2f6", padding="20px", border_radius="10px")
    .select("h1", color="royalblue", text_align="center")
    .select("p", font_size="18px", color="#333")
)

with my_style:
    st.write("# Hello Vibe")
    st.write("This paragraph and the header above are styled by the Style object.")
