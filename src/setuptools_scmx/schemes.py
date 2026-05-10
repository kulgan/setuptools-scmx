import logging
import os
import pathlib

from pyprojectr import pyproject
from setuptools_scm.version import ScmVersion, guess_next_version

from setuptools_scmx import ScmxTool

logger = logging.getLogger(__name__)


def version_scheme(version: ScmVersion) -> str:
    pyproject_path = os.getenv("SCMX_PYPROJECT_PATH", "pyproject.toml")
    pyproj = pyproject.from_file(path=pathlib.Path(pyproject_path))
    scmx_tool = pyproj.get_tool_options("setuptools-scmx", ScmxTool)
    if scmx_tool is None:
        return guess_next_version(version)

    if scmx_tool.scheme == "branch-scheme":
        return branch_scheme(version, scmx_tool)
    return guess_next_version(version)


def branch_scheme(version: ScmVersion, scmx_tool: ScmxTool) -> str:
    """
    Versioning scheme:
    - Tags: Always exact (e.g., 1.2.3)
    - Main/Master Branch: {next_version}.dev{distance}
    - Feature Branches: {next_version}.{branch_name}.{distance}
    """
    env_scheme = scmx_tool.get_env_scheme()
    logger.debug("env scheme detected: %s", scmx_tool.env_scheme)
    env_version = env_scheme.get_version()
    if env_version:
        return env_version

    if version.exact:
        return version.format_with("{tag}")

    base_version = guess_next_version(version)
    branch = env_scheme.get_branch_name() or version.branch
    version_distance = env_scheme.get_build_number() or version.distance

    label = scmx_tool.branch_scheme.get_release_label(branch)
    return f"{base_version}.{label}.{version_distance}"
