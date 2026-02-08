#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for configuration module."""

import json
import tempfile
from pathlib import Path

import pytest

from timeline_fishbone.core.config import (
    ArrowConfig,
    ColorConfig,
    LayoutConfig,
    OutputConfig,
    TimelineFishboneConfig,
    TimeLogicConfig,
    VisualConfig,
    load_config,
)


class TestLayoutConfig:
    """Test LayoutConfig class."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = LayoutConfig()
        assert config.timeline_width == "16cm"
        assert config.year_spacing == 2.7
        assert config.smart_spacing is False
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = LayoutConfig(
            timeline_width="20cm",
            year_spacing=3.0,
            smart_spacing=True
        )
        assert config.timeline_width == "20cm"
        assert config.year_spacing == 3.0
        assert config.smart_spacing is True
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = LayoutConfig()
        data = config.to_dict()
        assert isinstance(data, dict)
        assert data['timeline_width'] == "16cm"
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {'timeline_width': '20cm', 'year_spacing': 3.0}
        config = LayoutConfig.from_dict(data)
        assert config.timeline_width == "20cm"
        assert config.year_spacing == 3.0


class TestTimelineFishboneConfig:
    """Test TimelineFishboneConfig class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = TimelineFishboneConfig()
        assert isinstance(config.layout, LayoutConfig)
        assert isinstance(config.time_logic, TimeLogicConfig)
        assert isinstance(config.visual, VisualConfig)
    
    def test_to_dict(self):
        """Test conversion to nested dictionary."""
        config = TimelineFishboneConfig()
        data = config.to_dict()
        assert 'layout' in data
        assert 'time_logic' in data
        assert 'visual' in data
    
    def test_from_dict(self):
        """Test creation from nested dictionary."""
        data = {
            'layout': {'timeline_width': '20cm'},
            'visual': {'max_lines': 2}
        }
        config = TimelineFishboneConfig.from_dict(data)
        assert config.layout.timeline_width == "20cm"
        assert config.visual.max_lines == 2
    
    def test_json_save_load(self):
        """Test JSON save and load."""
        config = TimelineFishboneConfig()
        config.layout.smart_spacing = True
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            config.save_json(temp_file)
            loaded = TimelineFishboneConfig.from_json(temp_file)
            assert loaded.layout.smart_spacing is True
        finally:
            Path(temp_file).unlink(missing_ok=True)
    
    def test_merge(self):
        """Test configuration merging."""
        config1 = TimelineFishboneConfig()
        config2 = TimelineFishboneConfig()
        config2.layout.smart_spacing = True
        config2.visual.max_lines = 2
        
        merged = config1.merge(config2)
        assert merged.layout.smart_spacing is True
        assert merged.visual.max_lines == 2


class TestLoadConfig:
    """Test load_config function."""
    
    def test_load_default(self):
        """Test loading default configuration."""
        config = load_config()
        assert isinstance(config, TimelineFishboneConfig)
    
    def test_load_with_overrides(self):
        """Test loading with overrides."""
        config = load_config(
            layout__smart_spacing=True,
            visual__max_lines=2
        )
        assert config.layout.smart_spacing is True
        assert config.visual.max_lines == 2
    
    def test_load_from_json(self):
        """Test loading from JSON file."""
        data = {
            'layout': {'smart_spacing': True},
            'visual': {'max_lines': 2}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_file = f.name
        
        try:
            config = load_config(temp_file)
            assert config.layout.smart_spacing is True
            assert config.visual.max_lines == 2
        finally:
            Path(temp_file).unlink(missing_ok=True)
