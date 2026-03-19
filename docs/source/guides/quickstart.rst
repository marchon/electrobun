Quickstart Guide
================

This guide will help you create your first Electrobun application in minutes.

Prerequisites
-------------

Ensure you have completed :doc:`installation`.

Create a New Project
--------------------

Use the Electrobun CLI to create a new project:

.. code-block:: bash

   npx electrobun create my-app
   cd my-app

Or manually:

.. code-block:: bash

   mkdir my-app
   cd my-app
   bun init

Project Structure
-----------------

A basic Electrobun app has this structure:

.. code-block:: text

   my-app/
   ├── src/
   │   ├── bun/
   │   │   └── index.ts        # Main process entry
   │   └── views/
   │       └── main/
   │           └── index.html  # Main view
   ├── electrobun.config.ts    # Build configuration
   ├── package.json
   └── tsconfig.json

Main Process
------------

Create ``src/bun/index.ts``:

.. code-block:: typescript

   import Electrobun from 'electrobun';

   // Create a window
   const win = new Electrobun.BrowserWindow({
     title: 'My First App',
     width: 800,
     height: 600,
     url: 'views://main/index.html',
   });

   // Handle window events
   win.on('close', () => {
     console.log('Window is closing');
   });

WebView Content
---------------

Create ``src/views/main/index.html``:

.. code-block:: html

   <!DOCTYPE html>
   <html>
   <head>
     <title>My App</title>
     <style>
       body {
         font-family: -apple-system, BlinkMacSystemFont, sans-serif;
         padding: 20px;
       }
     </style>
   </head>
   <body>
     <h1>Hello from Electrobun!</h1>
     <p>This is your first desktop app.</p>
   </body>
   </html>

Configuration
-------------

Create ``electrobun.config.ts``:

.. code-block:: typescript

   import type { ElectrobunConfig } from 'electrobun';

   export default {
     app: {
       name: 'My First App',
       identifier: 'com.example.myapp',
       version: '1.0.0',
     },
     build: {
       bun: {
         entrypoint: 'src/bun/index.ts',
       },
       views: {
         main: {
           entrypoint: 'src/views/main/index.ts',
         },
       },
     },
   } satisfies ElectrobunConfig;

Run Your App
------------

Start in development mode:

.. code-block:: bash

   bun dev

Build for Distribution
----------------------

Create a production build:

.. code-block:: bash

   bun run electrobun build

The built app will be in the ``build/`` directory.

Next Steps
----------

- :doc:`window-management` - Learn about windows
- :doc:`webview-communication` - Bun ↔ WebView communication
- :doc:`../reference/browser-window` - Window API reference
