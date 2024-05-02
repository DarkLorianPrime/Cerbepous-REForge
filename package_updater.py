import os
import subprocess
from typing import List

import tomli
import re

import tomli_w

find_dev_version = re.compile(r"([0-9]+)")
with open("pyproject.toml", "rb") as f:
    config_file = tomli.load(f)


def get_dev_version(last_part: str) -> int:
    dev_version = find_dev_version.search(last_part)
    if not dev_version:
        return -1

    return int(dev_version.group(1))


def get_actual_version(old_actual_version: str) -> str:
    parts: List[str] = old_actual_version.split(".")
    if len(parts) != 4:
        return f"{old_actual_version}.dev0"

    last_part = parts[-1]
    dev_version = get_dev_version(last_part) + 1

    version = ".".join(parts[:-1])
    return f"{version}.dev{dev_version}"


new_version = get_actual_version(
    old_actual_version=config_file["tool"]["poetry"]["version"]
)

config_file["tool"]["poetry"]["version"] = new_version
f = open("pyproject.toml", "wb")
tomli_w.dump(config_file, f)
f.close()

subprocess.run(["rm", "-rf", "dist"])
subprocess.run(["poetry", "build", "--format", "wheel"])
subprocess.run(
    ["docker-compose", "--project-directory", "examples/cerberous", "restart"]
)
