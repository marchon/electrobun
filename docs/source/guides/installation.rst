Installation
============

This guide covers the installation of Electrobun for development.

Prerequisites
-------------

Before installing Electrobun, ensure you have the following installed:

- **Bun** >= 1.3.9 (https://bun.sh)
- **Zig** >= 0.13.0 (https://ziglang.org)
- **CMake** >= 3.20
- **Python 3** >= 3.9

See :doc:`../reference/system-requirements` for detailed system requirements.

Quick Install
-------------

Install via npm/bun:

.. code-block:: bash

   bun install electrobun

Or using npm:

.. code-block:: bash

   npm install electrobun

Development Setup
-----------------

Clone the repository:

.. code-block:: bash

   git clone --recurse-submodules https://github.com/blackboardsh/electrobun.git
   cd electrobun/package

Install dependencies:

.. code-block:: bash

   bun install

Build the project:

.. code-block:: bash

   bun dev

Platform-Specific Setup
-----------------------

macOS
~~~~~

Install Xcode Command Line Tools:

.. code-block:: bash

   xcode-select --install

Optional: Install CMake via Homebrew:

.. code-block:: bash

   brew install cmake

Windows
~~~~~~~

1. Install Visual Studio 2022 with C++ development tools
2. Install CMake (https://cmake.org/download/)
3. Windows SDK is included with Visual Studio

Linux (Ubuntu/Debian)
~~~~~~~~~~~~~~~~~~~~~

Install system dependencies:

.. code-block:: bash

   sudo apt update
   sudo apt install build-essential cmake pkg-config \
     libgtk-3-dev libwebkit2gtk-4.1-dev \
     libayatana-appindicator3-dev librsvg2-dev

Verification
------------

Verify your installation:

.. code-block:: bash

   bun run electrobun --version

Run the kitchen sink demo:

.. code-block:: bash

   cd package
   bun dev

Troubleshooting
---------------

Build fails with "CMake not found"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CMake will be auto-vendored on first build, or install it manually:

.. code-block:: bash

   # macOS
   brew install cmake
   
   # Windows
   # Download from https://cmake.org/download/
   
   # Ubuntu/Debian
   sudo apt install cmake

FFI errors on Linux
~~~~~~~~~~~~~~~~~~~

Ensure all native libraries are installed:

.. code-block:: bash

   sudo apt install libgtk-3-dev libwebkit2gtk-4.1-dev

CEF download fails
~~~~~~~~~~~~~~~~~~

Delete the cache and retry:

.. code-block:: bash

   rm -rf vendors/cef
   bun dev

Next Steps
----------

- :doc:`quickstart` - Create your first Electrobun app
- :doc:`project-structure` - Understand the project layout
- :doc:`architecture` - Learn about Electrobun's architecture
