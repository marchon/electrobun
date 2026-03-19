# Electrobun Documentation

This directory contains the Sphinx documentation for Electrobun.

## Setup

```bash
# Create virtual environment
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install TypeDoc (for TypeScript API docs)
npm install -g typedoc
```

## Building Documentation

```bash
# Build HTML docs
make html

# Build with live reload (for development)
make livehtml

# Clean build
make clean

# Check all external links
make links

# Quick build (no warnings)
make quick

# Production build (strict)
make prod
```

## Documentation Structure

```
source/
├── index.rst                 # Main documentation entry point
├── conf.py                   # Sphinx configuration
├── guides/                   # User guides
│   ├── installation.rst
│   ├── quickstart.rst
│   ├── project-structure.rst
│   ├── architecture.rst
│   ├── window-management.rst
│   ├── webview-communication.rst
│   ├── rpc-system.rst
│   ├── events.rst
│   ├── webgpu.rst
│   ├── cef-integration.rst
│   ├── auto-updates.rst
│   ├── code-signing.rst
│   ├── build-system.rst
│   ├── testing.rst
│   └── contributing.rst
├── reference/                # API reference
│   ├── requirements.rst
│   ├── system-requirements.rst
│   ├── rollout-plan.rst
│   ├── changelog.rst
│   ├── electrobun-config.rst
│   ├── build-config.rst
│   ├── browser-window.rst
│   ├── browser-view.rst
│   ├── gpu-window.rst
│   ├── tray.rst
│   ├── menus.rst
│   ├── updater.rst
│   └── utils.rst
└── _static/                  # Static assets
```

## Adding New Pages

1. Create `.rst` file in appropriate directory
2. Add to `index.rst` toctree
3. Run `make html` to verify

## Markdown Support

This documentation uses MyST parser which allows Markdown syntax in `.md` files:

```bash
# Create a Markdown file
touch source/guides/my-guide.md
```

Then add it to the toctree in `index.rst`.

## TypeScript API Documentation

To generate TypeScript API docs:

1. Enable `sphinx_js` in `source/conf.py`
2. Ensure TypeDoc is installed: `npm install -g typedoc`
3. Configure `js_source_path` in `conf.py`
4. Build: `make html`

## Deployment

The built documentation is in `build/html/` and can be deployed to:

- GitHub Pages
- Read the Docs
- Netlify
- Any static hosting

## License

Same as Electrobun project (MIT).
