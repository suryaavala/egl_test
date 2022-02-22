#!/usr/bin/env bash

set -euo pipefail

# https://stackoverflow.com/a/246128/6318316
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

pytest \
    -vvv \
    --verbose \
    "${SCRIPT_DIR}/../tests"
