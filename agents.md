# Project: setuptools-scmx

## Overview
`setuptools-scmx` is a utility designed to provide CI-friendly hooks for `setuptools-scm`. It simplifies version management in CI/CD environments by providing custom versioning schemes and configuration through `pyproject.toml`.

## Current State

### Core Modules
- **`models.py`**: Implements a `BaseModel` using `attrs` and `cattrs`. It includes a custom structure hook to automatically convert between Python-style underscores (`_`) and TOML-style hyphens (`-`) for attribute names.
- **`pyproject.py`**: Defines data models for parsing `pyproject.toml` files, including `Author`, `BuildSystem`, and a specialized `PyProjectScmxTool` configuration. It uses `tomli` for loading.
- **`schemes.py`**: Contains the logic for custom versioning schemes. Currently includes a placeholder for `jenkins_build_scheme`.

### Infrastructure
- Build system: `setuptools` with `setuptools-scm`.
- Dependency management: `uv`.
- Linting/Formatting: `ruff`.
- Testing framework: `pytest`.

## Roadmap / Testing Plan

### 1. Test `models.py`
- Validate `_underscores_to_hyphen` utility.
- Verify `cattrs` structure hooks correctly map hyphenated TOML keys to underscored attribute names.

### 2. Test `pyproject.py`
- Unit tests for all data models (`Author`, `BuildSystem`, `PyProjectScmxTool`).
- Integration tests for `PyProjectFile.from_file` using sample TOML data.
- Ensure `get_tool_options` correctly retrieves the `setuptools_scmx` section.

### 3. Test `schemes.py`
- Mock `setuptools_scm.version.ScmVersion` to test `jenkins_build_scheme`.
- Cover scenarios: main vs. feature branches, clean vs. dirty repositories, and tagged vs. untagged commits.

### 4. General Integration
- End-to-end loading of a full `pyproject.toml` file structure.
- Verification of CI-specific versioning logic in a simulated environment.
