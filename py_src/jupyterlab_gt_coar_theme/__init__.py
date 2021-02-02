from ._version import __js__, __version__


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": __js__["name"]}]


__all__ = ["__version__", "__js__"]
