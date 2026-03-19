System Requirements
===================

Development Machine
-------------------

.. list-table:: Development Machine Requirements
   :header-rows: 1
   :widths: 30 35 35

   * - Component
     - Minimum
     - Recommended
   * - CPU
     - x86_64 or ARM64
     - Apple Silicon M1+ / Intel i5+
   * - RAM
     - 8 GB
     - 16 GB+
   * - Disk Space
     - 10 GB free
     - 25 GB+ free
   * - OS
     - macOS 14 / Windows 11 / Ubuntu 22.04
     - Latest stable OS version
   * - Network
     - Broadband (initial setup)
     - High-speed (for CEF downloads)

Target Runtime (End User)
-------------------------

.. list-table:: End User Requirements
   :header-rows: 1
   :widths: 20 25 25 15 15

   * - Platform
     - Minimum Version
     - Architecture
     - RAM
     - Notes
   * - macOS
     - 14.0 (Sonoma)
     - x86_64, ARM64
     - 4 GB
     - WebKit native, CEF optional
   * - Windows
     - 11 (22H2)
     - x86_64
     - 4 GB
     - WebView2 native, CEF optional
   * - Linux
     - Ubuntu 22.04 LTS
     - x86_64, ARM64
     - 4 GB
     - GTKWebKit native, CEF optional

GPU Requirements
----------------

Standard Apps
~~~~~~~~~~~~~

- Any GPU with basic WebGL support
- Integrated graphics sufficient

WebGPU Apps
~~~~~~~~~~~

- **Windows**: DirectX 12 capable GPU
- **macOS**: Metal capable GPU (Apple Silicon or Intel with Metal)
- **Linux**: Vulkan capable GPU

CEF Renderer
~~~~~~~~~~~~

- GPU acceleration optional but recommended
- Falls back to software rendering if GPU unavailable

Display Requirements
--------------------

- **Minimum Resolution**: 1024x768
- **Recommended**: 1920x1080 or higher
- **High DPI**: Automatic scaling included

Platform-Specific Notes
-----------------------

macOS
~~~~~

- Rosetta 2 required for x86_64 apps on Apple Silicon (if not using universal binary)
- App must be in ``/Applications`` for some features (URL schemes, notifications)
- Gatekeeper may require notarization for distribution

Windows
~~~~~~~

- WebView2 Runtime required (auto-installed on Windows 11)
- Windows 10 22H2 supported but WebView2 must be manually installed
- Defender SmartScreen may flag unsigned binaries

Linux
~~~~~

- GTK 3.24+ required
- WebKit2GTK 4.1+ required
- AppIndicator support for system tray
- May require additional libraries on non-Ubuntu distributions

Network Requirements
--------------------

Development
~~~~~~~~~~~

- Internet connection for initial setup
- Git access for cloning repositories
- npm/bun registry access for dependencies
- GitHub releases access for CEF/WebGPU binaries

Runtime
~~~~~~~

- Optional: Internet for auto-updates
- Optional: Analytics/telemetry (configurable)
- Apps work offline by default

Disk Space Breakdown
--------------------

Typical app bundle sizes:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Component
     - Native Renderer
     - With CEF
   * - Bun Runtime
     - ~10 MB
     - ~10 MB
   * - Native Wrapper
     - ~2 MB
     - ~2 MB
   * - CEF (optional)
     - -
     - ~100-150 MB
   * - WebGPU/Dawn (optional)
     - ~5 MB
     - ~5 MB
   * - App Code
     - Variable
     - Variable
   * - **Total**
     - **~12-15 MB**
     - **~120-170 MB**

See Also
--------

- :doc:`requirements` - Software dependencies
- :doc:`installation` - Installation guide
