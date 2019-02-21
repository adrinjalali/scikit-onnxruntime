# Licensed under the MIT License.

# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.

import os
import sys
import shutil
import sphinx_gallery.gen_gallery
import skl2onnx
import onnxruntime
import sphinx_skl2onnx_extension
import sphinx_modern_theme_modified


# -- Project information -----------------------------------------------------

project = 'scikit-onnxruntime'
copyright = '2019, Microsoft'
author = 'Microsoft'
version = skonnxrt.__version__
release = version

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.imgmath',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    "sphinx.ext.autodoc",
    'sphinx.ext.githubpages',
    "sphinx_gallery.gen_gallery",
    'sphinx.ext.autodoc',
    "sphinxcontrib.blockdiag",
]

templates_path = ['_templates']
source_suffix = ['.rst']

master_doc = 'index'
language = "en"
exclude_patterns = []
pygments_style = 'default'

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_mo"
html_static_path = ['_static']
html_theme = "sphinx_modern_theme_modified"
html_theme_path = [sphinx_modern_theme_modified.get_html_theme_path()]
html_logo = "logo_main.png"

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# -- Options for Sphinx Gallery ----------------------------------------------

sphinx_gallery_conf = {
     'examples_dirs': 'examples',
     'gallery_dirs': 'auto_examples',
}

# -- Setup actions -----------------------------------------------------------

def setup(app):
    # Placeholder to initialize the folder before
    # generating the documentation.
    return app

