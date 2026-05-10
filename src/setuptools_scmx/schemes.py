import pathlib

from setuptools_scm.version import ScmVersion, guess_next_version
from pyprojectr import pyproject

from setuptools_scmx import ScmxTool


def version_scheme(version: ScmVersion) -> str:
    pyproj = pyproject.from_file(path=pathlib.Path("pyproject.toml"))
    scmx_tool = pyproj.get_tool_options("setuptools-scmx", ScmxTool)
    print(scmx_tool)
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
    if version.exact:
        return version.format_with("{tag}")

    base_version = guess_next_version(version)
    branch = version.branch

    label = scmx_tool.branch_scheme.get_release_label(branch)
    return f"{base_version}.{label}.{version.distance}"
