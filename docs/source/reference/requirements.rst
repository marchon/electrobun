Requirements
============

This page lists all dependencies required for building and running Electrobun applications.

Core Runtime Dependencies
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Dependency
     - Version
     - Notes
   * - Bun
     - >= 1.3.9
     - JavaScript/TypeScript runtime
   * - Zig
     - >= 0.13.0
     - Native code compilation
   * - Node.js
     - >= 18.0.0
     - CLI tooling (optional but recommended)

Build Dependencies
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Dependency
     - Version
     - Notes
   * - CMake
     - >= 3.20
     - Build system generator
   * - Make
     - >= 4.0
     - Build automation
   * - Python 3
     - >= 3.9
     - Build scripts

Platform-Specific Dependencies
------------------------------

macOS
~~~~~

.. code-block:: bash

   # Xcode Command Line Tools
   xcode-select --install
   
   # Or via Homebrew
   brew install cmake

Requirements:

- Xcode Command Line Tools >= 15.0
- Apple Clang >= 15.0
- macOS SDK >= 14.0

Windows
~~~~~~~

Requirements:

- Visual Studio 2022 (Community edition or higher)
- Windows SDK >= 10.0.22621.0
- WebView2 Runtime (included in Windows 11, optional for Windows 10)

Linux (Ubuntu/Debian)
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   sudo apt install build-essential cmake pkg-config \
     libgtk-3-dev libwebkit2gtk-4.1-dev \
     libayatana-appindicator3-dev librsvg2-dev

Requirements:

- libgtk-3-dev >= 3.24
- libwebkit2gtk-4.1-dev >= 2.40
- libayatana-appindicator3-dev >= 0.5
- librsvg2-dev >= 2.50
- pkg-config >= 0.29

Optional Dependencies
---------------------

CEF Support
~~~~~~~~~~~

For Chromium Embedded Framework support:

- CEF Binary Distribution >= 145.0.23

WebGPU Support
~~~~~~~~~~~~~~

For GPU-native rendering:

- Dawn/WebGPU >= 0.2.0

Code Signing (macOS)
~~~~~~~~~~~~~~~~~~~~

- ``codesign`` (included with Xcode)
- ``notarytool`` (included with Xcode >= 13)

NPM Dependencies
----------------

These are automatically installed via ``bun install``:

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Package
     - Version
     - Purpose
   * - TypeScript
     - >= 5.0
     - Type checking
   * - @types/bun
     - >= 1.0
     - Bun type definitions
   * - Three.js
     - >= 0.160
     - 3D graphics (optional)
   * - @babylonjs/core
     - >= 7.0
     - Alternative 3D engine (optional)

Python Virtual Environment
--------------------------

For documentation building:

.. code-block:: bash

   cd docs
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt

See :doc:`system-requirements` for hardware and OS requirements.
