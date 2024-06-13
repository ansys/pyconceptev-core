"""Sphinx documentation configuration file."""

from datetime import datetime
import os
import pathlib
import shutil

from ansys_sphinx_theme import get_version_match
from ansys_sphinx_theme import pyansys_logo_black as logo
import sphinx
from sphinx.util import logging

from ansys.conceptev.core import __version__

logger = logging.getLogger(__name__)
path = pathlib.Path(__file__).parent.parent.parent / "examples"
EXAMPLES_DIRECTORY = path.resolve()

# Project information
project = "ansys-conceptev-core"
copyright = f"(c) 2023-{datetime.today().year} ANSYS, Inc. and/or its affiliates."
author = "ANSYS, Inc."
release = version = __version__
cname = os.getenv("DOCUMENTATION_CNAME", "conceptev.docs.pyansys.com")
switcher_version = get_version_match(__version__)

# Select desired logo, theme, and declare the html title
html_logo = logo
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "pyconceptev"
html_context = {
    "github_user": "ansys",
    "github_repo": "pyconceptev",
    "github_version": "main",
    "doc_path": "doc/source",
}

# specify the location of your github repo
html_theme_options = {
    "github_url": "https://github.com/ansys/pyconceptev",
    "use_edit_page_button": True,
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": switcher_version,
    },
    "check_switcher": False,
}

# Sphinx extensions
extensions = [
    "nbsphinx",
    "numpydoc",
    "recommonmark",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.imgconverter",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}

# Static path
html_static_path = ["_static"]
html_css_files = [
    "custom.css",
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "*.txt",
    "conf.py",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# The master toctree document.
master_doc = "index"

# Examples gallery customization
nbsphinx_execute = "always"
nbsphinx_allow_errors = False
nbsphinx_thumbnails = {
    "examples/simple_workflow": "_static/thumbnails/simple_workflow.png",
}
nbsphinx_custom_formats = {
    ".py": ["jupytext.reads", {"fmt": ""}],
}

# Activate fontawesome icons in LaTeX
sd_fontawesome_latex = True

linkcheck_exclude_documents = ["index"]
linkcheck_ignore = [
    r"https://download.ansys.com/",
    r".*/examples/.*.py",
    r"_static/assets/.*",
]


# If we are on a release, we have to ignore the "release" URLs, since it is not
# available until the release is published.
if switcher_version != "dev":
    linkcheck_ignore.append(f"https://github.com/ansys/pyconceptev/releases/tag/v{__version__}")

# Sphinx event hooks


def directory_size(directory_path):
    """Compute the size (in mega bytes) of a directory."""
    res = 0
    for path, _, files in os.walk(directory_path):
        for f in files:
            fp = os.path.join(path, f)
            res += os.stat(fp).st_size
    # Convert in mega bytes
    res /= 1e6
    return res


def check_pandoc_installed(app):
    """Ensure that pandoc is installed."""
    import pypandoc

    try:
        pandoc_path = pypandoc.get_pandoc_path()
        pandoc_dir = os.path.dirname(pandoc_path)
        if pandoc_dir not in os.environ["PATH"].split(os.pathsep):
            logger.info("Pandoc directory is not in $PATH.")
            os.environ["PATH"] += os.pathsep + pandoc_dir
            logger.info(f"Pandoc directory '{pandoc_dir}' has been added to $PATH")
    except OSError:
        logger.error("Pandoc was not found, please add it to your path or install pypandoc-binary")


def copy_examples(app):
    """Copy directory examples (root directory) files into the doc/source/examples directory."""
    destination_dir = pathlib.Path(app.srcdir, "examples").resolve()
    logger.info(f"Copying examples from {EXAMPLES_DIRECTORY} to {destination_dir}.")

    if os.path.exists(destination_dir):
        size = directory_size(destination_dir)
        logger.info(f"Directory {destination_dir} ({size} MB) already exist, removing it.")
        shutil.rmtree(destination_dir)
        logger.info(f"Directory removed.")

    shutil.copytree(EXAMPLES_DIRECTORY, destination_dir)
    logger.info(f"Copy performed")


def remove_examples(app, exception):
    """Remove the doc/source/examples directory created during the documentation build."""
    destination_dir = pathlib.Path(app.srcdir) / "examples"

    size = directory_size(destination_dir)
    logger.info(f"Removing directory {destination_dir} ({size} MB).")
    shutil.rmtree(destination_dir, ignore_errors=True)
    logger.info(f"Directory removed.")


def setup(app: sphinx.application.Sphinx):
    """Run different hook functions during the documentation build.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Sphinx instance containing all the configuration for the documentation build.
    """
    app.connect("builder-inited", copy_examples)
    app.connect("builder-inited", check_pandoc_installed)
    app.connect("build-finished", remove_examples)
