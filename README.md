# setuptools-scmx

## Project Description

`setuptools-scmx` is a Python package designed to extend `setuptools-scm` with CI-friendly versioning schemes. It provides flexible, configuration-driven version management tailored for continuous integration and delivery workflows, allowing developers to define custom versioning logic based on Git branch names and tags directly within `pyproject.toml`.

## What it Does

This package enhances the standard `setuptools-scm` functionality by introducing:

-   **Custom Versioning Schemes**: Define how your project's version is determined based on its Git state.
-   **Branch-Aware Versioning**: Differentiate version numbers based on the current Git branch (e.g., `main`, `develop`, `feature/xyz`).
-   **Exact Tag Versions**: Ensures that builds from Git tags always result in the exact tag version, without any additional suffixes.
-   **Environment Variable Overrides**: Allows specifying a version directly via an environment variable, useful for specific CI/CD scenarios.
-   **`pyproject.toml` Integration**: All custom versioning logic and configurations are managed declaratively in your `pyproject.toml` file, leveraging `pyprojectr` for robust parsing.

This allows for consistent and predictable versioning across different development stages and CI environments, making it easier to track builds and releases.

## How to Use it as a Developer

To integrate `setuptools-scmx` into your project, follow these steps:

### 1. Installation

First, ensure `setuptools-scmx` and its dependencies are installed. You typically add it to your `build-system.requires` in `pyproject.toml`.

```toml
# pyproject.toml
[build-system]
requires = [
    "setuptools>=80",
    "setuptools-scm[toml]", # Ensure setuptools-scm[toml] is included
    "setuptools-scmx",     # Add setuptools-scmx here
]
build-backend = "setuptools.build_meta"

[project]
name = "your-project-name"
dynamic = ["version"]
# ... other project metadata
```

### 2. Configure `setuptools-scm`

In your `pyproject.toml`, configure `setuptools-scm` to use a custom `version_scheme` and `local_scheme`. You will point `version_scheme` to the entry point provided by `setuptools-scmx`.

```toml
# pyproject.toml
[tool.setuptools_scm]
version_scheme = "setuptools_scmx:version_scheme" # Use the custom scheme
local_scheme = "no-local-version" # Or 'node-and-date' as per your preference
```

### 3. Configure `setuptools-scmx`

Define your custom branch-aware versioning rules and other schemes under `[tool.setuptools-scmx]`.

```toml
# pyproject.toml
[tool.setuptools-scmx]
scheme = "branch-scheme" # This tells setuptools-scmx to use the branch-aware logic

[tool.setuptools-scmx.branch-scheme]
labels = [
  # Branches 'main' and 'master' will get a '.rc' label
  { name = "rc", branches = ["main", "master"] },
  # The 'develop' branch will get a '.dev' label
  { name = "dev", branches = ["develop"] },
  # Branches starting with 'feature/' will get an '.alpha' label
  { name = "alpha", branches = ["feature/.*"] }, # Example: feature/new-feature -> 1.2.3.alpha.4
  # The 'hotfix' branch will get a '.post' label
  { name = "post", branches = ["hotfix"] },
]

# You can also define environment variable based schemes
[tool.setuptools-scmx.env-schemes]
# If the environment variable SCMX_VERSION_OVERRIDE is set, its value will be used as the version.
custom = { version = "SCMX_VERSION_OVERRIDE" }
```

#### Explanation of `[tool.setuptools-scmx.branch-scheme.labels]`

Each entry in the `labels` list defines a rule:
-   `name`: The string to append to the version number (e.g., `rc`, `dev`, `alpha`, `post`). This should generally conform to [PEP 440](https://peps.python.org/pep-0440/) pre-release identifiers.
-   `branches`: A list of branch name regexes or exact branch names to match. If the current Git branch matches any of these, the corresponding `label` will be used.

*Note: The `setuptools-scmx` project's own `pyproject.toml` uses a simpler `labels` configuration for demonstration purposes.*

#### Explanation of `[tool.setuptools-scmx.env-schemes]`

This section allows you to define version schemes that are activated by the presence and value of environment variables.
-   `custom`: This is a user-defined name for the scheme.
-   `version = "ENV_VAR_NAME"`: If the environment variable `ENV_VAR_NAME` is set, its value will be used as the project's version, overriding any Git-based versioning. This is particularly useful in CI/CD pipelines where you might want to force a specific build version.

#### Versioning Behavior Examples:

Assuming the last tag is `1.0.0` and there are 5 commits since the tag (`distance=5`):

-   **On a Tag (`git checkout 1.0.0`)**:
    -   Version: `1.0.0` (exact)

-   **On `main` branch**:
    -   Version: `1.0.1.rc.5` (next version `1.0.1`, label `rc`, distance `5`)

-   **On `develop` branch**:
    -   Version: `1.0.1.dev.5` (next version `1.0.1`, label `dev`, distance `5`)

-   **On `feature/my-new-feature` branch**:
    -   Version: `1.0.1.alpha.5` (next version `1.0.1`, label `alpha`, distance `5`)

-   **On `hotfix` branch**:
    -   Version: `1.0.1.post.5` (next version `1.0.1`, label `post`, distance `5`)

-   **On an unmapped branch (e.g., `bugfix/issue-123`)**:
    -   Version: `1.0.1.bugfix-issue-123.5` (next version `1.0.1`, normalized branch name as label, distance `5`)

-   **With `SCMX_VERSION_OVERRIDE="2.0.0-beta.1"` environment variable set**:
    -   Version: `2.0.0-beta.1` (overrides Git-based versioning)

This setup provides a powerful and flexible way to manage your project's versioning in a CI/CD environment.
