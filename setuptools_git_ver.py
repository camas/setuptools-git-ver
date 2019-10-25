from typing import List
import subprocess
from setuptools.dist import Distribution
from distutils.errors import DistutilsSetupError
from collections.abc import Mapping
import os.path

DEFAULT_TEMPLATE: str = "{tag}"
DEFAULT_DEV_TEMPLATE: str = "{tag}.dev{ccount}+git.{sha}"
DEFAULT_DIRTY_TEMPLATE: str = "{tag}.dev{ccount}+git.{sha}.dirty"


def _exec(cmd: List[str]) -> List[str]:
    result = subprocess.run(cmd, capture_output=True, check=True)
    lines = result.stdout.decode().splitlines()
    return [l.rstrip() for l in lines]


def _get_tag() -> str:
    tags = _exec(
        "git tag --sort=-version:refname --merged".split(' '))
    if len(tags) == 0 or len(tags[0]) == 0:
        return None
    return tags[0]


def _get_sha(name: str) -> str:
    sha = _exec([*f"git rev-list -n 1".split(' '), name])
    if len(sha) == 0 or len(sha[0]) == 0:
        return None
    return sha[0]


def _is_dirty() -> bool:
    res = _exec("git status --short".split(' '))
    if len(res) == 0 or len(res[0]) == 0:
        return False
    return True


def _count_since(name: str) -> int:
    res = _exec([*"git rev-list --count HEAD".split(' '), f"^{name}"])
    return int(res[0])


def parse_config(dist: Distribution, _, value):
    if isinstance(value, bool):
        if value:
            version = version_from_git()
            dist.metadata.version = version
            return
        else:
            raise DistutilsSetupError("Can't be False")

    if not isinstance(value, Mapping):
        raise DistutilsSetupError("Config in the wrong format")

    template = value['template'] if 'template' in value else DEFAULT_TEMPLATE
    dev_template = value['dev_template'] if 'dev_template' in value \
        else DEFAULT_DEV_TEMPLATE
    dirty_template = value['dirty_template'] if 'dirty_template' in value \
        else DEFAULT_DIRTY_TEMPLATE

    version = version_from_git(
        template=template,
        dev_template=dev_template,
        dirty_template=dirty_template,
    )
    dist.metadata.version = version


def version_from_git(template: str = DEFAULT_TEMPLATE,
                     dev_template: str = DEFAULT_DEV_TEMPLATE,
                     dirty_template: str = DEFAULT_DIRTY_TEMPLATE,
                     ) -> None:

    # Check if PKG-INFO exists and return value in that if it does
    if os.path.exists('PKG-INFO'):
        with open('PKG-INFO', 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('Version:'):
                return line[8:].strip()

    tag = _get_tag()
    if tag is None:
        raise Exception("Couldn't find tag to use.")

    dirty = _is_dirty()
    tag_sha = _get_sha(tag)
    head_sha = _get_sha('HEAD')
    ccount = _count_since(tag)
    on_tag = head_sha == tag_sha

    if dirty:
        t = dirty_template
    elif not on_tag:
        t = dev_template
    else:
        t = template

    return t.format(sha=head_sha[:8], tag=tag, ccount=ccount)
