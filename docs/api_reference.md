# API Reference

This document summarizes the public API surface. For detailed signatures and
examples, refer to docstrings in the source code.

## High-Level Functions

### generate_timeline

- Location: timeline_fishbone.utils
- Purpose: Generate LaTeX code from a CSV/JSON input file

Parameters:
- input_file: Path to CSV/JSON data
- output_file: Optional output path for LaTeX
- config_file: Optional YAML/JSON config file
- kwargs: Configuration overrides (e.g., layout__smart_spacing=True)

Returns:
- LaTeX code as a string

### create_sample_data

- Location: timeline_fishbone.utils
- Purpose: Create a sample CSV data file

## Core Classes

### TimelineFishboneConfig

Main configuration container. Supports:
- from_yaml / from_json
- save_yaml / save_json
- merge

### DataValidator

Validates CSV/JSON data files and returns a DataFrame.

### SmartLayoutEngine

Computes spacing and positions to avoid overlap.

### LaTeXGenerator

Generates full TikZ LaTeX code for the timeline diagram.
