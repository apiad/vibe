from __future__ import annotations
import uuid
import textwrap
from typing import Dict, Any, Optional, Union

from streamlit.components.v2 import


class Style:
    """
    A Streamlit-aware CSS engine.
    Allows defining scoped CSS rules that apply only within the context manager.
    """

    def __init__(self, **default_rules):
        self.id = f"vibe-{uuid.uuid4().hex[:6]}"
        # Store selectors and their corresponding rules
        # Format: { "selector": {"property": "value"} }
        self._selectors: Dict[str, Dict[str, str]] = {}

        # If rules are passed to the constructor, apply them to the root container
        if default_rules:
            self.select("", **default_rules)

    def _kebab(self, name: str) -> str:
        """Converts snake_case to kebab-case."""
        return name.replace("_", "-")

    def select(self, selector: str, **rules) -> Style:
        """
        Generic CSS selector.
        The selector is automatically scoped to this Style instance's unique ID.
        """
        clean_rules = {self._kebab(k): str(v) for k, v in rules.items()}

        # Scope the selector. If selector is empty, it targets the wrapper div itself.
        scoped_selector = f"#:has({self.id}) {selector}".strip()

        if scoped_selector not in self._selectors:
            self._selectors[scoped_selector] = {}

        self._selectors[scoped_selector].update(clean_rules)
        return self

    def css(self) -> str:
        """Generates the full CSS string for all registered selectors."""
        blocks = []
        for selector, rules in self._selectors.items():
            if not rules:
                continue

            # We use !important to ensure we override Streamlit's base styles
            rules_str = "\n".join(
                [f"    {prop}: {val} !important;" for prop, val in rules.items()]
            )
            blocks.append(f"{selector} {{\n{rules_str}\n}}")

        return "\n\n".join(blocks)

    def __enter__(self):
        container = st.container()

        # 1. Inject the generated CSS
        full_css = self.css()

        container.markdown(f"<style>{full_css}</style>", unsafe_allow_html=True)
        container.markdown(
            f'<span id="{self.id}" class="vibe-container"></span>',
            unsafe_allow_html=True,
        )

        return container.__enter__()

    def __exit__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return f"<Style id={self.id} selectors={list(self._selectors.keys())}>"
