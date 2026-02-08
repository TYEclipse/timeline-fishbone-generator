#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced usage examples for Timeline Fishbone Generator.

Demonstrates programmatic configuration and advanced features.
"""

from timeline_fishbone.core import (
    TimelineFishboneConfig,
    LayoutConfig,
    VisualConfig,
    ColorConfig,
    LaTeXGenerator,
    DataValidator,
)
import pandas as pd

# Example 1: Programmatic configuration
print("Example 1: Building configuration programmatically...")

config = TimelineFishboneConfig()
config.layout.smart_spacing = True
config.layout.year_spacing = 3.0
config.visual.max_lines = 2
config.colors.color_single = "blue!30"
config.output.caption = "自定义学术时间线"

print("✓ Configuration built\n")

# Example 2: Save and load configuration
print("Example 2: Saving configuration to file...")

config.save_yaml("my_config.yaml")
config.save_json("my_config.json")

# Load it back
loaded_config = TimelineFishboneConfig.from_yaml("my_config.yaml")
print(f"✓ Config saved and loaded, smart_spacing = {loaded_config.layout.smart_spacing}\n")

# Example 3: Create custom data programmatically
print("Example 3: Creating custom dataset...")

data = {
    '年份': [2020, 2021, 2022, 2023],
    '种类': ['singleproto', 'multiproto', 'adaptive', 'vl'],
    '方法名': ['Method A', 'Method B', 'Method C', 'Method D'],
    '引用标识': ['RefA', 'RefB', 'RefC', 'RefD']
}

df = pd.DataFrame(data)
df.to_csv("custom_data.csv", index=False)
print("✓ Custom data created\n")

# Example 4: Validate data before processing
print("Example 4: Validating data...")

try:
    validated_df = DataValidator.load_and_validate("custom_data.csv")
    print(f"✓ Data validated: {len(validated_df)} records\n")
except Exception as e:
    print(f"✗ Validation failed: {e}\n")

# Example 5: Direct generator usage
print("Example 5: Using LaTeXGenerator directly...")

generator = LaTeXGenerator(
    config.layout,
    config.time_logic,
    config.visual,
    config.colors,
    config.arrows,
    config.output,
)

latex_code = generator.generate(validated_df)
with open("direct_generation.tex", "w", encoding="utf-8") as f:
    f.write(latex_code)

print(f"✓ Direct generation: {len(latex_code)} characters\n")

# Example 6: Configuration merging
print("Example 6: Merging configurations...")

base_config = TimelineFishboneConfig()
override_config = TimelineFishboneConfig()
override_config.layout.smart_spacing = True
override_config.visual.max_lines = 2

merged = base_config.merge(override_config)
print(f"✓ Merged config: smart_spacing={merged.layout.smart_spacing}, "
      f"max_lines={merged.visual.max_lines}\n")

# Example 7: Customizing colors for specific categories
print("Example 7: Custom color scheme...")

custom_colors = ColorConfig(
    color_single="teal!25",
    color_multi="lime!30",
    color_adaptive="amber!35",
    color_vl="violet!25",
    color_dense="orange!35",
    color_attention="crimson!25",
    color_hybrid="slate!30"
)

custom_config = TimelineFishboneConfig()
custom_config.colors = custom_colors

print("✓ Custom colors configured\n")

print("All advanced examples completed!")
