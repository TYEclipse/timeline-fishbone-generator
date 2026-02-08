#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart layout engine for Timeline Fishbone Generator.

Calculates optimal node positions and spacing to prevent overlaps.
"""

import logging
from typing import Any, Dict, List

import pandas as pd

from .config import LayoutConfig, TimeLogicConfig

logger = logging.getLogger(__name__)


class SmartLayoutEngine:
    """
    Intelligent layout engine for timeline diagrams.

    Automatically calculates optimal spacing and positioning to prevent
    node overlapping while maintaining visual consistency.
    """

    def __init__(
        self, layout_config: LayoutConfig, time_config: TimeLogicConfig
    ):
        """
        Initialize layout engine.

        Args:
            layout_config: Layout configuration
            time_config: Time logic configuration
        """
        self.config = layout_config
        self.time_config = time_config
        self._year_order: List[int] = []
        logger.debug("SmartLayoutEngine initialized")

    def calculate_layout(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate intelligent layout parameters.

        Args:
            df: Input DataFrame with timeline data

        Returns:
            Dictionary containing layout parameters including:
                - year_counts: Number of nodes per year
                - max_nodes: Maximum nodes in any year
                - years: Sorted list of years
                - positions: X-coordinate for each year
                - adjusted_spacing: Optimized year spacing
                - adjusted_branch: Optimized branch distance
                - total_width: Total diagram width
        """
        # Count nodes per year
        year_counts = df.groupby("年份").size().to_dict()
        max_nodes = max(year_counts.values()) if year_counts else 1
        years = sorted(df["年份"].unique())
        self._year_order = years

        logger.info(f"处理 {len(years)} 个年份，最多 {max_nodes} 个节点/年")

        layout_params = {
            "year_counts": year_counts,
            "max_nodes": max_nodes,
            "years": years,
            "positions": {},
        }

        # Smart spacing adjustment
        if self.config.smart_spacing:
            logger.debug("启用智能间距调整")

            # Adjust year spacing based on max nodes
            # More nodes = more horizontal space needed
            base_spacing = self.config.year_spacing
            req_width = max_nodes * 2.5  # ~2.5cm per node horizontally

            adjusted_spacing = max(
                self.config.min_year_spacing, min(req_width, base_spacing)
            )

            # Adjust branch distance for vertical stacking
            base_branch = self.config.branch_distance
            adjusted_branch = max(base_branch, max_nodes * 0.6)

            layout_params["adjusted_spacing"] = adjusted_spacing
            layout_params["adjusted_branch"] = adjusted_branch

            logger.debug(
                f"调整后间距: "
                f"spacing={adjusted_spacing:.2f}cm, "
                f"branch={adjusted_branch:.2f}cm"
            )
        else:
            layout_params["adjusted_spacing"] = self.config.year_spacing
            layout_params["adjusted_branch"] = self.config.branch_distance

        # Calculate year positions
        start = 0
        for i, year in enumerate(years):
            year_pos = start + i * layout_params["adjusted_spacing"]
            layout_params["positions"][year] = year_pos

        if len(years) > 1:
            total_w = (len(years) - 1) * layout_params["adjusted_spacing"]
        else:
            total_w = 0
        layout_params["total_width"] = total_w

        info_msg = f"布局计算完成: 总宽度 {layout_params['total_width']:.2f}cm"
        logger.info(info_msg)

        return layout_params

    def get_year_position(
        self, year: int, layout_params: Dict[str, Any]
    ) -> float:
        """
        Get X-coordinate for a specific year.

        Args:
            year: Year value
            layout_params: Layout parameters from calculate_layout()

        Returns:
            X-coordinate in cm
        """
        return float(layout_params["positions"].get(year, 0.0))

    def determine_side(self, year: int) -> str:
        """
        Determine which side (above/below) a year should be placed on.

        Args:
            year: Year value

        Returns:
            'above' or 'below'
        """
        upper_rule = (self.time_config.upper_years or "").lower()
        year_order = self._year_order or [year]

        if upper_rule in {"order", "sequence", "index"}:
            try:
                index = year_order.index(year)
            except ValueError:
                index = 0
            return "above" if index % 2 == 0 else "below"

        if upper_rule == "odd":

            def upper_years_fn(y: int) -> bool:
                return y % 2 == 1

        elif upper_rule == "even":

            def upper_years_fn(y: int) -> bool:
                return y % 2 == 0

        else:
            # Parse comma-separated year list
            try:
                year_strs = upper_rule.split(",")
                upper_list = [int(y.strip()) for y in year_strs if y.strip()]

                def upper_years_fn(y: int) -> bool:
                    return y in upper_list

            except (ValueError, AttributeError):
                warn_msg = (
                    f"无效的 upper_years 规则: {upper_rule}，"
                    "使用默认值 'order'"
                )
                logger.warning(warn_msg)
                try:
                    index = year_order.index(year)
                except ValueError:
                    index = 0
                return "above" if index % 2 == 0 else "below"

        return "above" if upper_years_fn(year) else "below"

    def get_node_distribution(
        self, df: pd.DataFrame
    ) -> Dict[int, Dict[str, int]]:
        """
        Get distribution of nodes by year and side.

        Args:
            df: Input DataFrame

        Returns:
            Dictionary mapping year to {'above': count, 'below': count}
        """
        distribution = {}
        years = sorted(df["年份"].unique())
        if not self._year_order:
            self._year_order = years

        for year in years:
            side = self.determine_side(year)
            year_data = df[df["年份"] == year]
            count = len(year_data)

            distribution[year] = {
                "above": count if side == "above" else 0,
                "below": count if side == "below" else 0,
                "total": count,
            }

        return distribution
