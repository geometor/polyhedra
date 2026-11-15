"""Sphinx configuration for GEOMETOR • polyhedra."""

from __future__ import annotations

from pathlib import Path
import sys

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_WORKSPACE_ROOT = _PROJECT_ROOT.parent

for _front_path in (
    _PROJECT_ROOT / "src",
    _WORKSPACE_ROOT / "model" / "src",
    _WORKSPACE_ROOT / "divine" / "src",
    _WORKSPACE_ROOT / "polyhedra" / "src",
):
    if _front_path.exists() and str(_front_path) not in sys.path:
        sys.path.insert(0, str(_front_path))

_VENV_SITE = _WORKSPACE_ROOT / ".venv" / "lib" / "python3.13" / "site-packages"
if _VENV_SITE.exists() and str(_VENV_SITE) not in sys.path:
    sys.path.append(str(_VENV_SITE))

from photon_platform.publish.global_conf import *  # noqa: E402, F403

import geometor.polyhedra as module  # noqa: E402

version = module.__version__

org = "geometor"
org_name = "GEOMETOR"

repo = "polyhedra"
repo_name = "polyhedra"

setup_globals(org, org_name, repo, repo_name)  # noqa: F405

project = "GEOMETOR • polyhedra"
author = "phi ARCHITECT • GEOMETOR"
copyright = "2026 · GEOMETOR"

# Local offline intersphinx resolution across sister GEOMETOR repositories
SISTER_REPOS: tuple[str, ...] = (
    "euclid",
    "elements",
    "pacioli",
    "kepler",
    "model",
    "explorer",
    "divine",
    "pappus",
)

for sister in SISTER_REPOS:
    inv = _WORKSPACE_ROOT / sister / "docs" / "objects.inv"
    if inv.is_file():
        intersphinx_mapping[sister] = (  # noqa: F405
            f"https://geometor.github.io/{sister}",
            (str(inv.resolve()), None),
        )

for key in list(intersphinx_mapping.keys()):  # noqa: F405
    _uri, inv_target = intersphinx_mapping[key]  # noqa: F405
    if inv_target is None:
        intersphinx_mapping.pop(key, None)  # noqa: F405

html_theme = "foundation"
html_static_path = ["_static"]
html_css_files = [*globals().get("html_css_files", []), "css/custom.css"]
html_js_files = [*globals().get("html_js_files", []), "js/polyhedra_3d_codex.js"]

autoapi_dirs = [str(_PROJECT_ROOT / "src" / "geometor")]
autoapi_add_toctree_entry = False
napoleon_use_ivar = True

for _excl in ("modules/api/geometor/polyhedra/index.rst",):
    if _excl not in exclude_patterns:  # noqa: F405
        exclude_patterns.append(_excl)  # noqa: F405

suppress_warnings = ["autoapi.python_import_resolution", "toc.not_included"]

mathjax3_config = {
    "tex": {
        "inlineMath": [["\\(", "\\)"], ["$", "$"]],
        "displayMath": [["\\[", "\\]"], ["$$", "$$"]],
    }
}
