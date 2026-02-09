#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integration tests for the complete workflow."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from timeline_fishbone import create_sample_data, generate_timeline
from timeline_fishbone.core import TimelineFishboneConfig


class TestIntegration:
    """Integration tests for complete workflow."""

    @pytest.fixture
    def sample_csv_file(self):
        """Create temporary CSV file with sample data."""
        df = pd.DataFrame(
            {
                "年份": [2020, 2021, 2022],
                "种类": ["singleproto", "multiproto", "adaptive"],
                "方法名": ["Method1", "Method2", "Method3"],
                "引用标识": ["Ref1", "Ref2", "Ref3"],
            }
        )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as f:
            df.to_csv(f, index=False)
            temp_file = f.name

        yield temp_file
        Path(temp_file).unlink(missing_ok=True)

    def test_end_to_end_generation(self, sample_csv_file):
        """Test complete end-to-end generation."""
        output_file = tempfile.mktemp(suffix=".tex")

        try:
            latex_code = generate_timeline(sample_csv_file, output_file)

            assert latex_code is not None
            assert len(latex_code) > 100
            assert Path(output_file).exists()

            # Verify file content
            content = Path(output_file).read_text(encoding="utf-8")
            assert content == latex_code
            assert "\\begin{figure}" in content

        finally:
            Path(output_file).unlink(missing_ok=True)

    def test_generation_with_config(self, sample_csv_file):
        """Test generation with custom configuration."""
        output_file = tempfile.mktemp(suffix=".tex")

        try:
            latex_code = generate_timeline(
                sample_csv_file,
                output_file,
                layout__smart_spacing=True,
                visual__max_lines=2,
            )

            assert latex_code is not None
            assert Path(output_file).exists()

        finally:
            Path(output_file).unlink(missing_ok=True)

    def test_generation_without_output_file(self, sample_csv_file):
        """Test generation returning code without saving."""
        latex_code = generate_timeline(sample_csv_file)

        assert latex_code is not None
        assert isinstance(latex_code, str)
        assert "\\begin{figure}" in latex_code

    def test_create_sample_data_function(self):
        """Test sample data creation function."""
        output_file = tempfile.mktemp(suffix=".csv")

        try:
            create_sample_data(output_file)

            assert Path(output_file).exists()

            # Verify it's valid data
            latex_code = generate_timeline(output_file)
            assert latex_code is not None

        finally:
            Path(output_file).unlink(missing_ok=True)

    def test_json_config_integration(self, sample_csv_file):
        """Test integration with JSON config file."""
        config = TimelineFishboneConfig()
        config.layout.smart_spacing = True
        config.visual.max_lines = 2

        config_file = tempfile.mktemp(suffix=".json")
        output_file = tempfile.mktemp(suffix=".tex")

        try:
            config.save_json(config_file)

            latex_code = generate_timeline(
                sample_csv_file, output_file, config_file
            )

            assert latex_code is not None
            assert Path(output_file).exists()

        finally:
            Path(config_file).unlink(missing_ok=True)
            Path(output_file).unlink(missing_ok=True)


class TestErrorHandling:
    """Test error handling in integration scenarios."""

    def test_invalid_input_file(self):
        """Test error handling for non-existent input file."""
        with pytest.raises(FileNotFoundError):
            generate_timeline("nonexistent_file.csv")

    def test_invalid_data(self):
        """Test error handling for invalid data."""
        invalid_csv = tempfile.mktemp(suffix=".csv")

        try:
            # Create invalid CSV (missing required columns)
            df = pd.DataFrame({"wrong_column": [1, 2, 3]})
            df.to_csv(invalid_csv, index=False)

            with pytest.raises(Exception):  # Should raise ValidationError
                generate_timeline(invalid_csv)

        finally:
            Path(invalid_csv).unlink(missing_ok=True)
