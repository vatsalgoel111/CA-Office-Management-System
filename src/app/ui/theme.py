"""
File Purpose: Theme manager and semantic UI design tokens.
Module: app.ui.theme
Author: CA Office CMS Development Team
Created Date: 2026-07-02
Last Modified: 2026-07-02
Dependencies: dataclasses, typing, customtkinter.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

import customtkinter as ctk


ColorPair = Tuple[str, str]


@dataclass(frozen=True)
class SpacingTokens:
    """Spacing tokens based on an 8px rhythm."""

    xs: int = 4
    sm: int = 8
    md: int = 12
    lg: int = 16
    xl: int = 24
    xxl: int = 32


@dataclass(frozen=True)
class FontTokens:
    """Font tokens for business UI consistency."""

    family: str = "Segoe UI"
    small: int = 12
    body: int = 14
    section: int = 18
    page: int = 22
    metric: int = 24


@dataclass(frozen=True)
class RadiusTokens:
    """Corner radius tokens."""

    sm: int = 4
    md: int = 6
    lg: int = 8


@dataclass(frozen=True)
class ThemeTokens:
    """Complete design token set."""

    colors: Dict[str, ColorPair]
    spacing: SpacingTokens
    fonts: FontTokens
    radius: RadiusTokens


class ThemeManager:
    """Applies and exposes semantic theme tokens."""

    def __init__(self) -> None:
        self.tokens = ThemeTokens(
            colors={
                "primary": ("#1F6F78", "#3AA6B2"),
                "primary_hover": ("#185D65", "#2E8E99"),
                "secondary": ("#334155", "#CBD5E1"),
                "accent": ("#B7791F", "#F6AD55"),
                "bg": ("#F8FAFC", "#101418"),
                "surface": ("#FFFFFF", "#171C22"),
                "surface_alt": ("#EEF2F7", "#202833"),
                "border": ("#D7DEE8", "#344050"),
                "text": ("#172033", "#E5E7EB"),
                "text_muted": ("#64748B", "#9CA3AF"),
                "success": ("#15803D", "#4ADE80"),
                "warning": ("#B45309", "#FBBF24"),
                "error": ("#B91C1C", "#F87171"),
                "info": ("#0369A1", "#38BDF8"),
                "neutral": ("#64748B", "#94A3B8"),
            },
            spacing=SpacingTokens(),
            fonts=FontTokens(),
            radius=RadiusTokens(),
        )

    def apply(self, appearance_mode: str = "dark") -> None:
        """Apply global CustomTkinter appearance settings."""

        ctk.set_appearance_mode(appearance_mode)
        ctk.set_default_color_theme("blue")

    def color(self, token: str) -> ColorPair:
        """Return a light/dark color pair for a semantic token."""

        return self.tokens.colors[token]

    def font(self, size: int, weight: str = "normal") -> ctk.CTkFont:
        """Return a standard UI font."""

        return ctk.CTkFont(
            family=self.tokens.fonts.family,
            size=size,
            weight=weight,
        )


theme_manager = ThemeManager()

