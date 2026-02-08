# Quick Start Guide

Get started with Timeline Fishbone Generator in minutes!

## Installation

```bash
pip install timeline-fishbone
```

## 5-Minute Tutorial

### Step 1: Create Sample Data

```bash
timeline-fishbone --create-sample my_data.csv
```

This creates a CSV file with sample timeline data.

### Step 2: Generate Timeline

```bash
timeline-fishbone -i my_data.csv -o timeline.tex
```

### Step 3: Use in LaTeX

Add to your LaTeX document:

```latex
\documentclass{article}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, backgrounds, matrix}
\usepackage{adjustbox}

\begin{document}

\input{timeline.tex}

\end{document}
```

### Step 4: Compile

```bash
pdflatex document.tex
```

## Customization Examples

### Enable Smart Spacing

```bash
timeline-fishbone -i data.csv -o timeline.tex --smart-spacing
```

### Double-Line Nodes

```bash
timeline-fishbone -i data.csv -o timeline.tex --max-lines 2
```

### Custom Colors

```bash
timeline-fishbone -i data.csv -o timeline.tex \
    --color-single "blue!30" \
    --color-multi "red!25"
```

### Use Configuration File

Create `config.yaml`:

```yaml
layout:
  smart_spacing: true
visual:
  max_lines: 2
colors:
  color_single: "teal!25"
```

Then:

```bash
timeline-fishbone -i data.csv -c config.yaml -o timeline.tex
```

## Python API

```python
from timeline_fishbone import generate_timeline

# Basic usage
generate_timeline("data.csv", "output.tex")

# With options
generate_timeline(
    "data.csv",
    "output.tex",
    layout__smart_spacing=True,
    visual__max_lines=2
)
```

## Next Steps

- Read the [User Guide](user_guide.md) for detailed documentation
- Check [Advanced Features](advanced_features.md) for power-user tips
- See [API Reference](api_reference.md) for complete API documentation

## Common Issues

### LaTeX Compilation Errors

Make sure you have these packages:
```latex
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, backgrounds, matrix}
\usepackage{adjustbox}
```

### Data Validation Errors

Ensure your CSV has these columns:
- 年份 (Year)
- 种类 (Category)
- 方法名 (Method name)
- 引用标识 (Citation key)

### Permission Errors

Run with appropriate permissions or install in user space:
```bash
pip install --user timeline-fishbone
```

## Getting Help

- Report bugs: [GitHub Issues](https://github.com/tyeclipse/timeline-fishbone/issues)
- Ask questions: [GitHub Discussions](https://github.com/tyeclipse/timeline-fishbone/discussions)
- Read docs: [Documentation](https://timeline-fishbone.readthedocs.io)
