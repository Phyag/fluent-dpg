# Fluent-DPG

**Fluent 2 Design System** controls for [DearPyGUI](https://github.com/hoffstadt/DearPyGui) with **MVVM architecture**.

> Brings Microsoft's Fluent 2 design language — rounded corners, accent colors, subtle hover animations, elevation — to DearPyGUI's immediate-mode rendering.

## Quick Start

```bash
pip install dearpygui
python demo.py
```

## Architecture

```
ViewModel ──(BindableProperty)──▶ View ──(DearPyGUI callbacks)──▶ Widget
   ▲                                  │
   └────────(two-way binding)─────────┘
```

- **ViewModel**: Pure Python data classes using `BindableProperty` descriptors
- **View**: Fluent-stDearPyGUI wrapper classes with MVVM binding
- **Model**: Your application data layer

## Controls

| Category | Controls |
|---|---|
| **Buttons** | `FluentButton`, `FluentAccentButton`, `FluentSubtleButton`, `FluentHyperlinkButton`, `FluentToggleButton`, `FluentSplitButton`, `FluentDropDownButton`, `FluentRepeatButton`, `FluentAppBarButton` |
| **Input** | `FluentTextBox`, `FluentPasswordBox`, `FluentSearchBox`, `FluentNumberBox`, `FluentRichEditBox`, `FluentAutoSuggestBox` |
| **Selection** | `FluentCheckBox`, `FluentToggleSwitch`, `FluentRadioButton` |
| **Sliders** | `FluentSlider`, `FluentProgressBar`, `FluentProgressBarRing`, `FluentRatingControl` |
| **Collections** | `FluentComboBox`, `FluentTreeView`, `FluentTreeViewItem`, `FluentListView`, `FluentDataGrid` |
| **Surfaces** | `FluentExpander`, `FluentInfoBar`, `FluentContentDialog`, `FluentTooltip`, `FluentMenu`, `FluentMenuItem` |
| **Navigation** | `FluentTabControl`, `FluentSplitView`, `FluentCommandBar`, `FluentBreadcrumbBar`, `FluentNavigationView`, `FluentCommandBarFlyout` |
| **Pickers** | `FluentColorPicker`, `FluentDatePicker`, `FluentCalendarDatePicker`, `FluentTimePicker` |
| **Layout** | `FluentStackPanel`, `FluentGrid`, `FluentCard`, `FluentExpanderGroup`, `FluentDialogHost`, `FluentScrollViewer` |
| **Misc** | `FluentPersonPicture`, `FluentInfoBadge`, `FluentIconLabel` |

## Theme

```python
from fluent_dpg import FluentTheme, FluentThemeMode

theme = FluentTheme(mode=FluentThemeMode.LIGHT)
theme.apply()       # Apply to DearPyGUI
theme.toggle()      # Toggle light/dark
theme.set_mode(FluentThemeMode.DARK)
```

## MVVM Binding

```python
from fluent_dpg import ViewModel, BindableProperty, FluentTextBox

class MyVM(ViewModel):
    name = BindableProperty("")

vm = MyVM()
txt = FluentTextBox(label="Name")
txt.bind_to(vm, "name")  # Two-way binding

vm.name = "Alice"        # VM → View updates
print(txt.get_value())   # View → VM updates
```

## Animations

```python
from fluent_dpg import FluentAnimator, Animation, Easing, FluentTokens

animator = FluentAnimator()
animator.play(Animation(
    target_id=widget_tag,
    property="frame_bg",
    from_value=(240, 240, 240, 255),
    to_value=(200, 200, 200, 255),
    duration_ms=FluentTokens.DURATION_NORMAL,
    easing=Easing.ease_out_quart,
))
```

## Fluent 2 Design Tokens

| Token | Value |
|---|---|
| Corner Radius (Small) | 2px |
| Corner Radius (Medium) | 4px |
| Corner Radius (Large) | 8px |
| Corner Radius (XLarge) | 12px |
| Control Height (Small) | 24px |
| Control Height (Medium) | 32px |
| Control Height (Large) | 40px |
| Animation Duration (Fast) | 150ms |
| Animation Duration (Normal) | 200ms |
| Animation Duration (Slow) | 300ms |
| Accent Color (Light) | #0078D4 |
| Accent Color (Dark) | #4DA3E8 |

## Project Structure

```
fluent-dpg/
├── fluent_dpg/
│   ├── __init__.py        # Package exports
│   ├── theme.py           # Fluent 2 color tokens & theme engine
│   ├── viewmodel.py       # MVVM base classes
│   ├── animations.py      # Animation system
│   ├── controls.py        # All Fluent controls
│   └── layout.py          # Layout containers
├── demo.py                # Full demo application
└── README.md
```
