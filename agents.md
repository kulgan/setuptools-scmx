# Versioning Scheme

This project utilizes `setuptools-scmx` with custom versioning schemes.

## Branch Scheme Logic

The `branch-scheme` operates as follows:

*   **Tags**: If the current commit is exactly on a tag, the version will be the exact tag (e.g., `1.2.3`).
*   **Branches**: For commits not directly on a tag, the version is derived from the next anticipated version, a branch-specific label, and the distance from the last tag. The format is `{next_version}.{label}.{distance}`.

    *   `{next_version}`: The version that `setuptools_scm` guesses will be the next release.
    *   `{label}`: A label determined by the branch name, as configured in `pyproject.toml`.
    *   `{distance}`: The number of commits since the last tag.

### Configured Labels

The `branch-scheme` is configured with specific labels for certain branches:

*   Branches `master` and `main` are assigned the label `rc` (release candidate).
    *   Example: If the last tag was `1.2.3` and you are on `main` branch with 5 commits since the tag, the version might be `1.2.4.rc.5`.
*   The `hotfix` branch is assigned the label `post`.
    *   Example: If the last tag was `1.2.3` and you are on `hotfix` branch with 2 commits since the tag, the version might be `1.2.4.post.2`.
*   Any other branch will use its sanitized branch name as the label.
    *   Example: If the last tag was `1.2.3` and you are on a `feature-x` branch with 10 commits since the tag, the version might be `1.2.4.feature-x.10`.

## CI Scheme Logic

The `ci-scheme` prioritizes environment variables for versioning, making it ideal for CI/CD pipelines. The version string is constructed from three optional environment variables: version, branch name, and build number.

The format is `{VERSION}.{BRANCH}.{BUILD_NUMBER}`.

*   `{VERSION}`: Read from the environment variable specified by `version_env`. This is the base version and is required for the `ci-scheme` to produce a version. If not found, it defaults to `0.0.0`.
*   `{BRANCH}`: Read from the environment variable specified by `branch_env`. If present, it's appended to the version. The branch name is sanitized (e.g., `/` and `_` are replaced with `-`).
*   `{BUILD_NUMBER}`: Read from the environment variable specified by `build_number_env`. If present, it's appended to the version.

### Configuration in `pyproject.toml`

To use the `ci-scheme`, set `scheme = "ci-scheme"` in your `pyproject.toml`. You can also customize the environment variable keys:

```toml
[tool.setuptools-scmx]
scheme = "ci-scheme"

[tool.setuptools-scmx.ci-scheme]
version_env = "MY_CI_VERSION"
branch_env = "MY_CI_BRANCH"
build_number_env = "MY_CI_BUILD_NUMBER"
```

If `ci-scheme` is selected but no `version_env` is provided, the version will default to `0.0.0`.

## General Configuration in `pyproject.toml`

Here's an example of how both schemes can be configured in `pyproject.toml`:

```toml
[tool.setuptools-scmx]
scheme = "branch-scheme" # or "ci-scheme"

# scmx branch scheme config
[tool.setuptools-scmx.branch-scheme]
labels = [
  { name = "rc", branches = [ "master", "main" ] },
  { name = "post", branches = [ "hotfix" ] },
]

# scmx ci scheme config
[tool.setuptools-scmx.ci-scheme]
version_env = "SCMX_VERSION"
branch_env = "SCMX_BRANCH"
build_number_env = "SCMX_BUILD_NUMBER"
```
