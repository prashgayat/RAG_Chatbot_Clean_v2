#!/bin/bash

echo "💣 Performing full environment nuke & reset..."

# Step 1: Remove old compiled Python files
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -r {} +

# Step 2: Locate and remove any shadowed semantic_text_splitter installations
SPLITTER_PATH=$(find ~/.local -type d -name "semantic_text_splitter" 2>/dev/null)

if [ -n "$SPLITTER_PATH" ]; then
  echo "🧹 Removing old semantic_text_splitter at: $SPLITTER_PATH"
  rm -rf "$SPLITTER_PATH"
else
  echo "✅ No shadowed semantic_text_splitter found in ~/.local"
fi

# Step 3: Reinstall semantic-text-splitter cleanly
pip install --no-cache-dir "semantic-text-splitter==0.25.1"

# Step 4: Confirm correct version is installed
pip show semantic-text-splitter

# Step 5: Restart Streamlit app
echo "🚀 Launching Streamlit app..."
streamlit run app.py
