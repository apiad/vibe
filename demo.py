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


import streamlit as st
from vibe.style import Style

# Define a layout where every nested container becomes a white card
grid_layout = (
    Style(
        display="grid",
        grid_template_columns="1fr 1fr",
        gap="20px",
        padding="20px",
        # background_color="#f8fafc" # Light grey background for the whole area
    )
    .container( # Target all nested st.container() blocks
        background_color="white",
        padding="20px",
        border_radius="12px",
        box_shadow="0 4px 6px -1px rgba(0,0,0,0.1)",
        border="1px solid #e2e8f0"
    )
    .button(width="100%") # Make all buttons inside span full width
)

st.header("Dashboard Grid")

with grid_layout:
    # This st.container automatically gets the card style!
    with st.container():
        st.subheader("Sales")
        st.metric("Total", "$45,000")
        st.button("View Details", key="b1")

    # So does this one
    with st.container():
        st.subheader("Traffic")
        st.metric("Visitors", "1,200")
        st.button("View Details", key="b2")

    # And this one...
    with st.container():
        st.subheader("Performance")
        st.line_chart([1, 2, 3, 2, 4])