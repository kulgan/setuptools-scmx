import pathlib

from pyprojectr import pyproject

from setuptools_scmx.models import ScmxTool
from setuptools_scmx.schemes import branch_scheme, version_scheme

__all__ = ["ScmxTool", "branch_scheme", "version_scheme"]


if __name__ == "__main__":
    pyt = pyproject.from_file(path=pathlib.Path("../../pyproject.toml"))
    print(pyt.get_tool_options("setuptools-scmx", ScmxTool))
