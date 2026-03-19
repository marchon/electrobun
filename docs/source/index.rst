Electrobun Documentation
========================

**Electrobun** is a complete solution-in-a-box for building, updating, and shipping ultra-fast, tiny, cross-platform desktop applications written in TypeScript.

.. image:: https://img.shields.io/badge/platform-macos%20%7C%20windows%20%7C%20linux-blue
   :target: #
   :alt: Platforms

.. image:: https://img.shields.io/badge/bundle%20size-~12MB-green
   :target: #
   :alt: Bundle Size

.. image:: https://img.shields.io/badge/license-MIT-yellow
   :target: #
   :alt: License

----

Key Features
------------

- **Tiny Bundles**: ~12MB self-extracting apps (mostly Bun runtime when using system webview)
- **Small Updates**: As small as 14KB using bsdiff for delta patches
- **Cross-Platform**: macOS 14+, Windows 11+, Ubuntu 22.04+
- **TypeScript-First**: Write your entire app in TypeScript
- **Native WebViews**: Uses platform-native webviews (WebKit, WebView2, GTKWebKit)
- **WebGPU Support**: GPU-native rendering with Dawn/WebGPU
- **Auto-Updates**: Built-in delta update system
- **Type-Safe RPC**: Encrypted communication between Bun and webviews

----

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   guides/installation
   guides/quickstart
   guides/project-structure

.. toctree::
   :maxdepth: 2
   :caption: Core Concepts

   guides/architecture
   guides/window-management
   guides/webview-communication
   guides/rpc-system
   guides/events

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   reference/browser-window
   reference/browser-view
   reference/gpu-window
   reference/tray
   reference/menus
   reference/updater
   reference/utils

.. toctree::
   :maxdepth: 2
   :caption: Configuration

   reference/electrobun-config
   reference/build-config

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics

   guides/webgpu
   guides/cef-integration
   guides/auto-updates
   guides/code-signing

.. toctree::
   :maxdepth: 2
   :caption: Development

   guides/build-system
   guides/testing
   guides/contributing

.. toctree::
   :maxdepth: 2
   :caption: Resources

   reference/requirements
   reference/system-requirements
   reference/rollout-plan
   reference/changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
