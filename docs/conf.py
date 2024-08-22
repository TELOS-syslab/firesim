# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import shutil
import os
import subprocess
import sys
import time

from sphinx.util import logging
logger = logging.getLogger(__name__)

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = u'FireSim'

this_year = time.strftime("%Y")

copyright = u'2018-' + this_year + ' Sagar Karandikar, David Biancolin, Abraham Gonzalez, Howard Mao, Donggyu Kim, Alon Amid, and Berkeley Architecture Research'
author = u'Sagar Karandikar, David Biancolin, Abraham Gonzalez, Howard Mao, Donggyu Kim, Alon Amid, and Berkeley Architecture Research'

on_rtd = os.environ.get("READTHEDOCS") == "True"
on_gha = os.environ.get("GITHUB_ACTIONS") == "true"

if on_rtd:
    for item, value in os.environ.items():
        print("[READTHEDOCS] {} = {}".format(item, value))

def get_git_tag():
    # get the latest git tag (which is what rtd normally builds under "stable")
    # this works since rtd builds things within the repo
    process = subprocess.Popen(["git", "describe", "--exact-match", "--tags"], stdout=subprocess.PIPE)
    tag = process.communicate()[0].decode("utf-8").strip()
    if process.returncode == 0:
        return tag
    else:
        return None

def get_git_branch_name():
    # When running locally, try to set version to a branch name that could be
    # used to reference files on GH that could be added or moved. This should match rtd_version when running
    # in a RTD build container
    process = subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE)
    branchname = process.communicate()[0].decode("utf-8").strip()
    if process.returncode == 0:
        return branchname
    else:
        return None

# Come up with a short version string for the build. This is doing a bunch of lifting:
#   - format doc text that self-references its version (see title page). This may be used in an ad-hoc
#     way to produce references to things like ScalaDoc, etc...
#   - procedurally generate github URL references using via `gh-file-ref`
#
# For FireSim, the RTD version can be multiple things:
#   1. 'stable' - This points to a branch called 'stable' in the repo. that was previously manually updated each release. This is outdated.
#   2. 'latest' - This points to the 'main' branch documentation. This is recommended.
#   3. '<another-branch-name>' - This points to a branch. Normally used for testing if a branches documentation builds.
if on_rtd:
    rtd_version = os.environ.get("READTHEDOCS_VERSION")
    if rtd_version == "latest":
        branchname = get_git_branch_name()
        assert branchname is not None
        version = branchname
    elif rtd_version == "stable":
        tag = get_git_tag()
        assert tag is not None
        version = tag
    else:
        version = rtd_version # should be name of a branch
elif on_gha:
    rtd_version = "latest"
    # GitHub actions does a build of the docs to ensure they are free of warnings.
    # Looking up a branch name or tag requires switching on the event type that triggered the workflow
    # so just use the SHA of the commit instead.
    version = os.environ.get("GITHUB_SHA")
else:
    rtd_version = "latest"
    # When running locally, try to set version to a branch name that could be
    # used to reference files on GH that could be added or moved. This should match rtd_version when running
    # in a RTD build container
    branchname = get_git_branch_name()
    assert branchname is not None
    version = branchname

logger.info(f"Setting |version| to {version}.")

# set chipyard docs version
cy_docs_version = "a800cd0df8b64db6a5a5fe31e8c7b44447e0f745"

# for now make these match
release = version

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_tabs.tabs',
    'sphinx_copybutton',
    'sphinx_substitution_extensions',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_parsers = {
}

source_suffix = ['.rst']
#source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = [u'_build', 'Thumbs.db', '.DS_Store', '**/*-Template.rst']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'collapse_navigation': False,
    'logo_only': True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

html_logo = '_static/firesim_logo_small.png'

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'FireSimdoc'

html_context = {
    "version": version
}

# add rst to beginning of each rst source file
# can put custom strings here that are generated from this file
# you can use these in .. code-block:: directives with :substitutions: added underneath
rst_prolog = f"""
.. |overall_version| replace:: {version}
.. |cy_docs_version| replace:: {cy_docs_version}
"""

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'FireSim.tex', u'FireSim Documentation',
     u'Sagar Karandikar, David Biancolin, \\\\ Abraham Gonzalez, Howard Mao, \\\\ Donggyu Kim, Alon Amid, \\\\ Berkeley Architecture Research', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'firesim', u'FireSim Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'FireSim', u'FireSim Documentation',
     author, 'FireSim', 'One line description of project.',
     'Miscellaneous'),
]

# -- handle re-directs for pages that move
# taken from https://tech.signavio.com/2017/managing-sphinx-redirects

redirect_files = [ ]

def copy_legacy_redirects(app, docname): # Sphinx expects two arguments
    if app.builder.name == 'html':
        for html_src_path in redirect_files:
            target_path = app.outdir + '/' + html_src_path
            src_path = app.srcdir + '/' + html_src_path

            if os.path.isfile(src_path):
                shutil.copyfile(src_path, target_path)

def gh_file_ref_role_impl(url, text_prefix, name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Produces a github.com reference to a blob or tree at path {text}.

    Example:

    :gh-file-ref:`my/path`

    Produces a hyperlink with the text "my/path" that refers to the url given.

    Where version is the same as would be substituted by using |version| in html text,
    and is resolved in conf.py.

    This is based off custom role sphinx plugins like
    https://github.com/tdi/sphinxcontrib-manpage. I've inlined this here for now, but we
    could just as well make it a module and register it under `extensions` in conf.py

    """

    import docutils
    import requests

    if text_prefix is not None:
        text = text_prefix + text

    logger.info(f"Testing GitHub URL {url} exists...")
    status_code = requests.get(url).status_code
    if status_code != 200:
        message = f"[Line {lineno}] :{name}:`{text}` produces URL {url} returning status code {status_code}. " \
                  "Ensure your path is correct and all commits that may have moved or renamed files have been pushed to github.com."
        logger.error(message)
        sys.exit(1)

    docutils.parsers.rst.roles.set_classes(options)
    node = docutils.nodes.reference(rawtext, text, refuri=url, **options)
    return [node], []

def fs_gh_file_ref_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    # Note GitHub permits referring to a tree as a 'blob' in these URLs without returning a 404.
    # So I've unconditionally chosen to use blob.
    url = f"https://www.github.com/firesim/firesim/blob/{version}/{text}"
    return gh_file_ref_role_impl(url, None, name, rawtext, text, lineno, inliner, options, content)

def cy_gh_file_ref_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    # Note GitHub permits referring to a tree as a 'blob' in these URLs without returning a 404.
    # So I've unconditionally chosen to use blob.
    url = f"https://www.github.com/ucb-bar/chipyard/blob/{cy_docs_version}/{text}"
    return gh_file_ref_role_impl(url, "${CY_DIR}/", name, rawtext, text, lineno, inliner, options, content)

def setup(app):
    # Add roles to simplify github reference generation
    app.add_role('gh-file-ref', fs_gh_file_ref_role)
    app.add_role('cy-gh-file-ref', cy_gh_file_ref_role)
    app.connect('build-finished', copy_legacy_redirects)
