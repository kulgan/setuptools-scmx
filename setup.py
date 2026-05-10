import os
import sys
import setuptools

here = os.path.dirname(os.path.abspath(__file__))


def scm_config():
    src = os.path.join(here, "src")

    # Force the src directory into sys.path
    if src not in sys.path:
        sys.path.insert(0, src)

    # Now attempt to import the versioning scheme.
    from setuptools_scmx.schemes import version_scheme

    return {
        "use_scm_version": {
            "version_scheme": version_scheme,
        }
    }


if __name__ == "__main__":
    setuptools.setup(**scm_config())
