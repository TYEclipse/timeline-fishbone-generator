# Advanced Features# Advanced Features












































```    generate_timeline(path, f"{path}.tex", config_file="config.yaml")for path in files:files = ["a.csv", "b.csv", "c.csv"]from timeline_fishbone import generate_timeline```pythonYou can loop over multiple files with a shared configuration:## Batch Processingbased on node density.Enable smart spacing to automatically adjust year spacing and branch distance## Layout StrategySet visual.max_lines to 2 to render method name and citation on two lines.## Multi-Line NodesYou can customize color schemes using YAML/JSON or programmatically.## Custom Category Colors```)    visual__max_lines=2    layout__smart_spacing=True,    "output.tex",    "data.csv",generate_timeline(from timeline_fishbone import generate_timeline```pythonCLI. Example:Use the double-underscore syntax to override configuration fields from code or## Configuration MergingThis page describes advanced usage patterns and configuration options.
This page describes advanced usage patterns and configuration options.

## Configuration Merging

Use the double-underscore syntax to override configuration fields from code or
CLI. Example:

```python
from timeline_fishbone import generate_timeline

generate_timeline(
    "data.csv",
    "output.tex",
    layout__smart_spacing=True,
    visual__max_lines=2
)
```

## Custom Category Colors

You can customize color schemes using YAML/JSON or programmatically.

## Multi-Line Nodes

Set visual.max_lines to 2 to render method name and citation on two lines.

## Layout Strategy

Enable smart spacing to automatically adjust year spacing and branch distance
based on node density.

## Batch Processing

You can loop over multiple files with a shared configuration:

```python
from timeline_fishbone import generate_timeline

files = ["a.csv", "b.csv", "c.csv"]
for path in files:
    generate_timeline(path, f"{path}.tex", config_file="config.yaml")
```
