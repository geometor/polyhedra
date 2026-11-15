"""Polyhedral 3D rendering, SVG visualization, and CAD export pipelines."""

from __future__ import annotations

from geometor.polyhedra.render.exporters import (
    export_blender_script,
    export_ingetrazo_script,
    export_obj_mtl,
)
from geometor.polyhedra.render.svg3d import (
    render_model2d_svg,
    render_net_svg,
    render_solid_svg,
)

__all__ = [
    "export_blender_script",
    "export_ingetrazo_script",
    "export_obj_mtl",
    "render_model2d_svg",
    "render_net_svg",
    "render_solid_svg",
]
