#!/bin/bash
# ViralDesk setup — creates the venv, installs deps, and (on this machine)
# trusts the egress proxy CA inside certifi so yt-dlp can reach YouTube.
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
./.venv/bin/pip install --quiet -r requirements.txt
# The sandbox egress proxy uses a self-signed CA that certifi doesn't trust.
# Appending it is the standard fix; harmless on machines without the file.
if [ -f /run/hatch/egress-tls/ca-bundle.pem ]; then
  CACERT=$(./.venv/bin/python -c "import certifi; print(certifi.where())")
  if ! grep -q "hatch-egress" "$CACERT" 2>/dev/null; then
    cat /run/hatch/egress-tls/ca-bundle.pem >> "$CACERT"
    echo "proxy CA added to certifi bundle"
  fi
fi
# yt-dlp is needed by fetchers.py but not by the Streamlit UI itself
./.venv/bin/pip install --quiet yt-dlp
chmod +x run.sh
echo "setup done — run ./run.sh"
