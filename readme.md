# setuptools-git-ver

[![PyPI version](https://badge.fury.io/py/setuptools-git-ver.svg)](https://badge.fury.io/py/setuptools-git-ver)
[![Build Status](https://travis-ci.org/camas/setuptools-git-ver.svg?branch=master)](https://travis-ci.org/camas/setuptools-git-ver)

Automatically set package version using git tag/hash

## Install

Install using pip

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
