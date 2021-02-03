# Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
# Distributed under the terms of the BSD-3-Clause License.

import json
from pathlib import Path

__js__ = json.loads(
    (Path(__file__).parent / "labextension/package.json").read_text(encoding="utf-8")
)
__version__ = __js__["version"]
