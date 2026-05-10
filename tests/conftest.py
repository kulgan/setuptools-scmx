import pathlib

import pytest


@pytest.fixture
def temp_pyproject(tmp_path: pathlib.Path) -> pathlib.Path:
    pyproject_content = """
[project]
name = "test-project"

[tool.setuptools-scmx]
scheme = "branch-scheme"

[tool.setuptools-scmx.branch-scheme]
labels = [
  { name = "rc", branches = ["main"] },
  { name = "alpha", branches = ["feature/alpha-branch"] },
  { name = "dev", branches = ["develop"] }
]
"""
    pp_path = tmp_path / "pyproject.toml"
    pp_path.write_text(pyproject_content)
    return pp_path
