"""GEOMETOR Polyhedra.

Exact symbolic Platonic, Archimedean, and Keplerian polyhedral geometry in
SymPy, Rational Trigonometry, and the GEOMETOR Digital Scriptorium.
"""

from __future__ import annotations

from geometor.polyhedra.golden import (
    GoldenPolyhedronTheorem,
    build_dodecahedron_five_cubes,
    build_icosahedron_golden_rectangles,
    build_icosahedron_meridian_model,
    build_octahedron_golden_icosahedron,
    build_odom_tetrahedron_section_model,
    build_pentagon_cross_section_model,
    build_rhombic_triacontahedron_golden,
    get_golden_theorem,
    get_golden_theorems,
)
from geometor.polyhedra.model3d import (
    Line3D,
    Plane3D,
    Point3D,
    Solid3D,
    Sphere3D,
    Vector3D,
    slice_solid_to_model,
    unfold_net_2d,
)
from geometor.polyhedra.operators import (
    elevate,
    polar_dual,
    rectify,
    truncate,
    vacuate,
)
from geometor.polyhedra.platonic import (
    PHI,
    PHI_INV,
    RegularSolid,
    cross_3d,
    dihedral_spread_3d,
    dot_3d,
    face_normal_3d,
    get_platonic_solid,
    get_platonic_solids,
    quadrance_3d,
)
from geometor.polyhedra.render import (
    export_blender_script,
    export_ingetrazo_script,
    export_obj_mtl,
    render_model2d_svg,
    render_net_svg,
    render_solid_svg,
)

__version__: str = "0.2.1"

__all__: list[str] = [
    "GoldenPolyhedronTheorem",
    "Line3D",
    "PHI",
    "PHI_INV",
    "Plane3D",
    "Point3D",
    "RegularSolid",
    "Solid3D",
    "Sphere3D",
    "Vector3D",
    "__version__",
    "build_dodecahedron_five_cubes",
    "build_icosahedron_golden_rectangles",
    "build_icosahedron_meridian_model",
    "build_octahedron_golden_icosahedron",
    "build_odom_tetrahedron_section_model",
    "build_pentagon_cross_section_model",
    "build_rhombic_triacontahedron_golden",
    "cross_3d",
    "dihedral_spread_3d",
    "dot_3d",
    "elevate",
    "export_blender_script",
    "export_ingetrazo_script",
    "export_obj_mtl",
    "face_normal_3d",
    "get_golden_theorem",
    "get_golden_theorems",
    "get_platonic_solid",
    "get_platonic_solids",
    "polar_dual",
    "quadrance_3d",
    "rectify",
    "render_model2d_svg",
    "render_net_svg",
    "render_solid_svg",
    "slice_solid_to_model",
    "truncate",
    "unfold_net_2d",
    "vacuate",
]
