Changelog
=========

All notable changes to Electrobun will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

Added
~~~~~

- Initial public release preparation
- Comprehensive documentation site

Changed
~~~~~~~

- N/A

Deprecated
~~~~~~~~~~

- N/A

Removed
~~~~~~~

- N/A

Fixed
~~~~~

- N/A

Security
~~~~~~~~

- N/A

[1.0.0] - 2024-Q4 (Target)
--------------------------

Added
~~~~~

- Core windowing API (BrowserWindow, GpuWindow)
- WebView management (BrowserView, WGPUView)
- System tray support
- Native menu bars (ApplicationMenu, ContextMenu)
- Global keyboard shortcuts
- File dialogs and native pickers
- Auto-update system with delta patches
- WebGPU support via Dawn
- Three.js and Babylon.js integration
- Type-safe RPC with AES-GCM encryption
- Multi-platform build system (macOS, Windows, Linux)
- CEF integration for all platforms
- Code signing and notarization support
- ASAR packaging
- Complete TypeScript API

Changed
~~~~~~~

- N/A (initial release)

[0.9.0] - Beta Release
----------------------

Added
~~~~~

- Beta API stabilization
- Kitchen sink test application
- Complete test framework
- Documentation site

[0.5.0] - Alpha Release
-----------------------

Added
~~~~~

- Alpha API for testing
- Basic window and webview support
- macOS and Windows support
- Initial Linux support

Release Schedule
----------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Version
     - Target Date
     - Status
   * - 0.5.0 (Alpha)
     - Q3 2024
     - Released
   * - 0.9.0 (Beta)
     - Q4 2024
     - In Progress
   * - 1.0.0 (Stable)
     - Q4 2024 / Q1 2025
     - Planned
   * - 1.1.0
     - Q2 2025
     - Planned
   * - 2.0.0
     - Q4 2025
     - Planned

Versioning Policy
-----------------

Electrobun follows `Semantic Versioning <https://semver.org/>`_:

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

Pre-release versions use the following format:

- ``1.0.0-alpha.1`` - Alpha releases
- ``1.0.0-beta.1`` - Beta releases
- ``1.0.0-rc.1`` - Release candidates

LTS Releases
~~~~~~~~~~~~

Even-numbered minor versions (1.0, 1.2, 1.4, etc.) will receive long-term support:

- 12 months of bug fixes
- 6 months of security updates after next LTS release

See Also
--------

- :doc:`rollout-plan` - Detailed rollout timeline
- `GitHub Releases <https://github.com/blackboardsh/electrobun/releases>`_ - Release notes
