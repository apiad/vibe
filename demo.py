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


# Define a layout where every nested container becomes a white card
grid_layout = (
    vb.Style(
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


st.divider()

# A 3-column grid where the middle column is wider (1fr 2fr 1fr)
dashboard_grid = (
    vb.grid(cols=[1, 2, 1], gap="20px")
    .container( # Style every nested container as a card
        background_color="white",
        padding="20px",
        border_radius="16px",
        box_shadow="0 2px 5px rgba(0,0,0,0.05)"
    )
)

with dashboard_grid:
    # Column 1 (automatically placed)
    with st.container():
        st.subheader("Sidebar")
        st.button("Home", use_container_width=True)
        st.button("Settings", use_container_width=True)

    # Column 2
    with st.container():
        st.subheader("Main Feed")
        st.bar_chart([10, 20, 15, 25])

    # Column 3
    with st.container():
        st.subheader("Stats")
        st.metric("Users", "4.2k")


# A flex row that spreads items apart
navbar = (
    vb.flex(justify="space-between", align="center", background_color="#f8fafc", padding="15px", border_radius="12px")
    .button(background_color="transparent", color="#333", border="1px solid #ddd")
)

with navbar:
    st.write("### 🚀 MyApp") # Left side

    # Right side group
    # We can nest another flex container here for the buttons!
    with vb.flex(gap="10px"):
        st.button("Login")
        st.button("Sign Up")

st.divider()

# Create a card that lifts up when hovered
interactive_card = (
    vb.Style(
        background_color="white",
        padding="20px",
        border_radius="12px",
        box_shadow="0 4px 6px rgba(0,0,0,0.1)",
        transition="transform 0.2s, box-shadow 0.2s" # Base state
    )
    .select(on="hover", # Applies to the container (&:hover)
            transform="translateY(-5px)",
            box_shadow="0 10px 20px rgba(0,0,0,0.15)")
    .button(background_color="#333", color="white")
    .button(on="hover", # Applies to the button inside (button:hover)
            background_color="black",
            transform="scale(1.05)")
)

with interactive_card:
    st.write("### Hover me!")
    st.button("Click")