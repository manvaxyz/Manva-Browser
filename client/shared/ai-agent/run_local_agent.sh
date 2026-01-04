#!/usr/bin/env bash
set -euo pipefail
python -m pip install --user -r requirements.txt
python agent.py
