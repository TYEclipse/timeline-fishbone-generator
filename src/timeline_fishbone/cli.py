#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line interface for Timeline Fishbone Generator.

Provides comprehensive CLI with argparse for all configuration options.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .core import TimelineFishboneConfig
from .utils import (
    create_sample_data,
    generate_timeline,
    setup_logging,
    validate_data_file,
)


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser with all CLI options."""
    parser = argparse.ArgumentParser(
        prog='timeline-fishbone',
        description='LaTeX Timeline Fishbone Generator - Generate publication-ready '
                   'TikZ timeline diagrams from CSV/JSON data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  timeline-fishbone -i data.csv -o timeline.tex
  
  # With smart layout
  timeline-fishbone -i data.csv --smart-spacing --max-lines 2
  
  # Use configuration file
  timeline-fishbone -i data.csv -c config.yaml
  
  # Create sample data
  timeline-fishbone --create-sample sample_data.csv
  
  # Validate data file
  timeline-fishbone --validate data.csv
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    # Main actions
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        '--create-sample',
        metavar='FILE',
        help='Create sample CSV file and exit'
    )
    action_group.add_argument(
        '--validate',
        metavar='FILE',
        help='Validate data file and exit'
    )
    
    # Input/Output
    io_group = parser.add_argument_group('Input/Output Options')
    io_group.add_argument(
        '-i', '--input',
        dest='input_file',
        help='Input CSV or JSON file path'
    )
    io_group.add_argument(
        '-o', '--output',
        default='timeline.tex',
        help='Output LaTeX file path (default: timeline.tex)'
    )
    io_group.add_argument(
        '-c', '--config',
        dest='config_file',
        help='Configuration file (YAML or JSON)'
    )
    
    # Layout parameters
    layout_group = parser.add_argument_group('Layout Options')
    layout_group.add_argument(
        '--timeline-width',
        default='16cm',
        help='Timeline total width (default: 16cm)'
    )
    layout_group.add_argument(
        '--year-spacing',
        type=float,
        default=2.7,
        help='Year spacing in cm (default: 2.7)'
    )
    layout_group.add_argument(
        '--branch-distance',
        type=float,
        default=1.2,
        help='Branch distance in cm (default: 1.2)'
    )
    layout_group.add_argument(
        '--spine-length',
        type=float,
        default=0.4,
        help='Spine length in cm (default: 0.4)'
    )
    layout_group.add_argument(
        '--smart-spacing',
        action='store_true',
        help='Enable smart spacing adjustment'
    )
    layout_group.add_argument(
        '--min-year-spacing',
        type=float,
        default=2.0,
        help='Minimum year spacing for smart adjustment (default: 2.0)'
    )
    
    # Time logic
    time_group = parser.add_argument_group('Time Logic Options')
    time_group.add_argument(
        '--time-direction',
        choices=['right', 'left'],
        default='right',
        help='Time flow direction (default: right)'
    )
    time_group.add_argument(
        '--start-year',
        type=int,
        default=2019,
        help='Start year (default: 2019)'
    )
    time_group.add_argument(
        '--end-year',
        type=int,
        default=2025,
        help='End year (default: 2025)'
    )
    time_group.add_argument(
        '--upper-years',
        default='order',
        help='Upper branch rule: order, odd, even, or comma-separated years (default: order)'
    )
    time_group.add_argument(
        '--lower-years',
        default='even',
        help='Lower branch rule (default: even)'
    )
    
    # Visual style
    visual_group = parser.add_argument_group('Visual Style Options')
    visual_group.add_argument(
        '--node-width',
        default='2.6cm',
        help='Node width (default: 2.6cm)'
    )
    visual_group.add_argument(
        '--node-height',
        default='0.5cm',
        help='Node height (default: 0.5cm)'
    )
    visual_group.add_argument(
        '--node-font',
        default=r'\tiny\bfseries',
        help=r'Node font (default: \tiny\bfseries)'
    )
    visual_group.add_argument(
        '--ref-font',
        default=r'\tiny',
        help=r'Reference font (default: \tiny)'
    )
    visual_group.add_argument(
        '--inner-sep',
        default='1.5pt',
        help='Inner separation (default: 1.5pt)'
    )
    visual_group.add_argument(
        '--line-width',
        default='0.8pt',
        help='Line width (default: 0.8pt)'
    )
    visual_group.add_argument(
        '--rounded-corners',
        default='3pt',
        help='Rounded corners radius (default: 3pt)'
    )
    visual_group.add_argument(
        '--max-lines',
        type=int,
        default=1,
        choices=[1, 2],
        help='Maximum lines per node: 1 or 2 (default: 1)'
    )
    
    # Colors
    color_group = parser.add_argument_group('Color Scheme Options')
    color_group.add_argument('--color-single', default='cyan!20',
                            help='Single-prototype color (default: cyan!20)')
    color_group.add_argument('--color-multi', default='green!20',
                            help='Multi-prototype color (default: green!20)')
    color_group.add_argument('--color-adaptive', default='yellow!40',
                            help='Adaptive color (default: yellow!40)')
    color_group.add_argument('--color-vl', default='purple!20',
                            help='Vision-language color (default: purple!20)')
    color_group.add_argument('--color-dense', default='orange!30',
                            help='Dense matching color (default: orange!30)')
    color_group.add_argument('--color-attention', default='red!20',
                            help='Attention color (default: red!20)')
    color_group.add_argument('--color-hybrid', default='gray!30',
                            help='Hybrid color (default: gray!30)')
    color_group.add_argument('--axis-color', default='black!70',
                            help='Axis color (default: black!70)')
    color_group.add_argument('--conn-color', default='gray!60',
                            help='Connection color (default: gray!60)')
    
    # Arrows
    arrow_group = parser.add_argument_group('Arrow Options')
    arrow_group.add_argument(
        '--arrow-style',
        default=r'-{Stealth[length=3mm, width=2mm]}',
        help='Arrow style (TikZ syntax)'
    )
    arrow_group.add_argument(
        '--arrow-color',
        default='gray!70',
        help='Arrow color (default: gray!70)'
    )
    arrow_group.add_argument(
        '--arrow-shorten',
        default='0.38cm',
        help='Arrow shorten distance (default: 0.38cm)'
    )
    
    # Output formatting
    format_group = parser.add_argument_group('Output Formatting Options')
    format_group.add_argument(
        '--show-legend',
        action='store_true',
        default=True,
        help='Show legend (default: True)'
    )
    format_group.add_argument(
        '--hide-legend',
        dest='show_legend',
        action='store_false',
        help='Hide legend'
    )
    format_group.add_argument(
        '--caption',
        default='时间线鱼骨图',
        help='Figure caption (default: 时间线鱼骨图)'
    )
    format_group.add_argument(
        '--label',
        default='fig:timeline',
        help='Figure label (default: fig:timeline)'
    )
    format_group.add_argument(
        '--adjustbox-width',
        default=r'0.8\textwidth',
        help=r'Adjustbox width (default: 0.8\textwidth)'
    )
    
    # Logging
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress output except errors'
    )
    
    return parser


def args_to_config_overrides(args: argparse.Namespace) -> dict:
    """
    Convert CLI arguments to configuration overrides.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Dictionary of configuration overrides
    """
    overrides = {}
    
    # Layout
    if args.timeline_width:
        overrides['layout__timeline_width'] = args.timeline_width
    if args.year_spacing:
        overrides['layout__year_spacing'] = args.year_spacing
    if args.branch_distance:
        overrides['layout__branch_distance'] = args.branch_distance
    if args.spine_length:
        overrides['layout__spine_length'] = args.spine_length
    if args.smart_spacing:
        overrides['layout__smart_spacing'] = args.smart_spacing
    if args.min_year_spacing:
        overrides['layout__min_year_spacing'] = args.min_year_spacing
    
    # Time logic
    if args.time_direction:
        overrides['time_logic__time_direction'] = args.time_direction
    if args.start_year:
        overrides['time_logic__start_year'] = args.start_year
    if args.end_year:
        overrides['time_logic__end_year'] = args.end_year
    if args.upper_years:
        overrides['time_logic__upper_years'] = args.upper_years
    if args.lower_years:
        overrides['time_logic__lower_years'] = args.lower_years
    
    # Visual
    if args.node_width:
        overrides['visual__node_width'] = args.node_width
    if args.node_height:
        overrides['visual__node_height'] = args.node_height
    if args.node_font:
        overrides['visual__node_font'] = args.node_font
    if args.ref_font:
        overrides['visual__ref_font'] = args.ref_font
    if args.inner_sep:
        overrides['visual__inner_sep'] = args.inner_sep
    if args.line_width:
        overrides['visual__line_width'] = args.line_width
    if args.rounded_corners:
        overrides['visual__rounded_corners'] = args.rounded_corners
    if args.max_lines:
        overrides['visual__max_lines'] = args.max_lines
    
    # Colors
    for color_attr in ['single', 'multi', 'adaptive', 'vl', 'dense', 'attention', 'hybrid']:
        arg_name = f'color_{color_attr}'
        if hasattr(args, arg_name) and getattr(args, arg_name):
            overrides[f'colors__color_{color_attr}'] = getattr(args, arg_name)
    if args.axis_color:
        overrides['colors__axis_color'] = args.axis_color
    if args.conn_color:
        overrides['colors__conn_color'] = args.conn_color
    
    # Arrows
    if args.arrow_style:
        overrides['arrows__arrow_style'] = args.arrow_style
    if args.arrow_color:
        overrides['arrows__arrow_color'] = args.arrow_color
    if args.arrow_shorten:
        overrides['arrows__arrow_shorten'] = args.arrow_shorten
    
    # Output
    overrides['output__show_legend'] = args.show_legend
    if args.caption:
        overrides['output__caption'] = args.caption
    if args.label:
        overrides['output__label'] = args.label
    if args.adjustbox_width:
        overrides['output__adjustbox_width'] = args.adjustbox_width
    
    return overrides


def main(argv: Optional[list] = None) -> int:
    """
    Main CLI entry point.
    
    Args:
        argv: Command-line arguments (defaults to sys.argv)
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Setup logging
    if args.quiet:
        log_level = 'ERROR'
    elif args.verbose:
        log_level = 'DEBUG'
    else:
        log_level = 'INFO'
    setup_logging(log_level)
    
    try:
        # Handle special actions
        if args.create_sample:
            create_sample_data(args.create_sample)
            return 0
        
        if args.validate:
            success = validate_data_file(args.validate)
            return 0 if success else 1
        
        # Normal operation - require input file
        if not args.input_file:
            parser.error("必须指定输入文件 (-i/--input) 或使用特殊操作 (--create-sample, --validate)")
        
        # Generate timeline
        overrides = args_to_config_overrides(args)
        generate_timeline(
            args.input_file,
            args.output,
            args.config_file,
            **overrides
        )
        
        if not args.quiet:
            print(f"✓ 成功生成: {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"✗ 错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
