# Package init — make skills/create-pptx importable
# Bundled python-pptx v0.6.18 available in packages/ as fallback

import os
import sys

# Add bundled packages to path as fallback
_packages_dir = os.path.join(os.path.dirname(__file__), "packages")
if os.path.isdir(_packages_dir) and _packages_dir not in sys.path:
    sys.path.insert(0, _packages_dir)
