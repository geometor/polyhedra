"""Exact symbolic Platonic solids registry and 3D Rational Trigonometry.

Provides canonical definitions of the five regular polyhedra over Z and Q(phi)
with exact coordinates, face orientations, edge topologies, and dihedral spreads.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

# Exact Golden Ratio: zero float or sp.Float
PHI: sp.Expr = (sp.Integer(1) + sp.sqrt(5)) / sp.Integer(2)
PHI_INV: sp.Expr = PHI - sp.Integer(1)


@dataclass(frozen=True)
class RegularSolid:
    """Exact symbolic specification of a regular convex Platonic solid.

    Attributes:
        slug: Short lowercase identifier ('tetrahedron', 'hexahedron', etc.).
        name: Standard English name ('Tetrahedron', 'Hexahedron', etc.).
        latin_name: Classical Latin name from Pacioli, Kepler, and Renaissance texts.
        greek_name: Ancient Greek name with polytonic Greek orthography.
        element: Classical natural element assigned in Plato's Timaeus.
        schlafli: Schläfli symbol {p, q} indicating p-gons with q meeting per vertex.
        dual_slug: Slug of the polar dual regular solid.
        euclid_prop: Proposition in Euclid's Elements Book XIII constructing the solid.
        g_index: GEOMETOR G-Index citation in elements canon.
        leonardo_plates: Mapping of variant keys to (plate_roman, folio_number) pairs.
        vertices: Tuple of exact 3D vertex coordinates over Z or Q(phi).
        faces: Tuple of oriented planar faces (vertex index cycles CCW outward).
        edges: Tuple of undirected edge pairs (i, j) with i < j.
        dihedral_spread: Exact rational dihedral spread sin^2(theta).
        q_in_over_q_out: Exact ratio of inquadrance to circumquadrance Q_in / Q_out.
        q_mid_over_q_out: Exact ratio of midquadrance to circumquadrance Q_mid / Q_out.
    """

    slug: str
    name: str
    latin_name: str
    greek_name: str
    element: str
    schlafli: tuple[int, int]
    dual_slug: str
    euclid_prop: str
    g_index: str
    leonardo_plates: dict[str, tuple[str, str]]
    vertices: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...]
    faces: tuple[tuple[int, ...], ...]
    edges: tuple[tuple[int, int], ...]
    dihedral_spread: sp.Rational
    q_in_over_q_out: sp.Expr
    q_mid_over_q_out: sp.Expr


def dot_3d(
    u: tuple[sp.Expr, sp.Expr, sp.Expr],
    v: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> sp.Expr:
    """Computes the exact dot product of two 3D vectors.

    Args:
        u: First 3D vector.
        v: Second 3D vector.

    Returns:
        Exact symbolic dot product u_x * v_x + u_y * v_y + u_z * v_z.
    """
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross_3d(
    u: tuple[sp.Expr, sp.Expr, sp.Expr],
    v: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Computes the exact cross product of two 3D vectors.

    Args:
        u: First 3D vector.
        v: Second 3D vector.

    Returns:
        Exact 3D vector u x v.
    """
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def quadrance_3d(v: tuple[sp.Expr, sp.Expr, sp.Expr]) -> sp.Expr:
    """Computes the exact 3D quadrance (squared Euclidean norm) of a vector.

    Args:
        v: 3D vector coordinates (x, y, z).

    Returns:
        Exact symbolic quadrance v_x^2 + v_y^2 + v_z^2.
    """
    return dot_3d(v, v)


def face_normal_3d(
    vertices: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...],
    face: tuple[int, ...],
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Computes the unnormalized outward normal vector of a planar face.

    Args:
        vertices: Sequence of 3D vertex coordinates.
        face: Sequence of vertex indices ordered counter-clockwise outward.

    Returns:
        Exact 3D normal vector via cross product of first two directed edges.
    """
    v0 = vertices[face[0]]
    v1 = vertices[face[1]]
    v2 = vertices[face[2]]
    d1 = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
    d2 = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
    return cross_3d(d1, d2)


def dihedral_spread_3d(
    n1: tuple[sp.Expr, sp.Expr, sp.Expr],
    n2: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> sp.Expr:
    """Computes the exact dihedral spread (sin^2 theta) between two face normals.

    In Rational Trigonometry, the spread between two planes with normal
    vectors n1 and n2 is 1 - (n1 . n2)^2 / (Q(n1) * Q(n2)).

    Args:
        n1: First face normal vector.
        n2: Second face normal vector.

    Returns:
        Exact rational or algebraic dihedral spread in [0, 1].
    """
    dot = dot_3d(n1, n2)
    q1 = quadrance_3d(n1)
    q2 = quadrance_3d(n2)
    return sp.simplify(sp.Integer(1) - (dot**2) / (q1 * q2))


def _make_tetrahedron() -> RegularSolid:
    """Constructs the exact symbolic Tetrahedron."""
    vertices: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...] = (
        (sp.Integer(1), sp.Integer(1), sp.Integer(1)),
        (sp.Integer(1), sp.Integer(-1), sp.Integer(-1)),
        (sp.Integer(-1), sp.Integer(1), sp.Integer(-1)),
        (sp.Integer(-1), sp.Integer(-1), sp.Integer(1)),
    )
    faces: tuple[tuple[int, ...], ...] = (
        (0, 1, 2),
        (0, 3, 1),
        (0, 2, 3),
        (1, 3, 2),
    )
    edges: tuple[tuple[int, int], ...] = (
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    )
    plates: dict[str, tuple[str, str]] = {
        "solidum": ("I", "0187"),
        "vacuum": ("II", "0189"),
        "abscisum_solidum": ("III", "0191"),
        "abscisum_vacuum": ("IIII", "0193"),
        "elevatum_solidum": ("V", "0195"),
        "elevatum_vacuum": ("VI", "0197"),
    }
    return RegularSolid(
        slug="tetrahedron",
        name="Tetrahedron",
        latin_name="Tetrahedron",
        greek_name="Τετράεδρον",
        element="Fire",
        schlafli=(3, 3),
        dual_slug="tetrahedron",
        euclid_prop="XIII.13",
        g_index="G.592",
        leonardo_plates=plates,
        vertices=vertices,
        faces=faces,
        edges=edges,
        dihedral_spread=sp.Rational(8, 9),
        q_in_over_q_out=sp.Rational(1, 9),
        q_mid_over_q_out=sp.Rational(1, 3),
    )


def _make_hexahedron() -> RegularSolid:
    """Constructs the exact symbolic Hexahedron (Cube)."""
    vertices: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...] = (
        (sp.Integer(1), sp.Integer(1), sp.Integer(1)),
        (sp.Integer(1), sp.Integer(1), sp.Integer(-1)),
        (sp.Integer(1), sp.Integer(-1), sp.Integer(1)),
        (sp.Integer(1), sp.Integer(-1), sp.Integer(-1)),
        (sp.Integer(-1), sp.Integer(1), sp.Integer(1)),
        (sp.Integer(-1), sp.Integer(1), sp.Integer(-1)),
        (sp.Integer(-1), sp.Integer(-1), sp.Integer(1)),
        (sp.Integer(-1), sp.Integer(-1), sp.Integer(-1)),
    )
    faces: tuple[tuple[int, ...], ...] = (
        (0, 2, 3, 1),
        (4, 5, 7, 6),
        (0, 1, 5, 4),
        (2, 6, 7, 3),
        (0, 4, 6, 2),
        (1, 3, 7, 5),
    )
    edges: tuple[tuple[int, int], ...] = (
        (0, 1),
        (0, 2),
        (0, 4),
        (1, 3),
        (1, 5),
        (2, 3),
        (2, 6),
        (3, 7),
        (4, 5),
        (4, 6),
        (5, 7),
        (6, 7),
    )
    plates: dict[str, tuple[str, str]] = {
        "solidum": ("VII", "0199"),
        "vacuum": ("VIII", "0201"),
        "abscisum_solidum": ("VIIII", "0203"),
        "abscisum_vacuum": ("X", "0205"),
        "elevatum_solidum": ("XI", "0207"),
        "elevatum_vacuum": ("XII", "0209"),
        "abscisum_elevatum_solidum": ("XIII", "0211"),
        "abscisum_elevatum_vacuum": ("XIIII", "0217"),
    }
    return RegularSolid(
        slug="hexahedron",
        name="Hexahedron",
        latin_name="Exahedron sive Cubus",
        greek_name="Ἑξάεδρον",
        element="Earth",
        schlafli=(4, 3),
        dual_slug="octahedron",
        euclid_prop="XIII.15",
        g_index="G.595",
        leonardo_plates=plates,
        vertices=vertices,
        faces=faces,
        edges=edges,
        dihedral_spread=sp.Rational(1, 1),
        q_in_over_q_out=sp.Rational(1, 3),
        q_mid_over_q_out=sp.Rational(2, 3),
    )


def _make_octahedron() -> RegularSolid:
    """Constructs the exact symbolic Octahedron."""
    vertices: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...] = (
        (sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        (sp.Integer(-1), sp.Integer(0), sp.Integer(0)),
        (sp.Integer(0), sp.Integer(1), sp.Integer(0)),
        (sp.Integer(0), sp.Integer(-1), sp.Integer(0)),
        (sp.Integer(0), sp.Integer(0), sp.Integer(1)),
        (sp.Integer(0), sp.Integer(0), sp.Integer(-1)),
    )
    faces: tuple[tuple[int, ...], ...] = (
        (0, 2, 4),
        (0, 4, 3),
        (0, 3, 5),
        (0, 5, 2),
        (1, 4, 2),
        (1, 3, 4),
        (1, 5, 3),
        (1, 2, 5),
    )
    edges: tuple[tuple[int, int], ...] = (
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 4),
        (2, 5),
        (3, 4),
        (3, 5),
    )
    plates: dict[str, tuple[str, str]] = {
        "solidum": ("XV", "0219"),
        "vacuum": ("XVI", "0221"),
        "abscisum_solidum": ("XVII", "0223"),
        "abscisum_vacuum": ("XVIII", "0225"),
        "elevatum_solidum": ("XIX", "0227"),
        "elevatum_vacuum": ("XX", "0229"),
    }
    return RegularSolid(
        slug="octahedron",
        name="Octahedron",
        latin_name="Octahedron",
        greek_name="Ὀκτάεδρον",
        element="Air",
        schlafli=(3, 4),
        dual_slug="hexahedron",
        euclid_prop="XIII.14",
        g_index="G.594",
        leonardo_plates=plates,
        vertices=vertices,
        faces=faces,
        edges=edges,
        dihedral_spread=sp.Rational(8, 9),
        q_in_over_q_out=sp.Rational(1, 3),
        q_mid_over_q_out=sp.Rational(1, 2),
    )


def _make_icosahedron() -> RegularSolid:
    """Constructs the exact symbolic Icosahedron."""
    vertices: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...] = (
        (sp.Integer(0), sp.Integer(1), PHI),
        (sp.Integer(0), sp.Integer(1), -PHI),
        (sp.Integer(0), sp.Integer(-1), PHI),
        (sp.Integer(0), sp.Integer(-1), -PHI),
        (sp.Integer(1), PHI, sp.Integer(0)),
        (sp.Integer(1), -PHI, sp.Integer(0)),
        (sp.Integer(-1), PHI, sp.Integer(0)),
        (sp.Integer(-1), -PHI, sp.Integer(0)),
        (PHI, sp.Integer(0), sp.Integer(1)),
        (PHI, sp.Integer(0), sp.Integer(-1)),
        (-PHI, sp.Integer(0), sp.Integer(1)),
        (-PHI, sp.Integer(0), sp.Integer(-1)),
    )
    faces: tuple[tuple[int, ...], ...] = (
        (0, 2, 8),
        (0, 10, 2),
        (0, 4, 6),
        (0, 8, 4),
        (0, 6, 10),
        (1, 9, 3),
        (1, 3, 11),
        (1, 6, 4),
        (1, 4, 9),
        (1, 11, 6),
        (2, 7, 5),
        (2, 5, 8),
        (2, 10, 7),
        (3, 5, 7),
        (3, 9, 5),
        (3, 7, 11),
        (4, 8, 9),
        (5, 9, 8),
        (6, 11, 10),
        (7, 10, 11),
    )
    edges: tuple[tuple[int, int], ...] = (
        (0, 2),
        (0, 4),
        (0, 6),
        (0, 8),
        (0, 10),
        (1, 3),
        (1, 4),
        (1, 6),
        (1, 9),
        (1, 11),
        (2, 5),
        (2, 7),
        (2, 8),
        (2, 10),
        (3, 5),
        (3, 7),
        (3, 9),
        (3, 11),
        (4, 6),
        (4, 8),
        (4, 9),
        (5, 7),
        (5, 8),
        (5, 9),
        (6, 10),
        (6, 11),
        (7, 10),
        (7, 11),
        (8, 9),
        (10, 11),
    )
    plates: dict[str, tuple[str, str]] = {
        "solidum": ("XXI", "0231"),
        "vacuum": ("XXII", "0233"),
        "abscisum_solidum": ("XXIII", "0235"),
        "abscisum_vacuum": ("XXIIII", "0237"),
        "elevatum_solidum": ("XXV", "0239"),
        "elevatum_vacuum": ("XXVI", "0241"),
    }
    return RegularSolid(
        slug="icosahedron",
        name="Icosahedron",
        latin_name="Icosahedron",
        greek_name="Εἰκοσάεδρον",
        element="Water",
        schlafli=(3, 5),
        dual_slug="dodecahedron",
        euclid_prop="XIII.16",
        g_index="G.597",
        leonardo_plates=plates,
        vertices=vertices,
        faces=faces,
        edges=edges,
        dihedral_spread=sp.Rational(4, 9),
        q_in_over_q_out=(sp.Integer(4) * PHI + sp.Integer(3)) / sp.Integer(15),
        q_mid_over_q_out=(PHI + sp.Integer(2)) / sp.Integer(5),
    )


def _make_dodecahedron() -> RegularSolid:
    """Constructs the exact symbolic Dodecahedron."""
    vertices: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...] = (
        (sp.Integer(1), sp.Integer(1), sp.Integer(1)),
        (sp.Integer(1), sp.Integer(1), sp.Integer(-1)),
        (sp.Integer(1), sp.Integer(-1), sp.Integer(1)),
        (sp.Integer(1), sp.Integer(-1), sp.Integer(-1)),
        (sp.Integer(-1), sp.Integer(1), sp.Integer(1)),
        (sp.Integer(-1), sp.Integer(1), sp.Integer(-1)),
        (sp.Integer(-1), sp.Integer(-1), sp.Integer(1)),
        (sp.Integer(-1), sp.Integer(-1), sp.Integer(-1)),
        (sp.Integer(0), PHI_INV, PHI),
        (sp.Integer(0), PHI_INV, -PHI),
        (sp.Integer(0), -PHI_INV, PHI),
        (sp.Integer(0), -PHI_INV, -PHI),
        (PHI_INV, PHI, sp.Integer(0)),
        (PHI_INV, -PHI, sp.Integer(0)),
        (-PHI_INV, PHI, sp.Integer(0)),
        (-PHI_INV, -PHI, sp.Integer(0)),
        (PHI, sp.Integer(0), PHI_INV),
        (PHI, sp.Integer(0), -PHI_INV),
        (-PHI, sp.Integer(0), PHI_INV),
        (-PHI, sp.Integer(0), -PHI_INV),
    )
    faces: tuple[tuple[int, ...], ...] = (
        (0, 12, 14, 4, 8),
        (0, 8, 10, 2, 16),
        (0, 16, 17, 1, 12),
        (1, 9, 5, 14, 12),
        (1, 17, 3, 11, 9),
        (2, 10, 6, 15, 13),
        (2, 13, 3, 17, 16),
        (3, 13, 15, 7, 11),
        (4, 18, 6, 10, 8),
        (4, 14, 5, 19, 18),
        (5, 9, 11, 7, 19),
        (6, 18, 19, 7, 15),
    )
    edges: tuple[tuple[int, int], ...] = (
        (0, 8),
        (0, 12),
        (0, 16),
        (1, 9),
        (1, 12),
        (1, 17),
        (2, 10),
        (2, 13),
        (2, 16),
        (3, 11),
        (3, 13),
        (3, 17),
        (4, 8),
        (4, 14),
        (4, 18),
        (5, 9),
        (5, 14),
        (5, 19),
        (6, 10),
        (6, 15),
        (6, 18),
        (7, 11),
        (7, 15),
        (7, 19),
        (8, 10),
        (9, 11),
        (12, 14),
        (13, 15),
        (16, 17),
        (18, 19),
    )
    plates: dict[str, tuple[str, str]] = {
        "solidum": ("XXVII", "0243"),
        "vacuum": ("XXVIII", "0245"),
        "abscisum_solidum": ("XXIX", "0247"),
        "abscisum_vacuum": ("XXX", "0249"),
        "elevatum_solidum": ("XXXI", "0251"),
        "elevatum_vacuum": ("XXXII", "0253"),
        "abscisum_elevatum_solidum": ("XXXIII", "0255"),
        "abscisum_elevatum_vacuum": ("XXXIIII", "0257"),
    }
    return RegularSolid(
        slug="dodecahedron",
        name="Dodecahedron",
        latin_name="Dodecahedron",
        greek_name="Δωδεκάεδρον",
        element="Aether",
        schlafli=(5, 3),
        dual_slug="icosahedron",
        euclid_prop="XIII.17",
        g_index="G.600",
        leonardo_plates=plates,
        vertices=vertices,
        faces=faces,
        edges=edges,
        dihedral_spread=sp.Rational(4, 5),
        q_in_over_q_out=(sp.Integer(4) * PHI + sp.Integer(3)) / sp.Integer(15),
        q_mid_over_q_out=(PHI + sp.Integer(1)) / sp.Integer(3),
    )


def get_platonic_solids() -> dict[str, RegularSolid]:
    """Retrieves all five Platonic solids mapped by slug.

    Returns:
        Dictionary mapping slug names ('tetrahedron', 'hexahedron',
        'octahedron', 'icosahedron', 'dodecahedron') to their exact
        symbolic RegularSolid instances.
    """
    return {
        "tetrahedron": _make_tetrahedron(),
        "hexahedron": _make_hexahedron(),
        "octahedron": _make_octahedron(),
        "icosahedron": _make_icosahedron(),
        "dodecahedron": _make_dodecahedron(),
    }


def get_platonic_solid(slug: str) -> RegularSolid:
    """Retrieves a single Platonic solid by slug name.

    Args:
        slug: Standard slug identifier ('tetrahedron', 'hexahedron', etc.).

    Returns:
        The corresponding RegularSolid instance.

    Raises:
        KeyError: If slug is not recognized.
    """
    solids = get_platonic_solids()
    if slug not in solids:
        raise KeyError(
            f"Unknown Platonic solid slug: {slug!r}. Available: {list(solids.keys())}"
        )
    return solids[slug]
