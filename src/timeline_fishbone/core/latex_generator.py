#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX code generator for Timeline Fishbone Generator.

Generates publication-ready TikZ code for timeline fishbone diagrams.
"""

import logging
from typing import Any, Dict

import pandas as pd

from .config import (
    ArrowConfig,
    ColorConfig,
    LayoutConfig,
    OutputConfig,
    TimeLogicConfig,
    VisualConfig,
)
from .layout_engine import SmartLayoutEngine

logger = logging.getLogger(__name__)


class LaTeXGenerator:
    """
    LaTeX TikZ code generator for timeline fishbone diagrams.

    Generates complete, publication-ready LaTeX code with proper styling,
    layout, and formatting.
    """

    def __init__(
        self,
        layout: LayoutConfig,
        time_logic: TimeLogicConfig,
        visual: VisualConfig,
        colors: ColorConfig,
        arrows: ArrowConfig,
        output: OutputConfig,
    ):
        """
        Initialize LaTeX generator.

        Args:
            layout: Layout configuration
            time_logic: Time logic configuration
            visual: Visual style configuration
            colors: Color scheme configuration
            arrows: Arrow configuration
            output: Output configuration
        """
        self.layout = layout
        self.time_logic = time_logic
        self.visual = visual
        self.colors = colors
        self.arrows = arrows
        self.output = output
        self.layout_engine = SmartLayoutEngine(layout, time_logic)
        # Will be populated when generating
        self.category_colors: Dict[str, str] = {}
        logger.debug("LaTeXGenerator initialized")

    def _generate_preamble(self) -> str:
        """Generate LaTeX preamble."""
        lines = [
            "% Required packages/settings (add these in LaTeX preamble):",
            r"% \usepackage{tikz}",
            r"% \usepackage{xcolor}",
            r"% \usepackage{adjustbox} % provide smart scaling",
            r"% \usepackage{geometry}",
            r"% \geometry{a4paper, left=2.5cm, right=2.5cm,",
            r"%   top=2.5cm, bottom=2.5cm}",
            r"% \usetikzlibrary{positioning, matrix, fit,",
            r"%   backgrounds, shapes, arrows.meta}",
            "",
            r"\begin{figure}[htbp]",
            r"\centering",
            (
                f"\\begin{{adjustbox}}{{center, "
                f"max width={self.output.adjustbox_width}, "
                f"max height=0.8\\textheight, keepaspectratio}}"
            ),
            r"\pgfdeclarelayer{background}",
            r"\pgfdeclarelayer{foreground}",
            r"\pgfsetlayers{background,main,foreground}",
            r"\begin{tikzpicture}[",
            "    scale=1.0,",
            "    transform shape,",
            r"    font=\footnotesize\sffamily,",
        ]
        return "\n".join(lines)

    def _generate_styles(self, categories: list) -> str:
        """
        Generate TikZ style definitions.

        Args:
            categories: List of categories from the data
        """
        styles = [
            "    % ========================================",
            "    % Category color definitions",
            "    % ========================================",
        ]

        # Get dynamic category colors
        self.category_colors = self.colors.get_category_colors(categories)

        # Generate styles for each category
        for cat in sorted(categories):
            color = self.category_colors[cat]
            # Extract base color (before first '!') for border color
            base_color = color.split("!")[0] if "!" in color else color
            border_color = f"{base_color}!60!black"

            style_def = (
                f"    {cat}/.style={{\n"
                f"        fill={color}, draw={border_color}, "
                f"line width={self.visual.line_width},\n"
                f"        rounded corners={self.visual.rounded_corners}, "
                f"minimum width={self.visual.node_width}, "
                f"minimum height={self.visual.node_height},\n"
                f"        align=center, font={self.visual.node_font}, "
                f"text=black!80, inner sep={self.visual.inner_sep}\n"
                f"    }},"
            )
            styles.append(style_def)

        # Additional styles
        styles.extend(
            [
                "    year/.style={",
                "        circle, fill=white, draw=black,",
                "        line width=1.2pt,",
                (
                    r"        minimum size=0.75cm, "
                    r"font=\bfseries\footnotesize, inner sep=0pt"
                ),
                "    },",
                "    axis/.style={",
                f"        line width=1.5pt, draw={self.colors.axis_color}",
                "    },",
                "    arrow/.style={",
                f"        {self.arrows.arrow_style},",
                "        line width=0.8pt,",
                f"        draw={self.arrows.arrow_color},",
                f"        shorten >={self.arrows.arrow_shorten},",
                f"        shorten <={self.arrows.arrow_shorten}",
                "    },",
                "    spine/.style={",
                "        line width=0.8pt, draw=gray!50, -",
                "    },",
                "    conn/.style={",
                f"        line width=0.5pt, draw={self.colors.conn_color}",
                "    },",
                "    methodmatrix/.style={",
                "        matrix of nodes, row sep=4pt, column sep=3pt,",
                "        nodes in empty cells, inner sep=0pt",
                "    }",
                "]",
            ]
        )

        return "\n".join(styles)

    def _format_method_text(self, name: str, ref: str) -> str:
        """
        Format method text (single or double line).

        Args:
            name: Method name
            ref: Citation reference

        Returns:
            Formatted LaTeX text
        """
        ref_cmd = f"{{{self.visual.ref_font}\\cite{{{ref}}}}}"

        if self.visual.max_lines == 1:
            # Single line: use ~ separator
            return f"{name}~{ref_cmd}"
        else:
            # Double line: use line break
            return f"{name}\\\\[-2pt]{ref_cmd}"

    def _generate_timeline_axis(self, layout_params: Dict[str, Any]) -> str:
        """Generate timeline axis and year coordinates."""
        total_width = layout_params["total_width"]
        years = layout_params["years"]

        lines = [
            "    % ========================================",
            "    % 1. Draw timeline axis and define year coordinates",
            "    % ========================================",
            f"    \\draw[axis] (0,0) -- ({total_width},0);",
            "",
            "    % Define year positions",
        ]

        # Generate coordinate definitions
        for year in years:
            pos = layout_params["positions"][year]
            lines.append(f"    \\coordinate (Y{year}) at ({pos},0);")

        # Generate arrows between years
        if len(years) > 1:
            lines.extend(
                [
                    "",
                    "    % Draw arrows between year nodes",
                ]
            )

            arrow_pairs = [
                f"{years[i]}/{years[i+1]}" for i in range(len(years) - 1)
            ]
            lines.append(
                "    \\foreach \\year/\\nextyear in {"
                + ",".join(arrow_pairs)
                + "} {"
            )
            lines.append("        \\draw[arrow] (Y\\year) -- (Y\\nextyear);")
            lines.append("    }")

        return "\n".join(lines)

    def _generate_method_nodes(
        self, df: pd.DataFrame, layout_params: Dict[str, Any]
    ) -> str:
        """Generate method nodes."""
        lines = [
            "",
            "    % ========================================",
            "    % 2. Define all method nodes",
            "    % ========================================",
        ]

        year_groups = df.groupby("年份")

        for year in sorted(df["年份"].unique()):
            if year not in year_groups.groups:
                continue

            group = year_groups.get_group(year)
            side = self.layout_engine.determine_side(year)

            lines.append("")
            side_mark = "upper" if side == "above" else "lower"
            lines.append(f"    % --- {year} ({side_mark}) ---")

            if len(group) == 1:
                # Single node
                row = group.iloc[0]
                text = self._format_method_text(row["方法名"], row["引用标识"])
                style = row["种类"]
                anchor = "above" if side == "above" else "below"
                branch_dist = layout_params["adjusted_branch"]

                node_str = (
                    f"\\node[{style}, {anchor}={branch_dist}cm "
                    f"of Y{year}] (M{year}) {{{text}}};"
                )
                lines.append(f"    {node_str}")
            else:
                # Multiple nodes - use matrix
                anchor = "south" if side == "above" else "north"
                position = "above" if side == "above" else "below"
                branch_dist = layout_params["adjusted_branch"]
                matrix_pos = f"{position}={branch_dist}cm of Y{year}"

                matrix_str = (
                    f"\\matrix[methodmatrix, {matrix_pos}, "
                    f"anchor={anchor}] (M{year}) {{"
                )
                lines.append(f"    {matrix_str}")

                # Generate matrix rows
                for idx, (_, row) in enumerate(group.iterrows()):
                    text = self._format_method_text(
                        row["方法名"], row["引用标识"]
                    )
                    style = row["种类"]

                    # Multi-column layout for many nodes
                    multi_col = (
                        len(group) > 3
                        and idx % 2 == 0
                        and idx < len(group) - 1
                    )
                    if multi_col:
                        next_row = group.iloc[idx + 1]
                        next_text = self._format_method_text(
                            next_row["方法名"], next_row["引用标识"]
                        )
                        next_style = next_row["种类"]
                        node1 = f"        \\node[{style}] {{{text}}}; &"
                        node2 = (
                            f"        \\node[{next_style}] "
                            f"{{{next_text}}}; \\\\"
                        )
                        lines.append(node1)
                        lines.append(node2)
                    elif not (len(group) > 3 and idx % 2 == 1):
                        node = f"        \\node[{style}] {{{text}}}; \\\\"
                        lines.append(node)

                lines.append("    };")

        return "\n".join(lines)

    def _generate_background_layer(self, df: pd.DataFrame) -> str:
        """Generate background layer connections."""
        lines = [
            "",
            "    % ========================================",
            "    % 3. Draw all connections in background layer",
            "    % ========================================",
            r"    \begin{pgfonlayer}{background}",
            "        % Year node spines",
        ]

        years = sorted(df["年份"].unique())

        # Spines
        years_str = ",".join(map(str, years))
        lines.append(f"        \\foreach \\year in {{{years_str}}} {{")
        lines.append(
            f"            \\draw[spine] (Y\\year.north) -- "
            f"++(0,{self.layout.spine_length});"
        )
        lines.append(
            f"            \\draw[spine] (Y\\year.south) -- "
            f"++(0,-{self.layout.spine_length});"
        )
        lines.append("        }")
        lines.append("")
        lines.append("        % Connect methods to year nodes")

        # Connection lines
        for year in years:
            side = self.layout_engine.determine_side(year)
            spine_len = self.layout.spine_length
            if side == "above":
                conn_str = (
                    f"\\draw[conn] (M{year}.south) -- "
                    f"([yshift={spine_len}cm]Y{year});"
                )
                lines.append(f"        {conn_str}")
            else:
                conn_str = (
                    f"\\draw[conn] (M{year}.north) -- "
                    f"([yshift=-{spine_len}cm]Y{year});"
                )
                lines.append(f"        {conn_str}")

        lines.append(r"    \end{pgfonlayer}")

        return "\n".join(lines)

    def _generate_year_nodes(self, df: pd.DataFrame) -> str:
        """Generate year nodes (top layer)."""
        years = sorted(df["年份"].unique())

        years_str = ",".join(map(str, years))
        lines = [
            "",
            "    % ========================================",
            "    % 4. Draw year nodes on top layer",
            "    % ========================================",
            f"    \\foreach \\year in {{{years_str}}} {{",
            "        \\node[year] at (Y\\year) {\\year};",
            "    }",
        ]

        return "\n".join(lines)

    def _generate_bounding_box(self) -> str:
        """Generate bounding box extension."""
        return (
            "\n"
            "    % ========================================\n"
            "    % 5. Extend bounding box\n"
            "    % ========================================\n"
            r"    \path (current bounding box.south west) +(-0.3,-0.5) "
            "(current bounding box.north east) +(0.3,0.5);"
        )

    def _generate_caption(self, categories: list) -> str:
        """
        Generate legend and caption.

        Args:
            categories: List of categories from the data
        """
        lines = [
            r"\end{tikzpicture}",
            r"\end{adjustbox}",
            f"\\caption{{{self.output.caption}。",
        ]

        if self.output.show_legend:
            # Generate legend dynamically from categories
            legend_text = "颜色标识："

            for category in sorted(categories):
                fill_color = self.category_colors[category]
                # Extract base color for border
                base_col = fill_color.split("!")[0]
                base_col = base_col if "!" in fill_color else fill_color
                border_color = f"{base_col}!60!black"

                legend_part = (
                    r"{\protect\tikz[baseline=-0.5ex]"
                    r"\protect\node["
                    f"fill={fill_color},"
                    f"draw={border_color},"
                    f"rounded corners=2pt,"
                    f"inner sep=2pt,"
                    f"font=\\tiny"
                    f"] {{{category}}};}}"
                )
                legend_text += legend_part + " "

            lines.append(legend_text)

        lines.append("}}")
        lines.append(f"\\label{{{self.output.label}}}")
        lines.append(r"\end{figure}")

        return "\n".join(lines)

    def generate(self, df: pd.DataFrame) -> str:
        """
        Generate complete LaTeX code.

        Args:
            df: Input DataFrame with validated data

        Returns:
            Complete LaTeX code string
        """
        logger.info("开始生成 LaTeX 代码")

        # Extract unique categories from data
        categories = df["种类"].unique().tolist()
        cat_list = ", ".join(sorted(categories))
        logger.info(f"提取到 {len(categories)} 个种类: {cat_list}")

        # Calculate layout
        layout_params = self.layout_engine.calculate_layout(df)

        # Generate sections
        parts = [
            self._generate_preamble(),
            self._generate_styles(categories),
            self._generate_timeline_axis(layout_params),
            self._generate_method_nodes(df, layout_params),
            self._generate_background_layer(df),
            self._generate_year_nodes(df),
            self._generate_bounding_box(),
            self._generate_caption(categories),
        ]

        latex_code = "\n".join(parts)

        lines_count = len(latex_code.split(chr(10)))
        logger.info(
            f"LaTeX 代码生成完成: {len(latex_code)} 字符, {lines_count} 行"
        )

        return latex_code
