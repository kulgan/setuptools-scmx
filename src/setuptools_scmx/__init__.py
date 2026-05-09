import pathlib

from pyprojectr import pyproject

from setuptools_scmx.models import ScmxTool


__all__ = [
    "ScmxTool",
]


if __name__ == '__main__':
    pyt = pyproject.from_file(path=pathlib.Path("../../pyproject.toml"))
    print(pyt.get_tool_options("setuptools-scmx", ScmxTool))