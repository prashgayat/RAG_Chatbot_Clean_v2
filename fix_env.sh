#!/bin/bash

echo "🔄 Cleaning up environment and reinstalling semantic-text-splitter..."

pip uninstall -y semantic-text-splitter
pip install semantic-text-splitter==0.25.1

echo "✅ semantic-text-splitter reinstalled successfully."
streamlit run app.py
