# Timeline Fishbone Generator - Project Structure

## 📁 Complete Project Structure

```
timeline-fishbone-generator/
├── .github/
│   └── workflows/
│       ├── test.yml              # CI: Testing and linting workflow
│       └── release.yml            # CD: PyPI publishing workflow
│
├── src/
│   └── timeline_fishbone/
│       ├── __init__.py            # Package initialization & exports
│       ├── cli.py                 # Command-line interface
│       ├── utils.py               # High-level utility functions
│       ├── py.typed               # PEP 561 type checking marker
│       └── core/
│           ├── __init__.py        # Core module exports
│           ├── config.py          # Configuration management
│           ├── validator.py       # Data validation
│           ├── layout_engine.py   # Smart layout engine
│           └── latex_generator.py # LaTeX TikZ code generator
│
├── tests/
│   ├── __init__.py
│   ├── test_config.py             # Configuration tests
│   ├── test_validator.py          # Validation tests
│   ├── test_layout.py             # Layout engine tests
│   ├── test_generator.py          # Generator tests
│   └── test_integration.py        # End-to-end tests
│
├── examples/
│   ├── sample_data.csv            # Example data file
│   ├── sample_config.yaml         # Example configuration
│   ├── basic_usage.py             # Basic usage examples
│   └── advanced_usage.py          # Advanced usage examples
│
├── docs/
│   ├── index.md                   # Documentation home
│   ├── quickstart.md              # Quick start guide
│   ├── api_reference.md           # API documentation
│   └── advanced_features.md       # Advanced features guide
│
├── scripts/
│   ├── install_deps.sh            # Dependency installation script
│   ├── build_docs.sh              # Documentation building script
│   └── release.py                 # Release automation script
│
├── pyproject.toml                 # Modern Python project configuration
├── setup.py                       # Backward compatibility setup
├── requirements.txt               # Production dependencies
├── requirements-dev.txt           # Development dependencies
├── README.md                      # Project README
├── LICENSE                        # MIT License
├── CONTRIBUTING.md                # Contribution guidelines
├── CHANGELOG.md                   # Version history
├── MANIFEST.in                    # Package data manifest
└── .gitignore                     # Git ignore rules
```

## 🔑 Key Components

### Core Modules

#### `config.py` (10.4 KB)
- **LayoutConfig**: Layout parameters (spacing, dimensions)
- **TimeLogicConfig**: Time direction and year placement rules
- **VisualConfig**: Visual styling (fonts, colors, sizes)
- **ColorConfig**: Color scheme for categories
- **ArrowConfig**: Arrow and connection styling
- **OutputConfig**: Output formatting options
- **TimelineFishboneConfig**: Main configuration container
- **load_config()**: Configuration loading with YAML/JSON support

#### `validator.py` (6.6 KB)
- **DataValidator**: CSV/JSON data validation
- **ValidationError**: Custom exception for validation errors
- **validate_file()**: File validation convenience function
- Comprehensive validation of required columns, data types, and values

#### `layout_engine.py` (6.1 KB)
- **SmartLayoutEngine**: Intelligent layout calculation
- Automatic spacing adjustment based on node density
- Year position calculation
- Side determination (above/below timeline)
- Node distribution analysis

#### `latex_generator.py` (14.9 KB)
- **LaTeXGenerator**: Complete LaTeX TikZ code generation
- Section generators:
  - Preamble and document structure
  - TikZ style definitions
  - Timeline axis and coordinates
  - Method nodes (single/matrix layouts)
  - Background connections
  - Year nodes
  - Legend and caption
- Multi-line text formatting support

### CLI & Utilities

#### `cli.py`
- Comprehensive argparse-based CLI
- 50+ command-line options
- Configuration file support
- Sample data creation
- Data validation mode
- Logging and error handling

#### `utils.py`
- **generate_timeline()**: High-level generation function
- **create_sample_data()**: Sample CSV generator
- **validate_data_file()**: Validation utility
- **setup_logging()**: Logging configuration

### Testing Suite (>85% coverage)

- **test_config.py**: Configuration classes and serialization
- **test_validator.py**: Data validation edge cases
- **test_layout.py**: Layout engine calculations
- **test_generator.py**: LaTeX generation
- **test_integration.py**: End-to-end workflows

## 🚀 Installation & Usage

### Quick Install
```bash
cd timeline-fishbone-generator
pip install -e .
```

### Development Install
```bash
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest --cov=timeline_fishbone --cov-report=html
```

### Generate Sample Timeline
```bash
timeline-fishbone --create-sample data.csv
timeline-fishbone -i data.csv -o timeline.tex --smart-spacing
```

## 📊 Code Statistics

| Component | Files | Lines | Features |
|-----------|-------|-------|----------|
| Core | 5 | ~1,500 | Config, Validation, Layout, Generation |
| CLI | 1 | ~400 | Full arg parsing, logging |
| Utils | 1 | ~150 | High-level API |
| Tests | 5 | ~800 | Comprehensive coverage |
| Examples | 4 | ~200 | Usage demonstrations |
| Docs | 4+ | ~1,000 | Complete documentation |

## 🔧 Development Workflow

### Code Quality Tools
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing with coverage

### CI/CD
- **GitHub Actions**: Automated testing on push/PR
- **Multi-platform**: Linux, macOS, Windows
- **Multi-version**: Python 3.8, 3.9, 3.10, 3.11, 3.12
- **Codecov**: Coverage tracking
- **Automated Release**: PyPI publishing on tag

## 📦 Package Features

### CLI Features
- ✅ CSV/JSON input
- ✅ YAML/JSON configuration files
- ✅ Smart spacing adjustment
- ✅ Customizable colors and styles
- ✅ Multi-line node support
- ✅ Legend generation
- ✅ Data validation
- ✅ Sample data creation

### API Features
- ✅ Programmatic configuration
- ✅ Configuration merging
- ✅ Direct generator access
- ✅ Type hints throughout
- ✅ Comprehensive error handling
- ✅ Logging support

### Build Features
- ✅ Modern pyproject.toml
- ✅ Backward compatible setup.py
- ✅ PEP 561 type marker
- ✅ MANIFEST.in for data files
- ✅ Install from source or PyPI

## 🎯 Design Principles

1. **Modularity**: Clean separation of concerns
2. **Extensibility**: Easy to add new features
3. **Testability**: Comprehensive test coverage
4. **Documentation**: Well-documented code and APIs
5. **Usability**: Both CLI and Python API
6. **Standards**: Follow Python best practices

## 🔄 Version Management

- **Version**: 0.1.0 (initial release)
- **Versioning**: Semantic Versioning (SemVer)
- **Changelog**: CHANGELOG.md tracks all changes
- **Release Script**: Automated version bumping

## 📝 License

MIT License - See LICENSE file for details

---

**Project Status**: ✅ Production Ready  
**Test Coverage**: ✅ >85%  
**Documentation**: ✅ Complete  
**CI/CD**: ✅ Configured  
**Type Hints**: ✅ Full Coverage
