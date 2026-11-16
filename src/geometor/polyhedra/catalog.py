"""Exact symbolic catalog and registry of the 26 canonical polyhedra.

Provides canonical specifications, historical metadata, exact Rational Trigonometry
invariants, and 3D manifold builders across five thematic families:

- ``01-platonic``: The Five Regular Convex Polyhedra of Plato and Euclid.
- ``02-archimedean``: Semi-Regular Truncations and Rectifications.
- ``03-catalan``: Face-Transitive Polar Duals of Archimedean Solids.
- ``04-elevated``: Pacioli & Leonardo da Vinci's Equilateral Stellations (*Corpora Elevata*).
- ``05-pyramids``: Great Pyramid Profiles, Kepler Harmonics, and Johnson Caps.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from geometor.polyhedra.model3d.primitives import (
    Point3D,
    Solid3D,
    _validate_exact,
)
from geometor.polyhedra.operators import (
    _order_polygon_around_axis,
    elevate,
    polar_dual,
    rectify,
    truncate,
)
from geometor.polyhedra.platonic import (
    PHI,
    get_platonic_solid,
)
from geometor.polyhedra.pyramid import (
    build_kepler_bipyramid_solid,
    build_kepler_pyramid_solid,
    build_seked_pyramid_solid,
)


@dataclass(frozen=True)
class PolyhedronFamily:
    """Specification of a thematic polyhedral family in the catalog.

    Attributes:
        slug: Unique identifier ('01-platonic', '02-archimedean', etc.).
        order: Order index in catalog (1..5).
        title: Descriptive title of the family.
        subtitle: Scholarly subtitle.
        summary: Mathematical and historical summary.
    """

    slug: str
    order: int
    title: str
    subtitle: str
    summary: str


@dataclass(frozen=True)
class PolyhedronEntry:
    """Exact symbolic catalog entry for a polyhedral manifold.

    Attributes:
        slug: Short lowercase identifier.
        canonical_id: Canonical catalog code ('P-01.01' .. 'P-05.04').
        family: Family slug.
        order: Order index within family.
        title: Standard English title.
        latin_name: Classical Latin designation.
        subtitle: Descriptive subtitle.
        enunciation: Crisp geometric definition.
        number_field: Algebraic number field in LaTeX.
        symmetry_group: Full symmetry point group and order.
        is_convex: Whether the solid is convex.
        dual_slug: Polar dual slug or descriptive name.
        historical_source: Primary literature citation.
        leonardo_plates: Tuples of (tabula_roman, folio_id, latin_caption).
        tags: Categorical search and indexing tags.
        vertices_count: Number of vertices (V).
        edges_count: Number of edges (E).
        faces_count: Number of faces (F).
        face_summary: Description of constituent polygon faces.
        edge_quadrances: Sorted unique exact edge quadrances.
        vertex_quadrances: Sorted unique exact vertex quadrances from origin.
        primary_dihedral_spread: Exact dihedral spread between adjacent faces.
        vacuum_genus: Topological genus of the hollow vacuate manifold (F - 1).
    """

    slug: str
    canonical_id: str
    family: str
    order: int
    title: str
    latin_name: str
    subtitle: str
    enunciation: str
    number_field: str
    symmetry_group: str
    is_convex: bool
    dual_slug: str | None
    historical_source: str
    leonardo_plates: tuple[tuple[str, str, str], ...]
    tags: tuple[str, ...]
    vertices_count: int
    edges_count: int
    faces_count: int
    face_summary: str
    edge_quadrances: tuple[sp.Expr, ...]
    vertex_quadrances: tuple[sp.Expr, ...]
    primary_dihedral_spread: sp.Expr | None
    vacuum_genus: int

    def __post_init__(self) -> None:
        """Validates exact algebraic parameters."""
        _validate_exact(*self.edge_quadrances)
        _validate_exact(*self.vertex_quadrances)
        if self.primary_dihedral_spread is not None:
            _validate_exact(self.primary_dihedral_spread)


def build_rhombicuboctahedron_solid() -> Solid3D:
    """Constructs Leonardo's 26-Base Body (Vigintisex Basium, Rhombicuboctahedron).

    Generates the exact Archimedean rhombicuboctahedron over Q(sqrt(2)) with 24 vertices,
    48 edges of uniform quadrance 4, and 26 faces (6 axial squares, 12 chamfer squares,
    and 8 octant equilateral triangles).

    Returns:
        Exact symbolic Solid3D instance centered at the origin.
    """
    c = sp.Integer(1) + sp.sqrt(2)
    verts: list[Point3D] = []
    vert_map: dict[tuple[sp.Expr, sp.Expr, sp.Expr], int] = {}
    for sx in (sp.Integer(1), sp.Integer(-1)):
        for sy in (sp.Integer(1), sp.Integer(-1)):
            for sz in (sp.Integer(1), sp.Integer(-1)):
                for perm in [
                    (sx * c, sy, sz),
                    (sx, sy * c, sz),
                    (sx, sy, sz * c),
                ]:
                    tup = (sp.expand(perm[0]), sp.expand(perm[1]), sp.expand(perm[2]))
                    if tup not in vert_map:
                        vert_map[tup] = len(verts)
                        verts.append(Point3D(perm[0], perm[1], perm[2]))

    faces: list[tuple[int, ...]] = []
    face_roles: list[str] = []

    def add_face(indices: list[int], role: str) -> None:
        face_pts = [verts[i] for i in indices]
        k = sp.Integer(len(indices))
        cx = sp.simplify(sum(verts[i].x for i in indices) / k)
        cy = sp.simplify(sum(verts[i].y for i in indices) / k)
        cz = sp.simplify(sum(verts[i].z for i in indices) / k)
        c_pt = Point3D(cx, cy, cz)
        ordered_local = _order_polygon_around_axis(face_pts, c_pt)
        faces.append(tuple(indices[i] for i in ordered_local))
        face_roles.append(role)

    # 6 axial squares
    for s in (sp.Integer(1), sp.Integer(-1)):
        add_face(
            [i for i, v in enumerate(verts) if sp.expand(v.x - s * c) == 0],
            "base",
        )
        add_face(
            [i for i, v in enumerate(verts) if sp.expand(v.y - s * c) == 0],
            "base",
        )
        add_face(
            [i for i, v in enumerate(verts) if sp.expand(v.z - s * c) == 0],
            "base",
        )

    # 12 diagonal chamfer squares
    val_chamf = sp.Integer(2) + sp.sqrt(2)
    for s1 in (sp.Integer(1), sp.Integer(-1)):
        for s2 in (sp.Integer(1), sp.Integer(-1)):
            add_face(
                [
                    i
                    for i, v in enumerate(verts)
                    if sp.expand(s1 * v.x + s2 * v.y - val_chamf) == 0
                ],
                "truncation",
            )
            add_face(
                [
                    i
                    for i, v in enumerate(verts)
                    if sp.expand(s1 * v.y + s2 * v.z - val_chamf) == 0
                ],
                "truncation",
            )
            add_face(
                [
                    i
                    for i, v in enumerate(verts)
                    if sp.expand(s1 * v.z + s2 * v.x - val_chamf) == 0
                ],
                "truncation",
            )

    # 8 octant equilateral triangles
    val_tri = sp.Integer(3) + sp.sqrt(2)
    for sx in (sp.Integer(1), sp.Integer(-1)):
        for sy in (sp.Integer(1), sp.Integer(-1)):
            for sz in (sp.Integer(1), sp.Integer(-1)):
                add_face(
                    [
                        i
                        for i, v in enumerate(verts)
                        if sp.expand(sx * v.x + sy * v.y + sz * v.z - val_tri) == 0
                    ],
                    "truncation",
                )

    return Solid3D(
        slug="rhombicuboctahedron",
        title="Rhombicuboctahedron",
        vertices=tuple(verts),
        faces=tuple(faces),
        face_roles=tuple(face_roles),
    )


def build_pentagonal_pyramid_solid(*, center_origin: bool = True) -> Solid3D:
    """Constructs the exact equilateral Regular Pentagonal Pyramid (Johnson Solid J2).

    Constructed directly from the 6-vertex icosahedral cap of Euclid Elements XIII.16
    and Leonardo da Vinci's Tabulae LI–LII over Q(phi).

    Args:
        center_origin: If True (default), translates vertices by -C so the centroid
            is at (0, 0, 0), placing the origin strictly inside the solid for
            manifold orientation and vacuation. If False, retains raw icosahedral
            coordinates.

    Returns:
        Exact symbolic Solid3D instance.
    """
    v_apex = Point3D(sp.Integer(0), sp.Integer(1), PHI)
    base_pts = [
        Point3D(sp.Integer(0), sp.Integer(-1), PHI),
        Point3D(PHI, sp.Integer(0), sp.Integer(1)),
        Point3D(sp.Integer(1), PHI, sp.Integer(0)),
        Point3D(sp.Integer(-1), PHI, sp.Integer(0)),
        Point3D(-PHI, sp.Integer(0), sp.Integer(1)),
    ]
    raw_verts = [v_apex] + base_pts
    if center_origin:
        cx = sp.simplify(sum(p.x for p in raw_verts) / sp.Integer(6))
        cy = sp.simplify(sum(p.y for p in raw_verts) / sp.Integer(6))
        cz = sp.simplify(sum(p.z for p in raw_verts) / sp.Integer(6))
        verts = [Point3D(p.x - cx, p.y - cy, p.z - cz) for p in raw_verts]
    else:
        verts = raw_verts

    base_face = (1, 5, 4, 3, 2)
    faces = [base_face] + [(0, base_face[(i + 1) % 5], base_face[i]) for i in range(5)]
    face_roles = ["base"] + ["pyramid"] * 5

    return Solid3D(
        slug="pentagonal-pyramid",
        title="Regular Pentagonal Pyramid (Johnson J2)",
        vertices=tuple(verts),
        faces=tuple(faces),
        face_roles=tuple(face_roles),
    )


@lru_cache(maxsize=None)
def build_catalog_solid(slug: str) -> Solid3D:
    """Constructs an exact 3D solid for any of the 26 canonical polyhedra.

    Args:
        slug: Canonical identifier for one of the 26 cataloged solids.

    Returns:
        Exact Solid3D instance.

    Raises:
        KeyError: If slug is not recognized.
    """
    # 01-platonic
    if slug == "tetrahedron":
        return Solid3D.from_regular_solid(get_platonic_solid("tetrahedron"))
    if slug == "hexahedron":
        return Solid3D.from_regular_solid(get_platonic_solid("hexahedron"))
    if slug == "octahedron":
        return Solid3D.from_regular_solid(get_platonic_solid("octahedron"))
    if slug == "icosahedron":
        return Solid3D.from_regular_solid(get_platonic_solid("icosahedron"))
    if slug == "dodecahedron":
        return Solid3D.from_regular_solid(get_platonic_solid("dodecahedron"))

    # 02-archimedean
    if slug == "truncated-tetrahedron":
        return truncate(build_catalog_solid("tetrahedron"), sp.Rational(1, 3))
    if slug == "cuboctahedron":
        return rectify(build_catalog_solid("hexahedron"))
    if slug == "truncated-hexahedron":
        return truncate(
            build_catalog_solid("hexahedron"),
            sp.Integer(1) - sp.sqrt(2) / sp.Integer(2),
        )
    if slug == "truncated-octahedron":
        return truncate(build_catalog_solid("octahedron"), sp.Rational(1, 3))
    if slug == "rhombicuboctahedron":
        return build_rhombicuboctahedron_solid()
    if slug == "icosidodecahedron":
        return rectify(build_catalog_solid("dodecahedron"))
    if slug == "truncated-icosahedron":
        return truncate(build_catalog_solid("icosahedron"), sp.Rational(1, 3))
    if slug == "truncated-dodecahedron":
        return truncate(
            build_catalog_solid("dodecahedron"),
            (sp.Integer(3) - PHI) / sp.Integer(5),
        )

    # 03-catalan
    if slug == "rhombic-dodecahedron":
        return polar_dual(build_catalog_solid("cuboctahedron"))
    if slug == "rhombic-triacontahedron":
        return polar_dual(build_catalog_solid("icosidodecahedron"))

    # 04-elevated
    if slug == "tetrahedron-elevatum":
        return elevate(build_catalog_solid("tetrahedron"))
    if slug == "hexahedron-elevatum":
        return elevate(build_catalog_solid("hexahedron"))
    if slug == "stella-octangula":
        return elevate(build_catalog_solid("octahedron"))
    if slug == "icosahedron-elevatum":
        return elevate(build_catalog_solid("icosahedron"))
    if slug == "dodecahedron-elevatum":
        return elevate(build_catalog_solid("dodecahedron"))
    if slug == "cuboctahedron-elevatum":
        return elevate(build_catalog_solid("cuboctahedron"))
    if slug == "icosidodecahedron-elevatum":
        return elevate(build_catalog_solid("icosidodecahedron"))

    # 05-pyramids
    if slug == "kepler-pyramid":
        return build_kepler_pyramid_solid(center_origin=True)
    if slug == "seked-pyramid":
        return build_seked_pyramid_solid(center_origin=True)
    if slug == "golden-bipyramid":
        return build_kepler_bipyramid_solid()
    if slug == "pentagonal-pyramid":
        return build_pentagonal_pyramid_solid(center_origin=True)

    raise KeyError(
        f"Unknown solid slug: {slug!r}. Available slugs: {list(_CANONICAL_ENTRIES.keys())}"
    )


def get_polyhedra_families() -> dict[str, PolyhedronFamily]:
    """Retrieves all five polyhedral families mapped by slug.

    Returns:
        Dictionary mapping family slugs ('01-platonic' .. '05-pyramids')
        to PolyhedronFamily instances.
    """
    return dict(_FAMILIES)


def get_polyhedra_catalog() -> dict[str, PolyhedronEntry]:
    """Retrieves all 26 canonical polyhedra mapped by slug.

    Returns:
        Dictionary mapping solid slug to PolyhedronEntry instances.
    """
    return dict(_CANONICAL_ENTRIES)


def get_polyhedron_entry(slug: str) -> PolyhedronEntry:
    """Retrieves a single polyhedron entry by slug name.

    Args:
        slug: Standard slug identifier ('tetrahedron', 'rhombicuboctahedron', etc.).

    Returns:
        Corresponding PolyhedronEntry instance.

    Raises:
        KeyError: If slug is not recognized.
    """
    catalog = get_polyhedra_catalog()
    if slug not in catalog:
        raise KeyError(
            f"Unknown polyhedron slug: {slug!r}. Available: {list(catalog.keys())}"
        )
    return catalog[slug]


# --- Static Catalog Data Definitions ---

_FAMILIES: dict[str, PolyhedronFamily] = {
    "01-platonic": PolyhedronFamily(
        slug="01-platonic",
        order=1,
        title="Platonic Solids",
        subtitle="The Five Regular Convex Polyhedra of Plato & Euclid",
        summary=(
            "Canonical regular polyhedra over ℤ and ℚ(ϕ) with identical "
            "regular polygon faces meeting at congruent vertex figures."
        ),
    ),
    "02-archimedean": PolyhedronFamily(
        slug="02-archimedean",
        order=2,
        title="Archimedean Solids",
        subtitle="Semi-Regular Truncations and Rectifications",
        summary=(
            "Convex uniform polyhedra composed of two or more types of regular "
            "polygons meeting at symmetric vertex figures."
        ),
    ),
    "03-catalan": PolyhedronFamily(
        slug="03-catalan",
        order=3,
        title="Catalan Solids",
        subtitle="Face-Transitive Duals of Archimedean Solids",
        summary=(
            "Convex polyhedra whose faces are congruent non-regular polygons, "
            "forming the polar duals of the semi-regular Archimedean solids."
        ),
    ),
    "04-elevated": PolyhedronFamily(
        slug="04-elevated",
        order=4,
        title="Elevated Solids (Corpora Elevata)",
        subtitle="Pacioli & Leonardo's Equilateral Stellations",
        summary=(
            "Non-convex polyhedra formed by erecting equilateral pyramids upon "
            "the planar faces of Platonic and Archimedean solids."
        ),
    ),
    "05-pyramids": PolyhedronFamily(
        slug="05-pyramids",
        order=5,
        title="Pyramids & Bipyramids",
        subtitle="Architectural Profiles, Kepler Harmonics & Johnson Caps",
        summary=(
            "Exact symbolic pyramid manifolds including the Kepler Golden Pyramid, "
            "Egyptian Seked 14:11, Golden Bipyramid, and Johnson Pentagonal Pyramid J2."
        ),
    ),
}

_CANONICAL_ENTRIES: dict[str, PolyhedronEntry] = {
    # 01-platonic
    "tetrahedron": PolyhedronEntry(
        slug="tetrahedron",
        canonical_id="P-01.01",
        family="01-platonic",
        order=1,
        title="Tetrahedron",
        latin_name="Tetrahedron",
        subtitle="Fire (Ignis) · Regular 4-Cell Simplex",
        enunciation=(
            "A regular polyhedron bounded by four equilateral triangular faces, "
            "with three meeting at each vertex."
        ),
        number_field=r"\mathbb{Z}",
        symmetry_group="T_d (order 24)",
        is_convex=True,
        dual_slug="tetrahedron",
        historical_source=(
            "Euclid, Elements XIII.13; Plato, Timaeus 54d–55a; "
            "Pacioli, De Divina Proportione (1509), Cap. XXI"
        ),
        leonardo_plates=(
            ("Tabula I", "0187", "Tetrahedron Planum Solidum"),
            ("Tabula II", "0189", "Tetrahedron Planum Vacuum"),
        ),
        tags=("platonic", "regular", "fire", "euclid", "pacioli", "simplex"),
        vertices_count=4,
        edges_count=6,
        faces_count=4,
        face_summary="4 equilateral triangles",
        edge_quadrances=(sp.Integer(8),),
        vertex_quadrances=(sp.Integer(3),),
        primary_dihedral_spread=sp.Rational(8, 9),
        vacuum_genus=3,
    ),
    "hexahedron": PolyhedronEntry(
        slug="hexahedron",
        canonical_id="P-01.02",
        family="01-platonic",
        order=2,
        title="Hexahedron (Cube)",
        latin_name="Hexahedron / Cubus",
        subtitle="Earth (Terra) · Regular Hexahedron",
        enunciation=(
            "A regular polyhedron bounded by six congruent square faces, "
            "with three meeting at each vertex."
        ),
        number_field=r"\mathbb{Z}",
        symmetry_group="O_h (order 48)",
        is_convex=True,
        dual_slug="octahedron",
        historical_source=(
            "Euclid, Elements XIII.15; Plato, Timaeus 55b–c; "
            "Pacioli, De Divina Proportione (1509), Cap. XXII"
        ),
        leonardo_plates=(
            ("Tabula VII", "0199", "Exahedron Planum Solidum"),
            ("Tabula VIII", "0201", "Exahedron Planum Vacuum"),
        ),
        tags=("platonic", "regular", "earth", "cube", "euclid", "pacioli"),
        vertices_count=8,
        edges_count=12,
        faces_count=6,
        face_summary="6 squares",
        edge_quadrances=(sp.Integer(4),),
        vertex_quadrances=(sp.Integer(3),),
        primary_dihedral_spread=sp.Integer(1),
        vacuum_genus=5,
    ),
    "octahedron": PolyhedronEntry(
        slug="octahedron",
        canonical_id="P-01.03",
        family="01-platonic",
        order=3,
        title="Octahedron",
        latin_name="Octahedron",
        subtitle="Air (Aer) · Regular Cross-Polytope",
        enunciation=(
            "A regular polyhedron bounded by eight equilateral triangular faces, "
            "with four meeting at each vertex."
        ),
        number_field=r"\mathbb{Z}",
        symmetry_group="O_h (order 48)",
        is_convex=True,
        dual_slug="hexahedron",
        historical_source=(
            "Euclid, Elements XIII.14; Plato, Timaeus 54c–d; "
            "Pacioli, De Divina Proportione (1509), Cap. XXIII"
        ),
        leonardo_plates=(
            ("Tabula XV", "0219", "Octahedron Planum Solidum"),
            ("Tabula XVI", "0221", "Octahedron Planum Vacuum"),
        ),
        tags=("platonic", "regular", "air", "octahedron", "euclid", "pacioli"),
        vertices_count=6,
        edges_count=12,
        faces_count=8,
        face_summary="8 equilateral triangles",
        edge_quadrances=(sp.Integer(2),),
        vertex_quadrances=(sp.Integer(1),),
        primary_dihedral_spread=sp.Rational(8, 9),
        vacuum_genus=7,
    ),
    "icosahedron": PolyhedronEntry(
        slug="icosahedron",
        canonical_id="P-01.04",
        family="01-platonic",
        order=4,
        title="Icosahedron",
        latin_name="Icosahedron",
        subtitle="Water (Aqua) · Golden Ratio Polyhedron",
        enunciation=(
            "A regular polyhedron bounded by twenty equilateral triangular faces, "
            "with five meeting at each vertex."
        ),
        number_field=r"\mathbb{Q}(\phi)",
        symmetry_group="I_h (order 120)",
        is_convex=True,
        dual_slug="dodecahedron",
        historical_source=(
            "Euclid, Elements XIII.16; Plato, Timaeus 54e–55a; "
            "Pacioli, De Divina Proportione (1509), Cap. XXIIII"
        ),
        leonardo_plates=(
            ("Tabula XXI", "0231", "Icosahedron Planum Solidum"),
            ("Tabula XXII", "0233", "Icosahedron Planum Vacuum"),
        ),
        tags=(
            "platonic",
            "regular",
            "water",
            "icosahedron",
            "phi",
            "golden-ratio",
            "euclid",
            "pacioli",
        ),
        vertices_count=12,
        edges_count=30,
        faces_count=20,
        face_summary="20 equilateral triangles",
        edge_quadrances=(sp.Integer(4),),
        vertex_quadrances=(sp.Rational(5, 2) + sp.sqrt(5) / sp.Integer(2),),
        primary_dihedral_spread=sp.Rational(4, 9),
        vacuum_genus=19,
    ),
    "dodecahedron": PolyhedronEntry(
        slug="dodecahedron",
        canonical_id="P-01.05",
        family="01-platonic",
        order=5,
        title="Dodecahedron",
        latin_name="Dodecahedron",
        subtitle="Aether (Cosmos) · Pentagonal Celestial Solid",
        enunciation=(
            "A regular polyhedron bounded by twelve regular pentagonal faces, "
            "with three meeting at each vertex."
        ),
        number_field=r"\mathbb{Q}(\phi)",
        symmetry_group="I_h (order 120)",
        is_convex=True,
        dual_slug="icosahedron",
        historical_source=(
            "Euclid, Elements XIII.17; Plato, Timaeus 55c; "
            "Pacioli, De Divina Proportione (1509), Cap. XXV"
        ),
        leonardo_plates=(
            ("Tabula XXVII", "0243", "Dodecahedron Planum Solidum"),
            ("Tabula XXVIII", "0245", "Dodecahedron Planum Vacuum"),
        ),
        tags=(
            "platonic",
            "regular",
            "aether",
            "dodecahedron",
            "phi",
            "pentagon",
            "euclid",
            "pacioli",
        ),
        vertices_count=20,
        edges_count=30,
        faces_count=12,
        face_summary="12 regular pentagons",
        edge_quadrances=(sp.Integer(6) - sp.Integer(2) * sp.sqrt(5),),
        vertex_quadrances=(sp.Integer(3),),
        primary_dihedral_spread=sp.Rational(4, 5),
        vacuum_genus=11,
    ),
    # 02-archimedean
    "truncated-tetrahedron": PolyhedronEntry(
        slug="truncated-tetrahedron",
        canonical_id="P-02.01",
        family="02-archimedean",
        order=1,
        title="Truncated Tetrahedron",
        latin_name="Tetrahedron Abscisum",
        subtitle="Archimedean Corner-Cut Tetrahedron (1/3 Edge Ratio)",
        enunciation=(
            "An Archimedean solid formed by truncating the vertices of a regular "
            "tetrahedron at one-third edge length."
        ),
        number_field=r"\mathbb{Q}",
        symmetry_group="T_d (order 24)",
        is_convex=True,
        dual_slug="triakis-tetrahedron",
        historical_source=(
            "Archimedes of Syracuse; Heron, Definitiones; "
            "Pacioli, De Divina Proportione (1509), Tabulae III–IIII"
        ),
        leonardo_plates=(
            ("Tabula III", "0191", "Tetrahedron Abscisum Solidum"),
            ("Tabula IIII", "0193", "Tetrahedron Abscisum Vacuum"),
        ),
        tags=("archimedean", "truncation", "tetrahedron", "pacioli", "semi-regular"),
        vertices_count=12,
        edges_count=18,
        faces_count=8,
        face_summary="4 equilateral triangles + 4 regular hexagons",
        edge_quadrances=(sp.Rational(8, 9),),
        vertex_quadrances=(sp.Rational(11, 9),),
        primary_dihedral_spread=sp.Rational(8, 9),
        vacuum_genus=7,
    ),
    "cuboctahedron": PolyhedronEntry(
        slug="cuboctahedron",
        canonical_id="P-02.02",
        family="02-archimedean",
        order=2,
        title="Cuboctahedron",
        latin_name="Exahedron Abscisum",
        subtitle="Pacioli's Edge-Midpoint Truncation of Cube & Octahedron",
        enunciation=(
            "A quasi-regular Archimedean solid formed by rectifying a regular "
            "hexahedron or octahedron at edge midpoints."
        ),
        number_field=r"\mathbb{Q}",
        symmetry_group="O_h (order 48)",
        is_convex=True,
        dual_slug="rhombic-dodecahedron",
        historical_source=(
            "Archimedes of Syracuse; Pacioli, De Divina Proportione (1509), "
            "Cap. XXII & Tabulae VIIII–X"
        ),
        leonardo_plates=(
            ("Tabula VIIII", "0203", "Exahedron Abscisum Solidum"),
            ("Tabula X", "0205", "Exahedron Abscisum Vacuum"),
        ),
        tags=(
            "archimedean",
            "rectification",
            "cube",
            "octahedron",
            "pacioli",
            "quasi-regular",
        ),
        vertices_count=12,
        edges_count=24,
        faces_count=14,
        face_summary="8 equilateral triangles + 6 squares",
        edge_quadrances=(sp.Integer(2),),
        vertex_quadrances=(sp.Integer(2),),
        primary_dihedral_spread=sp.Rational(2, 3),
        vacuum_genus=13,
    ),
    "truncated-hexahedron": PolyhedronEntry(
        slug="truncated-hexahedron",
        canonical_id="P-02.03",
        family="02-archimedean",
        order=3,
        title="Truncated Hexahedron",
        latin_name="Exahedron Abscisum Octogonale",
        subtitle="Archimedean Corner-Cut Cube with Regular Octagons",
        enunciation=(
            "An Archimedean solid formed by cutting corners of a cube at edge "
            "depth 1 - sqrt(2)/2 to yield regular octagons."
        ),
        number_field=r"\mathbb{Q}(\sqrt{2})",
        symmetry_group="O_h (order 48)",
        is_convex=True,
        dual_slug="triakis-octahedron",
        historical_source="Archimedes of Syracuse; Johannes Kepler, Harmonices Mundi (1619), Lib. II",
        leonardo_plates=(),
        tags=("archimedean", "truncation", "cube", "octagon", "sqrt2"),
        vertices_count=24,
        edges_count=36,
        faces_count=14,
        face_summary="8 equilateral triangles + 6 regular octagons",
        edge_quadrances=(sp.Integer(12) - sp.Integer(8) * sp.sqrt(2),),
        vertex_quadrances=(sp.Integer(5) - sp.Integer(2) * sp.sqrt(2),),
        primary_dihedral_spread=sp.Integer(1),
        vacuum_genus=13,
    ),
    "truncated-octahedron": PolyhedronEntry(
        slug="truncated-octahedron",
        canonical_id="P-02.04",
        family="02-archimedean",
        order=4,
        title="Truncated Octahedron",
        latin_name="Octahedron Abscisum",
        subtitle="Space-Filling Archimedean Solid (Permutohedron)",
        enunciation=(
            "A space-filling Archimedean solid formed by truncating the vertices "
            "of a regular octahedron at one-third edge length."
        ),
        number_field=r"\mathbb{Q}",
        symmetry_group="O_h (order 48)",
        is_convex=True,
        dual_slug="tetrakis-hexahedron",
        historical_source=(
            "Archimedes of Syracuse; Pacioli, De Divina Proportione (1509), "
            "Tabulae XVII–XVIII"
        ),
        leonardo_plates=(
            ("Tabula XVII", "0223", "Octahedron Abscisum Solidum"),
            ("Tabula XVIII", "0225", "Octahedron Abscisum Vacuum"),
        ),
        tags=(
            "archimedean",
            "truncation",
            "octahedron",
            "space-filling",
            "permutohedron",
            "pacioli",
        ),
        vertices_count=24,
        edges_count=36,
        faces_count=14,
        face_summary="6 squares + 8 regular hexagons",
        edge_quadrances=(sp.Rational(2, 9),),
        vertex_quadrances=(sp.Rational(5, 9),),
        primary_dihedral_spread=sp.Rational(8, 9),
        vacuum_genus=13,
    ),
    "rhombicuboctahedron": PolyhedronEntry(
        slug="rhombicuboctahedron",
        canonical_id="P-02.05",
        family="02-archimedean",
        order=5,
        title="Rhombicuboctahedron",
        latin_name="Vigintisex Basium",
        subtitle="Leonardo da Vinci's 26-Base Body (18 Squares + 8 Triangles)",
        enunciation=(
            "Leonardo's 26-base body (Vigintisex Basium), bounded by 18 squares "
            "and 8 equilateral triangles."
        ),
        number_field=r"\mathbb{Q}(\sqrt{2})",
        symmetry_group="O_h (order 48)",
        is_convex=True,
        dual_slug="deltoidal-icositetrahedron",
        historical_source=(
            "Archimedes of Syracuse; Pacioli, De Divina Proportione (1509), "
            "Cap. LXI & Tabulae XXXV–XXXVI"
        ),
        leonardo_plates=(
            ("Tabula XXXV", "0259", "Vigintisex Basium Planum Solidum"),
            ("Tabula XXXVI", "0261", "Vigintisex Basium Planum Vacuum"),
        ),
        tags=(
            "archimedean",
            "rhombicuboctahedron",
            "pacioli",
            "leonardo",
            "sqrt2",
            "vigintisex-basium",
        ),
        vertices_count=24,
        edges_count=48,
        faces_count=26,
        face_summary="8 equilateral triangles + 18 squares",
        edge_quadrances=(sp.Integer(4),),
        vertex_quadrances=(sp.Integer(5) + sp.Integer(2) * sp.sqrt(2),),
        primary_dihedral_spread=sp.Rational(1, 2),
        vacuum_genus=25,
    ),
    "icosidodecahedron": PolyhedronEntry(
        slug="icosidodecahedron",
        canonical_id="P-02.06",
        family="02-archimedean",
        order=6,
        title="Icosidodecahedron",
        latin_name="Dodecahedron Abscisum",
        subtitle="Quasi-Regular Golden Ratio Solid (20 Triangles + 12 Pentagons)",
        enunciation=(
            "A quasi-regular Archimedean solid formed by edge rectification of a "
            "regular dodecahedron or icosahedron."
        ),
        number_field=r"\mathbb{Q}(\phi)",
        symmetry_group="I_h (order 120)",
        is_convex=True,
        dual_slug="rhombic-triacontahedron",
        historical_source=(
            "Archimedes of Syracuse; Pacioli, De Divina Proportione (1509), "
            "Cap. XXVI & Tabulae XXIX–XXX"
        ),
        leonardo_plates=(
            ("Tabula XXIX", "0247", "Dodecahedron Abscisum Solidum"),
            ("Tabula XXX", "0249", "Dodecahedron Abscisum Vacuum"),
        ),
        tags=(
            "archimedean",
            "rectification",
            "dodecahedron",
            "icosahedron",
            "phi",
            "golden-ratio",
            "pacioli",
        ),
        vertices_count=30,
        edges_count=60,
        faces_count=32,
        face_summary="20 equilateral triangles + 12 regular pentagons",
        edge_quadrances=(sp.Integer(1),),
        vertex_quadrances=(sp.Rational(3, 2) + sp.sqrt(5) / sp.Integer(2),),
        primary_dihedral_spread=sp.Rational(2, 3)
        - sp.Integer(2) * sp.sqrt(5) / sp.Integer(15),
        vacuum_genus=31,
    ),
    "truncated-icosahedron": PolyhedronEntry(
        slug="truncated-icosahedron",
        canonical_id="P-02.07",
        family="02-archimedean",
        order=7,
        title="Truncated Icosahedron",
        latin_name="Icosahedron Abscisum",
        subtitle="The Archimedean Fullerene / Soccer Ball (C60 Buckyball)",
        enunciation=(
            "The canonical truncated icosahedron (fullerene Buckyball), bounded by "
            "12 pentagons and 20 hexagons."
        ),
        number_field=r"\mathbb{Q}(\phi)",
        symmetry_group="I_h (order 120)",
        is_convex=True,
        dual_slug="pentakis-dodecahedron",
        historical_source=(
            "Archimedes of Syracuse; Pacioli, De Divina Proportione (1509), "
            "Tabulae XXIII–XXIIII; Kepler (1619)"
        ),
        leonardo_plates=(
            ("Tabula XXIII", "0235", "Icosahedron Abscisum Solidum"),
            ("Tabula XXIIII", "0237", "Icosahedron Abscisum Vacuum"),
        ),
        tags=(
            "archimedean",
            "truncation",
            "icosahedron",
            "fullerene",
            "buckyball",
            "phi",
            "pacioli",
        ),
        vertices_count=60,
        edges_count=90,
        faces_count=32,
        face_summary="12 regular pentagons + 20 regular hexagons",
        edge_quadrances=(sp.Rational(4, 9),),
        vertex_quadrances=(sp.Rational(29, 18) + sp.sqrt(5) / sp.Integer(2),),
        primary_dihedral_spread=sp.Rational(4, 9),
        vacuum_genus=31,
    ),
    "truncated-dodecahedron": PolyhedronEntry(
        slug="truncated-dodecahedron",
        canonical_id="P-02.08",
        family="02-archimedean",
        order=8,
        title="Truncated Dodecahedron",
        latin_name="Dodecahedron Abscisum Decagonale",
        subtitle="Archimedean Decagonal Solid at Exact (3 - phi)/5 Truncation",
        enunciation=(
            "An Archimedean solid formed by truncating a dodecahedron at edge depth "
            "(3 - phi)/5 to yield regular decagons."
        ),
        number_field=r"\mathbb{Q}(\phi)",
        symmetry_group="I_h (order 120)",
        is_convex=True,
        dual_slug="triakis-icosahedron",
        historical_source=(
            "Archimedes of Syracuse; Piero della Francesca (1482); "
            "Kepler, Harmonices Mundi (1619)"
        ),
        leonardo_plates=(),
        tags=(
            "archimedean",
            "truncation",
            "dodecahedron",
            "decagon",
            "phi",
            "golden-ratio",
        ),
        vertices_count=60,
        edges_count=90,
        faces_count=32,
        face_summary="20 equilateral triangles + 12 regular decagons",
        edge_quadrances=(sp.Rational(6, 5) - sp.Rational(2, 5) * sp.sqrt(5),),
        vertex_quadrances=(sp.Rational(9, 5) + sp.Rational(2, 5) * sp.sqrt(5),),
        primary_dihedral_spread=sp.Rational(4, 5),
        vacuum_genus=31,
    ),
    # 03-catalan
    "rhombic-dodecahedron": PolyhedronEntry(
        slug="rhombic-dodecahedron",
        canonical_id="P-03.01",
        family="03-catalan",
        order=1,
        title="Rhombic Dodecahedron",
        latin_name="Dodecahedron Rhombicum",
        subtitle="Kepler's Space-Filling Catalan Solid · Polar Dual of Cuboctahedron",
        enunciation=(
            "A Catalan solid and space-filling polyhedron bounded by 12 congruent "
            "rhombi, polar dual to the cuboctahedron."
        ),
        number_field=r"\mathbb{Q}",
        symmetry_group="O_h (order 48)",
        is_convex=True,
        dual_slug="cuboctahedron",
        historical_source=(
            "Johannes Kepler, Strena seu de Nive Sexangula (1611); "
            "Eugène Catalan (1865)"
        ),
        leonardo_plates=(),
        tags=("catalan", "polar-dual", "space-filling", "rhombus", "kepler"),
        vertices_count=14,
        edges_count=24,
        faces_count=12,
        face_summary="12 rhombi",
        edge_quadrances=(sp.Rational(27, 16),),
        vertex_quadrances=(sp.Rational(27, 16), sp.Rational(9, 4)),
        primary_dihedral_spread=sp.Rational(3, 4),
        vacuum_genus=11,
    ),
    "rhombic-triacontahedron": PolyhedronEntry(
        slug="rhombic-triacontahedron",
        canonical_id="P-03.02",
        family="03-catalan",
        order=2,
        title="Rhombic Triacontahedron",
        latin_name="Triacontahedron Rhombicum",
        subtitle="Kepler's Golden Zonohedron · Polar Dual of Icosidodecahedron",
        enunciation=(
            "A Catalan zonohedron bounded by 30 congruent golden rhombi, polar "
            "dual to the icosidodecahedron."
        ),
        number_field=r"\mathbb{Q}(\phi)",
        symmetry_group="I_h (order 120)",
        is_convex=True,
        dual_slug="icosidodecahedron",
        historical_source=(
            "Johannes Kepler, Harmonices Mundi (1619), Lib. II; "
            "Eugène Catalan (1865)"
        ),
        leonardo_plates=(),
        tags=(
            "catalan",
            "polar-dual",
            "golden-ratio",
            "zonohedron",
            "kepler",
            "phi",
        ),
        vertices_count=32,
        edges_count=60,
        faces_count=30,
        face_summary="30 golden rhombi",
        edge_quadrances=(sp.Rational(25, 32) + sp.Rational(5, 32) * sp.sqrt(5),),
        vertex_quadrances=(
            sp.Rational(45, 32) + sp.Rational(15, 32) * sp.sqrt(5),
            sp.Rational(25, 16) + sp.Rational(5, 8) * sp.sqrt(5),
        ),
        primary_dihedral_spread=sp.Rational(5, 8) - sp.sqrt(5) / sp.Integer(8),
        vacuum_genus=29,
    ),
    # 04-elevated
    "tetrahedron-elevatum": PolyhedronEntry(
        slug="tetrahedron-elevatum",
        canonical_id="P-04.01",
        family="04-elevated",
        order=1,
        title="Tetrahedron Elevatum",
        latin_name="Tetrahedron Elevatum",
        subtitle="Triakis Tetrahedron · Pacioli Stellation of Tetrahedron",
        enunciation=(
            "A stellated polyhedron formed by erecting equilateral triangular pyramids "
            "on the four faces of a tetrahedron."
        ),
        number_field=r"\mathbb{Q}",
        symmetry_group="T_d (order 24)",
        is_convex=False,
        dual_slug="truncated-tetrahedron",
        historical_source="Luca Pacioli & Leonardo da Vinci, De Divina Proportione (1509), Tabulae V–VI",
        leonardo_plates=(
            ("Tabula V", "0195", "Tetrahedron Elevatum Solidum"),
            ("Tabula VI", "0197", "Tetrahedron Elevatum Vacuum"),
        ),
        tags=("elevated", "stellation", "tetrahedron", "pacioli", "triakis"),
        vertices_count=8,
        edges_count=18,
        faces_count=12,
        face_summary="12 equilateral triangles",
        edge_quadrances=(sp.Integer(8),),
        vertex_quadrances=(sp.Integer(3), sp.Rational(25, 3)),
        primary_dihedral_spread=sp.Rational(8, 9),
        vacuum_genus=11,
    ),
    "hexahedron-elevatum": PolyhedronEntry(
        slug="hexahedron-elevatum",
        canonical_id="P-04.02",
        family="04-elevated",
        order=2,
        title="Hexahedron Elevatum",
        latin_name="Exahedron Elevatum",
        subtitle="Tetrakis Hexahedron · Pacioli Stellation of Cube",
        enunciation=(
            "A stellated polyhedron formed by erecting equilateral pyramids on the "
            "six faces of a cube."
        ),
        number_field=r"\mathbb{Q}(\sqrt{2})",
        symmetry_group="O_h (order 48)",
        is_convex=False,
        dual_slug="truncated-octahedron",
        historical_source="Luca Pacioli & Leonardo da Vinci, De Divina Proportione (1509), Tabulae XI–XII",
        leonardo_plates=(
            ("Tabula XI", "0207", "Exahedron Elevatum Solidum"),
            ("Tabula XII", "0209", "Exahedron Elevatum Vacuum"),
        ),
        tags=("elevated", "stellation", "cube", "pacioli", "tetrakis"),
        vertices_count=14,
        edges_count=36,
        faces_count=24,
        face_summary="24 equilateral triangles",
        edge_quadrances=(sp.Integer(4),),
        vertex_quadrances=(
            sp.Integer(3),
            sp.Integer(3) + sp.Integer(2) * sp.sqrt(2),
        ),
        primary_dihedral_spread=sp.Rational(8, 9),
        vacuum_genus=23,
    ),
    "stella-octangula": PolyhedronEntry(
        slug="stella-octangula",
        canonical_id="P-04.03",
        family="04-elevated",
        order=3,
        title="Stella Octangula (Octahedron Elevatum)",
        latin_name="Octahedron Elevatum",
        subtitle="Compound of Two Dual Tetrahedra · Leonardo & Kepler's Star",
        enunciation=(
            "The Stella Octangula compound of two dual tetrahedra, formed by elevating "
            "the eight faces of an octahedron."
        ),
        number_field=r"\mathbb{Z}",
        symmetry_group="O_h (order 48)",
        is_convex=False,
        dual_slug="stella-octangula",
        historical_source=(
            "Luca Pacioli & Leonardo da Vinci (1509), Tabulae XIX–XX; "
            "Kepler, Harmonices Mundi (1619)"
        ),
        leonardo_plates=(
            ("Tabula XIX", "0227", "Octahedron Elevatum Solidum"),
            ("Tabula XX", "0229", "Octahedron Elevatum Vacuum"),
        ),
        tags=(
            "elevated",
            "stellation",
            "octahedron",
            "stella-octangula",
            "kepler",
            "compound",
            "pacioli",
        ),
        vertices_count=14,
        edges_count=36,
        faces_count=24,
        face_summary="24 equilateral triangles",
        edge_quadrances=(sp.Integer(2),),
        vertex_quadrances=(sp.Integer(1), sp.Integer(3)),
        primary_dihedral_spread=sp.Rational(8, 9),
        vacuum_genus=23,
    ),
    "icosahedron-elevatum": PolyhedronEntry(
        slug="icosahedron-elevatum",
        canonical_id="P-04.04",
        family="04-elevated",
        order=4,
        title="Icosahedron Elevatum",
        latin_name="Icosahedron Elevatum",
        subtitle="Triakis Icosahedron · Pacioli Stellation of Icosahedron",
        enunciation=(
            "A stellated polyhedron formed by erecting equilateral triangular pyramids "
            "on the twenty faces of an icosahedron."
        ),
        number_field=r"\mathbb{Q}(\phi, \sqrt{2})",
        symmetry_group="I_h (order 120)",
        is_convex=False,
        dual_slug="truncated-dodecahedron",
        historical_source=(
            "Luca Pacioli & Leonardo da Vinci, De Divina Proportione (1509), "
            "Tabulae XXV–XXVI"
        ),
        leonardo_plates=(
            ("Tabula XXV", "0239", "Icosahedron Elevatum Solidum"),
            ("Tabula XXVI", "0241", "Icosahedron Elevatum Vacuum"),
        ),
        tags=("elevated", "stellation", "icosahedron", "phi", "pacioli", "triakis"),
        vertices_count=32,
        edges_count=90,
        faces_count=60,
        face_summary="60 equilateral triangles",
        edge_quadrances=(sp.Integer(4),),
        vertex_quadrances=(
            sp.Rational(5, 2) + sp.sqrt(5) / sp.Integer(2),
            sp.Rational(23, 6)
            + sp.sqrt(5) / sp.Integer(2)
            + sp.Integer(2) * sp.sqrt(2)
            + sp.Rational(2, 3) * sp.sqrt(10),
        ),
        primary_dihedral_spread=sp.Rational(8, 9),
        vacuum_genus=59,
    ),
    "dodecahedron-elevatum": PolyhedronEntry(
        slug="dodecahedron-elevatum",
        canonical_id="P-04.05",
        family="04-elevated",
        order=5,
        title="Dodecahedron Elevatum",
        latin_name="Dodecahedron Elevatum",
        subtitle="Pentakis Dodecahedron · Pacioli Stellation of Dodecahedron",
        enunciation=(
            "A stellated polyhedron formed by erecting equilateral pentagonal pyramids "
            "on the twelve faces of a dodecahedron."
        ),
        number_field=r"\mathbb{Q}(\sqrt{5 - \sqrt{5}})",
        symmetry_group="I_h (order 120)",
        is_convex=False,
        dual_slug="truncated-icosahedron",
        historical_source=(
            "Luca Pacioli & Leonardo da Vinci, De Divina Proportione (1509), "
            "Tabulae XXXI–XXXII"
        ),
        leonardo_plates=(
            ("Tabula XXXI", "0251", "Dodecahedron Elevatum Solidum"),
            ("Tabula XXXII", "0253", "Dodecahedron Elevatum Vacuum"),
        ),
        tags=("elevated", "stellation", "dodecahedron", "phi", "pacioli", "pentakis"),
        vertices_count=32,
        edges_count=90,
        faces_count=60,
        face_summary="60 equilateral triangles",
        edge_quadrances=(sp.Integer(6) - sp.Integer(2) * sp.sqrt(5),),
        vertex_quadrances=(
            sp.Integer(3),
            sp.Integer(5) - sp.sqrt(5) + sp.sqrt(sp.Integer(50) - sp.Integer(20) * sp.sqrt(5)),
        ),
        primary_dihedral_spread=sp.Rational(4, 9),
        vacuum_genus=59,
    ),
    "cuboctahedron-elevatum": PolyhedronEntry(
        slug="cuboctahedron-elevatum",
        canonical_id="P-04.06",
        family="04-elevated",
        order=6,
        title="Cuboctahedron Elevatum",
        latin_name="Exahedron Abscisum Elevatum",
        subtitle="Pacioli's 14-Base Stellation (8 Triangles + 6 Squares Elevated)",
        enunciation=(
            "Pacioli's Exahedron Abscisum Elevatum, formed by erecting equilateral "
            "pyramids on the 14 faces of a cuboctahedron."
        ),
        number_field=r"\mathbb{Q}",
        symmetry_group="O_h (order 48)",
        is_convex=False,
        dual_slug=None,
        historical_source=(
            "Luca Pacioli & Leonardo da Vinci, De Divina Proportione (1509), "
            "Tabulae XIII–XIIII"
        ),
        leonardo_plates=(
            ("Tabula XIII", "0211", "Exahedron Abscisum Elevatum Solidum"),
            ("Tabula XIIII", "0217", "Exahedron Abscisum Elevatum Vacuum"),
        ),
        tags=("elevated", "stellation", "cuboctahedron", "pacioli"),
        vertices_count=26,
        edges_count=72,
        faces_count=48,
        face_summary="48 equilateral triangles",
        edge_quadrances=(sp.Integer(2),),
        vertex_quadrances=(sp.Integer(2), sp.Integer(4), sp.Rational(16, 3)),
        primary_dihedral_spread=sp.Rational(8, 9),
        vacuum_genus=47,
    ),
    "icosidodecahedron-elevatum": PolyhedronEntry(
        slug="icosidodecahedron-elevatum",
        canonical_id="P-04.07",
        family="04-elevated",
        order=7,
        title="Icosidodecahedron Elevatum",
        latin_name="Dodecahedron Abscisum Elevatum",
        subtitle="Pacioli's 32-Base Stellation (20 Triangles + 12 Pentagons Elevated)",
        enunciation=(
            "Pacioli's Dodecahedron Abscisum Elevatum, formed by erecting equilateral "
            "pyramids on the 32 faces of an icosidodecahedron."
        ),
        number_field=r"\mathbb{Q}(\sqrt{5 - \sqrt{5}}, \sqrt{2})",
        symmetry_group="I_h (order 120)",
        is_convex=False,
        dual_slug=None,
        historical_source=(
            "Luca Pacioli & Leonardo da Vinci, De Divina Proportione (1509), "
            "Tabulae XXXIII–XXXIIII"
        ),
        leonardo_plates=(
            ("Tabula XXXIII", "0255", "Dodecahedron Abscisum Elevatum Solidum"),
            ("Tabula XXXIIII", "0257", "Dodecahedron Abscisum Elevatum Vacuum"),
        ),
        tags=("elevated", "stellation", "icosidodecahedron", "pacioli", "phi"),
        vertices_count=62,
        edges_count=180,
        faces_count=120,
        face_summary="120 equilateral triangles",
        edge_quadrances=(sp.Integer(1),),
        vertex_quadrances=(
            sp.Rational(3, 2) + sp.sqrt(5) / sp.Integer(2),
            sp.Rational(11, 6)
            + sp.sqrt(5) / sp.Integer(2)
            + sp.sqrt(2)
            + sp.Rational(1, 3) * sp.sqrt(10),
            sp.Rational(3, 2)
            + sp.Rational(3, 10) * sp.sqrt(5)
            + sp.Integer(2) * sp.sqrt(sp.Integer(6) + sp.Integer(2) * sp.sqrt(5))
            + sp.sqrt(sp.Integer(30) + sp.Integer(10) * sp.sqrt(5))
            - sp.Rational(4, 5) * sp.sqrt(5) * sp.sqrt(sp.Integer(6) + sp.Integer(2) * sp.sqrt(5))
            - sp.Rational(2, 5) * sp.sqrt(5) * sp.sqrt(sp.Integer(30) + sp.Integer(10) * sp.sqrt(5)),
        ),
        primary_dihedral_spread=sp.Rational(8, 9),
        vacuum_genus=119,
    ),
    # 05-pyramids
    "kepler-pyramid": PolyhedronEntry(
        slug="kepler-pyramid",
        canonical_id="P-05.01",
        family="05-pyramids",
        order=1,
        title="Kepler Golden Pyramid",
        latin_name="Pyramis Aurea Kepleriana",
        subtitle="Herodotus's Golden Section Pyramid over Q(sqrt(phi))",
        enunciation=(
            "The Great Pyramid profile based on the Kepler right triangle "
            "1 : sqrt(phi) : phi satisfying Herodotus's area law."
        ),
        number_field=r"\mathbb{Q}(\sqrt{\phi})",
        symmetry_group="C_{4v} (order 8)",
        is_convex=True,
        dual_slug=None,
        historical_source=(
            "Johannes Kepler, Epistola ad Mästlinum (1597); "
            "Herodotus, Histories II.124"
        ),
        leonardo_plates=(
            ("Tabula XLVII", "0283", "Pyramis Laterata Quadrangula Solida"),
            ("Tabula XLVIII", "0287", "Pyramis Laterata Quadrangula Vacua"),
        ),
        tags=("pyramid", "kepler", "phi", "golden-ratio", "herodotus", "giza"),
        vertices_count=5,
        edges_count=8,
        faces_count=5,
        face_summary="1 square + 4 Kepler golden triangles",
        edge_quadrances=(sp.Rational(5, 2) + sp.sqrt(5) / sp.Integer(2), sp.Integer(4)),
        vertex_quadrances=(
            sp.Rational(9, 32) + sp.Rational(9, 32) * sp.sqrt(5),
            sp.Rational(65, 32) + sp.Rational(1, 32) * sp.sqrt(5),
        ),
        primary_dihedral_spread=sp.Integer(3) * PHI - sp.Integer(4),
        vacuum_genus=4,
    ),
    "seked-pyramid": PolyhedronEntry(
        slug="seked-pyramid",
        canonical_id="P-05.02",
        family="05-pyramids",
        order=2,
        title="Seked 14:11 Pyramid",
        latin_name="Pyramis Aegyptia Seked",
        subtitle="Khufu Historical Architectural Profile (Seked 5 1/2 Palms)",
        enunciation=(
            "The canonical Egyptian architectural pyramid with Seked slope 14:11 "
            "(rise 14 to run 11 palms)."
        ),
        number_field=r"\mathbb{Q}",
        symmetry_group="C_{4v} (order 8)",
        is_convex=True,
        dual_slug=None,
        historical_source=(
            "Rhind Mathematical Papyrus (c. 1550 BCE), Problem 56; "
            "Khufu Pyramid survey"
        ),
        leonardo_plates=(
            ("Tabula XLVII", "0283", "Pyramis Laterata Quadrangula Solida"),
            ("Tabula XLVIII", "0287", "Pyramis Laterata Quadrangula Vacua"),
        ),
        tags=("pyramid", "seked", "egyptian", "khufu", "giza", "rational"),
        vertices_count=5,
        edges_count=8,
        faces_count=5,
        face_summary="1 square + 4 Seked 14:11 triangles",
        edge_quadrances=(sp.Rational(438, 121), sp.Integer(4)),
        vertex_quadrances=(sp.Rational(441, 484), sp.Rational(1017, 484)),
        primary_dihedral_spread=sp.Rational(85848, 100489),
        vacuum_genus=4,
    ),
    "golden-bipyramid": PolyhedronEntry(
        slug="golden-bipyramid",
        canonical_id="P-05.03",
        family="05-pyramids",
        order=3,
        title="Golden Square Bipyramid",
        latin_name="Bipyramis Aurea",
        subtitle="Octahedral Double Pyramid over Kepler Right Triangle",
        enunciation=(
            "An octahedral bipyramid formed by reflecting the Kepler Golden Pyramid "
            "across its square base."
        ),
        number_field=r"\mathbb{Q}(\sqrt{\phi})",
        symmetry_group="D_{4h} (order 16)",
        is_convex=True,
        dual_slug=None,
        historical_source="Johannes Kepler (1597); GEOMETOR Golden Pyramid Canon",
        leonardo_plates=(),
        tags=("bipyramid", "kepler", "phi", "golden-ratio", "octahedral"),
        vertices_count=6,
        edges_count=12,
        faces_count=8,
        face_summary="8 Kepler golden triangles",
        edge_quadrances=(sp.Rational(5, 2) + sp.sqrt(5) / sp.Integer(2), sp.Integer(4)),
        vertex_quadrances=(sp.Rational(1, 2) + sp.sqrt(5) / sp.Integer(2), sp.Integer(2)),
        primary_dihedral_spread=sp.Integer(3) * PHI - sp.Integer(4),
        vacuum_genus=7,
    ),
    "pentagonal-pyramid": PolyhedronEntry(
        slug="pentagonal-pyramid",
        canonical_id="P-05.04",
        family="05-pyramids",
        order=4,
        title="Regular Pentagonal Pyramid (Johnson J2)",
        latin_name="Pyramis Laterata Penthagona (Johnson J2)",
        subtitle="The 6-Vertex Icosahedral Cap of Euclid XIII.16 & Leonardo",
        enunciation=(
            "The regular equilateral pentagonal pyramid (Johnson Solid J2), "
            "forming the 6-vertex cap of the regular icosahedron."
        ),
        number_field=r"\mathbb{Q}(\phi)",
        symmetry_group="C_{5v} (order 10)",
        is_convex=True,
        dual_slug="pentagonal-pyramid",
        historical_source=(
            "Euclid, Elements XIII.16; Luca Pacioli & Leonardo da Vinci (1509), "
            "Tabulae LI–LII; Norman Johnson (1966, J2)"
        ),
        leonardo_plates=(
            ("Tabula LI", "0293", "Pyramis Laterata Penthagona Solida"),
            ("Tabula LII", "0295", "Pyramis Laterata Penthagona Vacua"),
        ),
        tags=(
            "pyramid",
            "johnson",
            "j2",
            "icosahedron-cap",
            "phi",
            "golden-ratio",
            "euclid",
            "pacioli",
        ),
        vertices_count=6,
        edges_count=10,
        faces_count=6,
        face_summary="1 regular pentagon + 5 equilateral triangles",
        edge_quadrances=(sp.Integer(4),),
        vertex_quadrances=(
            sp.Rational(25, 18) - sp.Rational(5, 18) * sp.sqrt(5),
            sp.Rational(37, 18) + sp.Rational(7, 18) * sp.sqrt(5),
        ),
        primary_dihedral_spread=sp.Rational(2, 3)
        - sp.Integer(2) * sp.sqrt(5) / sp.Integer(15),
        vacuum_genus=5,
    ),
}
