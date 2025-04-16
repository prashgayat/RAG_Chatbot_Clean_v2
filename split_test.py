# split_test.py
from text_split.Hybrid_splitter import HybridTextSplitter

sample_text = """
Section 1: Introduction

This is a test document. It contains some example content.

Clause 2: Responsibilities

Each member shall...

Chapter 3: Closure
"""

splitter = HybridTextSplitter()
chunks = splitter.split(sample_text)

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ---\n{chunk}")
