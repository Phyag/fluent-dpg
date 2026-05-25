"""
Fluent 2 Design System color tokens and theme engine for DearPyGUI.

Implements the full Fluent 2 palette (light/dark), rounded corner radii,
elevation shadows, and typography scale. Maps Fluent tokens to DearPyGUI
style constants.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional
import dearpygui.dearpygui as dpg


class FluentThemeMode(Enum):
    LIGHT = "light"
    DARK = "dark"


# ── Fluent 2 Color Palette ──────────────────────────────────────────────────

class FluentColors:
    """
    Fluent 2 brand + system colors.
    Reference: https://fluent2.microsoft.design/color
    """
    # Brand accent
    ACCENT_LIGHT      = "#0078D4"
    ACCENT_DARK       = "#4DA3E8"
    ACCENT_HOVER_LIGHT = "#106EBE"
    ACCENT_HOVER_DARK  = "#60CDFF"
    ACCENT_PRESSED_LIGHT = "#005A9E"
    ACCENT_PRESSED_DARK  = "#4CA2E8"

    # Neutral / text
    TEXT_PRIMARY_LIGHT   = "#242424"
    TEXT_PRIMARY_DARK    = "#FFFFFF"
    TEXT_SECONDARY_LIGHT = "#616161"
    TEXT_SECONDARY_DARK  = "#D6D6D6"
    TEXT_DISABLED_LIGHT  = "#A0A0A0"
    TEXT_DISABLED_DARK   = "#8C8C8C"
    TEXT_ON_ACCENT_LIGHT = "#FFFFFF"
    TEXT_ON_ACCENT_DARK  = "#000000"

    # Backgrounds
    BACKGROUND_LIGHT       = "#F3F3F3"
    BACKGROUND_DARK        = "#202020"
    SURFACE_LIGHT          = "#FFFFFF"
    SURFACE_DARK           = "#2D2D2D"
    SURFACE_SUBTLE_LIGHT   = "#FAFAFA"
    SURFACE_SUBTLE_DARK    = "#383838"
    SURFACE_BRIGHT_LIGHT   = "#FFFFFF"
    SURFACE_BRIGHT_DARK    = "#3D3D3D"
    CARD_LIGHT             = "#FFFFFF"
    CARD_DARK              = "#323232"
    CARD_BRIGHT_LIGHT      = "#FFFFFF"
    CARD_BRIGHT_DARK       = "#3D3D3D"

    # Borders
    BORDER_LIGHT    = "#E0E0E0"
    BORDER_DARK     = "#424242"
    BORDER_STRONG_LIGHT = "#D1D1D1"
    BORDER_STRONG_DARK  = "#5C5C5C"

    # Fill / interactive
    FILL_SUBTLE_LIGHT      = "#F5F5F5"
    FILL_SUBTLE_DARK       = "#3A3A3A"
    FILL_SUBTLE_HOVER_LIGHT = "#EBEBEB"
    FILL_SUBTLE_HOVER_DARK  = "#454545"
    FILL_SUBTLE_PRESSED_LIGHT = "#E0E0E0"
    FILL_SUBTLE_PRESSED_DARK  = "#505050"

    # Semantic
    SUCCESS_LIGHT = "#0F7B0F"
    SUCCESS_DARK  = "#6CCB5F"
    WARNING_LIGHT = "#986F0B"
    WARNING_DARK  = "#FCE100"
    DANGER_LIGHT  = "#D13438"
    DANGER_DARK   = "#FF6B6B"
    INFO_LIGHT    = "#0078D4"
    INFO_DARK     = "#60CDFF"

    # Control
    CONTROL_DEFAULT_LIGHT         = "#FFFFFF"
    CONTROL_DEFAULT_DARK          = "#3D3D3D"
    CONTROL_DEFAULT_HOVER_LIGHT   = "#F5F5F5"
    CONTROL_DEFAULT_HOVER_DARK    = "#454545"
    CONTROL_DEFAULT_PRESSED_LIGHT = "#EBEBEB"
    CONTROL_DEFAULT_PRESSED_DARK  = "#505050"

    # Smoke / overlay
    SMOKE_LIGHT = "rgba(0, 0, 0, 0.3)"
    SMOKE_DARK  = "rgba(0, 0, 0, 0.4)"


# ── Fluent 2 Design Tokens ──────────────────────────────────────────────────

class FluentTokens:
    """
    Fluent 2 design tokens: corner radii, stroke widths, spacing, durations.
    Reference: https://fluent2.microsoft.design
    """
    # Corner radii (px)
    CORNER_RADIUS_NONE     = 0
    CORNER_RADIUS_SMALL    = 2
    CORNER_RADIUS_MEDIUM   = 4    # Default for most controls
    CORNER_RADIUS_LARGE    = 8    # Buttons, cards, dialogs
    CORNER_RADIUS_XLARGE   = 12   # Popovers, flyouts

    # Stroke widths
    STROKE_WIDTH_THIN  = 1
    STROKE_WIDTH_NORMAL = 1
    STROKE_WIDTH_THICK = 2

    # Spacing scale (px)
    SPACING_XS  = 2
    SPACING_S   = 4
    SPACING_M   = 8
    SPACING_L   = 12
    SPACING_XL  = 16
    SPACING_XXL = 24
    SPACING_XXXL = 32

    # Control sizing
    CONTROL_HEIGHT_SMALL  = 24
    CONTROL_HEIGHT_MEDIUM = 32   # Default
    CONTROL_HEIGHT_LARGE  = 40
    CONTROL_HEIGHT_XLARGE = 48

    # Icon sizes
    ICON_SMALL  = 12
    ICON_MEDIUM = 16
    ICON_LARGE  = 20
    ICON_XLARGE = 24

    # Font sizes (px)
    FONT_CAPTION  = 12
    FONT_BODY     = 14    # Default body text
    FONT_BODY_LG  = 16
    FONT_SUBTITLE = 20
    FONT_TITLE_III = 24
    FONT_TITLE_II  = 28
    FONT_TITLE_I   = 32
    FONT_LARGE_TITLE = 40

    # Font weight
    FONT_WEIGHT_REGULAR  = 400
    FONT_WEIGHT_SEMIBOLD = 600
    FONT_WEIGHT_BOLD     = 700

    # Animation durations (ms)
    DURATION_INSTANT  = 0
    DURATION_ULTRA_FAST  = 50
    DURATION_FASTER    = 100
    DURATION_FAST      = 150
    DURATION_NORMAL    = 200
    DURATION_GENTLE    = 250
    DURATION_SLOW      = 300
    DURATION_SLOWER    = 400

    # Font family
    FONT_FAMILY = "Segoe UI Variable, Segoe UI, system-ui, -apple-system, sans-serif"


# ── Theme Engine ─────────────────────────────────────────────────────────────

@dataclass
class _ThemeColors:
    """Resolved color palette for a given mode."""
    accent: str
    accent_hover: str
    accent_pressed: str
    text_primary: str
    text_secondary: str
    text_disabled: str
    text_on_accent: str
    background: str
    surface: str
    surface_subtle: str
    surface_bright: str
    card: str
    card_bright: str
    border: str
    border_strong: str
    fill_subtle: str
    fill_subtle_hover: str
    fill_subtle_pressed: str
    control_default: str
    control_default_hover: str
    control_default_pressed: str
    success: str
    warning: str
    danger: str
    info: str
    smoke: str


@dataclass
class FluentTheme:
    """
    Fluent 2 theme singleton for DearPyGUI.

    Usage:
        theme = FluentTheme(mode=FluentThemeMode.LIGHT)
        theme.apply()           # Apply to DearPyGUI
        colors = theme.colors    # Resolve color for current mode
    """
    mode: FluentThemeMode = FluentThemeMode.LIGHT
    _instance: Optional["FluentTheme"] = field(default=None, repr=False)
    _colors: Optional[_ThemeColors] = field(default=None, repr=False)

    @property
    def colors(self) -> _ThemeColors:
        if self._colors is None:
            self._colors = self._resolve_colors()
        return self._colors

    def _resolve_colors(self) -> _ThemeColors:
        dark = self.mode == FluentThemeMode.DARK
        pick = lambda light, dark_val: dark_val if dark else light
        return _ThemeColors(
            accent=pick(FluentColors.ACCENT_LIGHT, FluentColors.ACCENT_DARK),
            accent_hover=pick(FluentColors.ACCENT_HOVER_LIGHT, FluentColors.ACCENT_HOVER_DARK),
            accent_pressed=pick(FluentColors.ACCENT_PRESSED_LIGHT, FluentColors.ACCENT_PRESSED_DARK),
            text_primary=pick(FluentColors.TEXT_PRIMARY_LIGHT, FluentColors.TEXT_PRIMARY_DARK),
            text_secondary=pick(FluentColors.TEXT_SECONDARY_LIGHT, FluentColors.TEXT_SECONDARY_DARK),
            text_disabled=pick(FluentColors.TEXT_DISABLED_LIGHT, FluentColors.TEXT_DISABLED_DARK),
            text_on_accent=pick(FluentColors.TEXT_ON_ACCENT_LIGHT, FluentColors.TEXT_ON_ACCENT_DARK),
            background=pick(FluentColors.BACKGROUND_LIGHT, FluentColors.BACKGROUND_DARK),
            surface=pick(FluentColors.SURFACE_LIGHT, FluentColors.SURFACE_DARK),
            surface_subtle=pick(FluentColors.SURFACE_SUBTLE_LIGHT, FluentColors.SURFACE_SUBTLE_DARK),
            surface_bright=pick(FluentColors.SURFACE_BRIGHT_LIGHT, FluentColors.SURFACE_BRIGHT_DARK),
            card=pick(FluentColors.CARD_LIGHT, FluentColors.CARD_DARK),
            card_bright=pick(FluentColors.CARD_BRIGHT_LIGHT, FluentColors.CARD_BRIGHT_DARK),
            border=pick(FluentColors.BORDER_LIGHT, FluentColors.BORDER_DARK),
            border_strong=pick(FluentColors.BORDER_STRONG_LIGHT, FluentColors.BORDER_STRONG_DARK),
            fill_subtle=pick(FluentColors.FILL_SUBTLE_LIGHT, FluentColors.FILL_SUBTLE_DARK),
            fill_subtle_hover=pick(FluentColors.FILL_SUBTLE_HOVER_LIGHT, FluentColors.FILL_SUBTLE_HOVER_DARK),
            fill_subtle_pressed=pick(FluentColors.FILL_SUBTLE_PRESSED_LIGHT, FluentColors.FILL_SUBTLE_PRESSED_DARK),
            control_default=pick(FluentColors.CONTROL_DEFAULT_LIGHT, FluentColors.CONTROL_DEFAULT_DARK),
            control_default_hover=pick(FluentColors.CONTROL_DEFAULT_HOVER_LIGHT, FluentColors.CONTROL_DEFAULT_HOVER_DARK),
            control_default_pressed=pick(FluentColors.CONTROL_DEFAULT_PRESSED_LIGHT, FluentColors.CONTROL_DEFAULT_PRESSED_DARK),
            success=pick(FluentColors.SUCCESS_LIGHT, FluentColors.SUCCESS_DARK),
            warning=pick(FluentColors.WARNING_LIGHT, FluentColors.WARNING_DARK),
            danger=pick(FluentColors.DANGER_LIGHT, FluentColors.DANGER_DARK),
            info=pick(FluentColors.INFO_LIGHT, FluentColors.INFO_DARK),
            smoke=pick(FluentColors.SMOKE_LIGHT, FluentColors.SMOKE_DARK),
        )

    # ── DearPyGUI Style Application ─────────────────────────────────────────

    @staticmethod
    def _hex_to_rgba(hex_color: str) -> tuple:
        """Convert '#RRGGBB' or 'rgba(r,g,b,a)' to tuple (R, G, B, A) 0-255."""
        hex_color = hex_color.strip()
        if hex_color.startswith("rgba"):
            import re
            m = re.match(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", hex_color)
            if m:
                return (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(float(m.group(4)) * 255))
            return (0, 0, 0, 255)
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b, 255)
        return (0, 0, 0, 255)

    def apply(self, font_path: Optional[str] = None):
        """Apply Fluent 2 theme to DearPyGUI global style."""
        c = self.colors
        dark = self.mode == FluentThemeMode.DARK

        # ── DearPyGUI theme values ──────────────────────────────────────────
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                # Colors
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, self._hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, self._hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, self._hex_to_rgba(c.fill_subtle_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_Border, self._hex_to_rgba(c.border))
                dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_Text, self._hex_to_rgba(c.text_primary))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, self._hex_to_rgba(c.surface))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, self._hex_to_rgba(c.surface))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, self._hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, self._hex_to_rgba(c.surface))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, self._hex_to_rgba(c.card))
                dpg.add_theme_color(dpg.mvThemeCol_Header, self._hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, self._hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, self._hex_to_rgba(c.fill_subtle_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_Button, self._hex_to_rgba(c.control_default))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self._hex_to_rgba(c.control_default_hover))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self._hex_to_rgba(c.control_default_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, self._hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, self._hex_to_rgba(c.border_strong))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, self._hex_to_rgba(c.text_secondary))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, self._hex_to_rgba(c.text_primary))
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, self._hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, self._hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, self._hex_to_rgba(c.accent_hover))
                dpg.add_theme_color(dpg.mvThemeCol_Tab, self._hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered, self._hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_TabActive, self._hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, self._hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, self._hex_to_rgba(c.accent_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_PlotLines, self._hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered, self._hex_to_rgba(c.accent_hover))
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, self._hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered, self._hex_to_rgba(c.accent_hover))
                dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, self._hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, self._hex_to_rgba(c.border))
                dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, self._hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, self._hex_to_rgba(c.surface))
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, self._hex_to_rgba(c.surface_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, self._hex_to_rgba(c.accent_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, self._hex_to_rgba(c.smoke))
                dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight, self._hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg, self._hex_to_rgba(c.smoke))
                dpg.add_theme_color(dpg.mvThemeCol_Separator, self._hex_to_rgba(c.border))
                dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered, self._hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive, self._hex_to_rgba(c.accent_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, self._hex_to_rgba(c.border))
                dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered, self._hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive, self._hex_to_rgba(c.accent_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget, self._hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_DockingPreview, self._hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg, self._hex_to_rgba(c.background))
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, self._hex_to_rgba(c.background))
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self._hex_to_rgba(c.surface))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBorder, self._hex_to_rgba(c.border_strong))

                # Styling — Fluent 2 rounded corners
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, FluentTokens.CORNER_RADIUS_LARGE)
                dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, FluentTokens.CORNER_RADIUS_XLARGE)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, FluentTokens.CORNER_RADIUS_LARGE)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
                dpg.add_theme_style(dpg.mvStyleVar_TabRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, FluentTokens.STROKE_WIDTH_NORMAL)

                # Spacing
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, FluentTokens.SPACING_M, FluentTokens.SPACING_S)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, FluentTokens.SPACING_M, FluentTokens.SPACING_M)
                dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, FluentTokens.SPACING_M, FluentTokens.SPACING_S)
                dpg.add_theme_style(dpg.mvStyleVar_IndentSpacing, FluentTokens.SPACING_L)
                dpg.add_theme_style(dpg.mvStyleVar_CellPadding, FluentTokens.SPACING_M, FluentTokens.SPACING_S)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, FluentTokens.SPACING_L, FluentTokens.SPACING_M)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, FluentTokens.STROKE_WIDTH_NORMAL)
                dpg.add_theme_style(dpg.mvStyleVar_WindowMinSize, 200, 100)
                dpg.add_theme_style(dpg.mvStyleVar_PopupBorderSize, FluentTokens.STROKE_WIDTH_THICK)

            # Button accent color override
            with dpg.theme_component(dpg.mvButton, enabled_state=True):
                dpg.add_theme_color(dpg.mvThemeCol_Button, self._hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self._hex_to_rgba(c.accent_hover))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self._hex_to_rgba(c.accent_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_Text, self._hex_to_rgba(c.text_on_accent))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_LARGE)

        dpg.bind_theme(global_theme)

        # Background color for viewport
        dpg.configure_viewport(bg_color=self._hex_to_rgba(c.background))

    def toggle(self):
        """Toggle between light and dark mode, then re-apply."""
        self.mode = (
            FluentThemeMode.DARK
            if self.mode == FluentThemeMode.LIGHT
            else FluentThemeMode.LIGHT
        )
        self._colors = self._resolve_colors()
        self.apply()

    def set_mode(self, mode: FluentThemeMode):
        """Set theme mode explicitly."""
        self.mode = mode
        self._colors = self._resolve_colors()
        self.apply()

    def toggle_color(self, hex_color: str) -> tuple:
        """Helper: hex → RGBA tuple for DearPyGUI."""
        return self._hex_to_rgba(hex_color)