# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
from pathlib import Path
import re
import subprocess
import sys

DOC_SOURCE = Path(__file__).parent
DOC_ROOT = DOC_SOURCE.parent.absolute()
REPO_ROOT = DOC_ROOT.parent.absolute()
PACKAGE_DIR = (REPO_ROOT / 'shufflish').absolute()
sys.path.insert(0, str(REPO_ROOT.absolute()))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "shufflish"
copyright = "2024, Joachim Folz"
author = "Joachim Folz"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []

myst_ref_domains = ["py", "python"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_title = project
html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "light_logo": "img/shrug.svg",
    "dark_logo": "img/shrug.svg",
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#005fc8",
        "color-brand-content": "#005fc8",
        "color-api-pre-name": "#008151",
        "color-api-name": "#008151",
        "color-highlight-on-target": "rgba(101, 31, 255, 0.2)",
        "color-background-hover--transparent": "#80808010",
    },
    "dark_css_variables": {
        "color-brand-primary": "#00b9ec",
        "color-brand-content": "#00b9ec",
        "color-api-pre-name": "#00bfa5",
        "color-api-name": "#00bfa5",
        "color-highlight-on-target": "rgba(101, 31, 255, 0.2)",
        "color-background-hover--transparent": "#80808010",
    },
    "source_repository": "https://github.com/jfolz/shufflish",
    "source_branch": "main",
    "source_directory": "doc/source/",
}
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "links.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
        "sidebar/variant-selector.html",
    ]
}
html_css_files = [
    "css/custom.css",
]

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("http://docs.scipy.org/doc/numpy", None),
}

autoclass_content = "both"


def shorten_long_defaults(app, what, name, obj, options, signature, return_annotation, *args, **kwargs):
    signature = re.sub(r"\((?:\d+, |\d+)+\)", "shufflish.PRIMES", signature)
    print(signature)
    return signature, return_annotation


def change_readme_links(path_from: Path, path_to: Path):
    with path_from.open() as f:
        content = f.read()
    content, _ = re.subn(r"\[`(.+)`\]\(https://shufflish.readthedocs.io.+#\1\)", r"[](\1)", content)
    content, _ = re.subn(r"\[(.+)\]\(https://shufflish.readthedocs.io.+#(.+)\)", r"[\1](\2)", content)
    with path_to.open("wt", encoding="utf-8") as f:
        f.write(content)


def setup(app):
    app.connect('autodoc-process-signature', shorten_long_defaults)
    change_readme_links(
        REPO_ROOT / "README.md",
        DOC_SOURCE / "README.md",
    )
