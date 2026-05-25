"""
Fluent-DPG: Fluent 2 Design System controls for DearPyGUI with MVVM architecture.

Architecture:
    ViewModel  →  View  →  DearPyGUI Widget
    (pure data)   (binds)   (immediate-mode render)

Usage:
    from fluent_dpg import FluentTheme, FluentViewModel, FluentApp
    from fluent_dpg.controls import FluentButton, FluentTextBox, FluentToggleSwitch
    ...
"""

__version__ = "1.0.0"

from fluent_dpg.theme import FluentTheme, FluentColors, FluentTokens, FluentThemeMode
from fluent_dpg.viewmodel import (
    ViewModel,
    BindableProperty,
    Command,
    ObservableCollection,
)
from fluent_dpg.animations import Animation, Easing, FluentAnimator
from fluent_dpg.controls import (
    FluentButton,
    FluentAccentButton,
    FluentSubtleButton,
    FluentIconLabel,
    FluentTextBox,
    FluentPasswordBox,
    FluentSearchBox,
    FluentNumberBox,
    FluentComboBox,
    FluentAutoSuggestBox,
    FluentCheckBox,
    FluentToggleSwitch,
    FluentRadioButton,
    FluentSlider,
    FluentProgressBar,
    FluentRatingControl,
    FluentExpander,
    FluentInfoBar,
    FluentContentDialog,
    FluentTooltip,
    FluentMenu,
    FluentMenuItem,
    FluentTreeView,
    FluentTreeViewItem,
    FluentListView,
    FluentDataGrid,
    FluentTabControl,
    FluentSplitView,
    FluentCommandBar,
    FluentBreadcrumbBar,
    FluentNavigationView,
    FluentPersonPicture,
    FluentProgressBarRing,
    FluentInfoBadge,
    FluentDatePicker,
    FluentCalendarDatePicker,
    FluentTimePicker,
    FluentColorPicker,
    FluentRichEditBox,
    FluentDropDownButton,
    FluentSplitButton,
    FluentToggleButton,
    FluentRepeatButton,
    FluentHyperlinkButton,
    FluentAppBarButton,
    FluentCommandBarFlyout,
)
from fluent_dpg.layout import (
    FluentStackPanel,
    FluentGrid,
    FluentCard,
    FluentExpanderGroup,
    FluentDialogHost,
    FluentScrollViewer,
)

__all__ = [
    # Theme
    "FluentTheme",
    "FluentColors",
    "FluentTokens",
    "FluentThemeMode",
    # MVVM
    "ViewModel",
    "BindableProperty",
    "Command",
    "ObservableCollection",
    # Animations
    "Animation",
    "Easing",
    "FluentAnimator",
    # Controls
    "FluentButton",
    "FluentAccentButton",
    "FluentSubtleButton",
    "FluentIconLabel",
    "FluentTextBox",
    "FluentPasswordBox",
    "FluentSearchBox",
    "FluentNumberBox",
    "FluentComboBox",
    "FluentAutoSuggestBox",
    "FluentCheckBox",
    "FluentToggleSwitch",
    "FluentRadioButton",
    "FluentSlider",
    "FluentProgressBar",
    "FluentRatingControl",
    "FluentExpander",
    "FluentInfoBar",
    "FluentContentDialog",
    "FluentTooltip",
    "FluentMenu",
    "FluentMenuItem",
    "FluentTreeView",
    "FluentTreeViewItem",
    "FluentListView",
    "FluentDataGrid",
    "FluentTabControl",
    "FluentSplitView",
    "FluentCommandBar",
    "FluentBreadcrumbBar",
    "FluentNavigationView",
    "FluentPersonPicture",
    "FluentProgressBarRing",
    "FluentInfoBadge",
    "FluentDatePicker",
    "FluentCalendarDatePicker",
    "FluentTimePicker",
    "FluentColorPicker",
    "FluentRichEditBox",
    "FluentDropDownButton",
    "FluentSplitButton",
    "FluentToggleButton",
    "FluentRepeatButton",
    "FluentHyperlinkButton",
    "FluentAppBarButton",
    "FluentCommandBarFlyout",
    # Layout
    "FluentStackPanel",
    "FluentGrid",
    "FluentCard",
    "FluentExpanderGroup",
    "FluentDialogHost",
    "FluentScrollViewer",
]
