#!/bin/bash
# ViralDesk Phase 1 launcher — run from anywhere.
cd "$(dirname "$0")"
exec ./.venv/bin/streamlit run app.py --server.port 8501 --server.address 127.0.0.1
