from setuptools_scmx.models import (
    BranchScheme,
    EnvScheme,
    EnvSchemes,
    GithubEnvScheme,
    GitlabEnvScheme,
    JenkinsEnvScheme,
    ReleaseLabel,
    ScmxTool,
)


def test_release_label_match_exact():
    label = ReleaseLabel(name="rc", branches=["master"])
    assert label.match("master") == "rc"


def test_release_label_match_regex():
    label = ReleaseLabel(name="beta", branches=["feature/.*"])
    assert label.match("feature/new-feature") == "beta"


def test_release_label_no_match():
    label = ReleaseLabel(name="alpha", branches=["dev"])
    assert label.match("main") is None


def test_release_label_none_branch_name():
    label = ReleaseLabel(name="alpha", branches=["dev"])
    assert label.match(None) is None


def test_branch_scheme_get_release_label_match():
    rc_label = ReleaseLabel(name="rc", branches=["master"])
    beta_label = ReleaseLabel(name="beta", branches=["feature/.*"])
    scheme = BranchScheme(labels=[rc_label, beta_label])
    assert scheme.get_release_label("master") == ".rc"
    assert scheme.get_release_label("feature/new-feature") == ".beta"


def test_branch_scheme_get_release_label_no_match():
    rc_label = ReleaseLabel(name="rc", branches=["master"])
    scheme = BranchScheme(labels=[rc_label])
    assert scheme.get_release_label("dev") == "+dev"


def test_branch_scheme_get_release_label_none_branch_name():
    rc_label = ReleaseLabel(name="rc", branches=["master"])
    scheme = BranchScheme(labels=[rc_label])
    assert scheme.get_release_label(None) == "+detached"


def test_branch_scheme_get_release_label_branch_name_with_slash_and_underscore():
    scheme = BranchScheme(labels=[])
    assert scheme.get_release_label("feature/my_branch") == "+feature-my-branch"


def test_env_scheme_get_version(monkeypatch):
    monkeypatch.setenv("SCMX_VERSION_OVERRIDE", "1.2.3")
    scheme = EnvScheme()
    assert scheme.get_version() == "1.2.3"
    monkeypatch.delenv("SCMX_VERSION_OVERRIDE")
    assert scheme.get_version() is None


def test_env_scheme_get_branch_name(monkeypatch):
    monkeypatch.setenv("MY_BRANCH_VAR", "develop")
    scheme = EnvScheme(branch="MY_BRANCH_VAR")
    assert scheme.get_branch_name() == "develop"
    monkeypatch.delenv("MY_BRANCH_VAR")
    assert scheme.get_branch_name() is None


def test_env_scheme_get_build_number(monkeypatch):
    monkeypatch.setenv("MY_BUILD_VAR", "1234")
    scheme = EnvScheme(build_number="MY_BUILD_VAR")
    assert scheme.get_build_number() == "1234"
    monkeypatch.delenv("MY_BUILD_VAR")
    assert scheme.get_build_number() is None


def test_env_scheme_commit_hash(monkeypatch):
    monkeypatch.setenv("MY_COMMIT_VAR", "abcdef1234567890")
    scheme = EnvScheme(git_commit="MY_COMMIT_VAR")
    assert scheme.commit_hash() == "abcdef1234567890"
    monkeypatch.delenv("MY_COMMIT_VAR")
    assert scheme.commit_hash() is None


def test_env_scheme_short_commit_sha():
    scheme = EnvScheme(git_commit="abcdef1234567890")
    assert scheme.short_commit_sha == "abcdef1"
    scheme_no_commit = EnvScheme()
    assert scheme_no_commit.short_commit_sha == ""


def test_jenkins_env_scheme(monkeypatch):
    monkeypatch.setenv("BRANCH_NAME", "jenkins-feature")
    monkeypatch.setenv("GIT_COMMIT", "fedcba9876543210")
    monkeypatch.setenv("BUILD_NUMBER", "5678")
    scheme = JenkinsEnvScheme()
    assert scheme.get_branch_name() == "jenkins-feature"
    assert scheme.commit_hash() == "fedcba9876543210"
    assert scheme.get_build_number() == "5678"
    monkeypatch.delenv("BRANCH_NAME")
    monkeypatch.delenv("GIT_COMMIT")
    monkeypatch.delenv("BUILD_NUMBER")


def test_gitlab_env_scheme(monkeypatch):
    monkeypatch.setenv("CI_COMMIT_REF_SNAME", "gitlab-dev")
    monkeypatch.setenv("CI_COMMIT_SHA", "1234567890abcdef")
    monkeypatch.setenv("CI_JOB_ID", "9876")
    scheme = GitlabEnvScheme()
    assert scheme.get_branch_name() == "gitlab-dev"
    assert scheme.commit_hash() == "1234567890abcdef"
    assert scheme.get_build_number() == "9876"
    monkeypatch.delenv("CI_COMMIT_REF_SNAME")
    monkeypatch.delenv("CI_COMMIT_SHA")
    monkeypatch.delenv("CI_JOB_ID")


def test_github_env_scheme(monkeypatch):
    monkeypatch.setenv("GITHUB_REF_NAME", "github-main")
    monkeypatch.setenv("GITHUB_SHA", "fedcba9876543210")
    monkeypatch.setenv("GITHUB_RUN_ID", "112233")
    scheme = GithubEnvScheme()
    assert scheme.get_branch_name() == "github-main"
    assert scheme.commit_hash() == "fedcba9876543210"
    assert scheme.get_build_number() == "112233"
    monkeypatch.delenv("GITHUB_REF_NAME")
    monkeypatch.delenv("GITHUB_SHA")
    monkeypatch.delenv("GITHUB_RUN_ID")


def test_env_schemes_get():
    env_schemes = EnvSchemes()
    assert isinstance(env_schemes.get("github"), GithubEnvScheme)
    assert isinstance(env_schemes.get("jenkins"), JenkinsEnvScheme)
    assert isinstance(env_schemes.get("gitlab"), GitlabEnvScheme)
    assert isinstance(env_schemes.get("custom"), EnvScheme)


def test_scmx_tool_get_env_scheme():
    tool_github = ScmxTool(env_scheme="github")
    assert isinstance(tool_github.get_env_scheme(), GithubEnvScheme)

    tool_jenkins = ScmxTool(env_scheme="jenkins")
    assert isinstance(tool_jenkins.get_env_scheme(), JenkinsEnvScheme)

    tool_gitlab = ScmxTool(env_scheme="gitlab")
    assert isinstance(tool_gitlab.get_env_scheme(), GitlabEnvScheme)

    tool_custom = ScmxTool(env_scheme="custom")
    assert isinstance(tool_custom.get_env_scheme(), EnvScheme)
