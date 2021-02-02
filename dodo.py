import json
import os
from pathlib import Path

from doit.tools import config_changed

os.environ.update(
    NODE_OPTS="--max-old-space-size=4096",
    PYTHONIOENCODING="utf-8",
    PIP_DISABLE_PIP_VERSION_CHECK="1",
    MAMBA_NO_BANNER="1",
)

DOIT_CONFIG = {
    "backend": "sqlite3",
    "verbosity": 2,
    "par_type": "thread",
    "default_tasks": ["binder"],
}


def task_binder():
    """prepare for basic interactive development, as on binder"""
    return dict(actions=[["echo", "ok"]])


def task_setup():
    yield dict(
        name="js",
        uptodate=[
            config_changed(dict({k: D.PKG[k] for k in D.PKG if "ependencies" in k}))
        ],
        actions=[["jlpm", "--prefer-offline"]],
        targets=[P.YARN_INTEGRITY],
    )


def task_build():
    yield dict(
        name="lib",
        file_dep=[P.YARN_INTEGRITY, *P.ALL_TS_SRC, P.PKG_JSON, P.TSCONFIG],
        actions=[["jlpm", "build:lib"]],
        targets=[P.TSBUILD],
    )

    yield dict(
        name="ext",
        actions=[["jupyter", "labextension", "build", "."]],
        file_dep=[P.TSBUILD],
        targets=[P.EXT_PKG],
    )


def task_lab():
    """start jupyterlab"""
    return dict(actions=[["jupyter", "lab", "--no-browser", "--debug"]])


def task_lint():
    """apply source formatting and linting"""
    yield dict(
        name="py",
        file_dep=P.ALL_PY,
        actions=[
            ["isort", *P.ALL_PY],
            ["black", "--quiet", *P.ALL_PY],
        ],
    )

    yield dict(
        name="js",
        file_dep=[*P.ALL_PRETTIER, P.YARN_INTEGRITY],
        actions=[["jlpm", "--silent", "lint"]],
    )


class P:
    """paths"""

    DODO = Path(__file__)
    ROOT = DODO.parent

    BUILD = ROOT / "build"
    DIST = ROOT / "dist"

    SETUP_PY = ROOT / "setup.py"
    SETUP_CFG = ROOT / "setup.cfg"

    PKG_JSON = ROOT / "package.json"
    TSCONFIG = ROOT / "tsconfig.json"
    TSBUILD = BUILD / "tsconfig.tsbuildinfo"
    PY_SRC = ROOT / "py_src/jupyterlab_gt_coar_theme"
    EXT_DIST = PY_SRC / "labextension"
    EXT_PKG = EXT_DIST / "package.json"
    TS_SRC = ROOT / "src"
    STYLE = ROOT / "style"
    ALL_STYLE = [*STYLE.rglob("*.css"), *STYLE.rglob("*.svg")]

    ALL_TS_SRC = sorted(TS_SRC.rglob("*.ts"))
    ALL_PY_SRC = sorted(PY_SRC.rglob("*.py"))
    ALL_PY = [*ALL_PY_SRC, DODO]
    ALL_JSON = sorted(ROOT.glob("*.json"))
    ALL_MD = sorted(ROOT.glob("*.md"))
    ALL_PRETTIER = [*ALL_MD, *ALL_STYLE, *ALL_JSON]

    YARN_INTEGRITY = ROOT / "node_modules/.yarn-integrity"


class D:
    """data"""

    PKG = json.loads(P.PKG_JSON.read_text(encoding="utf-8"))
