#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Timeline Fishbone Generator - Core module.

This module provides the core functionality for generating LaTeX TikZ
timeline fishbone diagrams from CSV/JSON data.
"""

from .config import (
    ArrowConfig,
    ColorConfig,
    LayoutConfig,
    OutputConfig,
    TimeLogicConfig,
    TimelineFishboneConfig,
    VisualConfig,
    load_config,
)
from .latex_generator import LaTeXGenerator
from .layout_engine import SmartLayoutEngine
from .validator import DataValidator, ValidationError, validate_file

__all__ = [
    # Config classes
    "LayoutConfig",
    "TimeLogicConfig",
    "VisualConfig",
    "ColorConfig",
    "ArrowConfig",
    "OutputConfig",
    "TimelineFishboneConfig",
    "load_config",
    # Validator
    "DataValidator",
    "ValidationError",
    "validate_file",
    # Layout engine
    "SmartLayoutEngine",
    # Generator
    "LaTeXGenerator",
]
