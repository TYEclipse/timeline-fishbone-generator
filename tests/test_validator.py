#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for validator module."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from timeline_fishbone.core.validator import (
    DataValidator,
    ValidationError,
    validate_file,
)


class TestDataValidator:
    """Test DataValidator class."""
    
    def test_valid_dataframe(self):
        """Test validation of valid DataFrame."""
        df = pd.DataFrame({
            '年份': [2020, 2021, 2022],
            '种类': ['singleproto', 'multiproto', 'adaptive'],
            '方法名': ['Method1', 'Method2', 'Method3'],
            '引用标识': ['Ref1', 'Ref2', 'Ref3']
        })
        
        # Should not raise
        DataValidator.validate_dataframe(df)
    
    def test_missing_columns(self):
        """Test validation with missing columns."""
        df = pd.DataFrame({
            '年份': [2020, 2021],
            '种类': ['singleproto', 'multiproto']
        })
        
        with pytest.raises(ValidationError, match="缺少必需的列"):
            DataValidator.validate_dataframe(df)
    
    def test_null_values(self):
        """Test validation with null values."""
        df = pd.DataFrame({
            '年份': [2020, None, 2022],
            '种类': ['singleproto', 'multiproto', 'adaptive'],
            '方法名': ['Method1', 'Method2', 'Method3'],
            '引用标识': ['Ref1', 'Ref2', 'Ref3']
        })
        
        with pytest.raises(ValidationError, match="存在空值"):
            DataValidator.validate_dataframe(df)
    
    def test_invalid_categories(self):
        """Test validation with invalid categories."""
        df = pd.DataFrame({
            '年份': [2020, 2021, 2022],
            '种类': ['singleproto', 'invalid_type', 'adaptive'],
            '方法名': ['Method1', 'Method2', 'Method3'],
            '引用标识': ['Ref1', 'Ref2', 'Ref3']
        })
        
        with pytest.raises(ValidationError, match="无效的种类"):
            DataValidator.validate_dataframe(df)
    
    def test_invalid_years(self):
        """Test validation with invalid year values."""
        df = pd.DataFrame({
            '年份': [2020, 'invalid', 2022],
            '种类': ['singleproto', 'multiproto', 'adaptive'],
            '方法名': ['Method1', 'Method2', 'Method3'],
            '引用标识': ['Ref1', 'Ref2', 'Ref3']
        })
        
        with pytest.raises(ValidationError, match="年份"):
            DataValidator.validate_dataframe(df)
    
    def test_empty_dataframe(self):
        """Test validation of empty DataFrame."""
        df = pd.DataFrame()
        
        with pytest.raises(ValidationError, match="为空"):
            DataValidator.validate_dataframe(df)
    
    def test_load_csv(self):
        """Test loading and validating CSV file."""
        df = pd.DataFrame({
            '年份': [2020, 2021, 2022],
            '种类': ['singleproto', 'multiproto', 'adaptive'],
            '方法名': ['Method1', 'Method2', 'Method3'],
            '引用标识': ['Ref1', 'Ref2', 'Ref3']
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f, index=False)
            temp_file = f.name
        
        try:
            loaded_df = DataValidator.load_and_validate(temp_file)
            assert len(loaded_df) == 3
            assert loaded_df['年份'].dtype == int
        finally:
            Path(temp_file).unlink(missing_ok=True)
    
    def test_file_not_found(self):
        """Test error when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            DataValidator.load_and_validate("nonexistent_file.csv")
    
    def test_unsupported_format(self):
        """Test error with unsupported file format."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            with pytest.raises(ValidationError, match="不支持的文件格式"):
                DataValidator.load_and_validate(temp_file)
        finally:
            Path(temp_file).unlink(missing_ok=True)


class TestValidateFile:
    """Test validate_file function."""
    
    def test_valid_file(self):
        """Test validation of valid file."""
        df = pd.DataFrame({
            '年份': [2020, 2021],
            '种类': ['singleproto', 'multiproto'],
            '方法名': ['Method1', 'Method2'],
            '引用标识': ['Ref1', 'Ref2']
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f, index=False)
            temp_file = f.name
        
        try:
            is_valid, error = validate_file(temp_file)
            assert is_valid is True
            assert error is None
        finally:
            Path(temp_file).unlink(missing_ok=True)
    
    def test_invalid_file(self):
        """Test validation of invalid file."""
        is_valid, error = validate_file("nonexistent.csv")
        assert is_valid is False
        assert error is not None
