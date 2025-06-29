#!/bin/bash
set -e

export PYTHONPATH=/home/razie/C2Rust/c2rust/source
echo "PYTHONPATH is $PYTHONPATH"

# Run the Rust test suite
pytest -s output_test.py