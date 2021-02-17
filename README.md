# JupyterLab GT COAR Theme

[![launch interactive demo on binder][binder-badge]][binder]
[![install from PyPI][pypi-badge]][pypi]
[![install from conda-forge][conda-forge-badge]][conda-forge]
[![changelog][changelog-badge]][changelog]
[![contributing][contributing-badge]][contributing]

> an unoffical Georgia Tech theme for [JupyterLab] 3

## Install

```bash
pip install jupyterlab-gt-coar-theme
```

or

```bash
conda install -c conda-forge jupyterlab-gt-coar-theme
```

> See the [contributing guide][contributing] for a development install.

## Screenshots

| Light                                                | Dark                                               |
| ---------------------------------------------------- | -------------------------------------------------- |
| ![a screenshot of the light theme][screenshot-light] | ![a screenshot of the dark theme][screenshot-dark] |

[screenshot-light]:
  https://user-images.githubusercontent.com/7581399/106806206-a6a40900-6635-11eb-9e49-1c60fde1c1c5.png
[screenshot-dark]:
  https://user-images.githubusercontent.com/7581399/107781115-864f0b00-6d15-11eb-998b-789bc24ba921.png

## Usage

After launching JupyterLab, in the _Main Menu_, select _Settings ▸ JupyterLab Theme ▸ GT
COAR (Light|Dark) Theme_.

## Uninstall

```bash
pip uninstall jupyterlab-gt-coar-theme
```

or

```bash
conda uninstall jupyterlab-gt-coar-theme
```

---

> Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme
> contributors
>
> Distributed under the terms of the BSD-3-Clause License.

[pypi-badge]:
  https://img.shields.io/pypi/v/jupyterlab-gt-coar-theme?logo=pypi&style=flat-square&color=004f9f
[pypi]: https://pypi.org/project/jupyterlab-gt-coar-theme
[conda-forge-badge]:
  https://img.shields.io/conda/vn/conda-forge/jupyterlab-gt-coar-theme?logo=conda-forge&color=004f9f&style=flat-square
[conda-forge]: https://anaconda.org/conda-forge/jupyterlab-gt-coar-theme
[binder-badge]:
  https://img.shields.io/badge/binder-demo-f95e10?style=flat-square&logo=data:image/png;base64,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
[binder]: https://mybinder.org/v2/gh/gt-coar/jupyterlab-gt-coar-theme/HEAD?urlpath=lab
[jupyterlab]: https://github.com/jupyterlab/jupyterlab
[changelog]:
  https://github.com/gt-coar/jupyterlab-gt-coar-theme/blob/master/CHANGELOG.md
[changelog-badge]: https://img.shields.io/badge/CHANGELOG-md-f5d580?style=flat-square
[contributing-badge]:
  https://img.shields.io/badge/CONTRIBUTING-md-f5d580?style=flat-square
[contributing]:
  https://github.com/gt-coar/jupyterlab-gt-coar-theme/blob/master/CONTRIBUTING.md
