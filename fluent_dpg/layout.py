"""
Fluent 2 layout containers for DearPyGUI.

Provides:
    FluentStackPanel   — Horizontal/vertical stack
    FluentGrid         — Grid layout (row/column)
    FluentCard         — Card container with elevation
    FluentExpanderGroup — Accordion group (only one expanded)
    FluentDialogHost   — Dialog management
    FluentScrollViewer — Scrollable container
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
import dearpygui.dearpygui as dpg

from fluent_dpg.theme import FluentTheme, FluentTokens


def _hex_to_rgba(hex_color: str):
    return FluentTheme._hex_to_rgba(hex_color)


class FluentStackPanel:
    """Stack panel layout (horizontal or vertical)."""

    def __init__(self, orientation: str = "vertical", tag: Optional[str] = None,
                 parent: Optional[Any] = None, spacing: int = FluentTokens.SPACING_M):
        self.tag = tag or f"fluent_stack_{id(self)}"
        horizontal = orientation == "horizontal"
        dpg.add_group(horizontal=horizontal, tag=self.tag, parent=parent)


class FluentGrid:
    """
    Grid layout helper.
    DearPyGUI doesn't have native grid, so this uses groups + sizing hints.
    """

    def __init__(self, cols: int = 2, col_ratios: Optional[List[int]] = None,
                 tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 0, spacing: int = FluentTokens.SPACING_M):
        self.tag = tag or f"fluent_grid_{id(self)}"
        self._cols = cols
        self._col_ratios = col_ratios or [1] * cols
        self._width = width
        self._spacing = spacing

        # Use a table as grid
        dpg.add_table(tag=self.tag, header_row=False, parent=parent, width=width)
        for i in range(cols):
            dpg.add_table_column(label="", width_stretch=True, parent=self.tag)

    def add_cell(self, row: int, col: int, widget_tag: str):
        """Place an existing widget into a grid cell."""
        dpg.move_item(widget_tag, parent=self.tag)

    def add_row(self, *items: Any):
        """Add a row of items."""
        with dpg.table_row(parent=self.tag):
            for item in items:
                if isinstance(item, str):
                    dpg.add_text(item)
                else:
                    dpg.add_text(str(item))


class FluentCard:
    """
    Card container with Fluent 2 elevation styling.
    Rounded corners, subtle shadow via border, surface background.
    """

    def __init__(self, tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 300, height: int = 200, title: str = ""):
        self.tag = tag or f"fluent_card_{id(self)}"
        c = FluentTheme().colors

        with dpg.child_window(tag=self.tag, width=width, height=height,
                               parent=parent, no_scrollbar=True):
            if title:
                dpg.add_text(title)
                dpg.add_spacer(height=FluentTokens.SPACING_M)

            # Content area
            with dpg.group(tag=f"{self.tag}_content"):
                pass

        with dpg.theme() as card_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _hex_to_rgba(c.card))
                dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border))
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, FluentTokens.CORNER_RADIUS_LARGE)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, FluentTokens.STROKE_WIDTH_NORMAL)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, FluentTokens.SPACING_L, FluentTokens.SPACING_M)
        dpg.bind_item_theme(self.tag, card_theme)

    def add_content(self, widget_tag: str):
        """Add a widget to the card content area."""
        dpg.move_item(widget_tag, parent=f"{self.tag}_content")


class FluentExpanderGroup:
    """
    Accordion group: only one FluentExpander can be open at a time.
    """

    def __init__(self, tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 400):
        self.tag = tag or f"fluent_accordion_{id(self)}"
        self._expanders: List = []
        self._width = width

        dpg.add_group(tag=self.tag, parent=parent)

    def add_expander(self, header: str, content: str = "") -> str:
        """Add an expander to the group."""
        from fluent_dpg.controls import FluentExpander
        exp = FluentExpander(header=header, content=content,
                             parent=self.tag, width=self._width)
        self._expanders.append(exp)
        # Override toggle to close siblings
        orig_toggle = exp._toggle
        def _close_others(sender, app_data, user_data):
            orig_toggle(sender, app_data, user_data)
            if exp._expanded:
                for other in self._expanders:
                    if other is not exp and other._expanded:
                        other._toggle(None, None, None)
        exp._toggle = _close_others
        return exp.tag


class FluentDialogHost:
    """
    Host for managing FluentContentDialog instances.
    Provides show_dialog / hide_dialog methods.
    """

    def __init__(self, tag: Optional[str] = None, parent: Optional[Any] = None):
        self.tag = tag or f"fluent_dialoghost_{id(self)}"
        self._dialogs: Dict[str, Any] = {}
        dpg.add_group(tag=self.tag, parent=parent)

    def register_dialog(self, dialog_id: str, dialog: Any):
        """Register a dialog for management."""
        self._dialogs[dialog_id] = dialog

    def show_dialog(self, dialog_id: str):
        """Show a registered dialog."""
        if dialog_id in self._dialogs:
            self._dialogs[dialog_id].show()

    def hide_dialog(self, dialog_id: str):
        """Hide a registered dialog."""
        if dialog_id in self._dialogs:
            self._dialogs[dialog_id].hide()


class FluentScrollViewer:
    """Scrollable container with Fluent styling."""

    def __init__(self, tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 400, height: int = 300,
                 horizontal_scroll: bool = False, vertical_scroll: bool = True):
        self.tag = tag or f"fluent_scroll_{id(self)}"
        c = FluentTheme().colors

        dpg.add_child_window(tag=self.tag, width=width, height=height,
                              parent=parent, no_scrollbar=not vertical_scroll,
                              no_scroll_x=not horizontal_scroll)

        with dpg.theme() as scroll_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _hex_to_rgba(c.surface))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, _hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, _hex_to_rgba(c.border_strong))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, _hex_to_rgba(c.text_secondary))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, _hex_to_rgba(c.text_primary))
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 8)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
        dpg.bind_item_theme(self.tag, scroll_theme)
