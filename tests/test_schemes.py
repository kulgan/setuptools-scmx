from unittest.mock import Mock
import pytest
from setuptools_scmx.schemes import branch_scheme
from setuptools_scmx.models import ScmxTool, BranchScheme, ReleaseLabel


@pytest.fixture
def mock_version():
    version = Mock()
    # The versioning library expects version.tag to be an object with a .tag attribute
    tag_mock = Mock()
    tag_mock.tag = "1.0.0"
    version.tag = tag_mock

    version.distance = 5
    version.exact = False
    version.branch = "main"
    # format_with is used for exact tags
    version.format_with = lambda fmt: fmt.replace("{tag}", "1.0.0")
    return version


@pytest.fixture
def scmx_tool():
    # Setup a standard tool with main branch as 'dev'
    labels = [ReleaseLabel(label="dev", branches=["main", "master"]), ReleaseLabel(label="rc", branches=["release"])]
    scheme = BranchScheme(labels=labels)
    return ScmxTool(scheme="branch-scheme", branch_scheme=scheme)


def test_branch_scheme_exact_tag(mock_version, scmx_tool):
    mock_version.exact = True
    assert branch_scheme(mock_version, scmx_tool) == "1.0.0"


def test_branch_scheme_main_branch(mock_version, scmx_tool):
    mock_version.branch = "main"
    # guess_next_version will now receive version.tag,
    # and access version.tag.tag to get "1.0.0", bumping it to "1.0.1"
    assert branch_scheme(mock_version, scmx_tool) == "1.0.1.dev.5"


def test_branch_scheme_release_branch(mock_version, scmx_tool):
    mock_version.branch = "release"
    assert branch_scheme(mock_version, scmx_tool) == "1.0.1.rc.5"


def test_branch_scheme_detached_head(mock_version, scmx_tool):
    mock_version.branch = None
    assert branch_scheme(mock_version, scmx_tool) == "1.0.1.detached.5"
