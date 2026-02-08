#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX Timeline Fishbone Generator
=================================

A professional Python script for generating publication-ready LaTeX TikZ 
timeline diagrams (fishbone style) from CSV data sources.

Features:
- Smart layout algorithm to prevent node overlapping
- Comprehensive argparse configuration
- CSV/JSON data input support
- Automatic spacing adjustment based on node density
- Multi-line text support with intelligent wrapping
- Modular code generation

Usage:
    python timeline_generator.py -i data.csv -o output.tex
    python timeline_generator.py -i data.csv --time-direction left --smart-spacing
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import pandas as pd
import json
from dataclasses import dataclass, field, asdict


@dataclass
class LayoutConfig:
    """布局参数配置类"""
    timeline_width: str = "16cm"
    year_spacing: float = 2.7  # cm
    branch_distance: float = 1.2  # cm
    spine_length: float = 0.4  # cm
    smart_spacing: bool = False
    min_year_spacing: float = 2.0  # 智能调整时的最小间距


@dataclass
class TimeLogicConfig:
    """时间逻辑参数配置类"""
    time_direction: str = "right"  # 'right' or 'left'
    start_year: int = 2019
    end_year: int = 2025
    upper_years: str = "odd"  # 'odd', 'even', or comma-separated list
    lower_years: str = "even"


@dataclass
class VisualConfig:
    """视觉样式参数配置类"""
    node_width: str = "2.6cm"
    node_height: str = "0.5cm"
    node_font: str = r"\tiny\bfseries"
    ref_font: str = r"\tiny"
    inner_sep: str = "1.5pt"
    line_width: str = "0.8pt"
    rounded_corners: str = "3pt"
    max_lines: int = 1  # 最大行数，1表示单行，2表示双行


@dataclass
class ColorConfig:
    """配色方案配置类"""
    color_single: str = "cyan!20"
    color_multi: str = "green!20"
    color_adaptive: str = "yellow!40"
    color_vl: str = "purple!20"
    color_dense: str = "orange!30"
    color_attention: str = "red!20"
    color_hybrid: str = "gray!30"
    axis_color: str = "black!70"
    conn_color: str = "gray!60"


@dataclass
class ArrowConfig:
    """箭头与连线参数配置类"""
    arrow_style: str = r"-{Stealth[length=3mm, width=2mm]}"
    arrow_color: str = "gray!70"
    arrow_shorten: str = "0.38cm"


@dataclass
class OutputConfig:
    """输出配置类"""
    input_file: str = ""
    output_file: str = "timeline.tex"
    show_legend: bool = True
    caption: str = "时间线鱼骨图"
    label: str = "fig:timeline"
    adjustbox_width: str = "0.8\\textwidth"


class DataValidator:
    """数据验证器"""
    
    REQUIRED_COLUMNS = ['年份', '种类', '方法名', '引用标识']
    VALID_CATEGORIES = ['singleproto', 'multiproto', 'adaptive', 'vl', 
                       'dense', 'attention', 'hybrid']
    
    @classmethod
    def validate_csv(cls, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        验证CSV数据是否有效
        
        Args:
            df: pandas DataFrame
            
        Returns:
            (is_valid, error_message)
        """
        # 检查必需列
        missing_cols = [col for col in cls.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            return False, f"缺少必需的列: {', '.join(missing_cols)}"
        
        # 检查空值
        if df[cls.REQUIRED_COLUMNS].isnull().any().any():
            null_rows = df[df[cls.REQUIRED_COLUMNS].isnull().any(axis=1)].index.tolist()
            return False, f"第 {null_rows} 行存在空值"
        
        # 检查种类有效性
        invalid_cats = set(df['种类'].unique()) - set(cls.VALID_CATEGORIES)
        if invalid_cats:
            return False, f"无效的种类: {', '.join(invalid_cats)}。有效值: {', '.join(cls.VALID_CATEGORIES)}"
        
        # 检查年份是否为整数
        try:
            df['年份'] = df['年份'].astype(int)
        except ValueError:
            return False, "年份列必须包含整数"
        
        return True, ""
    
    @classmethod
    def load_data(cls, file_path: str) -> Tuple[Optional[pd.DataFrame], str]:
        """
        加载并验证数据文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            (DataFrame, error_message)
        """
        path = Path(file_path)
        
        if not path.exists():
            return None, f"文件不存在: {file_path}"
        
        try:
            if path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path, encoding='utf-8')
            elif path.suffix.lower() == '.json':
                df = pd.read_json(file_file)
            else:
                return None, f"不支持的文件格式: {path.suffix}。请使用 CSV 或 JSON"
            
            is_valid, msg = cls.validate_csv(df)
            if not is_valid:
                return None, msg
            
            return df, ""
            
        except Exception as e:
            return None, f"读取文件失败: {str(e)}"


class SmartLayoutEngine:
    """智能布局引擎"""
    
    def __init__(self, config: LayoutConfig, time_config: TimeLogicConfig):
        self.config = config
        self.time_config = time_config
    
    def calculate_layout(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        计算智能布局参数
        
        Args:
            df: 数据框
            
        Returns:
            布局参数字典
        """
        # 按年份统计节点数量
        year_counts = df.groupby('年份').size().to_dict()
        max_nodes = max(year_counts.values()) if year_counts else 1
        
        layout_params = {
            'year_counts': year_counts,
            'max_nodes': max_nodes,
            'years': sorted(df['年份'].unique()),
            'positions': {}
        }
        
        # 智能间距调整
        if self.config.smart_spacing:
            # 根据最大节点数调整年份间距
            # 节点越多，需要的水平间距越大以避免重叠
            base_spacing = self.config.year_spacing
            required_width = max_nodes * 2.5  # 每个节点大约需要2.5cm的横向空间
            
            if required_width > base_spacing:
                layout_params['adjusted_spacing'] = required_width
            else:
                layout_params['adjusted_spacing'] = base_spacing
            
            # 调整分支距离以适应垂直堆叠
            base_branch = self.config.branch_distance
            layout_params['adjusted_branch'] = max(
                base_branch, 
                max_nodes * 0.6  # 每个节点0.6cm的垂直空间
            )
        else:
            layout_params['adjusted_spacing'] = self.config.year_spacing
            layout_params['adjusted_branch'] = self.config.branch_distance
        
        # 计算年份位置
        start = 0
        for i, year in enumerate(sorted(df['年份'].unique())):
            layout_params['positions'][year] = start + i * layout_params['adjusted_spacing']
        
        layout_params['total_width'] = (len(layout_params['years']) - 1) * layout_params['adjusted_spacing']
        
        return layout_params
    
    def get_year_position(self, year: int, layout_params: Dict) -> float:
        """获取年份的X坐标"""
        return layout_params['positions'].get(year, 0)
    
    def determine_side(self, year: int) -> str:
        """
        确定年份应该放置在哪一侧（上/下）
        
        Args:
            year: 年份
            
        Returns:
            'above' 或 'below'
        """
        # 解析上方规则
        upper_rule = self.time_config.upper_years.lower()
        if upper_rule == 'odd':
            upper_years = lambda y: y % 2 == 1
        elif upper_rule == 'even':
            upper_years = lambda y: y % 2 == 0
        else:
            # 解析具体年份列表
            try:
                upper_list = [int(y.strip()) for y in upper_rule.split(',')]
                upper_years = lambda y: y in upper_list
            except:
                upper_years = lambda y: y % 2 == 1
        
        return 'above' if upper_years(year) else 'below'


class LaTeXGenerator:
    """LaTeX 代码生成器"""
    
    def __init__(self, 
                 layout: LayoutConfig,
                 time_logic: TimeLogicConfig,
                 visual: VisualConfig,
                 colors: ColorConfig,
                 arrows: ArrowConfig,
                 output: OutputConfig):
        self.layout = layout
        self.time_logic = time_logic
        self.visual = visual
        self.colors = colors
        self.arrows = arrows
        self.output = output
        self.layout_engine = SmartLayoutEngine(layout, time_logic)
    
    def _generate_preamble(self) -> str:
        """生成 LaTeX 前置代码"""
        lines = [
            r"\begin{figure}[htbp]",
            r"\centering",
            f"\\begin{{adjustbox}}{{center, max width={self.output.adjustbox_width}, max height=0.8\\textheight, keepaspectratio}}",
            r"\pgfdeclarelayer{background}",
            r"\pgfdeclarelayer{foreground}",
            r"\pgfsetlayers{background,main,foreground}",
            r"\begin{tikzpicture}[",
            "    scale=1.0,",
            "    transform shape,",
            r"    font=\footnotesize\sffamily,",
        ]
        return '\n'.join(lines)
    
    def _generate_styles(self) -> str:
        """生成 TikZ 样式定义"""
        styles = [
            "    % ========================================",
            "    % 类别颜色定义",
            "    % ========================================",
            f"    singleproto/.style={{{{\n"
            f"        fill={self.colors.color_single}, draw={self.colors.color_single}!50!black, "
            f"line width={self.visual.line_width}, \n"
            f"        rounded corners={self.visual.rounded_corners}, "
            f"minimum width={self.visual.node_width}, minimum height={self.visual.node_height},\n"
            f"        align=center, font={self.visual.node_font}, text=black!80, "
            f"inner sep={self.visual.inner_sep}\n"
            f"    }}}},",
            f"    multiproto/.style={{{{\n"
            f"        fill={self.colors.color_multi}, draw={self.colors.color_multi}!50!black, "
            f"line width={self.visual.line_width}, \n"
            f"        rounded corners={self.visual.rounded_corners}, "
            f"minimum width={self.visual.node_width}, minimum height={self.visual.node_height},\n"
            f"        align=center, font={self.visual.node_font}, text=black!80, "
            f"inner sep={self.visual.inner_sep}\n"
            f"    }}}},",
            f"    adaptive/.style={{{{\n"
            f"        fill={self.colors.color_adaptive}, draw={self.colors.color_adaptive}!70!black, "
            f"line width={self.visual.line_width}, \n"
            f"        rounded corners={self.visual.rounded_corners}, "
            f"minimum width={self.visual.node_width}, minimum height={self.visual.node_height},\n"
            f"        align=center, font={self.visual.node_font}, text=black!80, "
            f"inner sep={self.visual.inner_sep}\n"
            f"    }}}},",
            f"    vl/.style={{{{\n"
            f"        fill={self.colors.color_vl}, draw={self.colors.color_vl}!60!black, "
            f"line width={self.visual.line_width}, \n"
            f"        rounded corners={self.visual.rounded_corners}, "
            f"minimum width={self.visual.node_width}, minimum height={self.visual.node_height},\n"
            f"        align=center, font={self.visual.node_font}, text=black!80, "
            f"inner sep={self.visual.inner_sep}\n"
            f"    }}}},",
            f"    dense/.style={{{{\n"
            f"        fill={self.colors.color_dense}, draw={self.colors.color_dense}!70!black, "
            f"line width={self.visual.line_width}, \n"
            f"        rounded corners={self.visual.rounded_corners}, "
            f"minimum width={self.visual.node_width}, minimum height={self.visual.node_height},\n"
            f"        align=center, font={self.visual.node_font}, text=black!80, "
            f"inner sep={self.visual.inner_sep}\n"
            f"    }}}},",
            f"    attention/.style={{{{\n"
            f"        fill={self.colors.color_attention}, draw={self.colors.color_attention}!60!black, "
            f"line width={self.visual.line_width}, \n"
            f"        rounded corners={self.visual.rounded_corners}, "
            f"minimum width={self.visual.node_width}, minimum height={self.visual.node_height},\n"
            f"        align=center, font={self.visual.node_font}, text=black!80, "
            f"inner sep={self.visual.inner_sep}\n"
            f"    }}}},",
            f"    hybrid/.style={{{{\n"
            f"        fill={self.colors.color_hybrid}, draw={self.colors.color_hybrid}!70!black, "
            f"line width={self.visual.line_width}, \n"
            f"        rounded corners={self.visual.rounded_corners}, "
            f"minimum width={self.visual.node_width}, minimum height={self.visual.node_height},\n"
            f"        align=center, font={self.visual.node_font}, text=black!80, "
            f"inner sep={self.visual.inner_sep}\n"
            f"    }}}},",
            "    year/.style={{%",
            "        circle, fill=white, draw=black, line width=1.2pt, ",
            r"        minimum size=0.75cm, font=\bfseries\footnotesize, inner sep=0pt",
            "    }},",
            "    axis/.style={{%",
            f"        line width=1.5pt, draw={self.colors.axis_color}",
            "    }},",
            "    arrow/.style={{%",
            f"        {self.arrows.arrow_style}, ",
            f"        line width=0.8pt, draw={self.arrows.arrow_color},",
            f"        shorten >={self.arrows.arrow_shorten},",
            f"        shorten <={self.arrows.arrow_shorten}",
            "    }},",
            "    spine/.style={{%",
            "        line width=0.8pt, draw=gray!50, -",
            "    }},",
            "    conn/.style={{%",
            f"        line width=0.5pt, draw={self.colors.conn_color}",
            "    }},",
            "    methodmatrix/.style={{%",
            "        matrix of nodes, row sep=4pt, column sep=3pt, ",
            "        nodes in empty cells, inner sep=0pt",
            "    }}",
            "]"
        ]
        return '\n'.join(styles)
    
    def _format_method_text(self, name: str, ref: str) -> str:
        """
        格式化方法文本（单行或双行）
        
        Args:
            name: 方法名
            ref: 引用标识
            
        Returns:
            格式化后的 LaTeX 文本
        """
        ref_cmd = f"{{\\\\{self.visual.ref_font}\\\\cite{{{ref}}}}}"
        
        if self.visual.max_lines == 1:
            # 单行模式：使用 ~ 分隔
            return f"{name}~{ref_cmd}"
        else:
            # 双行模式：使用换行
            return f"{name}\\\\\\\\[-2pt]{ref_cmd}"
    
    def _generate_timeline_axis(self, layout_params: Dict) -> str:
        """生成时间轴和坐标定义"""
        total_width = layout_params['total_width']
        
        lines = [
            "    % ========================================",
            "    % 1. 绘制时间轴和定义年份坐标",
            "    % ========================================",
            f"    \\draw[axis] (0,0) -- ({total_width},0);",
            "",
            "    % 定义年份位置"
        ]
        
        # 生成坐标定义
        for year in layout_params['years']:
            pos = layout_params['positions'][year]
            lines.append(f"    \\coordinate (Y{year}) at ({pos},0);")
        
        # 生成年份间箭头
        lines.extend([
            "",
            "    % 绘制年份节点间的箭头",
            "    \\foreach \\year/\\nextyear in {"
        ])
        
        year_list = layout_params['years']
        arrow_pairs = [f"{year_list[i]}/{year_list[i+1]}" for i in range(len(year_list)-1)]
        lines.append("        " + ", ".join(arrow_pairs) + r"    } {")
        lines.append("        \\draw[arrow] (Y\\year) -- (Y\\nextyear);")
        lines.append("    }")
        
        return '\n'.join(lines)
    
    def _generate_method_nodes(self, df: pd.DataFrame, layout_params: Dict) -> str:
        """生成方法节点"""
        lines = [
            "",
            "    % ========================================",
            "    % 2. 先定义所有方法节点",
            "    % ========================================"
        ]
        
        # 按年份和位置分组
        year_groups = df.groupby('年份')
        
        for year in sorted(df['年份'].unique()):
            if year not in year_groups.groups:
                continue
            
            group = year_groups.get_group(year)
            side = self.layout_engine.determine_side(year)
            pos = f"Y{year}"
            
            lines.append(f"")
            lines.append(f"    % --- {year}年 ({'上侧' if side == 'above' else '下侧'}) ---")
            
            if len(group) == 1:
                # 单个节点，直接放置
                row = group.iloc[0]
                text = self._format_method_text(row['方法名'], row['引用标识'])
                style = row['种类']
                anchor = "above" if side == "above" else "below"
                yshift = f"[yshift={self.layout.spine_length}cm]" if side == "above" else f"[yshift=-{self.layout.spine_length}cm]"
                
                lines.append(
                    f"    \\node[{style}, {anchor}={self.layout.branch_distance}cm of {pos}] (M{year}) "
                    f"{{{text}}};"
                )
            else:
                # 多个节点，使用 matrix
                anchor = "south" if side == "above" else "north"
                matrix_pos = f"{anchor}={self.layout.branch_distance}cm of {pos}"
                
                lines.append(f"    \\matrix[methodmatrix, {matrix_pos}, anchor={anchor}] (M{year}) {{")
                
                # 生成矩阵行
                for idx, (_, row) in enumerate(group.iterrows()):
                    text = self._format_method_text(row['方法名'], row['引用标识'])
                    style = row['种类']
                    
                    # 检查是否需要双列布局（如果节点很多）
                    if len(group) > 3 and idx % 2 == 0 and idx < len(group) - 1:
                        next_row = group.iloc[idx + 1]
                        next_text = self._format_method_text(next_row['方法名'], next_row['引用标识'])
                        next_style = next_row['种类']
                        lines.append(f"        \\node[{style}] {{{text}}}; & ")
                        lines.append(f"\\node[{next_style}] {{{next_text}}}; \\\\")
                    else:
                        if not (len(group) > 3 and idx % 2 == 1):
                            lines.append(f"        \\node[{style}] {{{text}}}; \\\\")
                
                lines.append("    };")
        
        return '\n'.join(lines)
    
    def _generate_background_layer(self, df: pd.DataFrame) -> str:
        """生成背景层连线"""
        lines = [
            "",
            "    % ========================================",
            "    % 3. 在背景层绘制所有灰色连线",
            "    % ========================================",
            r"    \begin{pgfonlayer}{background}",
            "        % 年份节点的分支脊线（spine）"
        ]
        
        years = sorted(df['年份'].unique())
        
        # 生成分支脊线
        lines.append("        \\foreach \\year in {" + ", ".join(map(str, years)) + r"} {")
        lines.append(f"            \\draw[spine] (Y\\year.north) -- ++(0,{self.layout.spine_length});")
        lines.append(f"            \\draw[spine] (Y\\year.south) -- ++(0,-{self.layout.spine_length});")
        lines.append("        }")
        lines.append("")
        lines.append("        % 方法到年份节点的连接线（conn）")
        
        # 生成连接线
        for year in years:
            side = self.layout_engine.determine_side(year)
            if side == "above":
                lines.append(f"        \\draw[conn] (M{year}.south) -- ([yshift={self.layout.spine_length}cm]Y{year});")
            else:
                lines.append(f"        \\draw[conn] (M{year}.north) -- ([yshift=-{self.layout.spine_length}cm]Y{year});")
        
        lines.append(r"    \end{pgfonlayer}")
        
        return '\n'.join(lines)
    
    def _generate_year_nodes(self, df: pd.DataFrame) -> str:
        """生成年份节点（最上层）"""
        years = sorted(df['年份'].unique())
        
        lines = [
            "",
            "    % ========================================",
            "    % 4. 最后绘制所有年份节点（置于最上层，覆盖箭头末端）",
            "    % ========================================",
            "    \\foreach \\year in {" + ", ".join(map(str, years)) + r"} {",
            "        \\node[year] at (Y\\year) {\\year};",
            "    }"
        ]
        
        return '\n'.join(lines)
    
    def _generate_bounding_box(self) -> str:
        """生成边界框扩展"""
        return (
            "\n"
            "    % ========================================\n"
            "    % 5. 扩展边界框\n"
            "    % ========================================\n"
            r"    \path (current bounding box.south west) +(-0.3,-0.5) "
            "(current bounding box.north east) +(0.3,0.5);"
        )
    
    def _generate_caption(self) -> str:
        """生成图例和标题"""
        lines = [
            r"\end{tikzpicture}",
            r"\end{adjustbox}",
            f"\\caption{{{self.output.caption}。",
        ]
        
        if self.output.show_legend:
            # 生成图例说明
            legend_items = [
                (self.colors.color_single, "cyan!50!black", "单原型方法"),
                (self.colors.color_multi, "green!50!black", "多原型方法"),
                (self.colors.color_adaptive, "yellow!70!black", "自适应方法"),
                (self.colors.color_vl, "purple!60!black", "视觉语言方法"),
                (self.colors.color_dense, "orange!70!black", "稠密匹配"),
                (self.colors.color_attention, "red!60!black", "注意力匹配"),
                (self.colors.color_hybrid, "gray!70!black", "混合细化"),
            ]
            
            legend_text = "颜色标识："
            for fill, draw, desc in legend_items:
                legend_text += (
                    r"{\protect\tikz[baseline=-0.5ex]\protect\node["
                    f"fill={fill},draw={draw},rounded corners=2pt,inner sep=2pt,font=\\tiny] {{{desc}}};} "
                )
            
            lines.append(legend_text)
        
        lines.append(f"}}")
        lines.append(f"\\label{{{self.output.label}}}")
        lines.append(r"\end{figure}")
        
        return '\n'.join(lines)
    
    def generate(self, df: pd.DataFrame) -> str:
        """
        生成完整的 LaTeX 代码
        
        Args:
            df: 数据框
            
        Returns:
            完整 LaTeX 代码字符串
        """
        # 计算布局
        layout_params = self.layout_engine.calculate_layout(df)
        
        # 生成各部分
        parts = [
            self._generate_preamble(),
            self._generate_styles(),
            self._generate_timeline_axis(layout_params),
            self._generate_method_nodes(df, layout_params),
            self._generate_background_layer(df),
            self._generate_year_nodes(df),
            self._generate_bounding_box(),
            self._generate_caption()
        ]
        
        return '\n'.join(parts)


def create_sample_csv(output_path: str = "sample_data.csv"):
    """创建示例 CSV 文件"""
    data = {
        '年份': [2019, 2020, 2021, 2021, 2021, 2022, 2022, 2022, 
                2023, 2023, 2023, 2024, 2024, 2024, 2024, 2024, 2025, 2025],
        '种类': ['singleproto', 'multiproto', 'multiproto', 'dense', 'attention',
                'singleproto', 'singleproto', 'adaptive', 'adaptive', 'attention',
                'hybrid', 'vl', 'vl', 'vl', 'adaptive', 'hybrid', 'multiproto', 'multiproto'],
        '方法名': ['PANet', 'PPNet', 'ASGNet', 'HSNet', 'CWT', 'PFENet', 'BAM',
                  'DPCN', 'Self-reg', 'HDMNet', 'SCCAN', 'Proto-CLIP', 'TransBA',
                  'Zhu et al.', 'AdaptiveSS', 'DAM', 'HMPD', 'ProtoPT'],
        '引用标识': ['Wang2019PANet', 'Liu2020PPNet', 'Li2021ASGNet', 'Min2021HSNet',
                    'Lu2021CWT', 'Tian2022PFENet', 'Lang2022BAM', 'Liu2022DynamicPC',
                    'Ding2023Selfregularized', 'Peng2023HDMNet', 'Xu2023SCCAN',
                    'P2024ProtoCLIP', 'Chen2024TransformerBA', 'Zhu2024Unleashing',
                    'Shen2024AdaptiveSS', 'Chen2024DAM', 'Xu2025HMPD', 'Yu2025PrototypicalPT']
    }
    
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"已创建示例数据文件: {output_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='LaTeX 时间轴鱼骨图生成器 - 从 CSV 自动生成 TikZ 代码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 基本用法
  python timeline_generator.py -i data.csv -o timeline.tex
  
  # 使用智能布局
  python timeline_generator.py -i data.csv --smart-spacing --max-lines 2
  
  # 自定义配色和方向
  python timeline_generator.py -i data.csv --time-direction left 
      --color-single "blue!30" --color-multi "red!20"
  
  # 生成示例数据
  python timeline_generator.py --create-sample -o sample_data.csv
        """
    )
    
    # 输入输出参数
    parser.add_argument('-i', '--input', dest='input_file',
                       help='输入 CSV 文件路径')
    parser.add_argument('-o', '--output', default='timeline.tex',
                       help='输出 LaTeX 文件路径 (默认: timeline.tex)')
    parser.add_argument('--create-sample', action='store_true',
                       help='创建示例 CSV 文件并退出')
    
    # 布局参数
    layout_group = parser.add_argument_group('布局参数')
    layout_group.add_argument('--timeline-width', default='16cm',
                             help='时间轴总长度 (默认: 16cm)')
    layout_group.add_argument('--year-spacing', type=float, default=2.7,
                             help='年份间距 cm (默认: 2.7)')
    layout_group.add_argument('--branch-distance', type=float, default=1.2,
                             help='分支距离 cm (默认: 1.2)')
    layout_group.add_argument('--spine-length', type=float, default=0.4,
                             help='分支配线长度 cm (默认: 0.4)')
    layout_group.add_argument('--smart-spacing', action='store_true',
                             help='启用智能间距调整')
    layout_group.add_argument('--min-year-spacing', type=float, default=2.0,
                             help='智能调整时的最小间距 cm (默认: 2.0)')
    
    # 时间逻辑参数
    time_group = parser.add_argument_group('时间逻辑参数')
    time_group.add_argument('--time-direction', choices=['right', 'left'], default='right',
                           help='时间流向 (默认: right)')
    time_group.add_argument('--start-year', type=int, default=2019,
                           help='起始年份 (默认: 2019)')
    time_group.add_argument('--end-year', type=int, default=2025,
                           help='结束年份 (默认: 2025)')
    time_group.add_argument('--upper-years', default='odd',
                           help='上方分支规则: odd, even 或逗号分隔的年份列表 (默认: odd)')
    time_group.add_argument('--lower-years', default='even',
                           help='下方分支规则 (默认: even)')
    
    # 视觉样式参数
    visual_group = parser.add_argument_group('视觉样式参数')
    visual_group.add_argument('--node-width', default='2.6cm',
                             help='节点宽度 (默认: 2.6cm)')
    visual_group.add_argument('--node-height', default='0.5cm',
                             help='节点高度 (默认: 0.5cm)')
    visual_group.add_argument('--node-font', default=r'\tiny\bfseries',
                             help='节点字体 (默认: \\tiny\\bfseries)')
    visual_group.add_argument('--ref-font', default=r'\tiny',
                             help='引用字体 (默认: \\tiny)')
    visual_group.add_argument('--inner-sep', default='1.5pt',
                             help='内边距 (默认: 1.5pt)')
    visual_group.add_argument('--line-width', default='0.8pt',
                             help='线宽 (默认: 0.8pt)')
    visual_group.add_argument('--rounded-corners', default='3pt',
                             help='圆角半径 (默认: 3pt)')
    visual_group.add_argument('--max-lines', type=int, default=1, choices=[1, 2],
                             help='最大行数: 1单行或2双行 (默认: 1)')
    
    # 配色参数
    color_group = parser.add_argument_group('配色方案参数')
    color_group.add_argument('--color-single', default='cyan!20',
                            help='单原型颜色 (默认: cyan!20)')
    color_group.add_argument('--color-multi', default='green!20',
                            help='多原型颜色 (默认: green!20)')
    color_group.add_argument('--color-adaptive', default='yellow!40',
                            help='自适应颜色 (默认: yellow!40)')
    color_group.add_argument('--color-vl', default='purple!20',
                            help='视觉语言颜色 (默认: purple!20)')
    color_group.add_argument('--color-dense', default='orange!30',
                            help='稠密匹配颜色 (默认: orange!30)')
    color_group.add_argument('--color-attention', default='red!20',
                            help='注意力颜色 (默认: red!20)')
    color_group.add_argument('--color-hybrid', default='gray!30',
                            help='混合细化颜色 (默认: gray!30)')
    color_group.add_argument('--axis-color', default='black!70',
                            help='时间轴颜色 (默认: black!70)')
    color_group.add_argument('--conn-color', default='gray!60',
                            help='连接线颜色 (默认: gray!60)')
    
    # 箭头参数
    arrow_group = parser.add_argument_group('箭头与连线参数')
    arrow_group.add_argument('--arrow-style', 
                            default=r'-{Stealth[length=3mm, width=2mm]}',
                            help='箭头样式')
    arrow_group.add_argument('--arrow-color', default='gray!70',
                            help='箭头颜色 (默认: gray!70)')
    arrow_group.add_argument('--arrow-shorten', default='0.38cm',
                            help='箭头缩进 (默认: 0.38cm)')
    
    # 输出参数
    output_group = parser.add_argument_group('输出参数')
    output_group.add_argument('--show-legend', action='store_true', default=True,
                             help='显示图例 (默认: True)')
    output_group.add_argument('--hide-legend', dest='show_legend', action='store_false',
                             help='隐藏图例')
    output_group.add_argument('--caption', default='时间线鱼骨图',
                             help='图标题')
    output_group.add_argument('--label', default='fig:timeline',
                             help='标签')
    output_group.add_argument('--adjustbox-width', default='0.8\\\\textwidth',
                             help='adjustbox宽度 (默认: 0.8\\\\textwidth)')
    
    args = parser.parse_args()
    
    # 处理创建示例数据
    if args.create_sample:
        create_sample_csv(args.output)
        return 0
    
    # 验证输入文件
    if not args.input_file:
        print("错误: 必须指定输入文件 (-i) 或使用 --create-sample 创建示例")
        return 1
    
    # 加载并验证数据
    df, error = DataValidator.load_data(args.input_file)
    if df is None:
        print(f"错误: {error}")
        return 1
    
    print(f"成功加载数据: {len(df)} 条记录，{df['年份'].nunique()} 个年份")
    
    # 创建配置对象
    layout = LayoutConfig(
        timeline_width=args.timeline_width,
        year_spacing=args.year_spacing,
        branch_distance=args.branch_distance,
        spine_length=args.spine_length,
        smart_spacing=args.smart_spacing,
        min_year_spacing=args.min_year_spacing
    )
    
    time_logic = TimeLogicConfig(
        time_direction=args.time_direction,
        start_year=args.start_year,
        end_year=args.end_year,
        upper_years=args.upper_years,
        lower_years=args.lower_years
    )
    
    visual = VisualConfig(
        node_width=args.node_width,
        node_height=args.node_height,
        node_font=args.node_font,
        ref_font=args.ref_font,
        inner_sep=args.inner_sep,
        line_width=args.line_width,
        rounded_corners=args.rounded_corners,
        max_lines=args.max_lines
    )
    
    colors = ColorConfig(
        color_single=args.color_single,
        color_multi=args.color_multi,
        color_adaptive=args.color_adaptive,
        color_vl=args.color_vl,
        color_dense=args.color_dense,
        color_attention=args.color_attention,
        color_hybrid=args.color_hybrid,
        axis_color=args.axis_color,
        conn_color=args.conn_color
    )
    
    arrows = ArrowConfig(
        arrow_style=args.arrow_style,
        arrow_color=args.arrow_color,
        arrow_shorten=args.arrow_shorten
    )
    
    output = OutputConfig(
        input_file=args.input_file,
        output_file=args.output,
        show_legend=args.show_legend,
        caption=args.caption,
        label=args.label,
        adjustbox_width=args.adjustbox_width
    )
    
    # 生成 LaTeX
    generator = LaTeXGenerator(layout, time_logic, visual, colors, arrows, output)
    latex_code = generator.generate(df)
    
    # 写入文件
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(latex_code)
        print(f"成功生成 LaTeX 文件: {args.output}")
        print(f"文件大小: {os.path.getsize(args.output)} 字节")
        return 0
    except Exception as e:
        print(f"写入文件失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())