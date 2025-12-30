# Vibe ⚡️

**Tailwind-like styling for Streamlit. No CSS files. No hacks. Just Vibe.**

Vibe is a lightweight layout and styling engine for Streamlit. It lets you build modern, responsive interfaces using pure Python with a robust scoping system that ensures your styles never leak.

```python
import vibe as vb
import streamlit as st

# A clean grid layout with styled metrics
with vb.grid(cols=2, gap="2rem"):
    with vb.Style(background_color="white", padding="20px", border_radius="10px", box_shadow="0 4px 6px rgba(0,0,0,0.1)"):
        st.metric("Revenue", "$42,000", "+12%")
```

> [Check out the online demo!](https://st-vibe.streamlit.app/)

## Why Vibe?

Streamlit is great for data, but styling it often involves brittle `st.markdown` hacks that break easily and leak styles globally.

**Vibe is different:**

* **🛡️ True Scoping:** Uses the modern CSS `:has()` selector pattern to lock styles to specific containers.
* **🎨 Pythonic API:** Chainable methods like `.button()`, `.input()`, and `.select()`.
* **📐 Real Layouts:** Proper CSS Grid and Flexbox support (`vb.grid`, `vb.flex`) that works with native Streamlit widgets.
* **⚡️ Zero JavaScript:** No heavy custom components, just smart CSS injection.

## 📦 Installation

```bash
pip install streamlit-vibe
```
## 🚀 Quick Start

### 1. The Basics

Wrap standard Streamlit code in a `vb.Style` context. Everything inside gets styled.

```python
import vibe as vb
import streamlit as st

# Define a theme
neo_brutalism = (
    vb.Style(background_color="#fff", border="2px solid black", box_shadow="4px 4px 0px black")
    .button(background_color="#ffcc00", color="black", border="2px solid black", font_weight="bold")
    .header(font_family="Courier New")
)

# Use it
with neo_brutalism:
    st.title("Hello Vibe")
    st.button("Click Me") # This button is yellow & bold
```

### 2. Powerful Layouts

Forget `st.columns`. Use real CSS Grid and Flexbox.

```python
# A responsive grid: 1 column on mobile, 3 on desktop
with vb.grid(cols=[1, 3], gap="20px"):

    # Sidebar Area
    with vb.flex(direction="column", gap="10px"):
        st.button("Dashboard", use_container_width=True)
        st.button("Settings", use_container_width=True)

    # Main Content Area
    with vb.Style(background_color="white", padding="2rem", border_radius="8px"):
        st.line_chart([10, 20, 15, 25])
```

## ✨ Features

### 🎯 Component Targeting

Don't inspect the DOM to find obscure class names. Vibe knows Streamlit's internals.

```python
vb.Style()
    .button(...)    # Targets st.button, st.download_button
    .input(...)     # Targets st.text_input, st.number_input
    .metric(...)    # Targets st.metric
    .expander(...)  # Targets st.expander
    .header(...)    # Targets h1, h2, h3
    .text(...)      # Targets p tags
```

### 🖱️ Interactive States

Add hover effects (`on="hover"`) or focus states easily.

```python
# A container that lifts up when you hover over it
interactive_card = (
    vb.Style(transition="transform 0.2s", padding="20px", border_radius="10px")
    .select(on="hover", transform="translateY(-5px)", box_shadow="0 10px 20px rgba(0,0,0,0.1)")
)

with interactive_card:
    st.write("Hover me!")
```

### 📦 Automatic Cards

Turn every nested container into a card automatically using the `.container()` target. Perfect for dashboards.

```python
dashboard = vb.Style(display="grid", grid_template_columns="1fr 1fr", gap="20px") \
    .container(background="white", padding="20px", border_radius="12px", box_shadow="0 2px 4px rgba(0,0,0,0.1)")

with dashboard:
    with st.container():
        st.write("I'm automatically a card!")
    with st.container():
        st.write("Me too!")
```

## 🧩 Advanced Usage

### The "Slick" Chatbot Layout

Create a narrow, centered, shadow-styled chat interface.

```python
chat_theme = (
    vb.Style(max_width="700px", margin="auto", padding_top="4rem") # Centered Container
    .select("div[data-testid='stChatMessage']", # Target Chat Bubbles
            border_radius="16px",
            background_color="#f8fafc",
            border="1px solid #e2e8f0")
)

with chat_theme:
    st.title("Assistant")
    st.chat_message("ai").write("How can I help you today?")
```

### Nesting & Composition

Styles compose naturally. You can nest a grid inside a style block inside a flex container.

```python
# Style outer container
with vb.Style(background_color="#1e293b", color="white", padding="20px"):
    st.write("## Dark Mode Panel")

    # Create layout inside
    with vb.grid(cols=2, gap="10px"):
        st.metric("User", "Alice")

        # Nested style override for just this button
        with vb.Style().button(background_color="#ef4444"):
            st.button("Delete Account")
```

## 🛠 How it Works

Vibe uses a smart **CSS Injection Strategy**:

1. It wraps your content in a standard `st.container`.
2. It injects a hidden marker `<span>` with a unique ID inside that container.
3. It generates CSS using the `:has()` selector (e.g., `div:has(> ... > span#unique-id)`) to target **only** that specific container.

This guarantees that **styles never leak** to other parts of your app, even if you use the same component names.

## License

MIT. Go build something beautiful.
