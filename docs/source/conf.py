# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from pathlib import Path

# -- Path setup --------------------------------------------------------------
# Add project root to path for autodoc
sys.path.insert(0, os.path.abspath('../../package'))

# -- Project information -----------------------------------------------------
project = 'Electrobun'
copyright = '2026, Electrobun Team'
author = 'Electrobun Team'
release = '1.0.0'
version = '1.0.0'

# -- General configuration ---------------------------------------------------

extensions = [
    # Core Sphinx
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    
    # Markdown support
    'myst_parser',
    
    # TypeScript/JavaScript (requires typedoc setup)
    # 'sphinx_js',  # Enable when TypeScript API docs are ready
    
    # Type hints
    'sphinx_autodoc_typehints',
    
    # UX improvements
    'sphinx_copybutton',
    'sphinx_togglebutton',
    
    # Diagrams
    'sphinxcontrib.mermaid',
    
    # Versioning
    'sphinx_multiversion',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'env',
    'venv',
]

# The suffix(es) of source filenames.
source_suffix = {
    '.rst': None,
    '.md': 'markdown',
}

# The master toctree document.
master_doc = 'index'

language = 'en'

# -- MyST Parser configuration -----------------------------------------------
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_heading_anchors = 4

# -- sphinx-js configuration -------------------------------------------------
js_language = 'typescript'
js_source_path = '../../package/src'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_extra_path = []

# Theme options
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
}

html_title = 'Electrobun Documentation'
html_short_title = 'Electrobun'
html_logo = ''
html_favicon = ''

# -- Options for linkcheck ---------------------------------------------------
linkcheck_ignore = [
    r'http://localhost:\d+/',
]
linkcheck_timeout = 30

# -- Options for todo extension ----------------------------------------------
todo_include_todos = True

# -- sphinx-multiversion configuration ---------------------------------------
smv_tag_whitelist = r'^v\d+\.\d+\.\d+$'  # Only tags matching vX.Y.Z
smv_branch_whitelist = r'^(main|master)$'  # Only main/master branches
smv_remote_whitelist = r'^(origin|upstream)$'
smv_outputdir_format = '{ref.name}'
smv_prefer_remote_refs = True

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'bun': ('https://bun.sh/docs', None),
}

# -- Autodoc configuration ---------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'

# -- Copybutton configuration ------------------------------------------------
copybutton_prompt_text = r'>>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: '
copybutton_prompt_is_regexp = True
copybutton_copy_empty_lines = True
copybutton_line_continuation_character = '\\'
copybutton_here_doc_delimiter = 'EOF'

# -- Mermaid configuration ---------------------------------------------------
# Use inline mermaid.js (no CLI required)
mermaid_version = 'latest'
mermaid_output_format = 'raw'
mermaid_params = []

# -- Custom setup ------------------------------------------------------------
def setup(app):
    app.add_config_value('recommonmark_config', {
        'auto_toc_tree_section': 'Contents',
    }, True)
