#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data validation module for Timeline Fishbone Generator.

Provides comprehensive validation for CSV/JSON input data files.
"""

import logging
from pathlib import Path
from typing import Optional, Set, Tuple, Union

import pandas as pd

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class DataValidator:
    """
    Data validator for timeline fishbone input data.
    
    Validates CSV/JSON files to ensure they contain all required columns
    with valid data types and values.
    """
    
    REQUIRED_COLUMNS = ['年份', '种类', '方法名', '引用标识']
    
    @classmethod
    def validate_columns(cls, df: pd.DataFrame) -> None:
        """
        Validate that all required columns exist.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            ValidationError: If required columns are missing
        """
        missing_cols = [col for col in cls.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValidationError(
                f"缺少必需的列: {', '.join(missing_cols)}。"
                f"必需列: {', '.join(cls.REQUIRED_COLUMNS)}"
            )
        logger.debug("列验证通过")
    
    @classmethod
    def validate_null_values(cls, df: pd.DataFrame) -> None:
        """
        Validate that required columns don't have null values.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            ValidationError: If null values are found
        """
        null_mask = df[cls.REQUIRED_COLUMNS].isnull().any(axis=1)
        if null_mask.any():
            null_rows = df[null_mask].index.tolist()
            raise ValidationError(
                f"以下行存在空值: {[r + 1 for r in null_rows]}。"  # +1 for 1-based indexing
                "所有必需列都必须有值。"
            )
        logger.debug("空值验证通过")
    
    @classmethod
    def validate_categories(cls, df: pd.DataFrame) -> None:
        """
        Validate that categories column exists and has values.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            ValidationError: If categories are invalid
        """
        # Extract unique categories
        categories = set(df['种类'].unique())
        if not categories:
            raise ValidationError("未找到任何种类")
        
        logger.info(f"检测到 {len(categories)} 个种类: {', '.join(sorted(categories))}")
        logger.debug("种类验证通过")
    
    @classmethod
    def validate_years(cls, df: pd.DataFrame) -> None:
        """
        Validate that years are integers.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            ValidationError: If year values are invalid
        """
        try:
            years = pd.to_numeric(df['年份'], errors='coerce')
            if years.isnull().any():
                invalid_rows = df[years.isnull()].index.tolist()
                raise ValidationError(
                    f"以下行包含无效的年份值: {[r + 1 for r in invalid_rows]}。"
                    "年份必须是整数。"
                )
            # Check for unreasonable years
            if (years < 1900).any() or (years > 2100).any():
                logger.warning("检测到异常年份值（<1900 或 >2100）")
        except (ValueError, TypeError) as e:
            raise ValidationError(f"年份验证失败: {e}")
        
        logger.debug("年份验证通过")
    
    @classmethod
    def validate_dataframe(cls, df: pd.DataFrame) -> None:
        """
        Perform comprehensive validation on DataFrame.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            ValidationError: If any validation check fails
        """
        if df.empty:
            raise ValidationError("数据文件为空")
        
        cls.validate_columns(df)
        cls.validate_null_values(df)
        cls.validate_categories(df)
        cls.validate_years(df)
        
        logger.info(f"数据验证成功: {len(df)} 条记录，{df['年份'].nunique()} 个年份")
    
    @classmethod
    def load_and_validate(cls, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load file and validate data.
        
        Args:
            file_path: Path to CSV or JSON file
            
        Returns:
            Validated DataFrame
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValidationError: If data is invalid
            ValueError: If file format is unsupported
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        logger.info(f"加载数据文件: {path}")
        
        try:
            if path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path, encoding='utf-8')
            elif path.suffix.lower() == '.json':
                df = pd.read_json(file_path, encoding='utf-8')
            else:
                raise ValueError(
                    f"不支持的文件格式: {path.suffix}。"
                    "请使用 .csv 或 .json 文件"
                )
        except pd.errors.EmptyDataError:
            raise ValidationError("数据文件为空")
        except pd.errors.ParserError as e:
            raise ValidationError(f"文件解析失败: {e}")
        except Exception as e:
            raise ValidationError(f"读取文件失败: {e}")
        
        # Validate the loaded data
        cls.validate_dataframe(df)
        
        # Convert year to int
        df['年份'] = df['年份'].astype(int)
        
        return df


def validate_file(file_path: Union[str, Path]) -> Tuple[bool, Optional[str]]:
    """
    Validate a data file and return status.
    
    Args:
        file_path: Path to file to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        
    Example:
        >>> is_valid, error = validate_file("data.csv")
        >>> if not is_valid:
        ...     print(f"Validation failed: {error}")
    """
    try:
        DataValidator.load_and_validate(file_path)
        return True, None
    except Exception as e:
        return False, str(e)
