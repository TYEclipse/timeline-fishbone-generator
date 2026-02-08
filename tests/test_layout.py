#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for layout engine module."""

import pandas as pd
import pytest

from timeline_fishbone.core.config import LayoutConfig, TimeLogicConfig
from timeline_fishbone.core.layout_engine import SmartLayoutEngine


class TestSmartLayoutEngine:
    """Test SmartLayoutEngine class."""

    @pytest.fixture
    def sample_data(self):
        """Create sample DataFrame for testing."""
        return pd.DataFrame(
            {
                "年份": [2020, 2020, 2021, 2022, 2022, 2022],
                "种类": ["singleproto"] * 6,
                "方法名": ["M1", "M2", "M3", "M4", "M5", "M6"],
                "引用标识": ["R1", "R2", "R3", "R4", "R5", "R6"],
            }
        )

    def test_initialization(self):
        """Test engine initialization."""
        layout_config = LayoutConfig()
        time_config = TimeLogicConfig()
        engine = SmartLayoutEngine(layout_config, time_config)

        assert engine.config == layout_config
        assert engine.time_config == time_config

    def test_calculate_layout_basic(self, sample_data):
        """Test basic layout calculation."""
        layout_config = LayoutConfig()
        time_config = TimeLogicConfig()
        engine = SmartLayoutEngine(layout_config, time_config)

        layout_params = engine.calculate_layout(sample_data)

        assert "year_counts" in layout_params
        assert "max_nodes" in layout_params
        assert "years" in layout_params
        assert "positions" in layout_params
        assert layout_params["max_nodes"] == 3  # Year 2022 has 3 nodes

    def test_calculate_layout_smart_spacing(self, sample_data):
        """Test layout calculation with smart spacing."""
        layout_config = LayoutConfig(smart_spacing=True)
        time_config = TimeLogicConfig()
        engine = SmartLayoutEngine(layout_config, time_config)

        layout_params = engine.calculate_layout(sample_data)

        assert "adjusted_spacing" in layout_params
        assert "adjusted_branch" in layout_params
        assert layout_params["adjusted_spacing"] >= (
            layout_config.min_year_spacing
        )

    def test_get_year_position(self, sample_data):
        """Test getting year positions."""
        layout_config = LayoutConfig()
        time_config = TimeLogicConfig()
        engine = SmartLayoutEngine(layout_config, time_config)

        layout_params = engine.calculate_layout(sample_data)
        pos_2020 = engine.get_year_position(2020, layout_params)
        pos_2021 = engine.get_year_position(2021, layout_params)

        assert pos_2020 == 0.0
        assert pos_2021 > pos_2020

    def test_determine_side_odd(self):
        """Test side determination with odd rule."""
        layout_config = LayoutConfig()
        time_config = TimeLogicConfig(upper_years="odd")
        engine = SmartLayoutEngine(layout_config, time_config)

        assert engine.determine_side(2021) == "above"  # Odd
        assert engine.determine_side(2020) == "below"  # Even

    def test_determine_side_even(self):
        """Test side determination with even rule."""
        layout_config = LayoutConfig()
        time_config = TimeLogicConfig(upper_years="even")
        engine = SmartLayoutEngine(layout_config, time_config)

        assert engine.determine_side(2020) == "above"  # Even
        assert engine.determine_side(2021) == "below"  # Odd

    def test_determine_side_custom_list(self):
        """Test side determination with custom year list."""
        layout_config = LayoutConfig()
        time_config = TimeLogicConfig(upper_years="2020,2022")
        engine = SmartLayoutEngine(layout_config, time_config)

        assert engine.determine_side(2020) == "above"
        assert engine.determine_side(2021) == "below"
        assert engine.determine_side(2022) == "above"

    def test_get_node_distribution(self, sample_data):
        """Test node distribution calculation."""
        layout_config = LayoutConfig()
        time_config = TimeLogicConfig(upper_years="odd")
        engine = SmartLayoutEngine(layout_config, time_config)

        distribution = engine.get_node_distribution(sample_data)

        assert 2020 in distribution
        assert 2021 in distribution
        assert 2022 in distribution
        assert distribution[2022]["total"] == 3
