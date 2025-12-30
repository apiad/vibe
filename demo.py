import streamlit as st
import vibe as vb

st.set_page_config(layout="wide")

# --- 1. THE BASICS: HELLO VIBE ---
st.title("Vibe Demo Gallery ⚡️")
st.write("Welcome to the new styling engine. No CSS files, just Python.")

# Simple styling context
with st.echo("below"):
    with vb.Style(background_color="#f3f4f6", padding="20px", border_radius="12px"):
        st.write("### 1. Basic Scoping")
        st.write("I am inside a styled block (grey background).")
        st.button("I am a standard button")

    # Proof of scoping
    st.write("I am outside the block (standard white background).")

st.divider()

# --- 2. COMPONENT TARGETING (THE "NEO-BRUTALISM" THEME) ---
st.header("2. Component Targeting")

with st.echo("below"):
    brutalist_theme = (
        vb.Style(
            background_color="#ffde59",  # Bright Yellow Background
            border="3px solid black",
            box_shadow="8px 8px 0px black",
            padding="2rem"
        )
        .header(font_family="Courier New, monospace", color="black")
        .button(
            background_color="white",
            color="black",
            border="2px solid black",
            box_shadow="4px 4px 0px black",
            font_weight="bold"
        )
        .input(border="2px solid black", border_radius="0px")
    )

    with brutalist_theme:
        st.header("NEO-BRUTALISM")
        st.write("We can target specific components like buttons and inputs easily.")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Username", placeholder="user_01")
        with col2:
            st.button("SUBMIT ACTION", use_container_width=True)

st.divider()

# --- 3. LAYOUTS: GRID & FLEX ---
st.header("3. Grid & Flex Layouts")

with st.echo("below"):
    # A responsive Bento-Box Grid
    # 1 column on mobile (implicit), 4 columns on desktop
    with vb.grid(cols=[1, 2, 1], gap="20px"):

        # Left: Stats
        with vb.Style(background_color="#e0f2fe", padding="20px", border_radius="16px"):
            st.metric("Growth", "+12%", "High")
            st.metric("Users", "1.2k", "+50")

        # Center: Main Chart Area (Spans 2 columns defined in grid)
        with vb.Style(background_color="#f0fdf4", padding="20px", border_radius="16px"):
            st.subheader("Revenue Trajectory")
            st.bar_chart([10, 25, 40, 30, 50, 60], height=200)

        # Right: Actions (Flex Layout inside a Grid Cell)
        with vb.Style(background_color="#fff1f2", padding="20px", border_radius="16px"):
            st.write("**Quick Actions**")
            # Nesting a Flex layout for buttons
            with vb.flex(direction="column", gap="10px"):
                st.button("🚀 Deploy")
                st.button("💾 Save")
                st.button("⚙️ Settings")

st.divider()

# --- 4. INTERACTIVITY: HOVER & ANIMATION ---
st.header("4. 'Pop' Effects (Hover States)")

with st.echo("below"):
    # Define a "Glass" card with a hover effect
    glass_card = (
        vb.Style(
            background_color="rgba(255, 255, 255, 0.4)",
            border="1px solid rgba(255, 255, 255, 0.2)",
            box_shadow="0 4px 6px rgba(0,0,0,0.05)",
            border_radius="16px",
            padding="30px",
            transition="transform 0.2s ease, box_shadow 0.2s ease" # Smooth animation
        )
        .select(on="hover",
                transform="translateY(-8px)",
                box_shadow="0 20px 40px rgba(0,0,0,0.1)")
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        with glass_card:
            st.subheader("Hover Me!")
            st.write("I lift up when you mouse over.")

    with col2:
        with glass_card:
            st.subheader("Me Too!")
            st.write("Interactivity makes apps feel alive.")

    with col3:
        with glass_card:
            st.subheader("And Me!")
            st.button("Click", key="glass_btn")

st.divider()

# --- 5. ADVANCED: THE "AUTO-CARD" DASHBOARD ---
st.header("5. The 'Auto-Card' Dashboard")
st.write("Style every nested container automatically using `.container()`.")

with st.echo("below"):
    # Create a master grid style that styles its children
    dashboard_style = (
        vb.grid(cols=3, gap="20px")
        .container( # Target all nested st.container() blocks
            background_color="white",
            padding="20px",
            border_radius="12px",
            box_shadow="0 2px 4px rgba(0,0,0,0.05)",
            border="1px solid #e2e8f0"
        )
        .header(font_family="Inter", font_size="16px", color="#64748b")
    )

    with st.container():
        st.caption("All boxes below are standard `st.container()`, automatically styled.")

        with dashboard_style:
            # Card 1
            with st.container():
                st.subheader("Active Sessions")
                st.metric("Count", "432")

            # Card 2
            with st.container():
                st.subheader("Server Load")
                st.slider("CPU", 0, 100, 45)

            # Card 3
            with st.container():
                st.subheader("Messages")
                st.text_input("Send broadcast", placeholder="Type here...")

st.divider()

# --- 6. ADVANCED: SLICK CHAT INTERFACE ---
st.header("6. Complex Nesting: Slick Chat")

with st.echo("below"):
    chat_layout = (
        vb.Style(
            max_width="700px",
            margin="auto",
            background_color="#ffffff",
            padding="2rem",
            border_radius="24px",
            box_shadow="0 20px 50px -12px rgba(0,0,0,0.1)"
        )
        # Style the chat bubbles specifically
        .select("div[data-testid='stChatMessage']",
                background_color="#f8fafc",
                border_radius="16px",
                border="1px solid #e2e8f0")
        # Style user bubble differently using :nth-child or specific attributes if available
        # For now, we style the input box
        .select("div[data-testid='stChatInput']",
                border_radius="20px")
    )

    with chat_layout:
        st.write("#### 🤖 AI Assistant")
        st.caption("A narrow, focused chat interface.")

        st.chat_message("assistant").write("Hello! I am styling this interface using Vibe.")
        st.chat_message("user").write("It looks much cleaner than the default!")
        st.chat_message("assistant").write("I know, right? No CSS files needed.")

        st.chat_input("Type a message...")
