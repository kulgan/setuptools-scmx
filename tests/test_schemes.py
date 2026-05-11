import pytest
import setuptools_scm
from vcs_versioning._scm_version import meta
from vcs_versioning.overrides import GlobalOverrides

from setuptools_scmx.schemes import version_scheme


@pytest.fixture
def mock_version() -> setuptools_scm.ScmVersion:
    with GlobalOverrides.from_env("SETUPTOOLS_SCM"):
        c = setuptools_scm.Configuration()

        # Create test version with all properties set
        version = meta(
            "1.0.0",
            distance=5,
            dirty=True,
            node="abc123def456",
            branch="main",  # Default branch for the mock
            config=c,
        )
        return version


def test_version_scheme_with_env_var_main_rc(mock_version, temp_pyproject, monkeypatch):
    monkeypatch.setenv("SCMX_PYPROJECT_PATH", str(temp_pyproject))
    mock_version.branch = "main"
    result = version_scheme(mock_version)
    assert result == "1.0.1.rc.5"


def test_version_scheme_with_env_var_alpha_branch(mock_version, temp_pyproject, monkeypatch):
    monkeypatch.setenv("SCMX_PYPROJECT_PATH", str(temp_pyproject))
    mock_version.branch = "feature/alpha-branch"
    result = version_scheme(mock_version)
    assert result == "1.0.1.alpha.5"


def test_version_scheme_with_env_var_dev_branch(mock_version, temp_pyproject, monkeypatch):
    monkeypatch.setenv("SCMX_PYPROJECT_PATH", str(temp_pyproject))
    mock_version.branch = "develop"
    result = version_scheme(mock_version)
    assert result == "1.0.1.dev.5"


def test_version_scheme_unmapped_branch(mock_version, temp_pyproject, monkeypatch):
    monkeypatch.setenv("SCMX_PYPROJECT_PATH", str(temp_pyproject))
    mock_version.branch = "feature/unmapped-branch"  # This branch is not in labels
    result = version_scheme(mock_version)
    # The default behavior in BranchScheme.get_release_label for unmapped branches
    # is to normalize the branch name.
    assert result == "1.0.1+feature-unmapped-branch.5"


def test_version_scheme_default_no_config(mock_version, tmp_path, monkeypatch):
    # Create an empty pyproject.toml
    pp_path = tmp_path / "pyproject_empty.toml"
    pp_path.write_text("[project]\nname='empty'")

    monkeypatch.setenv("SCMX_PYPROJECT_PATH", str(pp_path))
    mock_version.branch = "any-branch"  # Branch doesn't matter here, as scmx_tool is None
    result = version_scheme(mock_version)
    assert result == "1.0.1+any-branch.5"
