"""
Fluent-style animation utilities for DearPyGUI.

Implements easing curves matching Fluent 2 motion design:
    • Accelerate / Decelerate / Accelerate-Decelerate
    • Elastic, Bounce, Spring
    • Duration tokens matching FluentTokens

Since DearPyGUI is immediate-mode, animations are timer-driven
value interpolations that update widget properties each frame.
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import math
import time
import dearpygui.dearpygui as dpg

from fluent_dpg.theme import FluentTokens


# ── Easing Functions ─────────────────────────────────────────────────────────

class Easing:
    """
    Standard easing curves. All functions accept t ∈ [0,1] → value ∈ [0,1].
    """

    @staticmethod
    def linear(t: float) -> float:
        return t

    @staticmethod
    def ease_in(t: float) -> float:
        """Accelerate from rest (Fluent accelerate)."""
        return t * t

    @staticmethod
    def ease_out(t: float) -> float:
        """Decelerate to rest (Fluent decelerate)."""
        return t * (2 - t)

    @staticmethod
    def ease_in_out(t: float) -> float:
        """Accelerate then decelerate (Fluent standard)."""
        if t < 0.5:
            return 2 * t * t
        return -1 + (4 - 2 * t) * t

    @staticmethod
    def ease_out_quart(t: float) -> float:
        """Fluent's default for entrance animations."""
        return 1 - (1 - t) ** 4

    @staticmethod
    def ease_in_quart(t: float) -> float:
        return t ** 4

    @staticmethod
    def spring(t: float) -> float:
        """Underdamped spring overshoot."""
        if t >= 1.0:
            return 1.0
        return 1 - math.exp(-6 * t) * math.cos(2 * math.pi * 1.5 * t)

    @staticmethod
    def elastic(t: float) -> float:
        """Elastic overshoot."""
        if t == 0 or t == 1:
            return t
        return (2 ** (-10 * t) * math.sin((t - 0.075) * (2 * math.pi) / 0.3)) + 1

    @staticmethod
    def bounce(t: float) -> float:
        """Bounce effect."""
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375


# ── Animation ────────────────────────────────────────────────────────────────

@dataclass
class Animation:
    """
    A single animation definition.

    Usage:
        anim = Animation(
            target_id=widget_tag,
            property="frame_bg",
            from_value=(240, 240, 240, 255),
            to_value=(200, 200, 200, 255),
            duration_ms=FluentTokens.DURATION_NORMAL,
            easing=Easing.ease_out,
        )
        animator.play(anim)
    """
    target_id: Any
    property: str
    from_value: Any
    to_value: Any
    duration_ms: int = FluentTokens.DURATION_NORMAL
    easing: Callable[[float], float] = field(default=Easing.ease_out_quart)
    delay_ms: int = 0
    on_complete: Optional[Callable[[], None]] = None


# ── Color Helpers ────────────────────────────────────────────────────────────

def _lerp_color(c1: Tuple, c2: Tuple, t: float) -> Tuple:
    """Linear interpolation between two RGBA tuples."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def _lerp_float(v1: float, v2: float, t: float) -> float:
    return v1 + (v2 - v1) * t


# ── FluentAnimator ───────────────────────────────────────────────────────────

class FluentAnimator:
    """
    Timer-driven animation manager for DearPyGUI widgets.

    Manages a queue of Animation objects, interpolates values per-frame
    using the specified easing, and applies to DearPyGUI widget properties.

    Usage:
        animator = FluentAnimator()
        animator.play(Animation(...))
        animator.tick()  # call in render loop
    """

    def __init__(self):
        self._active: List[Dict] = []
        self._timer_tag: Optional[str] = None

    def play(self, anim: Animation):
        """Schedule an animation for playback."""
        self._active.append({
            "anim": anim,
            "start_time": time.monotonic() + anim.delay_ms / 1000.0,
            "elapsed_ms": 0,
            "done": False,
        })
        if self._timer_tag is None:
            self._start_timer()

    def play_many(self, animations: List[Animation], stagger_ms: int = 0):
        """Play multiple animations with optional stagger delay."""
        for i, anim in enumerate(animations):
            a = Animation(
                target_id=anim.target_id,
                property=anim.property,
                from_value=anim.from_value,
                to_value=anim.to_value,
                duration_ms=anim.duration_ms,
                easing=anim.easing,
                delay_ms=anim.delay_ms + i * stagger_ms,
                on_complete=anim.on_complete,
            )
            self.play(a)

    def _start_timer(self):
        """Register a DearPyGUI render callback for animation ticks."""
        self._timer_tag = "__fluent_animator_tick__"
        if not dpg.does_item_exist(self._timer_tag):
            with dpg.handler_registry():
                dpg.add_render_handler(
                    callback=self.tick,
                    tag=self._timer_tag,
                )

    def tick(self, sender=None, app_data=None):
        """Process all active animations (called per frame)."""
        now = time.monotonic()
        to_remove = []
        for i, entry in enumerate(self._active):
            if entry["done"]:
                to_remove.append(i)
                continue
            anim: Animation = entry["anim"]
            elapsed = (now - entry["start_time"]) * 1000
            if elapsed < 0:
                continue  # still in delay
            entry["elapsed_ms"] = elapsed
            if elapsed >= anim.duration_ms:
                t = 1.0
                entry["done"] = True
            else:
                t = elapsed / anim.duration_ms
                t = anim.easing(t)

            self._apply(anim, t)

            if entry["done"]:
                if anim.on_complete:
                    try:
                        anim.on_complete()
                    except Exception:
                        pass
                to_remove.append(i)

        # Clean up finished (reverse order to preserve indices)
        for i in reversed(to_remove):
            self._active.pop(i)

        if not self._active and self._timer_tag:
            if dpg.does_item_exist(self._timer_tag):
                dpg.delete_item(self._timer_tag)
            self._timer_tag = None

    def _apply(self, anim: Animation, t: float):
        """Apply interpolated value to DearPyGUI widget."""
        tag = anim.target_id
        prop = anim.property
        from_v = anim.from_value
        to_v = anim.to_value

        if not dpg.does_item_exist(tag):
            return

        # Determine value type and interpolate
        if isinstance(from_v, (tuple, list)) and len(from_v) == 4:
            # RGBA color
            val = _lerp_color(from_v, to_v, t)  # type: ignore
            self._set_color(tag, prop, val)
        elif isinstance(from_v, (int, float)):
            val = _lerp_float(from_v, to_v, t)
            self._set_value(tag, prop, val)
        else:
            # Generic: snap at end
            if t >= 1.0:
                self._set_value(tag, prop, to_v)

    @staticmethod
    def _set_color(tag: Any, prop: str, value: Tuple):
        """Set a color property on a DearPyGUI item."""
        color_map = {
            "frame_bg": dpg.mvThemeCol_FrameBg,
            "frame_bg_hovered": dpg.mvThemeCol_FrameBgHovered,
            "frame_bg_active": dpg.mvThemeCol_FrameBgActive,
            "text": dpg.mvThemeCol_Text,
            "button": dpg.mvThemeCol_Button,
            "button_hovered": dpg.mvThemeCol_ButtonHovered,
            "button_active": dpg.mvThemeCol_ButtonActive,
            "border": dpg.mvThemeCol_Border,
        }
        theme_color = color_map.get(prop)
        if theme_color is not None:
            dpg.configure_item(tag, fill_color=value)
            # For theme colors, we use a theme component
            try:
                with dpg.theme() as anim_theme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(theme_color, value)
                dpg.bind_item_theme(tag, anim_theme)
            except Exception:
                dpg.configure_item(tag, fill_color=value)
        else:
            dpg.configure_item(tag, fill_color=value)

    @staticmethod
    def _set_value(tag: Any, prop: str, value: Any):
        """Set a generic property on a DearPyGUI item."""
        value_map = {
            "width": "width",
            "height": "height",
            "alpha": "alpha",
            "default_value": "default_value",
            "pos": "pos",
        }
        kw = value_map.get(prop, prop)
        try:
            dpg.configure_item(tag, **{kw: value})
        except Exception:
            pass

    def stop_all(self):
        """Cancel all active animations."""
        for entry in self._active:
            anim = entry["anim"]
            if anim.on_complete:
                try:
                    anim.on_complete()
                except Exception:
                    pass
        self._active.clear()
        if self._timer_tag and dpg.does_item_exist(self._timer_tag):
            dpg.delete_item(self._timer_tag)
            self._timer_tag = None

    @property
    def is_animating(self) -> bool:
        return len(self._active) > 0
