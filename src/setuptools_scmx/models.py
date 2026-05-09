from typing import Literal

import attrs

from pyprojectr import BaseModel, PyProjectTool

Label = Literal["rc", "beta", "alpha", "dev", "post"]


@attrs.define(auto_attribs=True)
class ReleaseLabel:
    label: Label = attrs.field(default="rc")
    branches: list[str] = attrs.field(default=["master", "main"])

    def match(self, name: str) -> Label | None:
        if name in self.branches:
            return self.label
        return None


@attrs.define(frozen=True)
class BranchScheme(BaseModel):
    labels: list[ReleaseLabel] = attrs.field(factory=list)

    def get_release_label(self, branch_name: str) -> str:
        label = next(label for label in self.labels if label.match(branch_name))
        return label.label


@attrs.define(frozen=True)
class ScmxTool(PyProjectTool):
    scheme: str
    branch_scheme: BranchScheme = attrs.field(factory=BranchScheme)

