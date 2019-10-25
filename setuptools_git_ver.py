from typing import List
import subprocess

DEFTAULT_TEMPLATE: str = "{tag}"
DEFAULT_DEV_TEMPLATE: str = "{tag}.dev+git.{sha}"
DEFAULT_DIRTY_TEMPLATE: str = "{tag}.dev+git.{sha}.dirty"


def _exec(cmd: List[str]) -> List[str]:
    result = subprocess.run(cmd, capture_output=True, check=True)
    lines = result.stdout.decode().splitlines()
    return [l.rstrip() for l in lines]


def _get_tag():
    tags = _exec(
        "git tag --sort=-taggerdate".split(' '))
    if len(tags) == 0 or len(tags[0]) == 0:
        return None
    return tags[0]


def _get_sha(name):
    sha = _exec(f"git rev-list -n 1 '{name}'".split(' '))
    if len(sha) == 0 or len(sha[0]) == 0:
        return None
    return sha[0]


def _is_dirty():
    res = _exec("git status --short".split(' '))
    if len(res) == 0 or len(res[0]) == 0:
        return True
    return False


def version_from_git(template: str = DEFTAULT_TEMPLATE,
                     dev_template: str = DEFAULT_DEV_TEMPLATE,
                     dirty_template: str = DEFAULT_DIRTY_TEMPLATE,
                     default_ver: str = None,
                     ) -> None:
    tag = _get_tag()
    dirty = _is_dirty()
    if tag is None:
        if default_ver is None:
            raise Exception(
                "Couldn't find tag to use and no default was specified")
        tag = default_ver
        tag_sha = _get_sha('HEAD')
        t = dirty_template if dirty else dev_template
    else:
        tag_sha = _get_sha(tag)
        head_sha = _get_sha('HEAD')

        if dirty:
            t = dirty_template
        elif head_sha != tag_sha:
            t = dev_template
        else:
            t = template

    return t.format(sha=tag_sha[:8], tag=tag)
