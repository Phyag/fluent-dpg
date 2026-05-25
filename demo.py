#!/usr/bin/env python3
"""
Fluent-DPG Demo — Showcase of Fluent 2 controls for DearPyGUI.

Run:
    python demo.py
"""

import dearpygui.dearpygui as dpg
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fluent_dpg.theme import FluentTheme, FluentTokens, FluentThemeMode
from fluent_dpg.viewmodel import ViewModel, BindableProperty, Command
from fluent_dpg.animations import FluentAnimator, Animation, Easing
from fluent_dpg.controls import *
from fluent_dpg.layout import *


class SettingsVM(ViewModel):
    username = BindableProperty("")
    notifications = BindableProperty(True)
    dark_mode = BindableProperty(False)
    volume = BindableProperty(75.0)
    selected_theme = BindableProperty("Fluent Light")
    rating = BindableProperty(4)


class FormVM(ViewModel):
    name = BindableProperty("")
    password = BindableProperty("")
    category = BindableProperty("")
    agree = BindableProperty(False)
    comments = BindableProperty("")


class MainVM(ViewModel):
    search_query = BindableProperty("")
    progress = BindableProperty(0.0)


class FluentDemoApp:

    def __init__(self):
        self.theme = FluentTheme(mode=FluentThemeMode.LIGHT)
        self.animator = FluentAnimator()
        self.main_vm = MainVM()
        self.settings_vm = SettingsVM()
        self.form_vm = FormVM()

    def run(self):
        dpg.create_context()
        self.theme.apply()
        dpg.create_viewport(
            title="Fluent-DPG Demo", width=1200, height=800,
        )
        dpg.setup_dearpygui()

        with dpg.window(label="Fluent-DPG Showcase", tag="main_win"):
            self._build_ui()

        dpg.show_viewport()
        dpg.set_primary_window("main_win", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def _show_page(self, page):
        for p in ["home","controls","form","settings","data","theme"]:
            tag = f"page_{p}"
            if dpg.does_item_exist(tag):
                dpg.configure_item(tag, show=(p == page))

    def _build_ui(self):
        c = self.theme.colors

        # Navigation View
        nav = FluentNavigationView(tag="demo_nav", width=1160, height=760, pane_width=200)
        nav.add_nav_item("🏠", "Home", callback=lambda s,a,u: self._show_page("home"))
        nav.add_nav_item("🎛️", "Controls", callback=lambda s,a,u: self._show_page("controls"))
        nav.add_nav_item("📝", "Form", callback=lambda s,a,u: self._show_page("form"))
        nav.add_nav_item("⚙️", "Settings", callback=lambda s,a,u: self._show_page("settings"))
        nav.add_nav_item("📊", "Data", callback=lambda s,a,u: self._show_page("data"))
        nav.add_nav_item("🎨", "Theme", callback=lambda s,a,u: self._show_page("theme"))

        dpg.add_spacer(height=16, parent="demo_nav_pane")
        FluentPersonPicture(name="F", size=40, parent="demo_nav_pane")
        dpg.add_text("  Fluent-DPG Demo", parent="demo_nav_pane")

        self._page("home")
        self._page("controls")
        self._page("form")
        self._page("settings")
        self._page("data")
        self._page("theme")
        self._show_page("home")

    def _page(self, name):
        tag = f"page_{name}"
        dpg.add_child_window(tag=tag, width=900, height=700,
                             parent="demo_nav_content", show=False,
                             no_scrollbar=False)
        return tag

    def _page_controls(self, tag):
        c = self.theme.colors

        dpg.add_text("Buttons", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        with dpg.group(horizontal=True, parent=tag):
            FluentButton("Default", callback=lambda *a: print("Default"))
            FluentAccentButton("Accent", callback=lambda *a: print("Accent"))
            FluentSubtleButton("Subtle", callback=lambda *a: print("Subtle"))
            FluentHyperlinkButton("Link", callback=lambda *a: print("Link"))

        dpg.add_spacer(height=16, parent=tag)
        with dpg.group(horizontal=True, parent=tag):
            FluentToggleButton("Toggle", callback=lambda *a: None)
            FluentSplitButton("Split", callback=lambda *a: None,
                              menu_callback=lambda *a: None)
            FluentDropDownButton("Dropdown", items=["A","B","C"],
                                 callback=lambda *a: None)

        dpg.add_spacer(height=24, parent=tag)
        dpg.add_text("Inputs", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        FluentTextBox("Name", "Enter name", parent=tag, width=300).bind_to(self.form_vm, "name")
        FluentPasswordBox("Password", parent=tag, width=300)
        FluentSearchBox("Search...", parent=tag, width=300)
        FluentNumberBox("Qty", default_value=5, parent=tag)

        dpg.add_spacer(height=24, parent=tag)
        dpg.add_text("Selection", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        FluentCheckBox("Notifications", parent=tag).bind_to(self.settings_vm, "notifications")
        FluentToggleSwitch("Dark Mode", parent=tag).bind_to(self.settings_vm, "dark_mode")
        FluentRadioButton("A", "g1", parent=tag)
        FluentRadioButton("B", "g1", True, parent=tag)
        FluentRadioButton("C", "g1", parent=tag)

        dpg.add_spacer(height=24, parent=tag)
        dpg.add_text("Sliders & Progress", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        FluentSlider("Volume", 75.0, parent=tag).bind_to(self.settings_vm, "volume")
        FluentProgressBar(0.65, show_label=True, parent=tag, width=300)
        FluentRatingControl(4, parent=tag).bind_to(self.settings_vm, "rating")

        dpg.add_spacer(height=24, parent=tag)
        dpg.add_text("Collections", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        FluentComboBox("Theme", ["Fluent Light","Fluent Dark","High Contrast"],
                       parent=tag, width=200).bind_to(self.settings_vm, "selected_theme")
        FluentAutoSuggestBox("Search", ["Apple","Banana","Cherry","Date"],
                             parent=tag, width=250)

        dpg.add_spacer(height=24, parent=tag)
        dpg.add_text("Pickers", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        with dpg.group(horizontal=True, parent=tag):
            FluentDatePicker(parent=tag)
            FluentTimePicker(parent=tag)
            FluentColorPicker(parent=tag)

        dpg.add_spacer(height=24, parent=tag)
        dpg.add_text("Surfaces", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        FluentExpander("Expand me", "Hidden content revealed here.", parent=tag, width=400)
        FluentInfoBar("Success!", "success", parent=tag, width=400)
        FluentInfoBar("Warning!", "warning", parent=tag, width=400)
        FluentInfoBar("Error!", "error", parent=tag, width=400)
        FluentAccentButton("Show Dialog", callback=self._demo_dialog, parent=tag)

        dpg.add_spacer(height=24, parent=tag)
        dpg.add_text("Cards", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        with dpg.group(horizontal=True, parent=tag):
            with FluentCard(180, 80, "Card 1", parent=tag):
                dpg.add_text("Content 1", wrap=160)
            with FluentCard(180, 80, "Card 2", parent=tag):
                dpg.add_text("Content 2", wrap=160)
            with FluentCard(180, 80, "Card 3", parent=tag):
                dpg.add_text("Content 3", wrap=160)

    def _page_form(self, tag):
        dpg.add_text("Sample Form", parent=tag)
        dpg.add_spacer(height=16, parent=tag)
        FluentTextBox("Name", "John Doe", parent=tag, width=400).bind_to(self.form_vm, "name")
        FluentPasswordBox("Password", parent=tag, width=400)
        FluentTextBox("Comments", multiline=True, parent=tag, width=400).bind_to(self.form_vm, "comments")
        FluentComboBox("Category", ["General","Bug","Feature","Support"],
                       parent=tag, width=300).bind_to(self.form_vm, "category")
        FluentCheckBox("Agree to terms", parent=tag).bind_to(self.form_vm, "agree")
        dpg.add_spacer(height=24, parent=tag)
        with dpg.group(horizontal=True, parent=tag):
            FluentAccentButton("Submit", callback=self._demo_dialog)
            FluentSubtleButton("Cancel")

    def _page_settings(self, tag):
        dpg.add_text("Settings", parent=tag)
        dpg.add_spacer(height=16, parent=tag)
        with FluentCard(500, 60, "Profile", parent=tag):
            with dpg.group(horizontal=True):
                FluentPersonPicture("U", 40)
                dpg.add_text("User\nuser@example.com")
        dpg.add_spacer(height=16, parent=tag)
        with FluentCard(500, 200, "Preferences", parent=tag):
            FluentToggleSwitch("Notifications", parent=tag).bind_to(self.settings_vm, "notifications")
            FluentToggleSwitch("Dark Mode", parent=tag).bind_to(self.settings_vm, "dark_mode")
            FluentSlider("Volume", 75.0, parent=tag, width=300).bind_to(self.settings_vm, "volume")

    def _page_data(self, tag):
        dpg.add_text("Data Grid", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        FluentDataGrid(
            headers=["Name","Role","Department","Status"],
            rows=[
                ["Alice","Engineer","Engineering","Active"],
                ["Bob","Designer","Design","Active"],
                ["Carol","Manager","Operations","On Leave"],
                ["David","Developer","Engineering","Active"],
                ["Eve","Analyst","Finance","Active"],
            ],
            parent=tag, width=700, height=250
        )
        dpg.add_spacer(height=24, parent=tag)
        dpg.add_text("Tree View", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        tree = FluentTreeView(parent=tag, width=300, height=250)
        n1 = tree.add_item("📁 Documents")
        tree.add_leaf("📄 Report.pdf", parent_node=n1)
        tree.add_leaf("📊 Data.xlsx", parent_node=n1)
        n2 = tree.add_item("📁 Images")
        tree.add_leaf("🖼️ Photo.jpg", parent_node=n2)

        dpg.add_spacer(height=24, parent=tag)
        dpg.add_text("Tabs", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        tabs = FluentTabControl(parent=tag, width=600, height=200)
        t1 = tabs.add_tab("Overview")
        dpg.add_text("Overview content", parent=t1)
        t2 = tabs.add_tab("Details")
        dpg.add_text("Details content", parent=t2)

    def _page_theme(self, tag):
        c = self.theme.colors
        dpg.add_text("Theme", parent=tag)
        dpg.add_spacer(height=16, parent=tag)
        FluentAccentButton("Toggle Light/Dark", callback=self._toggle_theme, parent=tag)
        dpg.add_spacer(height=24, parent=tag)
        dpg.add_text("Accent Color", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        FluentColorPicker(parent=tag)
        dpg.add_spacer(height=24, parent=tag)
        dpg.add_text("Color Tokens", parent=tag)
        dpg.add_spacer(height=8, parent=tag)
        with dpg.group(horizontal=True, parent=tag):
            for name, val in [("accent", c.accent), ("bg", c.background),
                              ("surface", c.surface), ("text", c.text_primary),
                              ("border", c.border), ("success", c.success),
                              ("warning", c.warning), ("danger", c.danger)]:
                dpg.add_button(label="", width=40, height=40)
                with dpg.theme() as swatch:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(dpg.mvThemeCol_Button, FluentTheme._hex_to_rgba(val))
                        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, FluentTokens.CORNER_RADIUS_LARGE)
                dpg.bind_item_theme(dpg.last_item(), swatch)
                dpg.add_text(name)

    def _toggle_theme(self, *a):
        self.theme.toggle()

    def _demo_dialog(self, *a):
        FluentContentDialog("Success", "Operation completed successfully!",
                            primary_text="OK", secondary_text="Close",
                            primary_callback=lambda: print("OK"))


if __name__ == "__main__":
    FluentDemoApp().run()
