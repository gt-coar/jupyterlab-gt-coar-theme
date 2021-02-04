# Contributing to jupyterlab-gt-coar-theme

## Get an environment

- get [Mambaforge](https://github.com/conda-forge/miniforge/releases)

```bash
CONDARC=.github/.condarc mamba env update --file .binder/environment.yml
```

Activate your environment:

```bash
mamba activate jupyterlab-gt-coar-theme
```

## Use doit

[doit](https://pydoit.org) is used to manage everything _inside_ your environment.

```
doit list --all --status
```

## Make a PR

Issues (and PRs) welcome, and will be reviewed to the best of the maintainers'
abilities/availability. Please ensure you've run `doit lint` before pushing!

---

> Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme
> contributors
>
> Distributed under the terms of the BSD-3-Clause License.
