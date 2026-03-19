# Electrobun - AI Agent Guide

This document provides essential information for AI coding agents working on the Electrobun project.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Requirements](#requirements)
   - [Requirements.txt](#requirementstxt)
   - [Minimum System Requirements](#minimum-system-requirements)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Build System](#build-system)
6. [Core APIs](#core-apis)
   - [Main Process (Bun)](#main-process-bun)
   - [Browser/Webview](#browserwebview)
   - [RPC System](#rpc-system)
   - [Events](#events)
7. [Module Reference](#module-reference)
   - [Window Management](#window-management)
   - [WebView Management](#webview-management)
   - [GPU/Graphics](#gpugraphics)
   - [System Integration](#system-integration)
   - [Utilities](#utilities)
8. [Configuration](#configuration)
9. [Testing](#testing)
10. [Security](#security)
11. [Development Conventions](#development-conventions)
12. [Roll Out Plan](#roll-out-plan)
13. [Important Notes](#important-notes)

---

## Project Overview

**Electrobun** is a complete solution-in-a-box for building, updating, and shipping ultra-fast, tiny, cross-platform desktop applications written in TypeScript. It enables developers to write desktop apps using web technologies while maintaining a native look and feel.

### Key Characteristics

- **Technology Stack**: TypeScript, Bun, Zig, CEF (Chromium Embedded Framework), WebKit/WebView2/GTKWebKit
- **Bundle Size**: ~12MB self-extracting apps (mostly Bun runtime when using system webview)
- **Update Size**: As small as 14KB using bsdiff for delta patches
- **Cross-Platform**: macOS 14+, Windows 11+, Ubuntu 22.04+ (with community support for other Linux distros)

---

## Requirements

### Requirements.txt

The following dependencies are required for building and running Electrobun:

**Core Runtime Dependencies:**
```
bun >= 1.3.9
zig >= 0.13.0
nodejs >= 18.0.0 (for CLI tooling)
```

**Build Dependencies:**
```
cmake >= 3.20
make >= 4.0
python3 >= 3.9
```

**Platform-Specific Dependencies:**

*macOS:*
```
Xcode Command Line Tools >= 15.0
Apple Clang >= 15.0
```

*Windows:*
```
Visual Studio 2022 (Community or higher)
Windows SDK >= 10.0.22621.0
WebView2 Runtime (included in Windows 11, optional install for Windows 10)
```

*Linux:*
```
libgtk-3-dev >= 3.24
libwebkit2gtk-4.1-dev >= 2.40
libayatana-appindicator3-dev >= 0.5
librsvg2-dev >= 2.50
pkg-config >= 0.29
```

**Optional Dependencies:**
```
# For CEF support
CEF Binary Distribution >= 145.0.23

# For WebGPU support
Dawn/WebGPU >= 0.2.0

# For code signing (macOS)
_codesign (included with Xcode)

# For notarization (macOS)
altool or notarytool (included with Xcode >= 13)
```

**NPM Dependencies** (auto-installed via `bun install`):
See `package/package.json` for full dependency tree. Key dependencies include:
- `typescript` >= 5.0
- `@types/bun` >= 1.0
- `three` >= 0.160 (for 3D graphics)
- `@babylonjs/core` >= 7.0 (alternative 3D engine)

---

### Minimum System Requirements

**Development Machine:**

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | x86_64 or ARM64 | Apple Silicon M1+ / Intel i5+ |
| RAM | 8 GB | 16 GB+ |
| Disk Space | 10 GB free | 25 GB+ free |
| OS | macOS 14 / Windows 11 / Ubuntu 22.04 | Latest stable OS version |
| Network | Broadband (for initial setup) | High-speed (for CEF downloads) |

**Target Runtime (End User):**

| Platform | Minimum Version | CPU Architecture | RAM | Notes |
|----------|----------------|------------------|-----|-------|
| macOS | 14.0 (Sonoma) | x86_64, ARM64 | 4 GB | WebKit native, CEF optional |
| Windows | 11 (22H2) | x86_64 | 4 GB | WebView2 native, CEF optional |
| Linux | Ubuntu 22.04 LTS | x86_64, ARM64 | 4 GB | GTKWebKit native, CEF optional |

**GPU Requirements:**
- **Standard Apps**: Any GPU with basic WebGL support
- **WebGPU Apps**: DirectX 12 (Windows), Metal (macOS), or Vulkan (Linux)
- **CEF Renderer**: GPU acceleration optional but recommended

**Display Requirements:**
- Minimum resolution: 1024x768
- Recommended: 1920x1080 or higher
- High DPI support included (scales automatically)

---

## Technology Stack

### Runtime Architecture

1. **Main Process**: Bun runtime executes TypeScript
2. **Webviews**: Platform-native webviews (WebKit on macOS, WebView2 on Windows, GTKWebKit on Linux) or optional CEF
3. **Native Layer**: Zig/C++ bindings for platform APIs via FFI
4. **Communication**: WebSocket-based RPC with AES-GCM encryption between bun and webview

### Version Constants

Key versions are defined in:
- `package/src/shared/bun-version.ts` - Bun runtime version (currently 1.3.9)
- `package/src/shared/cef-version.ts` - CEF version (currently 145.0.23+g3e7fe1c, Chromium 145.0.7632.68)
- `package/src/shared/electrobun-version.ts` - Electrobun version (from package.json)

### Native Wrappers

| Platform | WebView Engine | File | Notes |
|----------|---------------|------|-------|
| macOS | WebKit (CEF optional) | `libNativeWrapper.dylib` | Weak linking to CEF framework |
| Windows | WebView2 (CEF optional) | `libNativeWrapper.dll` | Runtime CEF detection |
| Linux | GTKWebKit | `libNativeWrapper.so` | GTK-only, no CEF |
| Linux | CEF | `libNativeWrapper_cef.so` | CEF-enabled variant |

Linux uses dual binaries because weak linking isn't reliable on Linux.

---

## Project Structure

```
electrobun/
├── package/                    # Main Electrobun npm package source
│   ├── src/
│   │   ├── bun/               # Main process TypeScript APIs
│   │   │   ├── core/          # Core classes (BrowserWindow, BrowserView, Tray, etc.)
│   │   │   ├── events/        # Event system (ApplicationEvents, WindowEvents, etc.)
│   │   │   ├── preload/       # Preload scripts injected into webviews
│   │   │   └── proc/          # Native process bindings (native.ts with FFI)
│   │   ├── browser/           # Webview/browser-side APIs
│   │   ├── cli/               # CLI implementation (index.ts - ~4800 lines)
│   │   ├── native/            # Platform-specific native code
│   │   │   ├── macos/         # macOS native wrapper (Objective-C++)
│   │   │   ├── win/           # Windows native wrapper (C++)
│   │   │   ├── linux/         # Linux native wrapper (C++)
│   │   │   └── shared/        # Shared native headers
│   │   ├── launcher/          # Zig launcher for self-extracting apps
│   │   ├── extractor/         # Self-extractor implementation (Zig)
│   │   └── shared/            # Shared TypeScript utilities
│   ├── build.ts               # Main build script (~2000+ lines)
│   └── package.json
├── kitchen/                    # Integration test app (Kitchen Sink)
│   ├── src/
│   │   ├── bun/               # Kitchen sink main process
│   │   ├── tests/             # Automated and interactive tests
│   │   └── playgrounds/       # Feature demonstration apps
│   └── electrobun.config.ts   # Example config with all features
├── bunny/                      # Bunny ecosystem (IDE and extensions)
│   ├── ears/                  # Bunny Ears - extensibility system
│   ├── dash/                  # Bunny Dash - IDE/editor
│   └── foundation-carrots/    # Built-in extensions
├── templates/                  # Starter templates for new apps
│   ├── hello-world/           # Minimal example
│   ├── react-tailwind-vite/   # React template
│   ├── svelte/                # Svelte template
│   ├── vue/                   # Vue template
│   ├── wgpu/                  # WebGPU examples
│   └── ...                    # More templates
└── .github/workflows/          # CI/CD workflows
    └── release.yml             # Build and release workflow
```

---

## Build System

### Prerequisites

**macOS:**
- Xcode command line tools (`xcode-select --install`)
- cmake (`brew install cmake`) - or it will be auto-vendored

**Windows:**
- Visual Studio 2022 with C++ development tools
- cmake

**Linux:**
```bash
sudo apt install build-essential cmake pkg-config \
  libgtk-3-dev libwebkit2gtk-4.1-dev \
  libayatana-appindicator3-dev librsvg2-dev
```

### Build Commands

All commands are run from the `/package` directory:

```bash
# Development build and run kitchen sink
bun dev

# Clean build (removes node_modules and CEF vendors)
bun dev:clean

# Release build
bun build:release

# Build for npm (JS/TS only)
bun build.ts --npm

# Type checking
bun typecheck

# Unit tests
bun test:unit
```

### Build Process Flow

The build system (`build.ts`) performs these phases:

1. **Setup Phase** (`setup()`):
   - Check dependencies (cmake, make, VS tools)
   - Vendor Bun, Zig, CEF, WGPU, bsdiff, zstd, asar from GitHub releases

2. **Build Phase** (`build()`):
   - Install npm dependencies
   - Build native wrappers (C++/Objective-C + Zig)
   - Generate template embeddings
   - Build preload scripts
   - Build self-extractor (Zig)
   - Build launcher (Zig)
   - Build CLI
   - Build main.js

3. **Distribution Phase** (`copyToDist()`):
   - Copy binaries to `dist/`
   - Create platform-specific folders (`dist-macos-arm64/`, etc.)

### NEVER run from `bin/` directly

Always use `bun dev` from `package/` directory. The binaries in `bin/` are build artifacts.

---

## Core APIs

### Main Process (Bun)

The main Electrobun API is accessed through the default export:

```typescript
import Electrobun from 'electrobun';

// Create a window
const win = new Electrobun.BrowserWindow({
  title: 'My App',
  width: 800,
  height: 600,
  webPreferences: {
    preload: './preload.js'
  }
});

// Create a tray icon
const tray = new Electrobun.Tray({ 
  title: 'My App',
  image: 'icon.png' 
});

// Listen for application events
Electrobun.events.on('open-url', (e) => {
  console.log('Opened with URL:', e.data.url);
});
```

### Browser/Webview

In the webview/browser process:

```typescript
import Electrobun from 'electrobun/browser';

// Initialize with RPC
const electroview = new Electrobun.Electroview({
  rpc: createRPC(...)
});
```

### RPC System

Electrobun uses a type-safe RPC system for communication between Bun and webviews:

```typescript
import { defineElectrobunRPC } from 'electrobun';

const { createRPC, schema } = defineElectrobunRPC({
  requests: {
    getData: {
      params: { id: '' as string },
      response: { data: '' as string }
    }
  },
  messages: {
    update: { value: 0 as number }
  }
});
```

### Events

Events use the `ElectrobunEventEmitter` class:

```typescript
// Window events
Electrobun.events.on('close', (e) => {
  console.log('Window closing:', e.data.id);
});

// Application events
Electrobun.events.on('open-url', (e) => {
  console.log('Opened with URL:', e.data.url);
});
```

---

## Module Reference

### Window Management

#### `BrowserWindow`

Main window class for web-based content.

**Constructor Options** (`WindowOptionsType`):
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `title` | `string` | `"Electrobun"` | Window title |
| `frame` | `{x, y, width, height}` | `{0,0,800,600}` | Window position and size |
| `url` | `string \| null` | `null` | URL to load |
| `html` | `string \| null` | `null` | HTML content to load |
| `preload` | `string \| null` | `null` | Path to preload script |
| `viewsRoot` | `string \| null` | `null` | Root directory for views |
| `renderer` | `"native" \| "cef"` | `buildConfig.defaultRenderer` | Webview renderer |
| `titleBarStyle` | `"default" \| "hidden" \| "hiddenInset"` | `"default"` | Title bar appearance |
| `transparent` | `boolean` | `false` | Transparent window background |
| `passthrough` | `boolean` | `false` | Mouse events pass through transparent regions |
| `hidden` | `boolean` | `false` | Create window hidden |
| `sandbox` | `boolean` | `false` | Disable RPC (for untrusted content) |
| `navigationRules` | `string \| null` | `null` | JSON string of allowed URL patterns |

**Instance Properties**:
- `id: number` - Unique window ID
- `ptr: Pointer` - Native window pointer
- `state: "creating" \| "created"` - Window state
- `title: string` - Window title
- `frame: {x, y, width, height}` - Current frame
- `webview: BrowserView` - The window's main webview

**Instance Methods**:
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `setTitle(title)` | `string` | `void` | Set window title |
| `close()` | - | `void` | Close the window |
| `focus()` | - | `void` | Focus the window |
| `show()` | - | `void` | Show the window |
| `minimize()` | - | `void` | Minimize window |
| `unminimize()` | - | `void` | Restore from minimized |
| `isMinimized()` | - | `boolean` | Check if minimized |
| `maximize()` | - | `void` | Maximize window |
| `unmaximize()` | - | `void` | Unmaximize window |
| `isMaximized()` | - | `boolean` | Check if maximized |
| `setFullScreen(fs)` | `boolean` | `void` | Toggle fullscreen |
| `isFullScreen()` | - | `boolean` | Check if fullscreen |
| `setAlwaysOnTop(alwaysOnTop)` | `boolean` | `void` | Set always on top |
| `isAlwaysOnTop()` | - | `boolean` | Check if always on top |
| `setVisibleOnAllWorkspaces(visible)` | `boolean` | `void` | Show on all workspaces |
| `isVisibleOnAllWorkspaces()` | - | `boolean` | Check visibility on all workspaces |
| `setPosition(x, y)` | `number, number` | `void` | Set window position |
| `setSize(w, h)` | `number, number` | `void` | Set window size |
| `setFrame(x, y, w, h)` | `number, number, number, number` | `void` | Set position and size |
| `getFrame()` | - | `{x, y, width, height}` | Get current frame |
| `getPosition()` | - | `{x, y}` | Get position |
| `getSize()` | - | `{width, height}` | Get size |
| `setPageZoom(zoom)` | `number` | `void` | Set zoom level (WebKit only) |
| `getPageZoom()` | - | `number` | Get zoom level |
| `on(name, handler)` | `string, function` | `void` | Listen to window events |

**Static Methods**:
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getById(id)` | `number` | `BrowserWindow \| undefined` | Get window by ID |

#### `GpuWindow`

Window class for GPU-native rendering (WebGPU/Dawn).

**Constructor Options** (`GpuWindowOptionsType`):
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `title` | `string` | `"Electrobun"` | Window title |
| `frame` | `{x, y, width, height}` | `{0,0,800,600}` | Window position and size |
| `titleBarStyle` | `"default" \| "hidden" \| "hiddenInset"` | `"default"` | Title bar appearance |
| `transparent` | `boolean` | `false` | Transparent window |

**Instance Properties**:
- `id: number` - Unique window ID
- `ptr: Pointer` - Native window pointer
- `wgpuView: WGPUView` - The window's WGPU view

**Instance Methods**:
All the same methods as `BrowserWindow`, plus:
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `wgpuView` | - | `WGPUView` | Access the WGPU view |

**Static Methods**:
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getById(id)` | `number` | `GpuWindow \| undefined` | Get window by ID |

---

### WebView Management

#### `BrowserView`

WebView for rendering web content within windows.

**Constructor Options** (`BrowserViewOptions`):
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `url` | `string \| null` | `null` | URL to load |
| `html` | `string \| null` | `null` | HTML content to load |
| `preload` | `string \| null` | `null` | Path to preload script |
| `viewsRoot` | `string \| null` | `null` | Root directory for views |
| `renderer` | `"native" \| "cef"` | `buildConfig.defaultRenderer` | Webview renderer |
| `frame` | `{x, y, width, height}` | `{0,0,800,600}` | View frame within window |
| `windowId` | `number` | `0` | Parent window ID |
| `hostWebviewId` | `number` | `undefined` | Host webview ID for OOPIF |
| `autoResize` | `boolean` | `true` | Auto-resize with window |
| `navigationRules` | `string \| null` | `null` | JSON string of URL patterns |
| `sandbox` | `boolean` | `false` | Disable RPC (untrusted content) |
| `partition` | `string \| null` | `null` | Storage partition |
| `startTransparent` | `boolean` | `false` | Start transparent |
| `startPassthrough` | `boolean` | `false` | Start with passthrough |

**Instance Properties**:
- `id: number` - Unique webview ID
- `ptr: Pointer` - Native webview pointer
- `windowId: number` - Parent window ID
- `renderer: "cef" \| "native"` - Renderer type
- `url: string \| null` - Current URL
- `frame: {x, y, width, height}` - Current frame
- `rpc?: RPCWithTransport` - RPC instance

**Instance Methods**:
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `loadURL(url)` | `string` | `void` | Load a URL |
| `loadHTML(html)` | `string` | `void` | Load HTML content |
| `setNavigationRules(rules)` | `string[]` | `void` | Set allowed navigation URLs |
| `findInPage(text, options)` | `string, {forward?, matchCase?}` | `void` | Find text in page |
| `stopFindInPage()` | - | `void` | Stop find operation |
| `openDevTools()` | - | `void` | Open developer tools |
| `closeDevTools()` | - | `void` | Close developer tools |
| `toggleDevTools()` | - | `void` | Toggle developer tools |
| `setPageZoom(zoom)` | `number` | `void` | Set zoom level (WebKit only) |
| `getPageZoom()` | - | `number` | Get zoom level |
| `executeJavascript(js)` | `string` | `void` | Execute JS in webview |
| `remove()` | - | `void` | Remove and cleanup webview |
| `on(name, handler)` | `WebviewEventType, function` | `void` | Listen to webview events |

**Static Methods**:
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getById(id)` | `number` | `BrowserView \| undefined` | Get view by ID |
| `getAll()` | - | `BrowserView[]` | Get all webviews |
| `defineRPC(config)` | `ElectrobunRPCConfig` | `RPCWithTransport` | Create typed RPC |

**Webview Event Types**:
- `will-navigate` - Before navigation starts
- `did-navigate` - Navigation completed
- `did-navigate-in-page` - In-page navigation
- `did-commit-navigation` - Navigation committed
- `dom-ready` - DOM is ready
- `download-started` - Download started
- `download-progress` - Download progress update
- `download-completed` - Download completed
- `download-failed` - Download failed

#### `WGPUView`

GPU-native view for WebGPU rendering.

**Constructor Options** (`WGPUViewOptions`):
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `frame` | `{x, y, width, height}` | `{0,0,800,600}` | View frame |
| `windowId` | `number` | `0` | Parent window ID |
| `autoResize` | `boolean` | `true` | Auto-resize with window |
| `startTransparent` | `boolean` | `false` | Start transparent |
| `startPassthrough` | `boolean` | `false` | Start with passthrough |

**Instance Methods**:
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `setFrame(x, y, w, h)` | `number, number, number, number` | `void` | Set frame |
| `setTransparent(transparent)` | `boolean` | `void` | Set transparency |
| `setPassthrough(passthrough)` | `boolean` | `void` | Set passthrough |
| `setHidden(hidden)` | `boolean` | `void` | Hide/show view |
| `getNativeHandle()` | - | `Pointer` | Get native surface handle |
| `remove()` | - | `void` | Remove view |
| `on(name, handler)` | `"frame-updated", function` | `void` | Listen to events |

**Static Methods**:
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getById(id)` | `number` | `WGPUView \| undefined` | Get view by ID |
| `getAll()` | - | `WGPUView[]` | Get all WGPU views |

---

### GPU/Graphics

#### `WGPU` (WebGPU)

WebGPU API access:

```typescript
import Electrobun from 'electrobun';

// Access WebGPU API
const adapter = await Electrobun.webgpu.requestAdapter();
```

#### `three` and `babylon`

Bundled 3D libraries:

```typescript
import Electrobun from 'electrobun';

// Access Three.js
const scene = new Electrobun.three.Scene();

// Access Babylon.js
const engine = new Electrobun.babylon.Engine(canvas);
```

---

### System Integration

#### `Tray`

System tray icon management.

**Constructor Options** (`TrayOptions`):
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `title` | `string` | `""` | Tray title text |
| `image` | `string` | `""` | Path to icon image |
| `template` | `boolean` | `true` | macOS template image |
| `width` | `number` | `16` | Icon width |
| `height` | `number` | `16` | Icon height |

**Instance Properties**:
- `id: number` - Unique tray ID
- `ptr: Pointer \| null` - Native tray pointer
- `visible: boolean` - Visibility state

**Instance Methods**:
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `setTitle(title)` | `string` | `void` | Set tray title |
| `setImage(path)` | `string` | `void` | Set tray icon |
| `setMenu(menu)` | `MenuItemConfig[]` | `void` | Set context menu |
| `setVisible(visible)` | `boolean` | `void` | Show/hide tray |
| `getBounds()` | - | `Rectangle` | Get tray bounds |
| `remove()` | - | `void` | Remove tray |
| `on(name, handler)` | `"tray-clicked", function` | `void` | Listen to tray events |

**Static Methods**:
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getById(id)` | `number` | `Tray \| undefined` | Get tray by ID |
| `getAll()` | - | `Tray[]` | Get all trays |
| `removeById(id)` | `number` | `void` | Remove tray by ID |

#### `ApplicationMenu`

Application menu bar (macOS) or window menu (Windows/Linux).

**Functions**:
| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `setApplicationMenu(menu)` | `ApplicationMenuItemConfig[]` | `void` | Set app menu |
| `on(name, handler)` | `"application-menu-clicked", function` | `void` | Listen for menu clicks |

#### `ContextMenu`

Context (right-click) menus.

**Functions**:
| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `showContextMenu(menu)` | `ApplicationMenuItemConfig[]` | `void` | Show context menu |
| `on(name, handler)` | `"context-menu-clicked", function` | `void` | Listen for menu clicks |

#### Menu Item Configuration

```typescript
interface MenuItemConfig {
  type?: "normal" | "divider" | "separator";
  label?: string;
  tooltip?: string;
  action?: string;
  role?: MenuRole;           // See menuRoles.ts for full list
  data?: unknown;
  submenu?: MenuItemConfig[];
  enabled?: boolean;
  checked?: boolean;
  hidden?: boolean;
  accelerator?: string;      // Keyboard shortcut (e.g., "Cmd+S")
}
```

**Common Menu Roles**:
- Application: `about`, `quit`, `hide`, `hideOthers`, `showAll`
- Window: `minimize`, `zoom`, `close`, `toggleFullScreen`
- Edit: `undo`, `redo`, `cut`, `copy`, `paste`, `selectAll`, `delete`
- Speech: `startSpeaking`, `stopSpeaking`
- Help: `showHelp`

#### `GlobalShortcut`

Global keyboard shortcuts.

**Functions**:
| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `register(accelerator, callback)` | `string, () => void` | `boolean` | Register shortcut |
| `unregister(accelerator)` | `string` | `void` | Unregister shortcut |
| `unregisterAll()` | - | `void` | Unregister all |
| `isRegistered(accelerator)` | `string` | `boolean` | Check if registered |

#### `Screen`

Display and screen information.

**Functions**:
| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `getAllDisplays()` | - | `Display[]` | Get all displays |
| `getPrimaryDisplay()` | - | `Display` | Get primary display |
| `getCursorScreenPoint()` | - | `Point` | Get cursor position |
| `getMouseButtons()` | - | `number` | Get mouse button state |

**Types**:
```typescript
interface Display {
  id: number;
  bounds: Rectangle;
  workArea: Rectangle;
  scaleFactor: number;
  isPrimary: boolean;
}

interface Rectangle {
  x: number;
  y: number;
  width: number;
  height: number;
}

interface Point {
  x: number;
  y: number;
}
```

#### `Session`

Cookie and storage management.

**Functions**:
| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `getCookies(filter?)` | `CookieFilter?` | `Cookie[]` | Get cookies |
| `setCookie(cookie)` | `Cookie` | `boolean` | Set cookie |
| `removeCookie(url, name)` | `string, string` | `boolean` | Remove cookie |
| `clearCookies()` | - | `void` | Clear all cookies |
| `clearStorageData(type?)` | `StorageType?` | `void` | Clear storage |

**Types**:
```typescript
interface Cookie {
  name: string;
  value: string;
  domain?: string;
  path?: string;
  secure?: boolean;
  httpOnly?: boolean;
  expirationDate?: number;
}

type StorageType = "cookies" | "localstorage" | "sessionstorage" | "cache" | "all";
```

---

### Utilities

#### `Updater`

Auto-update functionality.

**Functions**:
| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `checkForUpdate()` | - | `Promise<UpdateInfo>` | Check for updates |
| `downloadUpdate()` | - | `Promise<void>` | Download update |
| `applyUpdate()` | - | `Promise<void>` | Apply and restart |
| `getStatusHistory()` | - | `UpdateStatusEntry[]` | Get status history |
| `clearStatusHistory()` | - | `void` | Clear history |
| `onStatusChange(callback)` | `(entry) => void \| null` | `void` | Subscribe to status |

**Update Status Types**:
`idle`, `checking`, `check-complete`, `no-update`, `update-available`, `downloading`, 
`downloading-patch`, `applying-patch`, `patch-applied`, `patch-failed`, 
`downloading-full-bundle`, `decompressing`, `download-complete`, `applying`, 
`replacing-app`, `launching-new-version`, `complete`, `error`

#### `Utils`

Utility functions.

**System Operations**:
| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `quit()` | - | `never` | Quit application |
| `openExternal(url)` | `string` | `boolean` | Open URL in default browser |
| `openPath(path)` | `string` | `boolean` | Open file/folder with default app |
| `moveToTrash(path)` | `string` | `void` | Move file to trash |
| `showItemInFolder(path)` | `string` | `void` | Show file in folder |
| `setDockIconVisible(visible)` | `boolean` | `void` | Set dock icon visibility (macOS) |
| `isDockIconVisible()` | - | `boolean` | Check dock icon visibility |
| `showNotification(options)` | `NotificationOptions` | `void` | Show native notification |
| `showMessageBox(options)` | `MessageBoxOptions` | `Promise<MessageBoxResponse>` | Show message dialog |
| `openFileDialog(options?)` | `OpenFileDialogOptions` | `Promise<string[]>` | Open file picker |

**Notification Options**:
```typescript
interface NotificationOptions {
  title: string;
  body?: string;
  subtitle?: string;  // macOS only
  silent?: boolean;
}
```

**Message Box Options**:
```typescript
interface MessageBoxOptions {
  type?: "info" | "warning" | "error" | "question";
  title?: string;
  message?: string;
  detail?: string;
  buttons?: string[];
  defaultId?: number;
  cancelId?: number;
}

interface MessageBoxResponse {
  response: number;  // Index of clicked button
}
```

**Open File Dialog Options**:
```typescript
interface OpenFileDialogOptions {
  startingFolder?: string;
  allowedFileTypes?: string;
  canChooseFiles?: boolean;
  canChooseDirectory?: boolean;
  allowsMultipleSelection?: boolean;
}
```

**Clipboard API**:
| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `clipboardReadText()` | - | `string \| null` | Read text from clipboard |
| `clipboardWriteText(text)` | `string` | `void` | Write text to clipboard |
| `clipboardReadImage()` | - | `Uint8Array \| null` | Read image (PNG) |
| `clipboardWriteImage(data)` | `Uint8Array` | `void` | Write image (PNG) |
| `clipboardClear()` | - | `void` | Clear clipboard |
| `clipboardAvailableFormats()` | - | `string[]` | Get available formats |

**Path Constants** (`Utils.paths`):
| Property | Description |
|----------|-------------|
| `home` | User home directory |
| `appData` | Application data directory |
| `config` | Config directory |
| `cache` | Cache directory |
| `temp` | Temp directory |
| `logs` | Logs directory |
| `documents` | Documents folder |
| `downloads` | Downloads folder |
| `desktop` | Desktop folder |
| `pictures` | Pictures folder |
| `music` | Music folder |
| `videos` | Videos/Movies folder |
| `userData` | App-specific user data |
| `userCache` | App-specific cache |
| `userLogs` | App-specific logs |

#### `BuildConfig`

Runtime build configuration access.

**Functions**:
| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `get()` | - | `Promise<BuildConfigType>` | Load build config |
| `getCached()` | - | `BuildConfigType \| null` | Get cached config |

**BuildConfigType**:
```typescript
interface BuildConfigType {
  defaultRenderer: "native" | "cef";
  availableRenderers: ("native" | "cef")[];
  cefVersion?: string;
  bunVersion?: string;
  runtime?: {
    exitOnLastWindowClosed?: boolean;
    [key: string]: unknown;
  };
}
```

#### `PATHS`

Internal path constants.

| Constant | Description |
|----------|-------------|
| `VIEWS_FOLDER` | Path to views directory (`../Resources/app/views`) |

#### `Socket`

WebSocket server for Bun-webview communication.

| Export | Type | Description |
|--------|------|-------------|
| `rpcServer` | `Server` | Bun WebSocket server instance |
| `rpcPort` | `number` | Port number for RPC |
| `socketMap` | `object` | Map of webview IDs to sockets |

---

### Events System

#### `Electrobun.events`

Main event emitter for application lifecycle.

**Window Events** (`Electrobun.events.window`):
| Event | Data | Description |
|-------|------|-------------|
| `close` | `{id: number}` | Window closing |
| `resize` | `{id, x, y, width, height}` | Window resized |
| `move` | `{id, x, y}` | Window moved |
| `focus` | `{id: number}` | Window focused |
| `blur` | `{id: number}` | Window blurred |
| `keyDown` | `{id, keyCode, modifiers, isRepeat}` | Key pressed |
| `keyUp` | `{id, keyCode, modifiers, isRepeat}` | Key released |

**WebView Events** (`Electrobun.events.webview`):
| Event | Data | Description |
|-------|------|-------------|
| `willNavigate` | `{detail: string}` | Before navigation |
| `didNavigate` | `{detail: string}` | Navigation complete |
| `didNavigateInPage` | `{detail: string}` | In-page navigation |
| `didCommitNavigation` | `{detail: string}` | Navigation committed |
| `domReady` | `{detail: string}` | DOM ready |
| `newWindowOpen` | `{detail: object}` | New window requested |
| `hostMessage` | `{detail: string}` | Message from host |
| `downloadStarted` | `{detail: string}` | Download started |
| `downloadProgress` | `{detail: string}` | Download progress |
| `downloadCompleted` | `{detail: string}` | Download complete |
| `downloadFailed` | `{detail: string}` | Download failed |

**Application Events** (`Electrobun.events.app`):
| Event | Data | Response | Description |
|-------|------|----------|-------------|
| `applicationMenuClicked` | `{id?, action, data?}` | `{allow: boolean}` | Menu item clicked |
| `contextMenuClicked` | `{id?, action, data?}` | `{allow: boolean}` | Context menu clicked |
| `openUrl` | `{url: string}` | `void` | App opened via URL scheme |
| `reopen` | `{}` | `void` | App reopened (macOS dock click) |
| `beforeQuit` | `{}` | `{allow: boolean}` | Before quitting |

**Tray Events** (`Electrobun.events.tray`):
| Event | Data | Response | Description |
|-------|------|----------|-------------|
| `trayClicked` | `{id, action, data?}` | `{allow: boolean}` | Tray icon/menu clicked |

#### `ElectrobunEvent`

Event object passed to handlers.

```typescript
class ElectrobunEvent<DataType, ResponseType> {
  name: string;
  data: DataType;
  response?: ResponseType;
  responseWasSet: boolean;
  
  set response(value: ResponseType): void;
  clearResponse(): void;
}
```

**Usage**:
```typescript
Electrobun.events.on('before-quit', (e) => {
  // Prevent quitting
  e.response = { allow: false };
});
```

---

## Configuration

### Electrobun Config (`electrobun.config.ts`)

```typescript
import type { ElectrobunConfig } from "electrobun";

export default {
  app: {
    name: "My App",
    identifier: "com.example.myapp",
    version: "1.0.0",
    description?: "App description",
    urlSchemes?: ["myapp"],  // Deep linking
  },
  
  bunny?: {
    carrot?: {
      dependencies?: { [id: string]: string }  // Carrot dependencies
    }
  },
  
  build: {
    bun: {
      entrypoint: "src/bun/index.ts",
      // Any Bun.build() options
    },
    views: {
      main: {
        entrypoint: "src/views/main/index.ts",
        // Any Bun.build() options
      }
    },
    copy: { "source": "dest" },  // Files to copy
    buildFolder: "build",        // Output folder
    artifactFolder: "artifacts", // Dist folder
    targets: "current",          // Build targets
    useAsar: false,              // ASAR packaging
    asarUnpack: ["*.node"],      // ASAR unpack patterns
    cefVersion?: string,         // Override CEF version
    wgpuVersion?: string,        // Override Dawn version
    bunVersion?: string,         // Override Bun version
    locales: "*",                // ICU locales
    watch: [],                   // Additional watch paths
    watchIgnore: [],             // Ignore patterns
    
    mac: {
      codesign: false,
      notarize: false,
      createDmg: true,
      bundleCEF: false,
      bundleWGPU: false,
      defaultRenderer: "native",
      chromiumFlags: {},
      entitlements: {},
      icons: "icon.iconset",
    },
    
    win: {
      bundleCEF: false,
      bundleWGPU: false,
      defaultRenderer: "native",
      chromiumFlags: {},
      icon: "assets/icon.ico",
    },
    
    linux: {
      bundleCEF: false,
      bundleWGPU: false,
      defaultRenderer: "native",
      chromiumFlags: {},
      icon: "assets/icon.png",
    }
  },
  
  runtime: {
    exitOnLastWindowClosed: true,
    // Custom runtime config
  },
  
  scripts: {
    preBuild?: string,
    postBuild?: string,
    postWrap?: string,
    postPackage?: string,
  },
  
  release: {
    baseUrl: "https://releases.example.com",
    generatePatch: true,
  }
} satisfies ElectrobunConfig;
```

See `package/src/bun/ElectrobunConfig.ts` for full type definitions.

---

## Testing

### Unit Tests

Located in `package/src/shared/*.test.ts`:
```bash
bun test:unit  # Runs naming.test.ts and other unit tests
```

### Integration Tests

The **Kitchen Sink** app (`kitchen/`) serves as the integration test suite:

```bash
# Run kitchen sink in dev mode
bun dev  # from package/ directory

# Run with auto-test execution
AUTO_RUN=1 electrobun dev
```

Test categories:
- **Automated tests**: Run without user interaction (`src/tests/*.test.ts`)
- **Interactive tests**: Require user interaction (`src/tests/interactive/*.test.ts`)
- **Playgrounds**: Feature demonstrations (`src/playgrounds/*/`)

### Test Framework

Custom test framework in `kitchen/src/test-framework/`:
- `defineTest()` - Define individual tests
- `defineTestSuite()` - Define test suites with setup/teardown
- `expect()` - Assertion helpers (toBe, toEqual, toContain, etc.)

---

## Security

1. **RPC Encryption**: All webview<->bun communication uses AES-GCM encryption
2. **Code Signing**:
   - macOS: Developer ID signing with optional notarization
   - Windows: Authenticode signing support
3. **Sandboxing**: Webviews run in separate processes
4. **Permissions**: Carrot system has explicit permission model (for Bunny extensions)
5. **Sandbox Mode**: `sandbox: true` disables RPC for untrusted content (remote URLs)

---

## Development Conventions

### Code Style

- **Language**: TypeScript with strict mode enabled
- **Module System**: ES modules (`"type": "module"`)
- **Imports**: Use explicit extensions (`.js` for TS imports due to ES modules)

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "lib": ["ESNext", "DOM"],
    "target": "ESNext",
    "module": "ESNext",
    "moduleDetection": "force",
    "jsx": "react-jsx",
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "noEmit": true,
    "strict": true,
    "skipLibCheck": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noPropertyAccessFromIndexSignature": true,
    "noUncheckedIndexedAccess": true
  }
}
```

### Key Patterns

1. **RPC Definition**: Use `defineElectrobunRPC()` for typed communication between bun and webview
2. **Event Handling**: Use `Electrobun.events` event emitter for application lifecycle
3. **Native Bindings**: Access via `proc/native` with type definitions
4. **Configuration**: Apps use `electrobun.config.ts` for build configuration

---

## CI/CD and Release Process

### GitHub Actions Workflow

`.github/workflows/release.yml`:
- Builds for macOS (arm64, x64), Windows (x64), Linux (x64, arm64)
- Creates platform-specific dist folders
- Publishes artifacts to GitHub Releases
- Publishes npm package

### Release Channels

- **stable**: Production releases
- **canary**: Beta/pre-release versions
- **dev**: Development builds

### NPM Scripts for Release

```bash
# From package/ directory
bun push:patch   # Patch version bump
bun push:minor   # Minor version bump
bun push:major   # Major version bump
bun push:beta    # Beta release
bun push:stable  # Stable release
```

---

## Common Development Tasks

### Adding a New Template

1. Create directory in `templates/`
2. Add `package.json`, `tsconfig.json`, `electrobun.config.ts`
3. Add `README.md` with usage instructions
4. Update `package/src/cli/templates/embedded.ts` to include template

### Adding Native Bindings

1. Add C/C++ code in `package/src/native/{platform}/`
2. Update Zig bindings if needed
3. Rebuild with `bun dev:clean`

### Debugging

**macOS:**
```bash
lldb /path/to/MyApp.app/Contents/MacOS/launcher
(lldb) run
```

**General:**
- Use `console.log()` in bun process - outputs to terminal
- Webview DevTools: use `webview.openDevTools()` method

---

## Roll Out Plan

### Phase 1: Foundation (Weeks 1-4)

**Week 1-2: Core Platform Stabilization**
- [ ] Finalize native wrapper APIs for all platforms
- [ ] Complete FFI bindings documentation
- [ ] Stabilize RPC communication layer with encryption
- [ ] Finalize BrowserWindow and BrowserView APIs
- [ ] Complete test coverage for core modules

**Week 3-4: Build System Hardening**
- [ ] Cross-platform build pipeline validation
- [ ] CEF integration testing (all platforms)
- [ ] ASAR packaging optimization
- [ ] Code signing workflow automation
- [ ] Binary delta patch generation testing

**Deliverables:**
- Stable core API (v1.0.0-rc)
- Working build pipeline for macOS, Windows, Linux
- Automated release workflow

---

### Phase 2: Feature Completion (Weeks 5-8)

**Week 5-6: Advanced Windowing**
- [ ] Multi-window support finalization
- [ ] Window state management (restore, minimize, fullscreen)
- [ ] Transparent window support across platforms
- [ ] Custom title bar implementations
- [ ] Window composition and layering

**Week 7-8: System Integration**
- [ ] System tray implementation (all platforms)
- [ ] Native menu bars (ApplicationMenu, ContextMenu)
- [ ] Global keyboard shortcuts
- [ ] File dialogs and native pickers
- [ ] Notification system integration

**Deliverables:**
- Full windowing API
- Complete system integration features
- Kitchen sink demo app functional

---

### Phase 3: WebGPU & Graphics (Weeks 9-12)

**Week 9-10: WebGPU Foundation**
- [ ] Dawn integration completion
- [ ] WGPUView implementation
- [ ] GpuWindow stabilization
- [ ] Surface management and presentation
- [ ] Buffer and texture operations

**Week 11-12: 3D Engine Integration**
- [ ] Three.js bundling and testing
- [ ] Babylon.js integration
- [ ] Example 3D applications
- [ ] Performance optimization
- [ ] Documentation and tutorials

**Deliverables:**
- Stable WebGPU support
- Working 3D examples
- Performance benchmarks

---

### Phase 4: Distribution & Updates (Weeks 13-16)

**Week 13-14: Auto-Update System**
- [ ] Updater module finalization
- [ ] Delta patch testing at scale
- [ ] Rollback mechanisms
- [ ] Update server infrastructure
- [ ] Channel support (stable, canary, dev)

**Week 15-16: Distribution Packaging**
- [ ] DMG creation (macOS)
- [ ] MSI/EXE installer (Windows)
- [ ] AppImage/deb packaging (Linux)
- [ ] Store submission preparation
- [ ] Code signing certificates

**Deliverables:**
- Auto-update system live
- All platform installers
- Distribution documentation

---

### Phase 5: Documentation & Community (Weeks 17-20)

**Week 17-18: Documentation Sprint**
- [ ] API reference completion
- [ ] Tutorial series (10+ tutorials)
- [ ] Video walkthroughs
- [ ] Template documentation
- [ ] Migration guides (from Electron, Tauri)

**Week 19-20: Community Building**
- [ ] Discord server launch
- [ ] GitHub discussion templates
- [ ] Contribution guidelines
- [ ] Plugin/extension architecture
- [ ] Partner integrations

**Deliverables:**
- Complete documentation site
- Active community channels
- Contributor onboarding

---

### Phase 6: Public Release (Week 21+)

**Pre-Launch (Week 21-22)**
- [ ] Release candidate testing
- [ ] Performance benchmarking
- [ ] Security audit
- [ ] Marketing website launch
- [ ] Press kit preparation

**Launch Week (Week 23)**
- [ ] v1.0.0 release
- [ ] Product Hunt launch
- [ ] Hacker News announcement
- [ ] Twitter/X campaign
- [ ] YouTube demo videos

**Post-Launch (Week 24+)**
- [ ] Bug fix sprints (bi-weekly)
- [ ] Feature request triage
- [ ] Enterprise support tier
- [ ] Pro version development
- [ ] Conference presentations

---

### Milestone Summary

| Milestone | Target Date | Key Deliverables |
|-----------|-------------|------------------|
| Alpha (Core) | Week 4 | Basic window, build system |
| Beta (Features) | Week 8 | Full API, system integration |
| RC (Graphics) | Week 12 | WebGPU, 3D support |
| Distribution | Week 16 | Updates, installers |
| v1.0.0 | Week 23 | Public release |
| v1.1.0 | Month 6 | Performance, bug fixes |
| v2.0.0 | Month 12 | Major features, API evolution |

---

### Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| CEF compatibility issues | Medium | High | Maintain WebKit/WebView2 as default |
| Build system failures | Low | High | CI/CD with multiple runner types |
| API breaking changes | Medium | Medium | Strict semver, deprecation warnings |
| Performance issues | Medium | High | Profiling suite, optimization sprints |
| Security vulnerabilities | Low | Critical | Security audits, responsible disclosure |

---

## Important Notes

1. **Never run from `bin/` directly** - Always use `bun dev` from `package/` directory
2. **Build from `package/`** - All build commands must be run from this directory
3. **Submodules**: Some components use git submodules; clone with `--recurse-submodules`
4. **CEF Cache**: CEF builds are cached; delete `vendors/cef/` to force re-download
5. **Platform Dist Folders**: Build outputs to `dist-{os}-{arch}/` folders

---

## Useful Links

- Documentation: https://blackboard.sh/electrobun/
- NPM: https://www.npmjs.com/package/electrobun
- Discord: https://discord.gg/ueKE4tjaCE
- Twitter/X: @BlackboardTech, @YoavCodes
