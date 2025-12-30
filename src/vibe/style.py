from __future__ import annotations
import uuid
from typing import Dict
import streamlit as st


class Style:
    """
    A Streamlit-aware CSS engine using the ':has()' selector pattern.
    Allows defining scoped CSS rules that apply only within the context manager.
    """

    def __init__(self, **default_rules):
        self.id = f"vibe-{uuid.uuid4().hex[:6]}"
        # Store selectors and their corresponding rules
        # Format: { "selector": {"property": "value"} }
        self._selectors: Dict[str, Dict[str, str]] = {}
        self._container = None

        # If rules are passed to the constructor, apply them to the root container
        if default_rules:
            self.select("&", **default_rules)

    def _kebab(self, name: str) -> str:
        """Converts snake_case to kebab-case."""
        return name.replace("_", "-")

    def select(self, selector: str | None = None, on: str | None = None, **rules) -> Style:
        """
        Generic CSS selector.

        Args:
            selector: The CSS selector (e.g. 'div', 'p'). Defaults to '&' (the container).
            on: Pseudo-class to apply (e.g. 'hover', 'active', 'focus').
            **rules: CSS properties (snake_case handled automatically).
        """
        clean_rules = {self._kebab(k): str(v) for k, v in rules.items()}

        # Default to root if no selector provided
        if selector is None:
            selector = ""

        # If 'on' is provided, we need to append the pseudo-class.
        # If the selector implies the root ('&' or empty), we must ensure '&' is explicit.
        if on:
            base = selector if selector else "&"
            selector = f"{base}:{on}"

        # Final fallback for bare root selector
        if selector == "":
            selector = "&"

        if selector not in self._selectors:
            self._selectors[selector] = {}

        self._selectors[selector].update(clean_rules)
        return self

    def css(self) -> str:
        """Generates the full scoped CSS string."""
        # The magic selector: Finds the *innermost* Streamlit Vertical Block
        # that contains our hidden marker

        # NOTE: This will break when Streamlit changes
        container_scope = (
            f'div[data-testid="stVerticalBlock"]:'
            f'has(> div > div > span#{self.id})'
        )

        blocks = []

        blocks.append(
            f'{container_scope} > div:has(span#{self.id}) {{ display: none !important; }}'
        )

        for selector, rules in self._selectors.items():
            if not rules:
                continue

            # 1. Format the rules
            rules_str = "\n".join(
                [f"    {prop}: {val} !important;" for prop, val in rules.items()]
            )

            # 2. Scope the selector
            if selector == "&":
                # Target the container itself
                final_selector = container_scope
            else:
                # Target children inside the container
                # We handle generic cases. If it's a direct child selector (e.g. > div), preserve it.
                if selector.startswith("&"):
                    # Handle pseudo-classes on the container (e.g. &:hover)
                    final_selector = selector.replace("&", container_scope)
                else:
                    final_selector = f"{container_scope} {selector}"

            blocks.append(f"{final_selector} {{\n{rules_str}\n}}")

        return "\n\n".join(blocks)

    def __enter__(self):
        # 1. Create the native Streamlit container
        self._container = st.container()

        # 2. Enter the container's context
        self._container.__enter__()

        # 3. Generate and inject CSS + Marker
        full_css = self.css()

        # We inject the marker (span) and the style block.
        # The :has() selector in CSS will find this span's parent.
        self._container.html(
            f"""
            <style>{full_css}</style>
            <span id="{self.id}" style="display:none;"></span>
            """,
        )

        # 4. Return the container so users can add widgets to it
        return self._container

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 5. Exit the native container's context
        if self._container:
            self._container.__exit__(exc_type, exc_val, exc_tb)

    def __repr__(self):
        return f"<Style id={self.id} selectors={list(self._selectors.keys())}>"

    # --- STREAMLIT HELPERS ---
    # These methods just map human-friendly names to Streamlit's internal CSS structure.

    def button(self, **rules) -> Style:
        """Styles st.button, st.download_button, st.form_submit_button."""
        # Target the button element inside the stButton wrapper
        return self.select('div[data-testid="stButton"] button', **rules)

    def input(self, **rules) -> Style:
        """Styles text_input, number_input, text_area (border/bg)."""
        # Targets the input container (not the text itself)
        return self.select('div[data-baseweb="input"]', **rules)

    def slider(self, main_color=None, **rules) -> Style:
        """Styles st.slider."""
        if main_color:
            rules.update({"color": main_color, "accent-color": main_color})
            # Thumb and Track styling requires deeper selection which is hard to map generically,
            # but we can apply basic colors to the wrapper.
        return self.select('div[data-testid="stSlider"]', **rules)

    def metric(self, **rules) -> Style:
        """Styles st.metric container."""
        return self.select('div[data-testid="stMetric"]', **rules)

    def header(self, **rules) -> Style:
        """Styles h1, h2, h3 tags."""
        return self.select('h1, h2, h3', **rules)

    def text(self, **rules) -> Style:
        """Styles p (standard text) tags."""
        return self.select('p', **rules)

    def container(self, **rules) -> Style:
        """
        Styles nested st.container() blocks.
        Useful for making a 'grid of cards' layout.
        """
        return self.select('div[data-testid="stVerticalBlock"]', **rules)

    def column(self, **rules) -> Style:
        """
        Styles st.column() wrappers.
        Note: Columns often contain a vertical block inside them.
        """
        return self.select('div[data-testid="stColumn"]', **rules)

    def expander(self, **rules) -> Style:
        """Styles st.expander() container."""
        return self.select('div[data-testid="stExpander"]', **rules)