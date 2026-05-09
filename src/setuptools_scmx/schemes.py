import pathlib

from setuptools_scm.version import ScmVersion, guess_next_version

from pyprojectr import pyproject

from setuptools_scmx import ScmxTool


def version_scheme(version: ScmVersion) -> str:
    pyproj = pyproject.from_file(path=pathlib.Path("pyproject.toml"))
    scmx_tool = pyproj.get_tool_options("setuptools-scmx", ScmxTool)



def branch_aware_scheme(version: ScmVersion) -> str:
    """
    Versioning scheme:
    - Tags: Always exact (e.g., 1.2.3)
    - Main/Master Branch: {next_version}.dev{distance}
    - Feature Branches: {next_version}.{branch_name}.{distance}
    """
    if version.exact:
        return version.format_with("{tag}")

    base_version = guess_next_version(version.tag)
    branch = version.branch

    if branch in ["main", "master"]:
        return f"{base_version}.dev{version.distance}"

    # Normalize branch name for PEP 440 compatibility if possible,
    # or keep it descriptive for internal builds.
    branch_name = branch.replace("/", "-").replace("_", "-") if branch else "detached"
    return f"{base_version}.{branch_name}.{version.distance}"


def jenkins_build_scheme(version: ScmVersion) -> str:
    """
    Specialized version of the branch-aware scheme for Jenkins environments.
    """
    return branch_aware_scheme(version)


def ci_version_scheme(version: ScmVersion) -> str:
    """
    General CI version scheme.
    """
    return branch_aware_scheme(version)
