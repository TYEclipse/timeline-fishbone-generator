#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic usage example for Timeline Fishbone Generator.

This example demonstrates the most common use cases.
"""

from timeline_fishbone import generate_timeline, create_sample_data
from pathlib import Path

# Example 1: Create sample data
print("Example 1: Creating sample data...")
create_sample_data("my_data.csv")
print("✓ Sample data created: my_data.csv\n")

# Example 2: Generate timeline from CSV
print("Example 2: Basic timeline generation...")
latex_code = generate_timeline(
    input_file="my_data.csv",
    output_file="timeline.tex"
)
print(f"✓ Generated timeline: {len(latex_code)} characters\n")

# Example 3: Generate with custom options
print("Example 3: Timeline with custom options...")
latex_code = generate_timeline(
    input_file="my_data.csv",
    output_file="timeline_custom.tex",
    layout__smart_spacing=True,
    visual__max_lines=2,
    output__caption="我的时间线图"
)
print(f"✓ Generated custom timeline\n")

# Example 4: Use configuration file
print("Example 4: Using configuration file...")
latex_code = generate_timeline(
    input_file="my_data.csv",
    output_file="timeline_from_config.tex",
    config_file="sample_config.yaml"  # If available
)
print(f"✓ Generated from config\n")

# Example 5: Return LaTeX without saving
print("Example 5: Get LaTeX code without saving...")
latex_code = generate_timeline("my_data.csv")
print(f"✓ LaTeX code: {len(latex_code)} characters")
print("Preview (first 300 chars):")
print(latex_code[:300])
print("...\n")

print("All examples completed successfully!")
