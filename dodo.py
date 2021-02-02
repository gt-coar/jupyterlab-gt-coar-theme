import json
import os
import subprocess
from pathlib import Path

from doit.tools import PythonInteractiveAction, config_changed

os.environ.update(
    NODE_OPTS="--max-old-space-size=4096",
    PYTHONIOENCODING="utf-8",
    PIP_DISABLE_PIP_VERSION_CHECK="1",
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
            config_changed(
                dict({k: D.PKG[k] for k in D.PKG if "dependencies" in k.lower()})
            )
        ],
        actions=[["jlpm", "--prefer-offline"]],
        targets=[P.YARN_INTEGRITY],
    )


def task_build():
    yield dict(
        name="lib",
        file_dep=[P.YARN_INTEGRITY, *P.ALL_TS_SRC, P.PKG_JSON, P.TSCONFIG],
        actions=[["jlpm", "build:lib"]],
        targets=[P.TSBUILD, P.PLUGIN_JS],
    )

    yield dict(
        name="ext",
        actions=[[*C.LAB_EXT, "build", "--debug", "."]],
        file_dep=[P.TSBUILD],
        targets=[P.EXT_PKG],
    )

    for cmd, dist in D.PY_DIST_CMD.items():
        yield dict(
            name=cmd,
            actions=[[*C.SETUP, cmd]],
            file_dep=[
                *P.ALL_PY_SRC,
                P.EXT_PKG,
                P.README,
                P.LICENSE,
                P.MANIFEST,
                P.SETUP_PY,
                P.SETUP_CFG,
            ],
            targets=[dist],
        )


def task_dev():
    """start jupyterlab"""
    yield dict(
        name="py",
        actions=[
            [
                *C.PIP,
                "install",
                "-e",
                ".",
                "--no-deps",
                "--ignore-installed",
            ]
        ],
        file_dep=[P.EXT_PKG],
    )

    yield dict(
        name="ext",
        actions=[[*C.LAB_EXT, "develop", "--overwrite", "."]],
        task_dep=["dev:py"],
    )


def task_lab():
    """"""
    yield dict(
        name="start",
        uptodate=[lambda: False],
        task_dep=["dev:ext"],
        actions=[[*C.LAB, "--no-browser", "--debug"]],
    )


def task_watch():
    """watch typescript sources, rebuilding as files change"""

    def _watch():
        watchers = [
            subprocess.Popen(args)
            for args in [
                ["jlpm", "watch:lib"],
                # ["jlpm", "watch:webpack"],
                [*C.LAB_EXT, "watch", "."],
            ]
        ]

        def stop():
            [w.terminate() for w in watchers]
            [w.wait() for w in watchers]

        try:
            watchers[0].wait()
        except KeyboardInterrupt:
            pass
        finally:
            stop()
        return True

    return dict(
        uptodate=[lambda: False],
        task_dep=["dev:ext"],
        actions=[PythonInteractiveAction(_watch)],
    )


def task_lint():
    """apply source formatting and linting"""
    yield dict(
        name="py",
        file_dep=P.ALL_PY,
        actions=[
            ["isort", *P.ALL_PY],
            ["black", "--quiet", *P.ALL_PY],
            ["pyflakes", *P.ALL_PY],
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
    LIB = ROOT / "lib"

    SETUP_PY = ROOT / "setup.py"
    SETUP_CFG = ROOT / "setup.cfg"
    MANIFEST = ROOT / "MANIFEST.in"

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
    README = ROOT / "README.md"
    LICENSE = ROOT / "LICENSE.txt"
    ALL_MD = sorted(ROOT.glob("*.md"))
    ALL_PRETTIER = [*ALL_MD, *ALL_STYLE, *ALL_JSON]

    YARN_INTEGRITY = ROOT / "node_modules/.yarn-integrity"
    WEBPACK_JS = ROOT / "webpack.config.js"
    INDEX_CSS = LIB / "index.css"
    PLUGIN_JS = LIB / "index.js"


class D:
    """data"""

    PKG = json.loads(P.PKG_JSON.read_text(encoding="utf-8"))
    PY_NAME = PKG["jupyterlab"]["discovery"]["server"]["base"]["name"]
    SDIST = P.DIST / ("{}-{}.tar.gz".format(PY_NAME, PKG["version"]))
    WHEEL = P.DIST / (
        "{}-{}-py3-none-any.whl".format(PY_NAME.replace("-", "_"), PKG["version"])
    )
    PY_DIST_CMD = {"sdist": SDIST, "bdist_wheel": WHEEL}


class C:
    """commands"""

    PYM = ["python", "-m"]
    PIP = [*PYM, "pip"]
    JP = ["jupyter"]
    LAB_EXT = [*JP, "labextension"]
    LAB = [*JP, "lab"]
    SETUP = ["python", "setup.py"]
