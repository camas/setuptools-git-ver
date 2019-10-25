from typing import List
import subprocess

DEFTAULT_TEMPLATE: str = "{tag}"
DEFAULT_DEV_TEMPLATE: str = "{tag}.dev{ccount}+git.{sha}"
DEFAULT_DIRTY_TEMPLATE: str = "{tag}.dev{ccount}+git.{sha}.dirty"


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
    sha = _exec([*f"git rev-list -n 1".split(' '), name])
    if len(sha) == 0 or len(sha[0]) == 0:
        return None
    return sha[0]


def _is_dirty():
    res = _exec("git status --short".split(' '))
    if len(res) == 0 or len(res[0]) == 0:
        return False
    return True


def _count_since(name):
    res = _exec([*"git rev-list --count HEAD".split(' '), f"^{name}"])
    return int(res[0])


def version_from_git(template: str = DEFTAULT_TEMPLATE,
                     dev_template: str = DEFAULT_DEV_TEMPLATE,
                     dirty_template: str = DEFAULT_DIRTY_TEMPLATE,
                     ) -> None:
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
