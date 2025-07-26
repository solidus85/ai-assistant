#!/usr/bin/env python3
"""Legacy compatibility wrapper - use run.py instead."""
import warnings
from run import app

warnings.warn(
    "app.py is deprecated. Please use 'python run.py' instead.",
    DeprecationWarning,
    stacklevel=2
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)