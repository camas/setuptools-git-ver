# setuptools-git-ver

[![PyPI version](https://badge.fury.io/py/setuptools-git-ver.svg)](https://badge.fury.io/py/setuptools-git-ver)
[![Build Status](https://travis-ci.com/camas/setuptools-git-ver.svg?branch=master)](https://travis-ci.com/camas/setuptools-git-ver)

Automatically set package version using git tag/hash

## Installation

No need.

Adding `setup_requires=['setuptools-git-ver']` somewhere in `setup.py` will automatically download the latest version from PyPi and save it in the `.eggs` folder when `setup.py` is run.

## Usage

To just use the default templates for versioning:

```python
setuptools.setup(
    ...
    version_config=True,
    ...
    setup_requires=['setuptools-git-ver'],
    ...
)
```

Changing templates (also shows the defaults):

```python
setuptools.setup(
    ...
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}.dev{ccount}+git.{sha}"
        "dirty_template": "{tag}.dev{ccount}+git.{sha}.dirty"
    },
    ...
    setup_requires=['setuptools-git-ver'],
    ...
)
```

### Templates

- `template`: used if no untracked files and latest commit is tagged

- `dev_template`: used if no untracked files and latest commit isn't tagged

- `dirty_template`: used if untracked files exist or uncommitted changes have been made

### Format Options

- `{tag}`: Latest tag in the repository

- `{ccount}`: Number of commits since last tag

- `{sha}`: First 8 characters of the sha hash of the latest commit
