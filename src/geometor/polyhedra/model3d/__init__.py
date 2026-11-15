"""Exact 3D symbolic geometry, polyhedral models, and 2D bridge.

Exports primitives for 3D points, vectors, planes, lines, spheres, and polyhedra,
along with slicing and net-unfolding utilities into 2D GEOMETOR models.
"""

from __future__ import annotations

from geometor.polyhedra.model3d.bridge import slice_solid_to_model, unfold_net_2d
from geometor.polyhedra.model3d.primitives import (
    Line3D,
    Plane3D,
    Point3D,
    Solid3D,
    Sphere3D,
    Vector3D,
)

__all__ = [
    "Line3D",
    "Plane3D",
    "Point3D",
    "Solid3D",
    "Sphere3D",
    "Vector3D",
    "slice_solid_to_model",
    "unfold_net_2d",
]
