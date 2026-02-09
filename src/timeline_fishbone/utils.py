#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for Timeline Fishbone Generator.

Provides high-level convenience functions and helpers.
"""

import logging
from pathlib import Path
from typing import Any, Optional, Union

import pandas as pd

from .core import DataValidator, LaTeXGenerator, load_config

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """
    Set up logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def generate_timeline(
    input_file: Union[str, Path],
    output_file: Optional[Union[str, Path]] = None,
    config_file: Optional[Union[str, Path]] = None,
    **kwargs: Any,
) -> str:
    """
    High-level function to generate timeline from data file.

    Args:
        input_file: Path to CSV or JSON data file
        output_file: Optional output path for LaTeX file
        config_file: Optional YAML/JSON configuration file
        **kwargs: Additional configuration overrides

    Returns:
        Generated LaTeX code

    Raises:
        ValidationError: If input data is invalid
        FileNotFoundError: If input file doesn't exist

    Example:
        >>> latex_code = generate_timeline(
        ...     "data.csv",
        ...     "output.tex",
        ...     smart_spacing=True
        ... )
    """
    logger.info(
        f"生成时间线图: {input_file} -> {output_file or '(返回字符串)'}"
    )

    # Load configuration
    config = load_config(config_file, **kwargs)
    config.output.input_file = str(input_file)
    if output_file:
        config.output.output_file = str(output_file)

    # Load and validate data
    df = DataValidator.load_and_validate(input_file)

    # Generate LaTeX
    generator = LaTeXGenerator(
        config.layout,
        config.time_logic,
        config.visual,
        config.colors,
        config.arrows,
        config.output,
    )
    latex_code = generator.generate(df)

    # Write to file if specified
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(latex_code, encoding="utf-8")
        code_len = len(latex_code)
        logger.info(f"LaTeX 文件已保存: {output_file} ({code_len} 字符)")

    return latex_code


def create_sample_data(
    output_file: Union[str, Path] = "sample_data.csv",
) -> None:
    """
    Create sample CSV data file for demonstration.

    Args:
        output_file: Output path for sample CSV file

    Example:
        >>> create_sample_data("example.csv")
    """
    data = {
        "年份": [
            2019,
            2020,
            2021,
            2021,
            2021,
            2022,
            2022,
            2022,
            2023,
            2023,
            2023,
            2024,
            2024,
            2024,
            2024,
            2024,
            2025,
            2025,
        ],
        "种类": [
            "singleproto",
            "multiproto",
            "multiproto",
            "dense",
            "attention",
            "singleproto",
            "singleproto",
            "adaptive",
            "adaptive",
            "attention",
            "hybrid",
            "vl",
            "vl",
            "vl",
            "adaptive",
            "hybrid",
            "multiproto",
            "multiproto",
        ],
        "方法名": [
            "PANet",
            "PPNet",
            "ASGNet",
            "HSNet",
            "CWT",
            "PFENet",
            "BAM",
            "DPCN",
            "Self-reg",
            "HDMNet",
            "SCCAN",
            "Proto-CLIP",
            "TransBA",
            "Zhu et al.",
            "AdaptiveSS",
            "DAM",
            "HMPD",
            "ProtoPT",
        ],
        "引用标识": [
            "Wang2019PANet",
            "Liu2020PPNet",
            "Li2021ASGNet",
            "Min2021HSNet",
            "Lu2021CWT",
            "Tian2022PFENet",
            "Lang2022BAM",
            "Liu2022DynamicPC",
            "Ding2023Selfregularized",
            "Peng2023HDMNet",
            "Xu2023SCCAN",
            "P2024ProtoCLIP",
            "Chen2024TransformerBA",
            "Zhu2024Unleashing",
            "Shen2024AdaptiveSS",
            "Chen2024DAM",
            "Xu2025HMPD",
            "Yu2025PrototypicalPT",
        ],
    }

    df = pd.DataFrame(data)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")

    logger.info(f"示例数据文件已创建: {output_file}")
    print(f"[OK] 示例数据文件已创建: {output_file}")
    print(f"  包含 {len(df)} 条记录，{df['年份'].nunique()} 个年份")


def validate_data_file(file_path: Union[str, Path]) -> bool:
    """
    Validate a data file and print results.

    Args:
        file_path: Path to file to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        df = DataValidator.load_and_validate(file_path)
        print(f"[OK] 数据验证通过: {file_path}")
        print(f"  记录数: {len(df)}")
        print(f"  年份范围: {df['年份'].min()} - {df['年份'].max()}")
        print(f"  种类分布: {dict(df['种类'].value_counts())}")
        return True
    except Exception as e:
        print(f"[ERROR] 数据验证失败: {file_path}")
        print(f"  错误: {e}")
        return False
