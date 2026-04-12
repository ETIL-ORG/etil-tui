#!/usr/bin/env bash
# Copyright (c) 2026 Mark Deazley. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# Bump the TUI version in etil_mcp_client/version.py using semver semantics.
#
# Usage: version-bump.sh <major|minor|patch> [--dry-run]
#
# Modes:
#   major   — X+1.0.0  (breaking changes)
#   minor   — X.Y+1.0  (new feature, patch resets to 0)
#   patch   — X.Y.Z+1  (bug fix)
#
# Echoes the new version string on success.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION_FILE="$PROJECT_DIR/etil_mcp_client/version.py"

tui_log() {
    echo "[etil-tui] $(date '+%H:%M:%S') $*" >&2
}

tui_die() {
    tui_log "FATAL: $*"
    exit 1
}

# --- Parse args ---
MODE=""
DRY_RUN=false

for arg in "$@"; do
    case "$arg" in
        major|minor|patch) MODE="$arg" ;;
        --dry-run)         DRY_RUN=true ;;
        --help|-h)
            echo "Usage: $0 <major|minor|patch> [--dry-run]"
            echo ""
            echo "  major     X+1.0.0  (breaking changes)"
            echo "  minor     X.Y+1.0  (new feature, patch resets to 0)"
            echo "  patch     X.Y.Z+1  (bug fix)"
            echo "  --dry-run Show plan without modifying version.py"
            exit 0
            ;;
        *)
            echo "Unknown argument: $arg"
            echo "Run with --help for usage."
            exit 1
            ;;
    esac
done

if [[ -z "$MODE" ]]; then
    tui_die "Mode required: major, minor, or patch"
fi

# --- Parse current version ---
if [[ ! -f "$VERSION_FILE" ]]; then
    tui_die "version.py not found: $VERSION_FILE"
fi

OLD_VERSION=$(python3 -c "exec(open('$VERSION_FILE').read()); print(__version__)")
if [[ -z "$OLD_VERSION" ]]; then
    tui_die "Could not parse version from $VERSION_FILE"
fi

MAJOR="${OLD_VERSION%%.*}"
REST="${OLD_VERSION#*.}"
MINOR="${REST%%.*}"
PATCH="${REST#*.}"

# --- Compute new version ---
case "$MODE" in
    major) NEW_VERSION="$((MAJOR + 1)).0.0" ;;
    minor) NEW_VERSION="${MAJOR}.$((MINOR + 1)).0" ;;
    patch) NEW_VERSION="${MAJOR}.${MINOR}.$((PATCH + 1))" ;;
esac

if [[ "$DRY_RUN" == true ]]; then
    tui_log "[dry-run] Would bump v$OLD_VERSION → v$NEW_VERSION ($MODE)"
    echo "$NEW_VERSION"
    exit 0
fi

# --- Apply to version.py ---
sed -i "s/__version__ = \"${OLD_VERSION}\"/__version__ = \"${NEW_VERSION}\"/" "$VERSION_FILE"

# --- Verify ---
VERIFY=$(python3 -c "exec(open('$VERSION_FILE').read()); print(__version__)")
if [[ "$VERIFY" != "$NEW_VERSION" ]]; then
    tui_die "Version bump failed: expected $NEW_VERSION, got $VERIFY"
fi

tui_log "Bumped v$OLD_VERSION → v$NEW_VERSION ($MODE)"
echo "$NEW_VERSION"
