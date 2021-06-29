"""automation for jupyterlab-gt-coar-theme"""
# Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
# Distributed under the terms of the BSD-3-Clause License.

import json
import os
import shutil
import subprocess
from datetime import datetime
from hashlib import sha256
from pathlib import Path

from doit import tools

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
    return dict(task_dep=["dev:ext"], actions=[["echo", "ok"]])


def task_setup():
    """ensure a working setup"""
    yield dict(
        name="js",
        doc="ensure local npm dependencies",
        uptodate=[tools.config_changed(U.pkg_deps(P.PKG_JSONS))],
        actions=[[*C.JLPM, "--prefer-offline"], [*C.LERNA, "bootstrap"]],
        targets=[P.YARN_INTEGRITY],
    )


def task_build():
    """build intermediate artifacts"""
    yield dict(
        name="lib",
        doc="build the js libs",
        file_dep=[P.YARN_INTEGRITY, *P.ALL_TS_SRC, *P.PKG_JSONS, *P.TSCONFIGS],
        actions=[[*C.JLPM, "build:lib"]],
        targets=[P.TSBUILD],
    )

    yield dict(
        name="ext",
        doc="build the federated labextension",
        actions=[[*C.JLPM, "build:ext"]],
        file_dep=[P.TSBUILD, *P.ALL_STYLE],
        targets=[*B.EXT_PKGS],
    )


def task_dist():
    """build artifacts for distribution"""
    for variant, tgz in B.NPM_TGZS.items():
        yield dict(
            name=f"tgz:{variant}",
            doc=f"build the {variant} npm distribution",
            file_dep=[P.TSBUILD, *P.ALL_STYLE, *P.PKG_JSONS, *P.READMES, *P.LICENSES],
            actions=[
                (tools.create_folder, [P.DIST]),
                tools.CmdAction(
                    [*C.NPM_PACK, P.PACKAGES / variant], cwd=P.DIST, shell=False
                ),
            ],
            targets=[tgz],
        )

    for cmd, dist in B.PY_DIST_CMD.items():
        yield dict(
            name=cmd,
            doc=f"build the python {cmd}",
            actions=[[*C.SETUP, cmd], [*C.TWINE_CHECK, dist]],
            file_dep=[
                *P.ALL_PY_SRC,
                *B.EXT_PKGS,
                P.README,
                P.LICENSE,
                P.MANIFEST,
                P.SETUP_PY,
                P.SETUP_CFG,
            ],
            targets=[dist],
        )

    def _run_hash():
        # mimic sha256sum CLI
        if P.SHA256SUMS.exists():
            P.SHA256SUMS.unlink()

        lines = []

        for p in B.HASH_DEPS:
            if p.parent != P.DIST:
                tgt = P.DIST / p.name
                if tgt.exists():
                    tgt.unlink()
                shutil.copy2(p, tgt)
            lines += ["  ".join([sha256(p.read_bytes()).hexdigest(), p.name])]

        output = "\n".join(lines)
        print(output)
        P.SHA256SUMS.write_text(output)

    yield dict(
        name="hash",
        doc="make a hash bundle of the dist artifacts",
        actions=[_run_hash],
        file_dep=B.HASH_DEPS,
        targets=[P.SHA256SUMS],
    )


def task_dev():
    """prepare for interactive development"""
    yield dict(
        name="py",
        doc="install python for interactive development",
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
        file_dep=[*B.EXT_PKGS],
    )

    yield dict(
        name="ext",
        doc="ensure the labextension is symlinked for live development",
        actions=[[*C.LAB_EXT, "develop", "--overwrite", "."]],
        task_dep=["dev:py"],
    )


def task_lab():
    """start jupyterlab"""
    return dict(
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
                [*C.JLPM, "watch:lib"],
                [*C.JLPM, "watch:ext"],
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
        actions=[tools.PythonInteractiveAction(_watch)],
    )


def task_lint():
    """apply source formatting and linting"""
    yield dict(
        name="py",
        doc="run basic python formatting/checking",
        file_dep=P.ALL_PY,
        actions=[
            ["isort", *P.ALL_PY],
            ["black", "--quiet", *P.ALL_PY],
            ["pyflakes", *P.ALL_PY],
        ],
    )

    yield dict(
        name="prettier",
        doc="format things with prettier",
        file_dep=[*P.ALL_PRETTIER, P.YARN_INTEGRITY],
        actions=[[*C.JLPM, "--silent", "lint"]],
    )

    def _header(path):
        def _check():
            any_text = path.read_text()
            problems = []
            if C.COPYRIGHT not in any_text:
                problems += [f"{path.relative_to(P.ROOT)} missing copyright info"]
            if path != P.LICENSE and C.LICENSE not in any_text:
                problems += [f"{path.relative_to(P.ROOT)} missing license info"]
            if problems:
                print("\n".join(problems))
                return False
            return True

        return _check

    for path in P.ALL_HEADERS:
        yield dict(
            name=f"headers:{path.relative_to(P.ROOT)}",
            doc=f"ensure license/copyright on {path.name}",
            file_dep=[path],
            actions=[_header(path)],
        )


class C:
    """commands and constants"""

    PYM = ["python", "-m"]
    PIP = [*PYM, "pip"]
    JP = ["jupyter"]
    LAB_EXT = [*JP, "labextension"]
    LAB = [*JP, "lab"]
    SETUP = ["python", "setup.py"]
    NPM_PACK = ["npm", "pack"]
    TWINE_CHECK = [*PYM, "twine", "check"]
    JLPM = ["jlpm"]
    LERNA = [*JLPM, "lerna"]
    ENC = dict(encoding="utf-8")

    # the first one will be used for various metadata tasks
    VARIANTS = ["dark", "light"]

    JS_TGZ_PREFIX = "gt-coar-jupyterlab-theme"
    PY_NAME = "jupyterlab-gt-coar-theme"

    # this line is very long, should end with "contributors," but close enough
    COPYRIGHT = (
        "Copyright (c) {} "
        "University System of Georgia and jupyterlab-gt-coar-theme".format(
            datetime.now().year
        )
    )
    LICENSE = "Distributed under the terms of the BSD-3-Clause License."


class U:
    @staticmethod
    def clean(paths):
        return [p for p in paths if "checkpoints" not in str(p)]

    @staticmethod
    def pkg_deps(pkg_jsons):
        deps = {}
        for pkg_json in pkg_jsons:
            pkg = json.loads(pkg_json.read_text(**C.ENC))
            for key in ["dependencies", "devDependencies", "peerDependencies"]:
                deps.update(pkg.get(key, {}))
        return deps


class P:
    """paths"""

    DODO = Path(__file__)
    ROOT = DODO.parent

    BUILD = ROOT / "build"
    DIST = ROOT / "dist"
    LIB = ROOT / "lib"
    BINDER = ROOT / ".binder"
    CI = ROOT / ".github"

    SETUP_PY = ROOT / "setup.py"
    SETUP_CFG = ROOT / "setup.cfg"
    MANIFEST = ROOT / "MANIFEST.in"

    PACKAGES = ROOT / "packages"
    META = PACKAGES / "_meta"
    META_PKG_JSON = META / "package.json"

    PKG_JSON = ROOT / "package.json"
    A_PKG_JSON = PACKAGES / f"{C.VARIANTS[0]}/package.json"
    PKG_JSONS = [PKG_JSON, *PACKAGES.glob("*/package.json")]
    TSCONFIG = ROOT / "tsconfigbase.json"
    TSCONFIGS = [TSCONFIG, *PACKAGES.glob("*/tsconfig.json")]
    TSBUILD = META / "tsconfig.tsbuildinfo"
    PY_SRC = ROOT / "py_src/jupyterlab_gt_coar_theme"
    EXT_DIST = PY_SRC / "labextensions"

    ALL_TS_SRC = sorted(PACKAGES.glob("*/src/*.ts"))
    ALL_PY_SRC = sorted(PY_SRC.rglob("*.py"))
    ALL_PY = [*ALL_PY_SRC, DODO]
    ALL_CSS = [*PACKAGES.rglob("*/style/**/*.css")]
    ALL_JSON = [
        *ROOT.glob("*.json"),
        *PACKAGES.glob("*/*.json"),
        *BINDER.rglob("*.json"),
    ]
    README = ROOT / "README.md"
    READMES = [README, *PACKAGES.glob("*/README.md")]
    LICENSE = ROOT / "LICENSE.txt"
    LICENSES = [LICENSE, *PACKAGES.glob("*/LICENSE.txt")]
    ALL_MD = sorted([*ROOT.glob("*.md"), *PACKAGES.glob("*.md")])
    ALL_STYLE = [*ALL_CSS, *PACKAGES.rglob("*/style/**/*.svg")]
    ALL_YAML = [*CI.rglob("*.yml"), *BINDER.glob("*.yml")]
    ALL_PRETTIER = [*ALL_MD, *ALL_STYLE, *ALL_JSON, *ALL_YAML, *ALL_TS_SRC]
    ALL_SHELL = [BINDER / "postBuild"]
    ALL_HEADERS = U.clean(
        [
            *ALL_PY,
            *ALL_CSS,
            *ALL_TS_SRC,
            *ALL_MD,
            *ALL_YAML,
            *ALL_SHELL,
            LICENSE,
            SETUP_CFG,
        ]
    )

    YARN_INTEGRITY = ROOT / "node_modules/.yarn-integrity"
    WEBPACK_JS = ROOT / "webpack.config.js"
    INDEX_CSS = LIB / "index.css"
    PLUGIN_JS = LIB / "index.js"

    SHA256SUMS = DIST / "SHA256SUMS"


class D:
    """data"""

    PKG = json.loads(P.A_PKG_JSON.read_text(encoding="utf-8"))


class B:
    """builds"""

    EXT_PKGS = [P.EXT_DIST / f"{v}/package.json" for v in C.VARIANTS]
    NPM_TGZS = {
        v: P.DIST / ("{}-{}-{}.tgz".format(C.JS_TGZ_PREFIX, v, D.PKG["version"]))
        for v in [*C.VARIANTS, "brand"]
    }
    SDIST = P.DIST / ("{}-{}.tar.gz".format(C.PY_NAME, D.PKG["version"]))
    WHEEL = P.DIST / (
        "{}-{}-py3-none-any.whl".format(C.PY_NAME.replace("-", "_"), D.PKG["version"])
    )
    HASH_DEPS = [WHEEL, SDIST, *NPM_TGZS.values()]
    PY_DIST_CMD = {"sdist": SDIST, "bdist_wheel": WHEEL}
