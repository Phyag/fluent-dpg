"""
Fluent 2 styled controls for DearPyGUI.

Each control class encapsulates:
    • DearPyGUI widget creation with Fluent styling
    • Hover/pressed/active animations
    • Data binding to ViewModel properties
    • Consistent Fluent 2 visual language
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Tuple
import dearpygui.dearpygui as dpg

from fluent_dpg.theme import FluentTheme, FluentColors, FluentTokens
from fluent_dpg.viewmodel import ViewModel, BindableProperty, Command
from fluent_dpg.animations import FluentAnimator, Animation, Easing


def _hex_to_rgba(hex_color: str) -> Tuple[int, int, int, int]:
    return FluentTheme._hex_to_rgba(hex_color)


def _apply_fluent_style(
    tag: str,
    *,
    height: int = FluentTokens.CONTROL_HEIGHT_MEDIUM,
    border_color: Optional[Tuple] = None,
    bg_color: Optional[Tuple] = None,
    text_color: Optional[Tuple] = None,
    corner_radius: int = FluentTokens.CORNER_RADIUS_MEDIUM,
):
    """Apply Fluent 2 style overrides to a DearPyGUI item."""
    with dpg.theme() as item_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, corner_radius)
            if border_color:
                dpg.add_theme_color(dpg.mvThemeCol_Border, border_color)
            if bg_color:
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, bg_color)
            if text_color:
                dpg.add_theme_color(dpg.mvThemeCol_Text, text_color)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, FluentTokens.SPACING_M, FluentTokens.SPACING_S)
    dpg.bind_item_theme(tag, item_theme)
    dpg.configure_item(tag, height=height)
    return item_theme


# ═══════════════════════════════════════════════════════════════
# BUTTONS
# ═══════════════════════════════════════════════════════════════

class FluentButton:
    """Standard Fluent button with rounded corners and hover states."""

    def __init__(
        self, label: str = "Button", callback: Optional[Callable] = None,
        tag: Optional[str] = None, parent: Optional[Any] = None,
        width: int = 0, height: int = FluentTokens.CONTROL_HEIGHT_MEDIUM,
        enabled: bool = True, icon: Optional[str] = None,
    ):
        self.label = label
        self.callback = callback
        self.tag = tag or f"fluent_btn_{id(self)}"
        self._icon = icon

        with dpg.group(horizontal=True) as grp:
            if icon:
                dpg.add_text(icon, tag=f"{self.tag}_icon")
            dpg.add_button(label=label, callback=callback, tag=self.tag,
                           width=width, height=height, enabled=enabled)
        self._group = grp

        _apply_fluent_style(self.tag, corner_radius=FluentTokens.CORNER_RADIUS_LARGE, height=height)

    def set_label(self, text: str):
        dpg.configure_item(self.tag, label=text)

    def set_enabled(self, enabled: bool):
        dpg.configure_item(self.tag, enabled=enabled)

    def click(self):
        if self.callback:
            self.callback(self.tag, None, None)


class FluentAccentButton(FluentButton):
    """Primary action button with accent color fill."""

    def __init__(self, label: str = "Button", callback: Optional[Callable] = None, **kwargs):
        super().__init__(label=label, callback=callback, **kwargs)
        c = FluentTheme().colors
        with dpg.theme() as accent_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, _hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hex_to_rgba(c.accent_hover))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hex_to_rgba(c.accent_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_Text, _hex_to_rgba(c.text_on_accent))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_LARGE)
        dpg.bind_item_theme(self.tag, accent_theme)


class FluentSubtleButton(FluentButton):
    """Secondary button with transparent background and subtle hover."""

    def __init__(self, label: str = "Button", callback: Optional[Callable] = None, **kwargs):
        super().__init__(label=label, callback=callback, **kwargs)
        c = FluentTheme().colors
        with dpg.theme() as subtle_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hex_to_rgba(c.fill_subtle_pressed))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_LARGE)
        dpg.bind_item_theme(self.tag, subtle_theme)


class FluentHyperlinkButton(FluentButton):
    """Text-link style button with accent color."""

    def __init__(self, label: str = "Link", callback: Optional[Callable] = None, **kwargs):
        kwargs["height"] = FluentTokens.CONTROL_HEIGHT_MEDIUM
        super().__init__(label=label, callback=callback, **kwargs)
        c = FluentTheme().colors
        with dpg.theme() as link_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_Text, _hex_to_rgba(c.accent))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0)
        dpg.bind_item_theme(self.tag, link_theme)


class FluentToggleButton(FluentButton):
    """Toggle button with on/off visual state."""

    def __init__(self, label: str = "Toggle", callback: Optional[Callable] = None, **kwargs):
        self._toggled = False
        self._user_callback = callback
        def _on_toggle(sender, app_data, user_data):
            self._toggled = not self._toggled
            self._update_appearance()
            if self._user_callback:
                self._user_callback(sender, app_data, user_data)
        super().__init__(label=label, callback=_on_toggle, **kwargs)
        self._update_appearance()

    def _update_appearance(self):
        c = FluentTheme().colors
        if self._toggled:
            with dpg.theme() as t:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, _hex_to_rgba(c.fill_subtle_pressed))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hex_to_rgba(c.fill_subtle_pressed))
                    dpg.add_theme_color(dpg.mvThemeCol_Text, _hex_to_rgba(c.accent))
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_LARGE)
            dpg.bind_item_theme(self.tag, t)
        else:
            with dpg.theme() as t:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, _hex_to_rgba(c.control_default))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hex_to_rgba(c.control_default_hover))
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_LARGE)
            dpg.bind_item_theme(self.tag, t)

    @property
    def is_toggled(self) -> bool:
        return self._toggled


class FluentSplitButton:
    """Button with main action + dropdown chevron."""

    def __init__(self, label: str = "Split", callback: Optional[Callable] = None,
                 menu_callback: Optional[Callable] = None, tag: Optional[str] = None,
                 parent: Optional[Any] = None):
        self.tag = tag or f"fluent_split_{id(self)}"
        c = FluentTheme().colors
        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            with dpg.theme() as btn_t:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, _hex_to_rgba(c.accent))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hex_to_rgba(c.accent_hover))
                    dpg.add_theme_color(dpg.mvThemeCol_Text, _hex_to_rgba(c.text_on_accent))
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_LARGE)
                    dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 0, 0)
            with dpg.button(label=label, callback=callback, height=FluentTokens.CONTROL_HEIGHT_MEDIUM):
                pass
            dpg.bind_item_theme(dpg.last_item(), btn_t)
            with dpg.button(label="▾", callback=menu_callback, height=FluentTokens.CONTROL_HEIGHT_MEDIUM, width=28):
                pass
            dpg.bind_item_theme(dpg.last_item(), btn_t)


class FluentDropDownButton:
    """Button with dropdown chevron."""

    def __init__(self, label: str = "Dropdown", callback: Optional[Callable] = None,
                 tag: Optional[str] = None, parent: Optional[Any] = None,
                 items: Optional[List[str]] = None):
        self.tag = tag or f"fluent_drop_{id(self)}"
        self.items = items or []
        self._callback = callback
        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            dpg.add_button(label=f"{label} ▾", callback=callback, height=FluentTokens.CONTROL_HEIGHT_MEDIUM)
        _apply_fluent_style(
            dpg.get_item_alias(dpg.last_item()) or str(dpg.last_item()),
            corner_radius=FluentTokens.CORNER_RADIUS_LARGE,
        )

    def set_items(self, items: List[str]):
        self.items = items


class FluentRepeatButton:
    """Button that fires repeatedly while held down."""

    def __init__(self, label: str = "Repeat", callback: Optional[Callable] = None,
                 interval_ms: int = 100, tag: Optional[str] = None, parent: Optional[Any] = None):
        self.tag = tag or f"fluent_repeat_{id(self)}"
        self._callback = callback
        self._interval_ms = interval_ms
        self._timer_tag = f"{self.tag}_timer"
        self._holding = False

        with dpg.button(label=label, tag=self.tag, callback=self._on_down,
                        height=FluentTokens.CONTROL_HEIGHT_MEDIUM, parent=parent):
            pass
        _apply_fluent_style(self.tag, corner_radius=FluentTokens.CORNER_RADIUS_LARGE)

    def _on_down(self, sender, app_data, user_data):
        self._holding = True
        if self._callback:
            self._callback(sender, app_data, user_data)
        dpg.add_timer(self._interval_ms / 1000.0, self._tick, tag=self._timer_tag)

    def _tick(self):
        if self._holding and self._callback:
            self._callback(self.tag, None, None)

    def _on_up(self, sender, app_data, user_data):
        if self._holding:
            self._holding = False
            if dpg.does_item_exist(self._timer_tag):
                dpg.delete_item(self._timer_tag)


class FluentAppBarButton:
    """Command bar icon button."""

    def __init__(self, icon: str = "📁", label: str = "Action",
                 callback: Optional[Callable] = None, tag: Optional[str] = None,
                 parent: Optional[Any] = None):
        self.tag = tag or f"fluent_appbar_{id(self)}"
        c = FluentTheme().colors
        with dpg.group(tag=self.tag, parent=parent):
            dpg.add_button(label=icon, callback=callback, width=48, height=48)
            dpg.add_text(label, color=_hex_to_rgba(c.text_secondary))
        _apply_fluent_style(
            dpg.get_item_alias(dpg.last_item()) or str(dpg.last_item()),
            corner_radius=FluentTokens.CORNER_RADIUS_LARGE,
        )


class FluentIconLabel:
    """Icon + text label group."""

    def __init__(self, icon: str = "📌", label: str = "Label",
                 tag: Optional[str] = None, parent: Optional[Any] = None):
        self.tag = tag or f"fluent_icon_{id(self)}"
        c = FluentTheme().colors
        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            dpg.add_text(icon)
            dpg.add_text(label, color=_hex_to_rgba(c.text_primary))


# ═══════════════════════════════════════════════════════════════
# INPUT CONTROLS
# ═══════════════════════════════════════════════════════════════

class FluentTextBox:
    """Fluent text input with label, placeholder, and border."""

    def __init__(self, label: str = "", placeholder: str = "",
                 default_value: str = "", callback: Optional[Callable] = None,
                 tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 200, multiline: bool = False,
                 readonly: bool = False, password: bool = False):
        self.tag = tag or f"fluent_txt_{id(self)}"
        self._label = label
        self._placeholder = placeholder
        self._value = default_value
        c = FluentTheme().colors

        if label:
            dpg.add_text(label, tag=f"{self.tag}_label", parent=parent)

        if multiline:
            dpg.add_input_text(tag=self.tag, default_value=default_value,
                               width=width, height=100, callback=callback,
                               multiline=True, readonly=readonly, parent=parent)
        else:
            dpg.add_input_text(tag=self.tag, default_value=default_value,
                               hint=placeholder, width=width, callback=callback,
                               readonly=readonly, password=password, parent=parent)

        _apply_fluent_style(self.tag, height=FluentTokens.CONTROL_HEIGHT_MEDIUM,
                            border_color=_hex_to_rgba(c.border),
                            bg_color=_hex_to_rgba(c.control_default))

    def get_value(self) -> str:
        return dpg.get_value(self.tag) or ""

    def set_value(self, value: str):
        self._value = value
        dpg.set_value(self.tag, value)

    def set_placeholder(self, text: str):
        dpg.configure_item(self.tag, hint=text)

    def set_readonly(self, readonly: bool):
        dpg.configure_item(self.tag, readonly=readonly)

    def bind_to(self, vm: ViewModel, property_name: str):
        """Two-way bind to a ViewModel BindableProperty."""
        vm.add_property_handler(property_name, lambda n, o, v: self.set_value(v))
        self.set_value(getattr(vm, property_name, ""))
        dpg.configure_item(self.tag, callback=lambda s, a, u: setattr(vm, property_name, self.get_value()))


class FluentPasswordBox(FluentTextBox):
    """Password input (masked)."""

    def __init__(self, label: str = "Password", **kwargs):
        kwargs["password"] = True
        kwargs["placeholder"] = kwargs.get("placeholder", "Enter password")
        super().__init__(label=label, **kwargs)


class FluentSearchBox:
    """Search input with magnifier icon and clear button."""

    def __init__(self, placeholder: str = "Search", callback: Optional[Callable] = None,
                 tag: Optional[str] = None, parent: Optional[Any] = None, width: int = 250):
        self.tag = tag or f"fluent_search_{id(self)}"
        self._callback = callback
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            dpg.add_text("🔍")
            dpg.add_input_text(tag=f"{self.tag}_input", hint=placeholder,
                               width=width - 50, callback=callback)
            dpg.add_button(label="✕",
                           callback=lambda s, a, u: dpg.set_value(f"{self.tag}_input", ""),
                           width=24, height=24)

        inp_tag = f"{self.tag}_input"
        _apply_fluent_style(inp_tag, height=FluentTokens.CONTROL_HEIGHT_MEDIUM,
                            border_color=_hex_to_rgba(c.border),
                            bg_color=_hex_to_rgba(c.control_default))

    def get_value(self) -> str:
        return dpg.get_value(f"{self.tag}_input") or ""

    def set_value(self, value: str):
        dpg.set_value(f"{self.tag}_input", value)


class FluentNumberBox:
    """Numeric input with +/- spin buttons."""

    def __init__(self, label: str = "", default_value: float = 0.0,
                 min_value: float = 0.0, max_value: float = 100.0,
                 step: float = 1.0, callback: Optional[Callable] = None,
                 tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 150):
        self.tag = tag or f"fluent_num_{id(self)}"
        self._step = step
        self._callback = callback
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            if label:
                dpg.add_text(label)
            dpg.add_input_float(tag=f"{self.tag}_val", default_value=default_value,
                                width=width - 60, callback=callback,
                                min_value=min_value, max_value=max_value)
            dpg.add_button(label="+", callback=self._increment, width=24, height=24)
            dpg.add_button(label="−", callback=self._decrement, width=24, height=24)

        _apply_fluent_style(f"{self.tag}_val", height=FluentTokens.CONTROL_HEIGHT_MEDIUM,
                            border_color=_hex_to_rgba(c.border),
                            bg_color=_hex_to_rgba(c.control_default))

    def _increment(self, sender, app_data, user_data):
        val = dpg.get_value(f"{self.tag}_val") or 0
        dpg.set_value(f"{self.tag}_val", val + self._step)
        if self._callback:
            self._callback(f"{self.tag}_val", val + self._step, None)

    def _decrement(self, sender, app_data, user_data):
        val = dpg.get_value(f"{self.tag}_val") or 0
        dpg.set_value(f"{self.tag}_val", val - self._step)
        if self._callback:
            self._callback(f"{self.tag}_val", val - self._step, None)

    def get_value(self) -> float:
        return dpg.get_value(f"{self.tag}_val") or 0.0

    def set_value(self, value: float):
        dpg.set_value(f"{self.tag}_val", value)


class FluentRichEditBox:
    """Multi-line text area with Fluent styling."""

    def __init__(self, label: str = "", default_value: str = "",
                 callback: Optional[Callable] = None,
                 tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 300, height: int = 120):
        self.tag = tag or f"fluent_rich_{id(self)}"
        c = FluentTheme().colors

        if label:
            dpg.add_text(label, tag=f"{self.tag}_label", parent=parent)

        dpg.add_input_text(tag=self.tag, default_value=default_value,
                           width=width, height=height, callback=callback,
                           multiline=True, parent=parent)

# ═══════════════════════════════════════════════════════════════
# SELECTION CONTROLS
# ═══════════════════════════════════════════════════════════════

class FluentCheckBox:
    """Fluent checkbox with rounded corners and accent checkmark."""

    def __init__(self, label: str = "Checkbox", default_value: bool = False,
                 callback: Optional[Callable] = None, tag: Optional[str] = None,
                 parent: Optional[Any] = None):
        self.tag = tag or f"fluent_cb_{id(self)}"
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            dpg.add_checkbox(label="", default_value=default_value,
                             callback=callback, tag=f"{self.tag}_box")
            dpg.add_text(label, color=_hex_to_rgba(c.text_primary))

        # Style the checkbox
        with dpg.theme() as cb_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, _hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, _hex_to_rgba(c.control_default))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, _hex_to_rgba(c.fill_subtle_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border_strong))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_SMALL)
        dpg.bind_item_theme(f"{self.tag}_box", cb_theme)
        dpg.configure_item(f"{self.tag}_box", height=FluentTokens.CONTROL_HEIGHT_MEDIUM)

    def get_value(self) -> bool:
        return dpg.get_value(f"{self.tag}_box")

    def set_value(self, value: bool):
        dpg.set_value(f"{self.tag}_box", value)

    def bind_to(self, vm: ViewModel, property_name: str):
        vm.add_property_handler(property_name, lambda n, o, v: self.set_value(v))
        self.set_value(getattr(vm, property_name, False))
        dpg.configure_item(f"{self.tag}_box", callback=lambda s, a, u: setattr(vm, property_name, self.get_value()))


class FluentToggleSwitch:
    """
    Fluent toggle switch (pill-shaped).
    Mimics the Windows 11 Settings-style toggle.
    """

    def __init__(self, label: str = "Toggle", default_value: bool = False,
                 callback: Optional[Callable] = None, tag: Optional[str] = None,
                 parent: Optional[Any] = None):
        self.tag = tag or f"fluent_toggle_{id(self)}"
        self._value = default_value
        self._user_callback = callback
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            # Custom toggle: circle + track using draw commands + button
            dpg.add_button(
                label="●" if default_value else "○",
                tag=f"{self.tag}_btn",
                callback=self._on_toggle,
                width=44,
                height=22,
            )
            dpg.add_text(label, color=_hex_to_rgba(c.text_primary), tag=f"{self.tag}_lbl")

        self._update_theme()

    def _on_toggle(self, sender, app_data, user_data):
        self._value = not self._value
        self._update_theme()
        if self._user_callback:
            self._user_callback(self.tag, self._value, None)

    def _update_theme(self):
        c = FluentTheme().colors
        if self._value:
            with dpg.theme() as t:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, _hex_to_rgba(c.accent))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hex_to_rgba(c.accent_hover))
                    dpg.add_theme_color(dpg.mvThemeCol_Text, _hex_to_rgba(c.text_on_accent))
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 11)
            dpg.bind_item_theme(f"{self.tag}_btn", t)
            dpg.configure_item(f"{self.tag}_btn", label="●")
        else:
            with dpg.theme() as t:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, _hex_to_rgba(c.fill_subtle))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hex_to_rgba(c.fill_subtle_hover))
                    dpg.add_theme_color(dpg.mvThemeCol_Text, _hex_to_rgba(c.text_secondary))
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 11)
                    dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border_strong))
            dpg.bind_item_theme(f"{self.tag}_btn", t)
            dpg.configure_item(f"{self.tag}_btn", label="○")

    def get_value(self) -> bool:
        return self._value

    def set_value(self, value: bool):
        if self._value != value:
            self._value = value
            self._update_theme()

    def bind_to(self, vm: ViewModel, property_name: str):
        vm.add_property_handler(property_name, lambda n, o, v: self.set_value(v))
        self.set_value(getattr(vm, property_name, False))


class FluentRadioButton:
    """Fluent radio button with accent fill."""

    _group_tags: Dict[str, List["FluentRadioButton"]] = {}

    def __init__(self, label: str = "Option", group: str = "default",
                 default_value: bool = False, callback: Optional[Callable] = None,
                 tag: Optional[str] = None, parent: Optional[Any] = None):
        self.tag = tag or f"fluent_radio_{id(self)}"
        self._group = group
        self._label = label
        self._user_callback = callback
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            dpg.add_radio_button(label=label, default_value=default_value,
                                 callback=self._on_select, tag=f"{self.tag}_rb")

        # Style
        with dpg.theme() as rb_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, _hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, _hex_to_rgba(c.control_default))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, _hex_to_rgba(c.fill_subtle_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border_strong))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
        dpg.bind_item_theme(f"{self.tag}_rb", rb_theme)
        dpg.configure_item(f"{self.tag}_rb", height=FluentTokens.CONTROL_HEIGHT_MEDIUM)

        # Register in group
        FluentRadioButton._group_tags.setdefault(group, []).append(self)

    def _on_select(self, sender, app_data, user_data):
        # Deselect siblings
        for rb in FluentRadioButton._group_tags.get(self._group, []):
            if rb is not self:
                dpg.set_value(f"{rb.tag}_rb", False)
        if self._user_callback:
            self._user_callback(self.tag, True, None)

    def get_value(self) -> bool:
        return dpg.get_value(f"{self.tag}_rb")

    def set_value(self, value: bool):
        dpg.set_value(f"{self.tag}_rb", value)


# ═══════════════════════════════════════════════════════════════
# SLIDERS & PROGRESS
# ═══════════════════════════════════════════════════════════════

class FluentSlider:
    """Fluent slider with accent track and rounded thumb."""

    def __init__(self, label: str = "Slider", default_value: float = 50.0,
                 min_value: float = 0.0, max_value: float = 100.0,
                 callback: Optional[Callable] = None, tag: Optional[str] = None,
                 parent: Optional[Any] = None, width: int = 200):
        self.tag = tag or f"fluent_slider_{id(self)}"
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            if label:
                dpg.add_text(label, width=80)
            dpg.add_slider_float(tag=f"{self.tag}_slider", default_value=default_value,
                                 min_value=min_value, max_value=max_value,
                                 width=width, callback=callback,
                                 format="%.1f")
            dpg.add_text(f"{default_value:.1f}", tag=f"{self.tag}_val",
                         color=_hex_to_rgba(c.text_secondary), width=40)

        # Style slider
        with dpg.theme() as slider_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, _hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, _hex_to_rgba(c.accent_hover))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, _hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, FluentTokens.CORNER_RADIUS_LARGE)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_LARGE)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, FluentTokens.SPACING_S, FluentTokens.SPACING_XS)
        dpg.bind_item_theme(f"{self.tag}_slider", slider_theme)
        dpg.configure_item(f"{self.tag}_slider", height=FluentTokens.CONTROL_HEIGHT_MEDIUM)

        # Update display value
        if callback is None:
            dpg.configure_item(f"{self.tag}_slider", callback=self._update_val)

    def _update_val(self, sender, app_data, user_data):
        dpg.configure_item(f"{self.tag}_val", default_value=f"{app_data:.1f}")

    def get_value(self) -> float:
        return dpg.get_value(f"{self.tag}_slider") or 0.0

    def set_value(self, value: float):
        dpg.set_value(f"{self.tag}_slider", value)

    def bind_to(self, vm: ViewModel, property_name: str):
        vm.add_property_handler(property_name, lambda n, o, v: self.set_value(v))
        self.set_value(getattr(vm, property_name, 0.0))
        dpg.configure_item(f"{self.tag}_slider", callback=lambda s, a, u: setattr(vm, property_name, self.get_value()))


class FluentProgressBar:
    """Fluent progress bar with accent fill and rounded ends."""

    def __init__(self, value: float = 0.0, tag: Optional[str] = None,
                 parent: Optional[Any] = None, width: int = 200,
                 height: int = 4, show_label: bool = False):
        self.tag = tag or f"fluent_progress_{id(self)}"
        self._show_label = show_label
        c = FluentTheme().colors

        with dpg.group(tag=self.tag, parent=parent):
            # Progress bar as a "progress bar" widget
            dpg.add_progress_bar(tag=f"{self.tag}_bar", default_value=value,
                                 width=width, height=height)
            if show_label:
                dpg.add_text(f"{value:.0%}", tag=f"{self.tag}_pct",
                             color=_hex_to_rgba(c.text_secondary))

        with dpg.theme() as prog_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, _hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered, _hex_to_rgba(c.accent_hover))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, _hex_to_rgba(c.fill_subtle))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_LARGE)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, FluentTokens.CORNER_RADIUS_LARGE)
        dpg.bind_item_theme(f"{self.tag}_bar", prog_theme)

    def set_value(self, value: float):
        dpg.set_value(f"{self.tag}_bar", value)
        if self._show_label:
            dpg.configure_item(f"{self.tag}_pct", default_value=f"{value:.0%}")

    def get_value(self) -> float:
        return dpg.get_value(f"{self.tag}_bar") or 0.0


class FluentProgressBarRing:
    """Circular progress indicator (ring)."""

    def __init__(self, value: float = 0.0, radius: int = 30,
                 tag: Optional[str] = None, parent: Optional[Any] = None):
        self.tag = tag or f"fluent_ring_{id(self)}"
        self._radius = radius
        self._value = value
        c = FluentTheme().colors

        dpg.add_drawlist(width=radius * 2 + 10, height=radius * 2 + 10,
                         tag=self.tag, parent=parent)
        self._draw()

    def _draw(self):
        cx, cy = self._radius + 5, self._radius + 5
        c = FluentTheme().colors
        dpg.delete_item(self.tag, children_only=True)
        # Background ring
        dpg.draw_circle((cx, cy), self._radius, color=_hex_to_rgba(c.fill_subtle),
                        thickness=4, parent=self.tag)
        # Progress arc
        if self._value > 0:
            angle = 2 * 3.14159 * self._value - 3.14159 / 2
            end_x = cx + self._radius * __import__('math').cos(angle)
            end_y = cy + self._radius * __import__('math').sin(angle)
            dpg.draw_circle((cx, cy), self._radius, color=_hex_to_rgba(c.accent),
                            thickness=4, parent=self.tag)
            # Draw arc as partial circle
            dpg.draw_circle((cx, cy), self._radius, color=_hex_to_rgba(c.accent),
                            thickness=4, segments=max(int(60 * self._value), 3),
                            parent=self.tag)

    def set_value(self, value: float):
        self._value = max(0, min(1, value))
        self._draw()


class FluentRatingControl:
    """Star rating control (1-5 stars)."""

    def __init__(self, value: int = 0, max_stars: int = 5,
                 callback: Optional[Callable] = None, tag: Optional[str] = None,
                 parent: Optional[Any] = None):
        self.tag = tag or f"fluent_rating_{id(self)}"
        self._value = value
        self._max = max_stars
        self._callback = callback
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            for i in range(max_stars):
                star = "★" if i < value else "☆"
                dpg.add_text(star, tag=f"{self.tag}_star_{i}",
                             color=_hex_to_rgba(c.accent) if i < value else _hex_to_rgba(c.border),
                             callback=self._on_click, user_data=i + 1)
                # Make text clickable via handler
                def _mk_click(idx):
                    def _click(sender, app_data, user_data):
                        self._value = idx
                        self._update_stars()
                        if self._callback:
                            self._callback(self.tag, idx, None)
                    return _click
                dpg.configure_item(f"{self.tag}_star_{i}", callback=_mk_click(i + 1))

    def _on_click(self, sender, app_data, user_data):
        self._value = user_data
        self._update_stars()
        if self._callback:
            self._callback(self.tag, user_data, None)

    def _update_stars(self):
        c = FluentTheme().colors
        for i in range(self._max):
            star = "★" if i < self._value else "☆"
            clr = _hex_to_rgba(c.accent) if i < self._value else _hex_to_rgba(c.border)
            dpg.configure_item(f"{self.tag}_star_{i}", default_value=star, color=clr)

    def get_value(self) -> int:
        return self._value

    def set_value(self, value: int):
        self._value = value
        self._update_stars()


class FluentAutoSuggestBox:
    """Text input with suggestion dropdown."""

    def __init__(self, label: str = "", suggestions: Optional[List[str]] = None,
                 callback: Optional[Callable] = None, tag: Optional[str] = None,
                 parent: Optional[Any] = None, width: int = 250):
        self.tag = tag or f"fluent_auto_{id(self)}"
        self._suggestions = suggestions or []
        self._callback = callback
        c = FluentTheme().colors

        with dpg.group(tag=self.tag, parent=parent):
            if label:
                dpg.add_text(label)
            dpg.add_input_text(tag=f"{self.tag}_input", hint="Type to search...",
                               width=width, callback=self._on_text)
            dpg.add_listbox(tag=f"{self.tag}_list", items=self._suggestions,
                            width=width, height=120, default_value="")

        _apply_fluent_style(f"{self.tag}_input", height=FluentTokens.CONTROL_HEIGHT_MEDIUM,
                            border_color=_hex_to_rgba(c.border),
                            bg_color=_hex_to_rgba(c.control_default))

    def _on_text(self, sender, app_data, user_data):
        text = (app_data or "").lower()
        filtered = [s for s in self._suggestions if text in s.lower()]
        dpg.configure_item(f"{self.tag}_list", items=filtered)
        if self._callback:
            self._callback(self.tag, app_data, None)

    def set_suggestions(self, items: List[str]):
        self._suggestions = items

    def get_value(self) -> str:
        return dpg.get_value(f"{self.tag}_input") or ""


# ═══════════════════════════════════════════════════════════════
# COLLECTION CONTROLS
# ═══════════════════════════════════════════════════════════════

class FluentComboBox:
    """Fluent dropdown combo box with rounded corners."""

    def __init__(self, label: str = "", items: Optional[List[str]] = None,
                 default_value: str = "", callback: Optional[Callable] = None,
                 tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 200):
        self.tag = tag or f"fluent_combo_{id(self)}"
        self._items = items or []
        c = FluentTheme().colors

        if label:
            dpg.add_text(label, tag=f"{self.tag}_label", parent=parent)

        dpg.add_combo(tag=self.tag, items=self._items, default_value=default_value,
                      width=width, callback=callback, parent=parent,
                      popup_align=dpg.mvPopupAlign_Below)

        with dpg.theme() as combo_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, _hex_to_rgba(c.control_default))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border))
                dpg.add_theme_color(dpg.mvThemeCol_Header, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, _hex_to_rgba(c.card))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
        dpg.bind_item_theme(self.tag, combo_theme)
        dpg.configure_item(self.tag, height=FluentTokens.CONTROL_HEIGHT_MEDIUM)
    def get_value(self) -> str:
        return dpg.get_value(self.tag) or ""

    def set_value(self, value: str):
        dpg.set_value(self.tag, value)

    def set_items(self, items: List[str]):
        self._items = items
        dpg.configure_item(self.tag, items=items)

    def bind_to(self, vm: ViewModel, property_name: str):
        vm.add_property_handler(property_name, lambda n, o, v: self.set_value(v))
        self.set_value(getattr(vm, property_name, ""))
        dpg.configure_item(self.tag, callback=lambda s, a, u: setattr(vm, property_name, self.get_value()))


class FluentTreeView:
    """Tree view with expandable nodes."""

    def __init__(self, tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 250, height: int = 300):
        self.tag = tag or f"fluent_tree_{id(self)}"
        c = FluentTheme().colors

        dpg.add_tree_node(tag=self.tag, parent=parent,
                           width=width, height=height)
        # Style
        with dpg.theme() as tree_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Header, _hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, _hex_to_rgba(c.fill_subtle_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, _hex_to_rgba(c.surface))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
        dpg.bind_item_theme(self.tag, tree_theme)

    def add_item(self, label: str, parent_node: Optional[str] = None,
                 callback: Optional[Callable] = None) -> str:
        p = parent_node or self.tag
        tag = f"{self.tag}_{label.replace(' ', '_')}"
        dpg.add_tree_node(label=label, tag=tag, parent=p, callback=callback)
        return tag

    def add_leaf(self, label: str, parent_node: Optional[str] = None,
                 callback: Optional[Callable] = None) -> str:
        p = parent_node or self.tag
        tag = f"{self.tag}_leaf_{label.replace(' ', '_')}"
        dpg.add_selectable(label=label, tag=tag, parent=p, callback=callback)
        return tag


class FluentTreeViewItem:
    """Individual tree node (helper)."""

    def __init__(self, label: str, tag: Optional[str] = None,
                 parent: Optional[Any] = None, callback: Optional[Callable] = None):
        self.tag = tag or f"fluent_treeitem_{id(self)}"
        dpg.add_tree_node(label=label, tag=self.tag, parent=parent, callback=callback)


class FluentListView:
    """List view with selectable items."""

    def __init__(self, items: Optional[List[str]] = None,
                 callback: Optional[Callable] = None, tag: Optional[str] = None,
                 parent: Optional[Any] = None, width: int = 250, height: int = 200):
        self.tag = tag or f"fluent_list_{id(self)}"
        self._items = items or []
        c = FluentTheme().colors

        dpg.add_listbox(tag=self.tag, items=self._items,
                        width=width, height=height, callback=callback, parent=parent)

        with dpg.theme() as list_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Header, _hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, _hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, _hex_to_rgba(c.surface))
                dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
        dpg.bind_item_theme(self.tag, list_theme)

    def get_value(self) -> str:
        return dpg.get_value(self.tag) or ""

    def set_items(self, items: List[str]):
        self._items = items
        dpg.configure_item(self.tag, items=items)


class FluentDataGrid:
    """Data grid / table with Fluent styling."""

    def __init__(self, headers: Optional[List[str]] = None,
                 rows: Optional[List[List[Any]]] = None,
                 tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 500, height: int = 300,
                 policy: int = dpg.mvTable_SizingStretchProp):
        self.tag = tag or f"fluent_grid_{id(self)}"
        self._headers = headers or []
        self._rows = rows or []
        c = FluentTheme().colors
        n_cols = len(self._headers)

        with dpg.table(tag=self.tag, header_row=True,
                       policy=policy, width=width, height=height, parent=parent):
            for h in self._headers:
                dpg.add_table_column(label=h, width_stretch=True)
            for row in self._rows:
                with dpg.table_row():
                    for cell in row:
                        dpg.add_text(str(cell))

        with dpg.theme() as grid_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, _hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, _hex_to_rgba(c.border))
                dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, _hex_to_rgba(c.surface))
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, _hex_to_rgba(c.surface_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_Header, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, _hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, _hex_to_rgba(c.accent_pressed))
        dpg.bind_item_theme(self.tag, grid_theme)

    def add_row(self, cells: List[Any]):
        with dpg.table_row(parent=self.tag):
            for cell in cells:
                dpg.add_text(str(cell))


# ═══════════════════════════════════════════════════════════════
# SURFACE / POPUP CONTROLS
# ═══════════════════════════════════════════════════════════════

class FluentExpander:
    """Expandable content section (accordion)."""

    def __init__(self, header: str = "Expander", content: str = "",
                 tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 400):
        self.tag = tag or f"fluent_expand_{id(self)}"
        self._expanded = False
        self._header = header
        c = FluentTheme().colors

        with dpg.group(tag=self.tag, parent=parent, width=width):
            # Header button
            with dpg.theme() as exp_btn_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, _hex_to_rgba(c.fill_subtle))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hex_to_rgba(c.fill_subtle_hover))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hex_to_rgba(c.fill_subtle_pressed))
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_LARGE)
                    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, FluentTokens.SPACING_M, FluentTokens.SPACING_M)
            dpg.add_button(label=f"▶ {header}", tag=f"{self.tag}_hdr",
                           callback=self._toggle, width=width)
            dpg.bind_item_theme(f"{self.tag}_hdr", exp_btn_theme)

            # Collapsible content
            with dpg.group(tag=f"{self.tag}_content", show=False):
                dpg.add_text(content, wrap=width - 20)

    def _toggle(self, sender, app_data, user_data):
        self._expanded = not self._expanded
        dpg.configure_item(f"{self.tag}_content", show=self._expanded)
        prefix = "▼" if self._expanded else "▶"
        dpg.configure_item(f"{self.tag}_hdr", label=f"{prefix} {self._header}")

    @property
    def is_expanded(self) -> bool:
        return self._expanded


class FluentInfoBar:
    """Informational banner with icon, message, and dismiss."""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

    def __init__(self, message: str = "", severity: str = "info",
                 tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 500, dismissible: bool = True):
        self.tag = tag or f"fluent_infobar_{id(self)}"
        c = FluentTheme().colors

        severity_colors = {
            "info": c.info,
            "success": c.success,
            "warning": c.warning,
            "error": c.danger,
        }
        severity_icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
        }
        clr = severity_colors.get(severity, c.info)
        icon = severity_icons.get(severity, "ℹ️")

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            with dpg.theme() as bar_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _hex_to_rgba(c.card))
                    dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(clr))
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, FluentTokens.CORNER_RADIUS_LARGE)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, FluentTokens.STROKE_WIDTH_THICK)

            with dpg.child_window(tag=f"{self.tag}_child", width=width, height=40):
                dpg.bind_item_theme(f"{self.tag}_child", bar_theme)
                with dpg.group(horizontal=True):
                    dpg.add_text(icon)
                    dpg.add_text(message, wrap=width - 60)
                    if dismissible:
                        dpg.add_button(label="✕", callback=lambda s, a, u: dpg.hide_item(self.tag),
                                       width=20, height=20)


class FluentContentDialog:
    """Modal dialog with title, message, and action buttons."""

    def __init__(self, title: str = "Dialog", message: str = "",
                 primary_text: str = "OK", secondary_text: str = "Cancel",
                 primary_callback: Optional[Callable] = None,
                 secondary_callback: Optional[Callable] = None,
                 tag: Optional[str] = None, parent: Optional[Any] = None):
        self.tag = tag or f"fluent_dialog_{id(self)}"
        c = FluentTheme().colors

        # Create as a child window overlay
        with dpg.child_window(tag=self.tag, show=False,
                               width=400, height=200, modal=True,
                               no_title_bar=False, parent=parent or dpg.root_container()):
            dpg.configure_item(self.tag, label=title)

            with dpg.theme() as dlg_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _hex_to_rgba(c.card_bright))
                    dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border_strong))
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, FluentTokens.CORNER_RADIUS_XLARGE)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, FluentTokens.STROKE_WIDTH_THICK)
            dpg.bind_item_theme(self.tag, dlg_theme)

            dpg.add_spacer(height=10)
            dpg.add_text(message, wrap=360)
            dpg.add_spacer(height=16)

            with dpg.group(horizontal=True):
                if secondary_text:
                    FluentSubtleButton(label=secondary_text,
                                       callback=lambda s, a, u: self._close(secondary_callback))
                FluentAccentButton(label=primary_text,
                                   callback=lambda s, a, u: self._close(primary_callback))

    def show(self):
        dpg.show_item(self.tag)

    def hide(self):
        dpg.hide_item(self.tag)

    def _close(self, cb):
        self.hide()
        if cb:
            cb()


class FluentTooltip:
    """Tooltip that appears on hover."""

    def __init__(self, tip_text: str = "", target_tag: Optional[str] = None):
        self.tip_text = tip_text
        self.target = target_tag
        c = FluentTheme().colors

        if target_tag and dpg.does_item_exist(target_tag):
            with dpg.tooltip(parent=target_tag):
                with dpg.theme() as tip_theme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, _hex_to_rgba(c.card))
                        dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border_strong))
                        dpg.add_theme_color(dpg.mvThemeCol_Text, _hex_to_rgba(c.text_primary))
                        dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
                        dpg.add_theme_style(dpg.mvStyleVar_PopupBorderSize, FluentTokens.STROKE_WIDTH_NORMAL)
                        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, FluentTokens.SPACING_M, FluentTokens.SPACING_S)
                dpg.bind_item_theme(dpg.last_container(), tip_theme)
                dpg.add_text(tip_text)


class FluentMenu:
    """Context menu / dropdown menu."""

    def __init__(self, tag: Optional[str] = None, parent: Optional[Any] = None):
        self.tag = tag or f"fluent_menu_{id(self)}"
        c = FluentTheme().colors
        self._items: List[Dict] = []

        with dpg.menu_bar(tag=f"{self.tag}_bar", parent=parent):
            pass  # Items added via add_item

        with dpg.theme() as menu_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, _hex_to_rgba(c.surface))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, _hex_to_rgba(c.card))
                dpg.add_theme_color(dpg.mvThemeCol_Header, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, _hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, _hex_to_rgba(c.accent_pressed))
                dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border_strong))
                dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
                dpg.add_theme_style(dpg.mvStyleVar_PopupBorderSize, FluentTokens.STROKE_WIDTH_THICK)
        dpg.bind_item_theme(f"{self.tag}_bar", menu_theme)

    def add_item(self, label: str, callback: Optional[Callable] = None,
                 shortcut: str = "", separator: bool = False):
        tag = f"{self.tag}_{label.replace(' ', '_')}"
        if separator:
            dpg.add_menu_item(label=label, callback=callback, tag=tag,
                              parent=f"{self.tag}_bar")
            dpg.add_spacer(height=1)  # Visual separator
        else:
            dpg.add_menu_item(label=label, callback=callback, tag=tag,
                              shortcut=shortcut, parent=f"{self.tag}_bar")
        self._items.append({"label": label, "tag": tag})


class FluentMenuItem:
    """Single menu item."""

    def __init__(self, label: str, callback: Optional[Callable] = None,
                 shortcut: str = "", parent: Optional[Any] = None):
        self.tag = f"fluent_mi_{id(self)}"
        dpg.add_menu_item(label=label, callback=callback, tag=self.tag,
                          shortcut=shortcut, parent=parent)


# ═══════════════════════════════════════════════════════════════
# NAVIGATION CONTROLS
# ═══════════════════════════════════════════════════════════════

class FluentTabControl:
    """Tab control with Fluent 2 styling."""

    def __init__(self, tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 600, height: int = 400):
        self.tag = tag or f"fluent_tabs_{id(self)}"
        self._tab_count = 0
        c = FluentTheme().colors

        dpg.add_tab_bar(tag=self.tag, parent=parent, width=width, height=height)

        with dpg.theme() as tab_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Tab, _hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered, _hex_to_rgba(c.fill_subtle_hover))
                dpg.add_theme_color(dpg.mvThemeCol_TabActive, _hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, _hex_to_rgba(c.fill_subtle))
                dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, _hex_to_rgba(c.accent_pressed))
                dpg.add_theme_style(dpg.mvStyleVar_TabRounding, FluentTokens.CORNER_RADIUS_MEDIUM)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, FluentTokens.SPACING_M, FluentTokens.SPACING_S)
        dpg.bind_item_theme(self.tag, tab_theme)

    def add_tab(self, label: str, no_close: bool = True) -> str:
        self._tab_count += 1
        tab_tag = f"{self.tag}_tab_{self._tab_count}"
        dpg.add_tab(label=label, tag=tab_tag, parent=self.tag)
        return tab_tag


class FluentSplitView:
    """Split pane with collapsible sidebar."""

    def __init__(self, tag: Optional[str] = None, parent: Optional[Any] = None,
                 sidebar_width: int = 200, width: int = 800, height: int = 600):
        self.tag = tag or f"fluent_split_{id(self)}"
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            with dpg.child_window(tag=f"{self.tag}_sidebar",
                                   width=sidebar_width, height=height):
                with dpg.theme() as sidebar_theme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _hex_to_rgba(c.surface_subtle))
                        dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border))
                        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, FluentTokens.STROKE_WIDTH_NORMAL)
                dpg.bind_item_theme(f"{self.tag}_sidebar", sidebar_theme)

            with dpg.child_window(tag=f"{self.tag}_content",
                                   width=width - sidebar_width, height=height):
                with dpg.theme() as content_theme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _hex_to_rgba(c.background))
                dpg.bind_item_theme(f"{self.tag}_content", content_theme)

    def toggle_sidebar(self):
        sidebar = f"{self.tag}_sidebar"
        if dpg.is_item_shown(sidebar):
            dpg.hide_item(sidebar)
        else:
            dpg.show_item(sidebar)


class FluentCommandBar:
    """Command bar with action buttons."""

    def __init__(self, tag: Optional[str] = None, parent: Optional[Any] = None):
        self.tag = tag or f"fluent_cmdbar_{id(self)}"
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            with dpg.theme() as bar_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _hex_to_rgba(c.surface))
                    dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border))
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, FluentTokens.CORNER_RADIUS_LARGE)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, FluentTokens.STROKE_WIDTH_NORMAL)
            dpg.add_child_window(tag=f"{self.tag}_child", height=40, width=-1)
            dpg.bind_item_theme(f"{self.tag}_child", bar_theme)

    def add_button(self, icon: str, label: str, callback: Optional[Callable] = None):
        with dpg.group(horizontal=True, parent=f"{self.tag}_child"):
            dpg.add_button(label=icon, callback=callback, width=36, height=32)
            dpg.add_text(label)


class FluentBreadcrumbBar:
    """Breadcrumb navigation path."""

    def __init__(self, items: Optional[List[str]] = None,
                 callback: Optional[Callable] = None, tag: Optional[str] = None,
                 parent: Optional[Any] = None):
        self.tag = tag or f"fluent_bc_{id(self)}"
        self._items = items or []
        self._callback = callback
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            for i, item in enumerate(self._items):
                if i > 0:
                    dpg.add_text("›", color=_hex_to_rgba(c.text_secondary))
                dpg.add_button(label=item, callback=callback,
                               height=FluentTokens.CONTROL_HEIGHT_MEDIUM)
                _apply_fluent_style(
                    dpg.get_item_alias(dpg.last_item()) or str(dpg.last_item()),
                    corner_radius=FluentTokens.CORNER_RADIUS_SMALL,
                )


class FluentNavigationView:
    """Navigation view with pane and content area."""

    def __init__(self, tag: Optional[str] = None, parent: Optional[Any] = None,
                 width: int = 800, height: int = 600,
                 pane_width: int = 200, compact_width: int = 48):
        self.tag = tag or f"fluent_navview_{id(self)}"
        self._pane_open = True
        c = FluentTheme().colors
        self._items: List[Dict] = []

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            # Navigation pane
            with dpg.child_window(tag=f"{self.tag}_pane",
                                   width=pane_width, height=height):
                with dpg.theme() as pane_theme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _hex_to_rgba(c.surface_subtle))
                        dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border))
                        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, FluentTokens.STROKE_WIDTH_NORMAL)
                dpg.bind_item_theme(f"{self.tag}_pane", pane_theme)

            # Toggle button
            with dpg.group():
                dpg.add_button(label="☰", callback=self._toggle_pane,
                               width=24, height=24)

            # Content area
            with dpg.child_window(tag=f"{self.tag}_content",
                                   width=width - pane_width - 30, height=height):
                with dpg.theme() as content_theme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _hex_to_rgba(c.background))
                dpg.bind_item_theme(f"{self.tag}_content", content_theme)

    def _toggle_pane(self, sender, app_data, user_data):
        self._pane_open = not self._pane_open
        if self._pane_open:
            dpg.show_item(f"{self.tag}_pane")
        else:
            dpg.hide_item(f"{self.tag}_pane")

    def add_nav_item(self, icon: str, label: str, callback: Optional[Callable] = None) -> str:
        tag = f"{self.tag}_nav_{label.replace(' ', '_')}"
        with dpg.group(horizontal=True, parent=f"{self.tag}_pane"):
            dpg.add_text(icon, width=20)
            dpg.add_button(label=label, callback=callback, width=160, height=32)
        _apply_fluent_style(
            dpg.get_item_alias(dpg.last_item()) or str(dpg.last_item()),
            corner_radius=FluentTokens.CORNER_RADIUS_LARGE,
        )
        return tag


# ═══════════════════════════════════════════════════════════════
# PICKERS
# ═══════════════════════════════════════════════════════════════

class FluentColorPicker:
    """Color picker with Fluent styling."""

    def __init__(self, label: str = "Color", default_color: Tuple = (0, 120, 212, 255),
                 callback: Optional[Callable] = None, tag: Optional[str] = None,
                 parent: Optional[Any] = None):
        self.tag = tag or f"fluent_color_{id(self)}"
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            if label:
                dpg.add_text(label)
            dpg.add_color_edit(default_value=default_color, tag=f"{self.tag}_picker",
                               callback=callback, no_alpha=True)
            dpg.add_text(f"#{default_color[0]:02X}{default_color[1]:02X}{default_color[2]:02X}",
                         tag=f"{self.tag}_hex", color=_hex_to_rgba(c.text_secondary))

        if callback is None:
            dpg.configure_item(f"{self.tag}_picker", callback=self._update_hex)

    def _update_hex(self, sender, app_data, user_data):
        r, g, b = int(app_data[0]), int(app_data[1]), int(app_data[2])
        dpg.configure_item(f"{self.tag}_hex", default_value=f"#{r:02X}{g:02X}{b:02X}")

    def get_value(self) -> Tuple:
        return dpg.get_value(f"{self.tag}_picker") or (0, 0, 0, 255)


class FluentDatePicker:
    """Date picker control."""

    def __init__(self, label: str = "Date", tag: Optional[str] = None,
                 parent: Optional[Any] = None, callback: Optional[Callable] = None):
        self.tag = tag or f"fluent_date_{id(self)}"
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            if label:
                dpg.add_text(label)
            dpg.add_input_int(tag=f"{self.tag}_day", default_value=1, width=50, min_value=1, max_value=31)
            dpg.add_combo(tag=f"{self.tag}_month",
                          items=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                          default_value="Jan", width=60)
            dpg.add_input_int(tag=f"{self.tag}_year", default_value=2024, width=60, min_value=1900, max_value=2100)

        for item in [f"{self.tag}_day", f"{self.tag}_month", f"{self.tag}_year"]:
            _apply_fluent_style(item, height=FluentTokens.CONTROL_HEIGHT_MEDIUM,
                                border_color=_hex_to_rgba(c.border),
                                bg_color=_hex_to_rgba(c.control_default))

    def get_value(self) -> str:
        day = dpg.get_value(f"{self.tag}_day") or 1
        month = dpg.get_value(f"{self.tag}_month") or "Jan"
        year = dpg.get_value(f"{self.tag}_year") or 2024
        return f"{year}-{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].index(month)+1:02d}-{day:02d}"


class FluentCalendarDatePicker(FluentDatePicker):
    """Calendar date picker (same as DatePicker, extended for naming compatibility)."""
    pass


class FluentTimePicker:
    """Time picker control."""

    def __init__(self, label: str = "Time", tag: Optional[str] = None,
                 parent: Optional[Any] = None, callback: Optional[Callable] = None):
        self.tag = tag or f"fluent_time_{id(self)}"
        c = FluentTheme().colors

        with dpg.group(horizontal=True, tag=self.tag, parent=parent):
            if label:
                dpg.add_text(label)
            dpg.add_input_int(tag=f"{self.tag}_hour", default_value=12, width=50, min_value=0, max_value=23)
            dpg.add_text(":")
            dpg.add_input_int(tag=f"{self.tag}_min", default_value=0, width=50, min_value=0, max_value=59)
            dpg.add_combo(tag=f"{self.tag}_ampm", items=["AM", "PM"], default_value="AM", width=50)

        for item in [f"{self.tag}_hour", f"{self.tag}_min", f"{self.tag}_ampm"]:
            _apply_fluent_style(item, height=FluentTokens.CONTROL_HEIGHT_MEDIUM,
                                border_color=_hex_to_rgba(c.border),
                                bg_color=_hex_to_rgba(c.control_default))

    def get_value(self) -> str:
        h = dpg.get_value(f"{self.tag}_hour") or 0
        m = dpg.get_value(f"{self.tag}_min") or 0
        ap = dpg.get_value(f"{self.tag}_ampm") or "AM"
        return f"{h:02d}:{m:02d} {ap}"


class FluentCommandBarFlyout:
    """Flyout command bar that appears near a target."""

    def __init__(self, tag: Optional[str] = None, parent: Optional[Any] = None):
        self.tag = tag or f"fluent_flyout_{id(self)}"
        c = FluentTheme().colors

        with dpg.child_window(tag=self.tag, show=False,
                               height=40, width=-1):
            with dpg.theme() as flyout_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, _hex_to_rgba(c.card))
                    dpg.add_theme_color(dpg.mvThemeCol_Border, _hex_to_rgba(c.border_strong))
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, FluentTokens.CORNER_RADIUS_LARGE)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, FluentTokens.STROKE_WIDTH_THICK)
            dpg.bind_item_theme(self.tag, flyout_theme)
            with dpg.group(horizontal=True):
                pass  # Add buttons via add_button

    def add_button(self, icon: str, label: str, callback: Optional[Callable] = None):
        with dpg.group(horizontal=True, parent=self.tag):
            dpg.add_button(label=f"{icon} {label}", callback=callback,
                           height=32)

    def show(self):
        dpg.show_item(self.tag)

    def hide(self):
        dpg.hide_item(self.tag)


class FluentPersonPicture:
    """Person avatar / profile picture placeholder."""

    def __init__(self, name: str = "A", size: int = 48,
                 tag: Optional[str] = None, parent: Optional[Any] = None):
        self.tag = tag or f"fluent_person_{id(self)}"
        self._name = name
        self._size = size
        c = FluentTheme().colors

        # Generate a color from name hash
        hue = sum(ord(c) for c in name) % 360
        # Draw as a circle button with initial
        dpg.add_button(label=name[:1].upper(), tag=self.tag,
                       width=size, height=size, callback=None, parent=parent)

        with dpg.theme() as person_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, _hex_to_rgba(c.accent))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hex_to_rgba(c.accent_hover))
                dpg.add_theme_color(dpg.mvThemeCol_Text, _hex_to_rgba(c.text_on_accent))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, size // 2)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
        dpg.bind_item_theme(self.tag, person_theme)

    def set_name(self, name: str):
        self._name = name
        dpg.configure_item(self.tag, label=name[:1].upper())


class FluentInfoBadge:
    """Small badge for notifications / counts."""

    def __init__(self, text: str = "1", tag: Optional[str] = None,
                 parent: Optional[Any] = None):
        self.tag = tag or f"fluent_badge_{id(self)}"
        c = FluentTheme().colors

        dpg.add_text(text, tag=self.tag, parent=parent)

        with dpg.theme() as badge_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, _hex_to_rgba(c.text_on_accent))
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 1)
        dpg.bind_item_theme(self.tag, badge_theme)
        # Wrap in a colored group
        with dpg.drawlist(width=20, height=16, parent=parent):
            dpg.draw_circle((10, 8), 8, fill=_hex_to_rgba(c.danger))

    def set_text(self, text: str):
        dpg.configure_item(self.tag, default_value=text)
