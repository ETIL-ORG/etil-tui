<!--
  Copyright (c) 2026 Mark Deazley. All rights reserved.
  SPDX-License-Identifier: BSD-3-Clause
-->

# ETIL MCP Client TUI

An interactive terminal UI for the [ETIL](https://github.com/krystalmonolith/evolutionary-til) MCP server, built
with Python 3.12 and [Textual](https://textual.textualize.io/).

- **Support**: [evolutionary-til-support@googlegroups.com](mailto:evolutionary-til-support@googlegroups.com)
- **Platform**: Linux only. Tested on Ubuntu 24.04 — YMMV on other distributions. Not available for Windows.
  macOS-specific modifications will not be accepted.

## Features

- **Triple-window layout** — JSON-RPC traffic log (left), interpreter I/O with command history (right),
  color-coded notification bar (bottom)
- **Full-screen help browser** (F1) — categorized word index with clickable links, word manpages with live
  examples auto-executed in a sandbox container, search, breadcrumb navigation, keyboard shortcuts (n/p/i/Backspace)
- **OAuth login** — `/login`, `/logout`, `/whoami` with JWT caching in `~/.etil/connections.json`
- **Script execution** — `--exec <file|URL>` runs a `.til` file through the TUI and exits;
  `--execux` stays interactive after the script
- **Session logging** — automatic plain-text (`.log`) and JSONL (`.json`) logging with rotation
- **HTTP Streamable Transport** — real-time SSE streaming for server notifications during long-running commands
- **Named connections** — `~/.etil/connections.json` stores server URLs, API keys, and cached JWTs
- **Panel resizing** — all panels re-render at the correct width when layout changes or terminal resizes

## Installation

### From `.deb` package (Ubuntu 24.04)

```bash
scripts/build-tui-deb.sh --output /tmp
sudo dpkg -i /tmp/etil-tui_*.deb
```

The `.deb` package installs a self-contained Python virtual environment at `/opt/etil-tui/` and a
launcher script at `/usr/local/bin/etil-tui`.

## Dependencies

- Python 3.12+
- [Textual](https://textual.textualize.io/) >= 0.85.0
- [httpx](https://www.python-httpx.org/) >= 0.27.0

## Usage

```bash
# Connect to a named server
etil-tui --connect myserver

# Connect to a URL (first time — must pair with --login)
etil-tui --connect https://etil.example.com/mcp --login github

# Run with default connection
etil-tui

# Execute a script and exit
etil-tui --exec my_script.til

# Execute a script, then stay interactive
etil-tui --execux my_script.til
```

### CLI Options

| Option | Description |
|--------|-------------|
| `--connect NAME_OR_URL` | Connect by saved name or ad-hoc URL |
| `--login [PROVIDER]` | Start OAuth login on launch (default: `github`) |
| `--list-connections` | List saved connections and exit |
| `--exec SOURCE` | Execute a `.til` file or URL, then exit |
| `--execux SOURCE` | Execute a `.til` file or URL, then stay interactive |
| `--nologs` | Disable automatic session logging |
| `--norotate` | Keep all old log files (skip rotation) |
| `--screendir DIR` | Directory for screenshot SVGs (`.` = current directory) |
| `--logdir DIR` | Directory for log files (`.` = current directory) |

## Keybindings

| Key | Action |
|-----|--------|
| F1 | Open help browser |
| F2 | Toggle panel layout (both / IO-only / RPC-only) |
| F3 | Toggle notification fullscreen |
| F4 | Scroll notification log top/bottom |
| Tab | Cycle focus between panels |
| Ctrl+Q | Quit |
| Ctrl+D | Dismiss notification |
| Ctrl+L | Clear output panel |
| Ctrl+P | Save screenshot |
| Escape | Focus command input |
| Up/Down | Command history |

### Help Browser Keybindings

| Key | Action |
|-----|--------|
| Escape / q | Close help browser |
| Backspace | Go back |
| i | Jump to index |
| n / p | Next / previous word in category |
| / | Open search |

## Meta-Commands

Type these at the command prompt (prefix with `/`):

| Command | Description |
|---------|-------------|
| `/stack` | Show current stack contents |
| `/reset` | Reset the interpreter session |
| `/stats` | Show session statistics |
| `/info <word>` | Open help page for a word |
| `/help [word]` | Open help browser (optionally at a word) |
| `/load <path>` | Load and execute a local `.til` file |
| `/upload <path> [name]` | Upload a file to the server's LVFS |
| `/download <path> [local]` | Download a file from the server's LVFS |
| `/verbose [on\|off]` | Toggle full JSON output display |
| `/logfile [path]` | Toggle plain-text logging |
| `/logjson [path]` | Toggle JSONL logging |
| `/log` | Toggle both log types |
| `/login [provider]` | Start OAuth device flow login |
| `/logout` | Revert to API key auth |
| `/whoami` | Show current auth state |
| `/clear` | Clear output panel |
| `/quit` | Quit the TUI |

Any other input is sent to the ETIL interpreter as TIL code.

## Help Browser

Press **F1** or type `/help` to open the full-screen help browser:

- **Index** — categorized word table with stack effects and clickable `etil://` links
- **Category pages** — filtered word list for a single category
- **Word manpages** — description, stack effect, live examples (auto-executed in a sandbox container),
  implementations with source locations, type signatures, and see-also references
- **Breadcrumbs** — clickable navigation trail: Index > Category > Word
- **Search** — press `/` to search words by name or description (real-time filtering)

## Session Logging

The TUI automatically opens both plain-text and JSONL log files on startup:
- `YYYYMMDD_HHMMSS-tui.log` — human-readable session log
- `YYYYMMDD_HHMMSS-tui.json` — machine-readable JSONL log

Default directory: `/tmp` (override with `--logdir`).

Old logs are rotated on startup, keeping the 5 most recent of each type. Use `--norotate` to keep all logs,
or `--nologs` to disable automatic logging entirely. The `/log` command toggles logging on/off during a session.

## Server Response Formatting

Server responses are automatically unpacked from JSON:
- **Output** in green
- **Errors** in red (also sent to notification bar)
- **Stack** in yellow

## Connections

Server connections are stored in `~/.etil/connections.json`. On first run, a setup wizard guides you through
creating your first connection.

```bash
# List saved connections
etil-tui --list-connections

# Connect by name
etil-tui --connect production
```

## ETIL Word Reference

See [README.etil.md](README.etil.md) for the full ETIL project documentation including all words
organized by category with stack effects and examples. This file is a copy of the ETIL repository's
`README.md` and is refreshed on each ETIL release.

## Building `.deb` Packages

```bash
scripts/build-tui-deb.sh --output /tmp
```

The script creates a self-contained `.deb` package with an embedded Python virtual environment. The package
name includes a build timestamp: `etil-tui_X.Y.Z+YYYYMMDDhhmmss_amd64.deb`.

## Project Structure

```
etil-tui/
├── etil_mcp_client/           # Python package
│   ├── __main__.py            # CLI entry point
│   ├── app.py                 # Main Textual application
│   ├── config.py              # ClientConfig dataclass
│   ├── connections.py         # Connection storage (~/.etil/connections.json)
│   ├── completer.py           # Tab completion for commands
│   ├── help_renderer.py       # Markdown rendering for help pages
│   ├── http_transport.py      # HTTP Streamable Transport (SSE)
│   ├── models.py              # Data models
│   ├── protocol.py            # JSON-RPC 2.0 client protocol
│   ├── session_logger.py      # Plain-text and JSONL logging
│   ├── themes.py              # Nord-inspired dark/light themes
│   ├── transport.py           # Transport ABC
│   ├── version.py             # Version string
│   ├── wizard.py              # First-run setup wizard
│   ├── screens/
│   │   └── help_screen.py     # Full-screen help browser
│   └── widgets/
│       ├── jsonrpc_panel.py   # JSON-RPC traffic log panel
│       ├── notification_bar.py # Color-coded notification bar
│       └── server_io_panel.py # Interpreter I/O panel
├── scripts/
│   └── build-tui-deb.sh       # .deb package builder
├── tests/                     # Unit tests
├── setup.sh                   # Create venv + install deps
├── run.sh                     # Launch TUI
└── requirements.txt           # Python dependencies
```

## Requirements

- Python 3.12+
- textual >= 0.85.0
- httpx (for HTTP Streamable Transport)

## License

BSD-3-Clause

## Author

Mark Deazley — [github.com/krystalmonolith](https://github.com/krystalmonolith)
