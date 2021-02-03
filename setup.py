# Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
# Distributed under the terms of the BSD-3-Clause License.

import re
from pathlib import Path
import json

import setuptools

HERE = Path(__file__).parent
MOD = "jupyterlab_gt_coar_theme"
EXT = HERE / "py_src" / MOD / "labextension"
PKG_JSON = EXT / "package.json"
PKG = json.loads(PKG_JSON.read_text(encoding="utf-8"))

SHARE = f"""share/jupyter/labextensions/{PKG["name"]}"""
EXT_FILES = {SHARE: ["install.json"]}

for ext_path in [EXT] + [d for d in EXT.rglob("*") if d.is_dir()]:
    if ext_path == EXT:
        target = str(SHARE)
    else:
        target = f"{SHARE}/{ext_path.relative_to(EXT)}"
    EXT_FILES[target] = [
        str(p.relative_to(HERE).as_posix())
        for p in ext_path.glob("*")
        if not p.is_dir()
    ]

SETUP_ARGS = dict(
    name=PKG["jupyterlab"]["discovery"]["server"]["base"]["name"],
    description=PKG["description"],
    version=PKG["version"],
    url=PKG["homepage"],
    license=PKG["license"],
    data_files=[(k, v) for k, v in EXT_FILES.items()],
    project_urls={
        "Bug Tracker": PKG["bugs"]["url"],
        "Source Code": PKG["repository"]["url"]
    },
    author=PKG["author"]["name"],
    author_email=PKG["author"]["email"]
)


if __name__ == "__main__":
    setuptools.setup(**SETUP_ARGS)
