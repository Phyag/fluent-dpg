"""
MVVM foundation for Fluent-DPG.

Provides:
    ViewModel       — Base class with property-change notification
    BindableProperty — Descriptor for observable properties
    Command         — ICommand pattern with CanExecute
    ObservableCollection — List with change events

Architecture:
    ViewModel exposes BindableProperty / Command
    View binds to ViewModel via DearPyGUI callbacks
    No retained widget tree — binding is callback-driven
"""

from __future__ import annotations
from typing import (
    Any, Callable, Dict, Generic, List, Optional, TypeVar,
    TYPE_CHECKING,
)
from dataclasses import dataclass, field
import threading

if TYPE_CHECKING:
    pass  # no circular deps needed

T = TypeVar("T")
Callback = Callable[..., Any]


# ── BindableProperty ────────────────────────────────────────────────────────

class BindableProperty(Generic[T]):
    """
    Descriptor implementing an observable property on ViewModel.

    Usage:
        class MyVM(ViewModel):
            name = BindableProperty("default")

    When set, fires `on_property_changed(name, old, new)`.
    """

    def __init__(self, default: Optional[T] = None):
        self._default = default

    def __set_name__(self, owner, name: str):
        self._name = name
        self._attr = f"_bp_{name}"

    def __get__(self, obj, objtype=None) -> T:
        if obj is None:
            return self._default  # type: ignore
        return getattr(obj, self._attr, self._default)

    def __set__(self, obj, value: T):
        old = getattr(obj, self._attr, self._default)
        if old == value:
            return
        setattr(obj, self._attr, value)
        if hasattr(obj, "on_property_changed"):
            obj.on_property_changed(self._name, old, value)


# ── Command (ICommand pattern) ──────────────────────────────────────────────

class Command:
    """
    WPF-style ICommand for DearPyGUI.

    Usage:
        self.save_cmd = Command(self.save, can_execute=lambda: self.dirty)
        dpg.add_button(label="Save", callback=self.save_cmd.execute)
    """

    def __init__(
        self,
        execute: Callback,
        can_execute: Optional[Callable[[], bool]] = None,
    ):
        self._execute = execute
        self._can_execute = can_execute or (lambda: True)
        self._listeners: List[Callback] = []

    def execute(self, sender=None, app_data=None, user_data=None):
        if self.can_execute():
            self._execute(sender, app_data, user_data)

    def can_execute(self) -> bool:
        try:
            return self._can_execute()
        except Exception:
            return True

    def on_can_execute_changed(self, listener: Callback):
        """Register a listener for CanExecute changes."""
        self._listeners.append(listener)

    def notify_can_execute_changed(self):
        for cb in self._listeners:
            try:
                cb()
            except Exception:
                pass


# ── ObservableCollection ───────────────────────────────────────────────────

class ObservableCollection(List[T]):
    """
    List that fires events on mutation.

    Events:
        on_collection_changed(action, index, item)
        action ∈ {"added", "removed", "cleared", "replaced"}
    """

    def __init__(self, items: Optional[List[T]] = None):
        super().__init__(items or [])
        self._handlers: List[Callable[[str, int, Any], None]] = []

    def _fire(self, action: str, index: int = -1, item: Any = None):
        for h in self._handlers:
            try:
                h(action, index, item)
            except Exception:
                pass

    def on_changed(self, handler: Callable[[str, int, Any], None]):
        self._handlers.append(handler)

    def append(self, item: T):
        super().append(item)
        self._fire("added", len(self) - 1, item)

    def insert(self, index: int, item: T):
        super().insert(index, item)
        self._fire("added", index, item)

    def pop(self, index: int = -1) -> T:
        item = super().pop(index)
        self._fire("removed", index, item)
        return item

    def remove(self, item: T):
        idx = self.index(item)
        super().remove(item)
        self._fire("removed", idx, item)

    def clear(self):
        super().clear()
        self._fire("cleared")

    def __setitem__(self, index, item: T):
        old = self[index]
        super().__setitem__(index, item)
        self._fire("replaced", index, item)


# ── ViewModel Base ──────────────────────────────────────────────────────────

class ViewModel:
    """
    Base class for all ViewModels.

    Subclasses use BindableProperty for observable properties
    and Command for user actions.

    Usage:
        class PersonVM(ViewModel):
            name = BindableProperty("")
            age  = BindableProperty(0)

            def __init__(self):
                super().__init__()

        vm = PersonVM()
        vm.name = "Alice"   # fires on_property_changed
    """

    def __init__(self):
        self._property_handlers: Dict[str, List[Callback]] = {}
        self._global_handlers: List[Callback] = []

    def on_property_changed(self, property_name: str, old_value: Any, new_value: Any):
        """Override in subclass for custom reaction, or register handlers below."""
        # Notify registered handlers
        for h in self._property_handlers.get(property_name, []):
            try:
                h(property_name, old_value, new_value)
            except Exception:
                pass
        for h in self._global_handlers:
            try:
                h(self, property_name, old_value, new_value)
            except Exception:
                pass

    def add_property_handler(self, property_name: str, handler: Callback):
        """Subscribe to a specific property change."""
        self._property_handlers.setdefault(property_name, []).append(handler)

    def add_global_handler(self, handler: Callback):
        """Subscribe to ALL property changes."""
        self._global_handlers.append(handler)

    def remove_property_handler(self, property_name: str, handler: Callback):
        lst = self._property_handlers.get(property_name, [])
        if handler in lst:
            lst.remove(handler)

    def remove_global_handler(self, handler: Callback):
        if handler in self._global_handlers:
            self._global_handlers.remove(handler)


# ── Composite ViewModel / Relay ─────────────────────────────────────────────

class RelayVM(ViewModel):
    """
    Forwards property changes from a child VM to the parent.
    Useful for nested MVVM scenarios.
    """

    def __init__(self, child: ViewModel, prefix: str = ""):
        super().__init__()
        self._child = child
        self._prefix = prefix
        child.add_global_handler(self._relay)

    def _relay(self, vm: ViewModel, prop: str, old: Any, new: Any):
        full = f"{self._prefix}.{prop}" if self._prefix else prop
        self.on_property_changed(full, old, new)
