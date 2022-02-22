#!/usr/bin/env bash

set -euo pipefail

# https://stackoverflow.com/a/246128/6318316
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# https://levelup.gitconnected.com/how-to-live-reload-code-for-golang-and-docker-without-third-parties-ee90721ef641
fswatch -or -e ".*" -i "\\.py$" --event=Updated "${SCRIPT_DIR}/../" | xargs -n1 -I{} "${SCRIPT_DIR}/test.sh"
