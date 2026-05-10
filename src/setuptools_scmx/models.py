from typing import Literal

import attrs
from pyprojectr import BaseModel, PyProjectTool

LabelName = Literal["rc", "beta", "alpha", "dev", "post"]
ScmxScheme = Literal["branch-scheme"]


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
class ScmxTool(PyProjectTool):
    scheme: ScmxScheme
    branch_scheme: BranchScheme = attrs.field(factory=BranchScheme)
