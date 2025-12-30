from typing import Union, List
from .style import Style

__version__ = "0.2.2"


def grid(
    cols: Union[int, str, List[Union[int, str]]] = 1,
    rows: Union[int, str, List[Union[int, str]]] | None = None,
    gap: str = "1rem",
    align: str | None = None,
    justify: str | None = None,
    **kwargs,
) -> Style:
    """
    Creates a CSS Grid layout.

    Args:
        cols: Number of columns (int) or specific widths (list/str).
              Examples: 3, "1fr 2fr", [1, 2, 1]
        rows: Number of rows or specific heights.
        gap: Spacing between items.
    """
    # 1. Parse Columns
    if isinstance(cols, int):
        # repeat(N, minmax(0, 1fr)) is robust: prevents blowout on wide content
        template_cols = f"repeat({cols}, minmax(0, 1fr))"
    elif isinstance(cols, list):
        # Convert [1, 2] -> "1fr 2fr"
        template_cols = " ".join(
            [f"{c}fr" if isinstance(c, (int, float)) else str(c) for c in cols]
        )
    else:
        template_cols = cols

    # 2. Parse Rows (Optional)
    template_rows = None
    if rows:
        if isinstance(rows, int):
            template_rows = f"repeat({rows}, 1fr)"
        elif isinstance(rows, list):
            template_rows = " ".join(
                [f"{r}fr" if isinstance(r, (int, float)) else str(r) for r in rows]
            )
        else:
            template_rows = rows

    # 3. Build Rules
    rules = {
        "display": "grid",
        "grid_template_columns": template_cols,
        "gap": gap,
        **kwargs,
    }

    if template_rows:
        rules["grid_template_rows"] = template_rows
    if align:
        rules["align_items"] = align
    if justify:
        rules["justify_items"] = justify

    # 4. Return Style Object
    # We add a generic selector for direct children divs to ensure they behave
    # well in a grid (Streamlit wraps everything in divs).
    style = Style(**rules)

    # Ensure items take full width/height of their cell
    style.select("& > div", width="100%", height="100%")

    return style


def flex(
    direction: str = "row",
    gap: str = "1rem",
    justify: str = "start",
    align: str = "center",
    wrap: bool = False,
    **kwargs,
) -> Style:
    """
    Creates a CSS Flexbox layout.
    """
    rules = {
        "display": "flex",
        "flex_direction": direction,
        "gap": gap,
        "justify_content": justify,
        "align_items": align,
        "flex_wrap": "wrap" if wrap else "nowrap",
        **kwargs,
    }

    style = Style(**rules)

    # Streamlit's internal wrappers can sometimes collapse in flex containers.
    # We force them to respect the flex model.
    style.select("& > div", min_width="0")

    return style
