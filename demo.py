import streamlit as st
import vibe as vb

# Define a custom style
my_style = (
    vb.Style(background_color="#f0f2f6", padding="20px",  border_radius="10px")
    .select("h1", color="royalblue", text_align="center")
    .select("p", font_size="18px", color="#333", text_align="center")
)

with my_style:
    st.write("# Hello Vibe")
    st.write("This paragraph and the header above are styled by the Style object.")

st.write("Back to normality here!")

st.divider()

# 1. Define a Theme
slick_card = (
    vb.Style(background_color="white",
          border_radius="16px",
          box_shadow="0 4px 12px rgba(0,0,0,0.05)",
          padding="2rem")
    .button(background_color="#1e293b", color="white", border_radius="20px")
    .input(border="1px solid #e2e8f0", background_color="#f8fafc")
    .header(font_family="Inter, sans-serif", color="#0f172a")
)

# 2. Use it
with slick_card:
    st.header("Login")
    st.text_input("Email")
    st.button("Continue")

# 3. Verify Scoping (Standard elements outside remain untouched)
st.button("I am standard grey")