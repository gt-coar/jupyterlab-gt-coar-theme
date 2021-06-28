# Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
# Distributed under the terms of the BSD-3-Clause License.

import json
from pathlib import Path

__js__ = [
    json.loads(pkg_json.read_text(encoding="utf-8"))
    for pkg_json in sorted(Path(__file__).parent.glob("labextensions/*/package.json"))
]

# have to pick one
__version__ = __js__[0]["version"]
