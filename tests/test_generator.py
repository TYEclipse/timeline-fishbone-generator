#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for LaTeX generator module."""

import pandas as pd
import pytest

from timeline_fishbone.core.config import (
    ArrowConfig,
    ColorConfig,
    LayoutConfig,
    OutputConfig,
    TimeLogicConfig,
    VisualConfig,
)
from timeline_fishbone.core.latex_generator import LaTeXGenerator


class TestLaTeXGenerator:
    """Test LaTeXGenerator class."""

    @pytest.fixture
    def sample_data(self):
        """Create sample DataFrame for testing."""
        return pd.DataFrame(
            {
                "年份": [2020, 2021, 2022],
                "种类": ["singleproto", "multiproto", "adaptive"],
                "方法名": ["Method1", "Method2", "Method3"],
                "引用标识": ["Ref1", "Ref2", "Ref3"],
            }
        )

    @pytest.fixture
    def generator(self):
        """Create LaTeX generator instance."""
        return LaTeXGenerator(
            LayoutConfig(),
            TimeLogicConfig(),
            VisualConfig(),
            ColorConfig(),
            ArrowConfig(),
            OutputConfig(),
        )

    def test_initialization(self, generator):
        """Test generator initialization."""
        assert isinstance(generator.layout, LayoutConfig)
        assert isinstance(generator.visual, VisualConfig)
        assert generator.layout_engine is not None

    def test_format_method_text_single_line(self):
        """Test method text formatting for single line."""
        visual = VisualConfig(max_lines=1)
        generator = LaTeXGenerator(
            LayoutConfig(),
            TimeLogicConfig(),
            visual,
            ColorConfig(),
            ArrowConfig(),
            OutputConfig(),
        )

        text = generator._format_method_text("MyMethod", "MyRef")
        assert "MyMethod~" in text
        assert "\\cite{MyRef}" in text

    def test_format_method_text_double_line(self):
        """Test method text formatting for double line."""
        visual = VisualConfig(max_lines=2)
        generator = LaTeXGenerator(
            LayoutConfig(),
            TimeLogicConfig(),
            visual,
            ColorConfig(),
            ArrowConfig(),
            OutputConfig(),
        )

        text = generator._format_method_text("MyMethod", "MyRef")
        assert "MyMethod\\\\" in text
        assert "\\cite{MyRef}" in text

    def test_generate_preamble(self, generator):
        """Test preamble generation."""
        preamble = generator._generate_preamble()
        assert "\\begin{figure}" in preamble
        assert "\\begin{tikzpicture}" in preamble
        assert "pgfdeclarelayer" in preamble

    def test_generate_styles(self, generator, sample_data):
        """Test style definitions generation."""
        categories = sample_data["种类"].unique().tolist()
        styles = generator._generate_styles(categories)
        assert "singleproto/.style" in styles
        assert "multiproto/.style" in styles
        assert "year/.style" in styles

    def test_generate_timeline_axis(self, generator, sample_data):
        """Test timeline axis generation."""
        layout_params = generator.layout_engine.calculate_layout(sample_data)
        axis = generator._generate_timeline_axis(layout_params)

        assert "\\draw[axis]" in axis
        assert "\\coordinate (Y2020)" in axis
        assert "\\coordinate (Y2021)" in axis
        assert "\\coordinate (Y2022)" in axis

    def test_generate_method_nodes(self, generator, sample_data):
        """Test method nodes generation."""
        layout_params = generator.layout_engine.calculate_layout(sample_data)
        nodes = generator._generate_method_nodes(sample_data, layout_params)

        assert "Method1" in nodes
        assert "Method2" in nodes
        assert "Method3" in nodes

    def test_generate_background_layer(self, generator, sample_data):
        """Test background layer generation."""
        bg_layer = generator._generate_background_layer(sample_data)

        assert "pgfonlayer" in bg_layer
        assert "background" in bg_layer
        assert "spine" in bg_layer
        assert "conn" in bg_layer

    def test_generate_year_nodes(self, generator, sample_data):
        """Test year nodes generation."""
        year_nodes = generator._generate_year_nodes(sample_data)

        assert "\\node[year]" in year_nodes
        assert "2020" in year_nodes or "\\year" in year_nodes

    def test_generate_caption(self, generator, sample_data):
        """Test caption generation."""
        categories = sample_data["种类"].unique().tolist()
        # First need to set category_colors for caption generation
        generator.category_colors = generator.colors.get_category_colors(
            categories
        )
        caption = generator._generate_caption(categories)

        assert "\\caption" in caption
        assert "\\label" in caption
        assert "\\end{figure}" in caption

    def test_generate_complete(self, generator, sample_data):
        """Test complete LaTeX generation."""
        latex_code = generator.generate(sample_data)

        assert "\\begin{figure}" in latex_code
        assert "\\begin{tikzpicture}" in latex_code
        assert "\\end{tikzpicture}" in latex_code
        assert "\\end{figure}" in latex_code
        assert len(latex_code) > 100

    def test_generate_with_legend(self, sample_data):
        """Test generation with legend."""
        output = OutputConfig(show_legend=True)
        generator = LaTeXGenerator(
            LayoutConfig(),
            TimeLogicConfig(),
            VisualConfig(),
            ColorConfig(),
            ArrowConfig(),
            output,
        )

        latex_code = generator.generate(sample_data)
        assert "颜色标识" in latex_code or "\\tikz" in latex_code

    def test_generate_without_legend(self, sample_data):
        """Test generation without legend."""
        output = OutputConfig(show_legend=False)
        generator = LaTeXGenerator(
            LayoutConfig(),
            TimeLogicConfig(),
            VisualConfig(),
            ColorConfig(),
            ArrowConfig(),
            output,
        )

        latex_code = generator.generate(sample_data)
        assert "\\caption{" in latex_code
