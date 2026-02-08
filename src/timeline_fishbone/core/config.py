#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration module for Timeline Fishbone Generator.

Provides comprehensive configuration management with support for YAML/JSON
files, command-line arguments, and programmatic configuration.
"""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Union

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass
class LayoutConfig:
    """Layout parameter configuration."""

    timeline_width: str = "16cm"
    year_spacing: float = 2.7  # cm
    branch_distance: float = 1.2  # cm
    spine_length: float = 0.4  # cm
    smart_spacing: bool = False
    min_year_spacing: float = 2.0  # minimum spacing for smart adjustment

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayoutConfig":
        """Create from dictionary."""
        return cls(
            **{k: v for k, v in data.items() if k in cls.__annotations__}
        )


@dataclass
class TimeLogicConfig:
    """Time logic parameter configuration."""

    time_direction: str = "right"  # 'right' or 'left'
    start_year: int = 2019
    end_year: int = 2025
    upper_years: str = "order"  # 'order', 'odd', 'even', or
    # comma-separated list
    lower_years: str = "even"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimeLogicConfig":
        """Create from dictionary."""
        return cls(
            **{k: v for k, v in data.items() if k in cls.__annotations__}
        )


@dataclass
class VisualConfig:
    """Visual style parameter configuration."""

    node_width: str = "2.6cm"
    node_height: str = "0.5cm"
    node_font: str = r"\tiny\bfseries"
    ref_font: str = r"\tiny"
    inner_sep: str = "1.5pt"
    line_width: str = "0.8pt"
    rounded_corners: str = "3pt"
    max_lines: int = 1  # 1 for single line, 2 for double line

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VisualConfig":
        """Create from dictionary."""
        return cls(
            **{k: v for k, v in data.items() if k in cls.__annotations__}
        )


@dataclass
class ColorConfig:
    """Color scheme configuration."""

    # Legacy color fields for backward compatibility
    color_single: str = "cyan!20"
    color_multi: str = "green!20"
    color_adaptive: str = "yellow!40"
    color_vl: str = "purple!20"
    color_dense: str = "orange!30"
    color_attention: str = "red!20"
    color_hybrid: str = "gray!30"
    axis_color: str = "black!70"
    conn_color: str = "gray!60"

    # Default color palette for dynamic category assignment
    DEFAULT_COLORS = [
        "cyan!20",
        "green!20",
        "yellow!40",
        "purple!20",
        "orange!30",
        "red!20",
        "blue!20",
        "pink!20",
        "teal!20",
        "lime!30",
        "magenta!20",
        "brown!20",
        "violet!20",
        "olive!30",
        "navy!20",
        "maroon!20",
        "gray!30",
        "indigo!20",
        "gold!30",
        "coral!20",
    ]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ColorConfig":
        """Create from dictionary."""
        return cls(
            **{k: v for k, v in data.items() if k in cls.__annotations__}
        )

    def get_category_colors(self, categories: list) -> Dict[str, str]:
        """
        Generate color mapping for given categories.

        Args:
            categories: List of category names

        Returns:
            Dictionary mapping category names to colors
        """
        # Legacy mapping for backward compatibility
        legacy_mapping = {
            "singleproto": self.color_single,
            "multiproto": self.color_multi,
            "adaptive": self.color_adaptive,
            "vl": self.color_vl,
            "dense": self.color_dense,
            "attention": self.color_attention,
            "hybrid": self.color_hybrid,
        }

        color_map = {}
        for i, category in enumerate(sorted(categories)):
            # Use legacy color if available
            if category in legacy_mapping:
                color_map[category] = legacy_mapping[category]
            else:
                # Assign color from palette, cycling if necessary
                default_len = len(self.DEFAULT_COLORS)
                color_map[category] = self.DEFAULT_COLORS[i % default_len]

        return color_map


@dataclass
class ArrowConfig:
    """Arrow and connection parameter configuration."""

    arrow_style: str = r"-{Stealth[length=3mm, width=2mm]}"
    arrow_color: str = "gray!70"
    arrow_shorten: str = "0.38cm"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArrowConfig":
        """Create from dictionary."""
        return cls(
            **{k: v for k, v in data.items() if k in cls.__annotations__}
        )


@dataclass
class OutputConfig:
    """Output configuration."""

    input_file: str = ""
    output_file: str = "timeline.tex"
    show_legend: bool = True
    caption: str = "时间线鱼骨图"
    label: str = "fig:timeline"
    adjustbox_width: str = r"0.8\textwidth"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OutputConfig":
        """Create from dictionary."""
        return cls(
            **{k: v for k, v in data.items() if k in cls.__annotations__}
        )


@dataclass
class TimelineFishboneConfig:
    """Main configuration class combining all sub-configurations."""

    layout: LayoutConfig = field(default_factory=LayoutConfig)
    time_logic: TimeLogicConfig = field(default_factory=TimeLogicConfig)
    visual: VisualConfig = field(default_factory=VisualConfig)
    colors: ColorConfig = field(default_factory=ColorConfig)
    arrows: ArrowConfig = field(default_factory=ArrowConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to nested dictionary."""
        return {
            "layout": self.layout.to_dict(),
            "time_logic": self.time_logic.to_dict(),
            "visual": self.visual.to_dict(),
            "colors": self.colors.to_dict(),
            "arrows": self.arrows.to_dict(),
            "output": self.output.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimelineFishboneConfig":
        """Create from nested dictionary."""
        return cls(
            layout=LayoutConfig.from_dict(data.get("layout", {})),
            time_logic=TimeLogicConfig.from_dict(data.get("time_logic", {})),
            visual=VisualConfig.from_dict(data.get("visual", {})),
            colors=ColorConfig.from_dict(data.get("colors", {})),
            arrows=ArrowConfig.from_dict(data.get("arrows", {})),
            output=OutputConfig.from_dict(data.get("output", {})),
        )

    @classmethod
    def from_yaml(
        cls, file_path: Union[str, Path]
    ) -> "TimelineFishboneConfig":
        """
        Load configuration from YAML file.

        Args:
            file_path: Path to YAML configuration file

        Returns:
            TimelineFishboneConfig instance

        Raises:
            ImportError: If PyYAML is not installed
            FileNotFoundError: If file doesn't exist
            yaml.YAMLError: If YAML is invalid
        """
        if not YAML_AVAILABLE:
            raise ImportError(
                "PyYAML is required to load YAML config files. "
                "Install with: pip install pyyaml"
            )

        path = Path(file_path)
        if not path.exists():
            msg = f"Configuration file not found: {file_path}"
            raise FileNotFoundError(msg)

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls.from_dict(data or {})

    @classmethod
    def from_json(
        cls, file_path: Union[str, Path]
    ) -> "TimelineFishboneConfig":
        """
        Load configuration from JSON file.

        Args:
            file_path: Path to JSON configuration file

        Returns:
            TimelineFishboneConfig instance

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If JSON is invalid
        """
        path = Path(file_path)
        if not path.exists():
            msg = f"Configuration file not found: {file_path}"
            raise FileNotFoundError(msg)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls.from_dict(data)

    def save_yaml(self, file_path: Union[str, Path]) -> None:
        """
        Save configuration to YAML file.

        Args:
            file_path: Output path for YAML file

        Raises:
            ImportError: If PyYAML is not installed
        """
        if not YAML_AVAILABLE:
            raise ImportError(
                "PyYAML is required to save YAML config files. "
                "Install with: pip install pyyaml"
            )

        with open(file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                self.to_dict(),
                f,
                default_flow_style=False,
                allow_unicode=True,
            )

    def save_json(self, file_path: Union[str, Path], indent: int = 2) -> None:
        """
        Save configuration to JSON file.

        Args:
            file_path: Output path for JSON file
            indent: JSON indentation level
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=indent, ensure_ascii=False)

    def merge(
        self, other: "TimelineFishboneConfig"
    ) -> "TimelineFishboneConfig":
        """
        Merge with another configuration (other takes precedence).

        Args:
            other: Configuration to merge with

        Returns:
            New merged configuration
        """
        merged_dict = self.to_dict()
        other_dict = other.to_dict()

        for section, values in other_dict.items():
            if section in merged_dict:
                merged_dict[section].update(values)

        return TimelineFishboneConfig.from_dict(merged_dict)


def load_config(
    config_file: Optional[Union[str, Path]] = None, **overrides: Any
) -> TimelineFishboneConfig:
    """
    Load configuration with optional overrides.

    Args:
        config_file: Optional path to YAML/JSON config file
        **overrides: Key-value pairs to override config values

    Returns:
        TimelineFishboneConfig instance

    Example:
        >>> config = load_config("config.yaml", layout__smart_spacing=True)
    """
    # Start with default config
    config = TimelineFishboneConfig()

    # Load from file if provided
    if config_file:
        path = Path(config_file)
        if path.suffix in [".yaml", ".yml"]:
            config = TimelineFishboneConfig.from_yaml(config_file)
        elif path.suffix == ".json":
            config = TimelineFishboneConfig.from_json(config_file)
        else:
            raise ValueError(f"Unsupported config file format: {path.suffix}")

    # Apply overrides using double underscore notation
    # e.g., layout__smart_spacing=True -> config.layout.smart_spacing = True
    for key, value in overrides.items():
        if "__" in key:
            section, param = key.split("__", 1)
            if hasattr(config, section):
                section_obj = getattr(config, section)
                if hasattr(section_obj, param):
                    setattr(section_obj, param, value)

    return config
