# Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
# Distributed under the terms of the BSD-3-Clause License.

from ._version import __js__, __version__


def _jupyter_labextension_paths():
    return [
        {"src": f"""labextensions/{pkg["name"].split("-")[-1]}""", "dest": pkg["name"]}
        for pkg in __js__
    ]


__all__ = ["__version__", "__js__"]
