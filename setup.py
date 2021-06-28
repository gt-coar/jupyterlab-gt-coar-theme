# Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
# Distributed under the terms of the BSD-3-Clause License.

import re
from pathlib import Path
import json

import setuptools

HERE = Path(__file__).parent
MOD = "jupyterlab_gt_coar_theme"
VARIANTS = ["dark", "light"]
EXTS = [
    HERE / "py_src" / MOD / f"labextensions/{v}"
    for v in VARIANTS
]
PKG_JSONS = [
    ext / "package.json"
    for ext in EXTS
]
PKGS = [
    json.loads(pkg_json.read_text(encoding="utf-8"))
    for pkg_json in PKG_JSONS
]

SHARE = f"""share/jupyter/labextensions"""
EXT_FILES = {
    f"""{SHARE}/{pkg["name"]}""": ["install.json"]
    for pkg in PKGS
}

for ext, pkg in zip(EXTS, PKGS):
    for ext_path in [ext] + [d for d in ext.rglob("*") if d.is_dir()]:
        target = f"""{SHARE}/{pkg["name"]}"""
        if ext_path != ext:
            target = f"""{target}/{ext_path.relative_to(ext)}"""
        EXT_FILES[target] = [
            str(p.relative_to(HERE).as_posix())
            for p in ext_path.glob("*")
            if not p.is_dir()
        ]

DATA_FILES = sorted([(k, v) for k, v in EXT_FILES.items()])

SETUP_ARGS = dict(
    name=PKGS[0]["jupyterlab"]["discovery"]["server"]["base"]["name"],
    description=PKGS[0]["description"],
    version=PKGS[0]["version"],
    url=PKGS[0]["homepage"],
    license=PKGS[0]["license"],
    data_files=DATA_FILES,
    project_urls={
        "Bug Tracker": PKGS[0]["bugs"]["url"],
        "Source Code": PKGS[0]["repository"]["url"]
    },
    author=re.findall(r'^[^<]+', PKGS[0]["author"])[0].strip(),
    author_email=re.findall(r'<(.*)>$', PKGS[0]["author"])[0].strip()
)


if __name__ == "__main__":
    setuptools.setup(**SETUP_ARGS)
