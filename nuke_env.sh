#!/bin/bash

echo "💣 Performing full environment nuke & reset..."

# Remove ghost installs of semantic-text-splitter
SEMANTIC_PATH=$(python3 -c "import site; print([p for p in site.getusersitepackages().split(':') if 'site-packages' in p][0])")/semantic_text_splitter
if [ -d "$SEMANTIC_PATH" ]; then
    echo "🧹 Removing old semantic_text_splitter at: $SEMANTIC_PATH"
    rm -rf "$SEMANTIC_PATH"
else
    echo "✅ No shadowed semantic_text_splitter found in ~/.local"
fi

# Reinstall semantic-text-splitter
pip install semantic-text-splitter==0.25.1 --user

# Ensure langchain-community is installed
echo "🔄 Installing langchain-community module..."
pip install -U langchain-community --user

# Install Streamlit if not found
echo "🔍 Checking Streamlit availability..."
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit not found. Installing..."
    pip install streamlit --user
fi

# Fix PATH for ~/.local/bin
LOCAL_BIN="$HOME/.local/bin"
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    export PATH="$LOCAL_BIN:$PATH"
    echo "✅ Added $LOCAL_BIN to PATH"
else
    echo "✅ ~/.local/bin already in PATH"
fi

# Confirm Streamlit visibility and launch app
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit still not found after install. Run this to fix manually:"
    echo "    export PATH=$HOME/.local/bin:\$PATH"
else
    echo "✅ Environment Ready:"
    streamlit version
    echo -e "\\n🚀 Launching Streamlit app..."
    streamlit run app.py
fi
