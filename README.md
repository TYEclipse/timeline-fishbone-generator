# Timeline Fishbone Generator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional Python package for generating publication-ready LaTeX TikZ timeline diagrams (fishbone style) from CSV/JSON data sources.

## ✨ Features

- 🎨 **Smart Layout Algorithm** - Automatically prevents node overlapping
- ⚙️ **Comprehensive Configuration** - CLI, YAML, JSON, and programmatic options
- 📊 **Multiple Data Formats** - Support for CSV and JSON input
- 🔧 **Highly Customizable** - Fine-tune colors, fonts, spacing, and more
- 📝 **Multi-line Support** - Intelligent text wrapping for node labels
- 🏗️ **Modular Architecture** - Clean, extensible, well-documented codebase
- ✅ **Well Tested** - pytest suite with coverage reporting
- 📚 **Publication Ready** - Generate LaTeX code for academic papers

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Data Format](#data-format)
- [Command Line Interface](#command-line-interface)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

### From PyPI (when published)

```bash
pip install timeline-fishbone
```

### From Source

```bash
git clone https://github.com/tyeclipse/timeline-fishbone.git
cd timeline-fishbone
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/tyeclipse/timeline-fishbone.git
cd timeline-fishbone
pip install -e ".[dev]"
```

## Quick Start

### 1. Create Sample Data

```bash
timeline-fishbone --create-sample sample_data.csv
```

### 2. Generate Timeline

```bash
timeline-fishbone -i sample_data.csv -o timeline.tex
```

### 3. Compile with LaTeX

```bash
pdflatex your_document.tex  # Include the generated timeline.tex
```

## Usage Examples

### Command Line

```bash
# Basic usage
timeline-fishbone -i data.csv -o timeline.tex

# With smart spacing and double-line nodes
timeline-fishbone -i data.csv -o timeline.tex --smart-spacing --max-lines 2

# Using configuration file
timeline-fishbone -i data.csv -c config.yaml -o timeline.tex

# Custom colors and styling
timeline-fishbone -i data.csv -o timeline.tex \
    --color-single "blue!30" \
    --color-multi "red!25" \
    --node-font "\\small\\bfseries"

# Validate data file
timeline-fishbone --validate my_data.csv
```

### Python API

```python
from timeline_fishbone import generate_timeline, create_sample_data

# Create sample data
create_sample_data("my_data.csv")

# Generate timeline
latex_code = generate_timeline(
    input_file="my_data.csv",
    output_file="timeline.tex",
    layout__smart_spacing=True,
    visual__max_lines=2
)

# Get LaTeX code without saving
latex_code = generate_timeline("my_data.csv")
print(latex_code)
```

### Advanced Programmatic Usage

```python
from timeline_fishbone.core import (
    TimelineFishboneConfig,
    LaTeXGenerator,
    DataValidator
)

# Load and customize configuration
config = TimelineFishboneConfig.from_yaml("config.yaml")
config.layout.smart_spacing = True
config.colors.color_single = "teal!25"

# Load and validate data
df = DataValidator.load_and_validate("data.csv")

# Generate LaTeX
generator = LaTeXGenerator(
    config.layout,
    config.time_logic,
    config.visual,
    config.colors,
    config.arrows,
    config.output
)
latex_code = generator.generate(df)

# Save configuration for reuse
config.save_yaml("my_config.yaml")
```

## Configuration

### Configuration File Example (YAML)

```yaml
layout:
  timeline_width: "16cm"
  year_spacing: 2.7
  branch_distance: 1.2
  smart_spacing: true

time_logic:
  time_direction: "right"
  upper_years: "odd"  # or "even" or "2019,2021,2023"

visual:
  node_width: "2.6cm"
  max_lines: 2
  node_font: "\\tiny\\bfseries"

colors:
  color_single: "cyan!20"
  color_multi: "green!20"
  color_adaptive: "yellow!40"

output:
  show_legend: true
  caption: "Timeline Fishbone Diagram"
```

### Configuration Hierarchy

1. Default values
2. Configuration file (YAML/JSON)
3. Command-line arguments / API parameters

## Data Format

### CSV Format

Your CSV file must contain these columns:

| Column | Description | Example |
| -------- | ------------- | --------- |
| 年份 | Year (integer) | 2020 |
| 种类 | Category | singleproto, multiproto, adaptive, vl, dense, attention, hybrid |
| 方法名 | Method name | PANet |
| 引用标识 | Citation key | Wang2019PANet |

### Example CSV

```csv
年份,种类,方法名,引用标识
2019,singleproto,PANet,Wang2019PANet
2020,multiproto,PPNet,Liu2020PPNet
2021,adaptive,ASGNet,Li2021ASGNet
```

### Valid Categories

- `singleproto` - Single prototype methods (cyan)
- `multiproto` - Multi-prototype methods (green)
- `adaptive` - Adaptive methods (yellow)
- `vl` - Vision-language methods (purple)
- `dense` - Dense matching (orange)
- `attention` - Attention-based (red)
- `hybrid` - Hybrid refinement (gray)

## Command Line Interface

```plaintext
usage: timeline-fishbone [-h] [--version] [--create-sample FILE] 
                        [--validate FILE] [-i INPUT_FILE] [-o OUTPUT]
                        [-c CONFIG_FILE] [OPTIONS...]

Options:
  -i, --input FILE          Input CSV or JSON file
  -o, --output FILE         Output LaTeX file (default: timeline.tex)
  -c, --config FILE         Configuration file (YAML/JSON)
  
  --create-sample FILE      Create sample CSV and exit
  --validate FILE           Validate data file and exit
  
  --smart-spacing           Enable smart spacing adjustment
  --max-lines {1,2}         Maximum lines per node
  --time-direction {left,right}
  --upper-years RULE        Upper branch rule: odd, even, or years
  
  --color-single COLOR      Single-prototype color
  --color-multi COLOR       Multi-prototype color
  ... (see --help for all options)
  
  -v, --verbose            Verbose output
  -q, --quiet              Suppress output except errors
```

## API Documentation

### High-level Functions

#### `generate_timeline()`

```python
def generate_timeline(
    input_file: Union[str, Path],
    output_file: Optional[Union[str, Path]] = None,
    config_file: Optional[Union[str, Path]] = None,
    **kwargs
) -> str:
    """Generate timeline from data file.
    
    Args:
        input_file: Path to CSV/JSON data
        output_file: Optional output path for LaTeX
        config_file: Optional YAML/JSON config
        **kwargs: Config overrides (e.g., layout__smart_spacing=True)
    
    Returns:
        Generated LaTeX code
    """
```

#### `create_sample_data()`

```python
def create_sample_data(output_file: Union[str, Path] = "sample_data.csv") -> None:
    """Create sample CSV data file."""
```

### Core Classes

- **`TimelineFishboneConfig`** - Main configuration container
- **`DataValidator`** - Data validation and loading
- **`SmartLayoutEngine`** - Intelligent layout calculation
- **`LaTeXGenerator`** - LaTeX code generation

See [docs/api_reference.md](docs/api_reference.md) and [docs/index.md](docs/index.md) for documentation entry points.

## Development

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=timeline_fishbone --cov-report=html

# Run specific test file
pytest tests/test_config.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/
```

## LaTeX Requirements

Your LaTeX document needs these packages:

```latex
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, backgrounds, matrix}
\usepackage{adjustbox}
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code (`black`, `isort`)
7. Commit changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by academic timeline visualization needs
- Built with modern Python best practices
- Community feedback and contributions

## Contact

- GitHub Issues: [Timeline Fishbone Issues](https://github.com/tyeclipse/timeline-fishbone/issues)
- Documentation: [Read the Docs](https://timeline-fishbone.readthedocs.io)

## Roadmap

- [ ] PDF/PNG export via matplotlib
- [ ] Interactive web preview
- [ ] Template system for different styles
- [ ] Batch processing support
- [ ] Docker container
- [ ] VS Code extension

---

Made with ❤️ for researchers and LaTeX enthusiasts
