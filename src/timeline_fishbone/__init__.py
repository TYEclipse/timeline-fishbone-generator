#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Timeline Fishbone Generator.

A professional Python package for generating publication-ready LaTeX TikZ
timeline diagrams (fishbone style) from CSV/JSON data sources.

Features:
    - Smart layout algorithm to prevent node overlapping
    - Comprehensive configuration management (CLI, YAML, JSON)
    - CSV/JSON data input support
    - Automatic spacing adjustment based on node density
    - Multi-line text support with intelligent wrapping
    - Modular, extensible architecture

Example:
    Basic usage from command line::

        $ timeline-fishbone -i data.csv -o output.tex

    Programmatic usage::

        from timeline_fishbone import generate_timeline

        generate_timeline(
            input_file="data.csv",
            output_file="timeline.tex",
            smart_spacing=True
        )
"""

__version__ = "0.1.0"
__author__ = "Timeline Fishbone Contributors"
__license__ = "MIT"

from .core import (
    ArrowConfig,
    ColorConfig,
    DataValidator,
    LaTeXGenerator,
    LayoutConfig,
    OutputConfig,
    SmartLayoutEngine,
    TimelineFishboneConfig,
    TimeLogicConfig,
    ValidationError,
    VisualConfig,
    load_config,
    validate_file,
)
from .utils import create_sample_data, generate_timeline

__all__ = [
    "__version__",
    # High-level functions
    "generate_timeline",
    "create_sample_data",
    # Config
    "LayoutConfig",
    "TimeLogicConfig",
    "VisualConfig",
    "ColorConfig",
    "ArrowConfig",
    "OutputConfig",
    "TimelineFishboneConfig",
    "load_config",
    # Core classes
    "DataValidator",
    "ValidationError",
    "validate_file",
    "SmartLayoutEngine",
    "LaTeXGenerator",
]
