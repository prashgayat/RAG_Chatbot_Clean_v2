#!/bin/bash

echo "🔄 Fixing environment: reinstalling semantic-text-splitter and launching Streamlit..."

# Reinstall semantic-text-splitter cleanly
pip uninstall -y semantic-text-splitter >/dev/null 2>&1
pip install --user semantic-text-splitter==0.25.1

# Ensure Streamlit is installed and find its path
if ! which streamlit >/dev/null 2>&1; then
    echo "⚠️  Streamlit not found. Installing..."
    pip install --user streamlit
else
    echo "✅ Streamlit is already available"
fi

# Get Streamlit path
STREAMLIT_BIN=$(which streamlit)
if [ -z "$STREAMLIT_BIN" ]; then
    echo "❌ Streamlit still not found after install. Please check your PATH manually."
    exit 1
fi

# Confirm versions
echo
echo "✅ Environment Fixed:"
$STREAMLIT_BIN --version
semantic-text-splitter --version

# Launch app
echo
echo "🚀 Launching Streamlit app..."
$STREAMLIT_BIN run app.py
