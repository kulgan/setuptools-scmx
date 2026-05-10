import os
from typing import Literal

import attrs
from pyprojectr import BaseModel, PyProjectTool

LabelName = Literal["rc", "beta", "alpha", "dev", "post"]
ScmxScheme = Literal["branch-scheme", "ci-scheme"]
ScmxEnvScheme = Literal["jenkins", "gitlab", "github", "custom"]


@attrs.define(auto_attribs=True)
class ReleaseLabel:
    name: LabelName = attrs.field(default="rc")
    branches: list[str] = attrs.field(default=["master", "main"])

    def match(self, name: str | None) -> LabelName | None:
        if name not in self.branches:
            return None
        return self.name


@attrs.define(frozen=True)
class BranchScheme(BaseModel):
    labels: list[ReleaseLabel] = attrs.field(factory=list)

    def get_release_label(self, branch_name: str | None) -> LabelName | str:
        label = next((label for label in self.labels if label.match(branch_name)), None)
        if label:
            return label.name
        return branch_name.replace("/", "-").replace("_", "-") if branch_name else "detached"


@attrs.define(frozen=True)
class CiScheme(BaseModel):
    version_env: str = attrs.field(default="SCMX_VERSION")
    branch_env: str = attrs.field(default="SCMX_BRANCH")
    build_number_env: str = attrs.field(default="SCMX_BUILD_NUMBER")


@attrs.define(frozen=True)
class EnvScheme:
    version: str | None = None
    branch: str | None = None
    git_commit: str | None = None
    build_number: str | None = None

    @property
    def short_commit_sha(self) -> str:
        if self.git_commit:
            return self.git_commit[:7]
        return ""

    @classmethod
    def __get_env__(cls, key: str | None) -> str | None:
        if key:
            return os.getenv(key)
        return None

    def get_version(self) -> str | None:
        return self.__get_env__(self.version)

    def get_branch_name(self) -> str | None:
        return self.__get_env__(self.branch)

    def get_build_number(self) -> str | None:
        return self.__get_env__(self.build_number)

    def commit_hash(self) -> str | None:
        return self.__get_env__(self.git_commit)


@attrs.define(frozen=True)
class JenkinsEnvScheme(EnvScheme):
    version: str | None = None
    branch: str = "BRANCH_NAME"
    git_commit: str = "GIT_COMMIT"
    build_number: str = "BUILD_NUMBER"


@attrs.define(frozen=True)
class GitlabEnvScheme(EnvScheme):
    version: str | None = None
    branch: str = "CI_COMMIT_REF_SNAME"
    git_commit: str = "CI_COMMIT_SHA"
    build_number: str = "CI_JOB_ID"


@attrs.define(frozen=True)
class GithubEnvScheme(EnvScheme):
    version: str | None = None
    branch: str = "GITHUB_REF_NAME"
    git_commit: str = "GITHUB_SHA"
    build_number: str = "GITHUB_RUN_ID"


@attrs.define(frozen=True)
class EnvSchemes:
    github: GithubEnvScheme = attrs.field(factory=GithubEnvScheme)
    jenkins: JenkinsEnvScheme = attrs.field(factory=JenkinsEnvScheme)
    gitlab: GitlabEnvScheme = attrs.field(factory=GitlabEnvScheme)
    custom: EnvScheme = attrs.field(factory=EnvScheme)

    def get(self, name: ScmxEnvScheme) -> EnvScheme:
        if name == "github":
            return self.github
        if name == "jenkins":
            return self.jenkins
        if name == "gitlab":
            return self.gitlab
        return self.custom


@attrs.define(frozen=True)
class ScmxTool(PyProjectTool):
    scheme: ScmxScheme = attrs.field(default="branch-scheme")
    env_scheme: ScmxEnvScheme = attrs.field(default="custom")
    branch_scheme: BranchScheme = attrs.field(factory=BranchScheme)
    env_schemes: EnvSchemes = attrs.field(factory=EnvSchemes)

    def get_env_scheme(self) -> EnvScheme:
        return self.env_schemes.get(self.env_scheme)
