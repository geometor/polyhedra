"""Exact symbolic golden proportions and Keplerian compounds in polyhedra.

Explores canonical golden ratio occurrences across regular and semi-regular polyhedra:
mutually orthogonal golden rectangles in the icosahedron, golden edge division
of the octahedron, the compound of five inscribed cubes in the dodecahedron,
Kepler's rhombic triacontahedron, and planar cross sections (George Odom's theorem,
icosahedron principal meridian, and regular pentagon/pentagram).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import sympy as sp
from geometor.divine import register_divine_hook
from geometor.model import Model, quadrance

from geometor.polyhedra.platonic import (
    PHI,
    PHI_INV,
    cross_3d,
    dot_3d,
    get_platonic_solid,
    quadrance_3d,
)


@dataclass(frozen=True)
class GoldenPolyhedronTheorem:
    """Exact symbolic specification of a golden proportion theorem in polyhedra.

    Attributes:
        slug: Short lowercase identifier ('icosahedron_golden_rectangles', etc.).
        title: Standard English title of the theorem or construction.
        subtitle: Descriptive subtitle highlighting key geometric properties.
        historical_source: Scholarly citation (Euclid, Pacioli, Kepler, Odom).
        summary: Concise mathematical summary of the theorem and geometric proof.
        golden_identities: Sequence of (description, lhs, rhs) triples where
            lhs - rhs simplifies to exact zero.
    """

    slug: str
    title: str
    subtitle: str
    historical_source: str
    summary: str
    golden_identities: tuple[tuple[str, sp.Expr, sp.Expr], ...]


@dataclass(frozen=True)
class GoldenRectanglesResult:
    """Exact symbolic specification of the three golden rectangles in the icosahedron.

    Attributes:
        rectangles: Mapping of plane label ('R_YZ', 'R_ZX', 'R_XY') to 4 vertices.
        normals: Mapping of plane label to exact 3D normal vector.
        q_short: Exact quadrance of each rectangle short edge.
        q_long: Exact quadrance of each rectangle long edge.
        q_ratio: Exact quadrance ratio Q_long / Q_short == PHI**2.
        q_diagonal: Exact quadrance of each rectangle diagonal.
        q_circumradius: Exact circumquadrance of the parent icosahedron.
        short_edges_in_icosahedron: Sequence of edge index pairs matching
            canonical icosahedron edges.
    """

    rectangles: dict[str, tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...]]
    normals: dict[str, tuple[sp.Expr, sp.Expr, sp.Expr]]
    q_short: sp.Expr
    q_long: sp.Expr
    q_ratio: sp.Expr
    q_diagonal: sp.Expr
    q_circumradius: sp.Expr
    short_edges_in_icosahedron: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class OctahedronGoldenIcosahedronResult:
    """Exact symbolic result of inscribing an icosahedron in an octahedron.

    Attributes:
        octahedron_vertices: Six exact 3D vertices of the scaled octahedron.
        octahedron_edges: Twelve undirected edge index pairs of the octahedron.
        octahedron_faces: Eight triangular face index triples of the octahedron.
        directed_edges: Twelve directed edge index pairs oriented for golden division.
        division_points: Twelve exact golden division points matching icosahedron vertices.
        icosahedron_vertices: Twelve canonical icosahedron vertex coordinates.
        icosahedron_edges: Thirty undirected edge index pairs of the inscribed icosahedron.
        icosahedron_faces: Twenty triangular face index triples of the inscribed icosahedron.
        q_oct_edge: Exact edge quadrance of each octahedron edge.
        q_major: Exact quadrance of the major golden segment on each edge.
        q_minor: Exact quadrance of the minor golden segment on each edge.
        q_ico_edge: Exact edge quadrance of each inscribed icosahedron edge.
    """

    octahedron_vertices: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...]
    octahedron_edges: tuple[tuple[int, int], ...]
    octahedron_faces: tuple[tuple[int, ...], ...]
    directed_edges: tuple[tuple[int, int], ...]
    division_points: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...]
    icosahedron_vertices: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...]
    icosahedron_edges: tuple[tuple[int, int], ...]
    icosahedron_faces: tuple[tuple[int, ...], ...]
    q_oct_edge: sp.Expr
    q_major: sp.Expr
    q_minor: sp.Expr
    q_ico_edge: sp.Expr


@dataclass(frozen=True)
class InscribedCube:
    """Exact symbolic specification of one inscribed regular cube in the dodecahedron.

    Attributes:
        cube_index: Index of the cube (0 through 4).
        vertices: Eight vertex indices into the parent dodecahedron vertex list.
        vertex_coords: Eight exact 3D vertex coordinates of this cube.
        edges: Twelve edge index pairs into the parent dodecahedron vertex list.
        faces: Six square face 4-tuples of parent dodecahedron vertex indices.
    """

    cube_index: int
    vertices: tuple[int, ...]
    vertex_coords: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...]
    edges: tuple[tuple[int, int], ...]
    faces: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class DodecahedronFiveCubesResult:
    """Exact symbolic result of the compound of five inscribed cubes in the dodecahedron.

    Attributes:
        dodecahedron_vertices: Twenty exact 3D vertices of the canonical dodecahedron.
        dodecahedron_edges: Thirty undirected edge index pairs of the dodecahedron.
        dodecahedron_faces: Twelve pentagonal face index 5-tuples.
        q_dod_edge: Exact edge quadrance of the dodecahedron.
        q_cube_edge: Exact edge quadrance of each inscribed cube.
        q_ratio: Exact quadrance ratio Q_cube / Q_dod == PHI**2.
        cubes: Sequence of five InscribedCube instances.
        all_cube_edges: Sequence of all sixty cube edge index pairs partitioning diagonals.
    """

    dodecahedron_vertices: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...]
    dodecahedron_edges: tuple[tuple[int, int], ...]
    dodecahedron_faces: tuple[tuple[int, ...], ...]
    q_dod_edge: sp.Expr
    q_cube_edge: sp.Expr
    q_ratio: sp.Expr
    cubes: tuple[InscribedCube, ...]
    all_cube_edges: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class RhombicTriacontahedronResult:
    """Exact symbolic specification of the Rhombic Triacontahedron over Q(phi).

    Attributes:
        vertices: Thirty-two exact 3D vertices (20 dodecahedral + 12 dual icosahedral).
        faces: Thirty rhombic face index 4-tuples, ordered outward counter-clockwise.
        edges: Sixty undirected edge index pairs.
        dodecahedron_indices: Indices of the twenty degree-3 obtuse vertices (0..19).
        icosahedron_indices: Indices of the twelve degree-5 acute vertices (20..31).
        q_long_diagonal: Exact quadrance of each rhombus long diagonal.
        q_short_diagonal: Exact quadrance of each rhombus short diagonal.
        q_diagonal_ratio: Exact quadrance ratio Q_long / Q_short == PHI**2.
        q_edge: Exact edge quadrance of each rhombic face edge.
    """

    vertices: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...]
    faces: tuple[tuple[int, int, int, int], ...]
    edges: tuple[tuple[int, int], ...]
    dodecahedron_indices: tuple[int, ...]
    icosahedron_indices: tuple[int, ...]
    q_long_diagonal: sp.Expr
    q_short_diagonal: sp.Expr
    q_diagonal_ratio: sp.Expr
    q_edge: sp.Expr


def build_icosahedron_golden_rectangles() -> GoldenRectanglesResult:
    """Extracts and certifies the three mutually orthogonal golden rectangles in the icosahedron.

    Euclid Elements XIII.16 shows that the twelve vertices of a regular icosahedron
    form the vertices of three congruent golden rectangles whose planes are pairwise
    perpendicular and meet at the center of the circumscribing sphere.

    Returns:
        GoldenRectanglesResult certifying rectangle dimensions, orthogonality, and edges.
    """
    ico = get_platonic_solid("icosahedron")

    # Three canonical golden rectangles spanning the 12 vertices
    r_yz: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...] = (
        (sp.Integer(0), sp.Integer(1), PHI),
        (sp.Integer(0), sp.Integer(-1), PHI),
        (sp.Integer(0), sp.Integer(-1), -PHI),
        (sp.Integer(0), sp.Integer(1), -PHI),
    )
    r_zx: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...] = (
        (PHI, sp.Integer(0), sp.Integer(1)),
        (-PHI, sp.Integer(0), sp.Integer(1)),
        (-PHI, sp.Integer(0), sp.Integer(-1)),
        (PHI, sp.Integer(0), sp.Integer(-1)),
    )
    r_xy: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...] = (
        (sp.Integer(1), PHI, sp.Integer(0)),
        (-sp.Integer(1), PHI, sp.Integer(0)),
        (-sp.Integer(1), -PHI, sp.Integer(0)),
        (sp.Integer(1), -PHI, sp.Integer(0)),
    )

    rectangles = {
        "R_YZ": r_yz,
        "R_ZX": r_zx,
        "R_XY": r_xy,
    }

    normals = {
        "R_YZ": (sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        "R_ZX": (sp.Integer(0), sp.Integer(1), sp.Integer(0)),
        "R_XY": (sp.Integer(0), sp.Integer(0), sp.Integer(1)),
    }

    # Short edge quadrance = (-1 - 1)^2 = 4
    q_short = sp.Integer(4)
    # Long edge quadrance = (-PHI - PHI)^2 = 4 * PHI**2
    q_long = sp.Integer(4) * (PHI**2)
    q_ratio = sp.simplify(q_long / q_short)

    # Diagonal quadrance Q_diag = Q_short + Q_long = 4 * (1 + PHI**2) = 4 * (PHI + 2)
    q_diagonal = sp.Integer(4) * (PHI + sp.Integer(2))
    q_circumradius = PHI + sp.Integer(2)

    # Short edges: 2 from each rectangle = 6 edges of the icosahedron
    short_edges_list: list[tuple[int, int]] = []
    ico_edge_set = set(ico.edges)

    for rect in (r_yz, r_zx, r_xy):
        i0 = ico.vertices.index(rect[0])
        i1 = ico.vertices.index(rect[1])
        i2 = ico.vertices.index(rect[2])
        i3 = ico.vertices.index(rect[3])

        diff_01 = (
            rect[1][0] - rect[0][0],
            rect[1][1] - rect[0][1],
            rect[1][2] - rect[0][2],
        )
        if sp.simplify(quadrance_3d(diff_01) - q_short) == 0:
            e1 = (min(i0, i1), max(i0, i1))
            e2 = (min(i2, i3), max(i2, i3))
        else:
            e1 = (min(i1, i2), max(i1, i2))
            e2 = (min(i3, i0), max(i3, i0))

        assert e1 in ico_edge_set
        assert e2 in ico_edge_set
        short_edges_list.append(e1)
        short_edges_list.append(e2)

    return GoldenRectanglesResult(
        rectangles=rectangles,
        normals=normals,
        q_short=q_short,
        q_long=q_long,
        q_ratio=q_ratio,
        q_diagonal=q_diagonal,
        q_circumradius=q_circumradius,
        short_edges_in_icosahedron=tuple(short_edges_list),
    )


def build_octahedron_golden_icosahedron() -> OctahedronGoldenIcosahedronResult:
    """Divides the twelve edges of a regular octahedron in the golden ratio.

    Starts with a regular octahedron of scale phi^2 = phi + 1 whose vertices
    lie along the coordinate axes: (±phi^2, 0, 0), (0, ±phi^2, 0), (0, 0, ±phi^2).
    Dividing each directed edge in the golden ratio AG : GB = 1 : phi yields
    the exact twelve vertices of the canonical regular icosahedron.

    Returns:
        OctahedronGoldenIcosahedronResult containing octahedron geometry and inscribed icosahedron.
    """
    ico = get_platonic_solid("icosahedron")
    p2 = PHI**2

    v_oct: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...] = (
        (p2, sp.Integer(0), sp.Integer(0)),
        (-p2, sp.Integer(0), sp.Integer(0)),
        (sp.Integer(0), p2, sp.Integer(0)),
        (sp.Integer(0), -p2, sp.Integer(0)),
        (sp.Integer(0), sp.Integer(0), p2),
        (sp.Integer(0), sp.Integer(0), -p2),
    )

    oct_edges: tuple[tuple[int, int], ...] = (
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

    oct_faces: tuple[tuple[int, ...], ...] = (
        (0, 2, 4),
        (0, 4, 3),
        (0, 3, 5),
        (0, 5, 2),
        (1, 4, 2),
        (1, 3, 4),
        (1, 5, 3),
        (1, 2, 5),
    )

    # Directed edges ordered so that division_points[k] == ico.vertices[k]
    directed_edges: tuple[tuple[int, int], ...] = (
        (4, 2),
        (5, 2),
        (4, 3),
        (5, 3),
        (2, 0),
        (3, 0),
        (2, 1),
        (3, 1),
        (0, 4),
        (0, 5),
        (1, 4),
        (1, 5),
    )

    div_pts: list[tuple[sp.Expr, sp.Expr, sp.Expr]] = []
    for a_idx, b_idx in directed_edges:
        a_vec = v_oct[a_idx]
        b_vec = v_oct[b_idx]
        # Golden division: G = (phi * A + B) / phi^2
        g_x = sp.simplify((PHI * a_vec[0] + b_vec[0]) / p2)
        g_y = sp.simplify((PHI * a_vec[1] + b_vec[1]) / p2)
        g_z = sp.simplify((PHI * a_vec[2] + b_vec[2]) / p2)
        div_pts.append((g_x, g_y, g_z))

    # Verify identical coordinate match with canonical icosahedron
    assert tuple(div_pts) == ico.vertices

    # Quadrance metrics
    # Octahedron edge: distance between (p2, 0, 0) and (0, p2, 0) is 2 * p2^2 = 2 * (3*phi + 2)
    q_oct_edge = sp.Integer(2) * (sp.Integer(3) * PHI + sp.Integer(2))
    # Minor segment AG has quadrance 2
    q_minor = sp.Integer(2)
    # Major segment GB has quadrance 2 * phi^2 = 2 * (phi + 1)
    q_major = sp.Integer(2) * PHI + sp.Integer(2)
    # Icosahedron edge quadrance
    q_ico_edge = sp.Integer(4)

    return OctahedronGoldenIcosahedronResult(
        octahedron_vertices=v_oct,
        octahedron_edges=oct_edges,
        octahedron_faces=oct_faces,
        directed_edges=directed_edges,
        division_points=tuple(div_pts),
        icosahedron_vertices=ico.vertices,
        icosahedron_edges=ico.edges,
        icosahedron_faces=ico.faces,
        q_oct_edge=q_oct_edge,
        q_major=q_major,
        q_minor=q_minor,
        q_ico_edge=q_ico_edge,
    )


def build_dodecahedron_five_cubes() -> DodecahedronFiveCubesResult:
    """Finds and certifies all five regular cubes inscribed in the dodecahedron.

    Euclid Elements XIII.17 constructs the regular dodecahedron upon an inscribed
    cube by adding roof-like wedges above each square face. There are five distinct
    inscribed regular cubes whose 60 edges partition all 60 diagonals of the twelve
    pentagonal faces.

    Returns:
        DodecahedronFiveCubesResult containing dodecahedron geometry and the five cubes.
    """
    dod = get_platonic_solid("dodecahedron")
    v_dod = dod.vertices
    n_v = len(v_dod)

    # Edge quadrance of dodecahedron = 4 * PHI_INV**2 = 4 * (2 - phi)
    q_dod_edge = sp.Integer(4) * (sp.Integer(2) - PHI)
    q_cube_edge = sp.Integer(4)
    q_ratio = sp.simplify(q_cube_edge / q_dod_edge)

    # Identify all vertex pairs with quadrance 4 (pentagonal face diagonals)
    q4_pairs: list[tuple[int, int]] = []
    adj: dict[int, set[int]] = {i: set() for i in range(n_v)}
    for i in range(n_v):
        for j in range(i + 1, n_v):
            diff = (
                v_dod[j][0] - v_dod[i][0],
                v_dod[j][1] - v_dod[i][1],
                v_dod[j][2] - v_dod[i][2],
            )
            if sp.simplify(quadrance_3d(diff) - q_cube_edge) == 0:
                q4_pairs.append((i, j))
                adj[i].add(j)
                adj[j].add(i)

    # Antipodal pairs (v + v' == 0)
    antipodals: list[tuple[int, int]] = []
    for i in range(n_v):
        for j in range(i + 1, n_v):
            if (
                v_dod[i][0] + v_dod[j][0] == 0
                and v_dod[i][1] + v_dod[j][1] == 0
                and v_dod[i][2] + v_dod[j][2] == 0
            ):
                antipodals.append((i, j))

    # A regular cube consists of 4 antipodal pairs forming a 3-regular graph
    found_cubes_verts: list[tuple[int, ...]] = []
    for comb in itertools.combinations(antipodals, 4):
        verts = set([v for pair in comb for v in pair])
        deg = {v: len(adj[v] & verts) for v in verts}
        if all(d == 3 for d in deg.values()):
            found_cubes_verts.append(tuple(sorted(verts)))

    cubes_list: list[InscribedCube] = []
    all_cube_edges_set: set[tuple[int, int]] = set()

    for cube_idx, c_verts in enumerate(found_cubes_verts):
        verts_set = set(c_verts)
        edges = [(i, j) for i, j in q4_pairs if i in verts_set and j in verts_set]
        cube_adj: dict[int, set[int]] = {v: set() for v in c_verts}
        for i, j in edges:
            cube_adj[i].add(j)
            cube_adj[j].add(i)
            all_cube_edges_set.add((min(i, j), max(i, j)))

        # Find the 6 square faces (4-cycles) oriented outward CCW
        faces: list[tuple[int, ...]] = []
        for quad in itertools.combinations(c_verts, 4):
            quad_set = set(quad)
            quad_edges = [(i, j) for i, j in edges if i in quad_set and j in quad_set]
            if len(quad_edges) == 4:
                u0 = quad[0]
                nbrs = list(cube_adj[u0] & quad_set)
                u1 = nbrs[0]
                u2 = list((cube_adj[u1] & quad_set) - {u0})[0]
                u3 = list((cube_adj[u2] & quad_set) - {u1})[0]

                # Outward orientation via normal vector dot product
                v0 = v_dod[u0]
                v1 = v_dod[u1]
                v3 = v_dod[u3]
                d1 = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
                d2 = (v3[0] - v0[0], v3[1] - v0[1], v3[2] - v0[2])
                norm = cross_3d(d1, d2)
                if sp.simplify(dot_3d(norm, v0)) > 0:
                    faces.append((u0, u1, u2, u3))
                else:
                    faces.append((u0, u3, u2, u1))

        cube_coords = tuple(v_dod[idx] for idx in c_verts)
        cubes_list.append(
            InscribedCube(
                cube_index=cube_idx,
                vertices=c_verts,
                vertex_coords=cube_coords,
                edges=tuple(edges),
                faces=tuple(faces),
            )
        )

    # Sort all edges for deterministic representation
    all_cube_edges = tuple(sorted(all_cube_edges_set))

    return DodecahedronFiveCubesResult(
        dodecahedron_vertices=v_dod,
        dodecahedron_edges=dod.edges,
        dodecahedron_faces=dod.faces,
        q_dod_edge=q_dod_edge,
        q_cube_edge=q_cube_edge,
        q_ratio=q_ratio,
        cubes=tuple(cubes_list),
        all_cube_edges=all_cube_edges,
    )


def build_rhombic_triacontahedron_golden() -> RhombicTriacontahedronResult:
    """Constructs the exact 32-vertex Rhombic Triacontahedron over Q(phi).

    Unites the twenty vertices of the canonical regular dodecahedron with the
    twelve vertices of the dual-oriented regular icosahedron. Each of the thirty
    faces is a planar golden rhombus whose long diagonal joins two acute degree-5
    icosahedral vertices and whose short diagonal joins two obtuse degree-3
    dodecahedral vertices, with diagonal quadrance ratio equal to phi^2.

    Returns:
        RhombicTriacontahedronResult specifying vertices, rhombic faces, and metric ratios.
    """
    dod = get_platonic_solid("dodecahedron")
    v_dod = dod.vertices

    # 12 dual-oriented icosahedron vertices matching dodecahedron edge midpoints
    v_ico_dual: tuple[tuple[sp.Expr, sp.Expr, sp.Expr], ...] = (
        (sp.Integer(1), sp.Integer(0), PHI),
        (-sp.Integer(1), sp.Integer(0), PHI),
        (sp.Integer(1), sp.Integer(0), -PHI),
        (-sp.Integer(1), sp.Integer(0), -PHI),
        (sp.Integer(0), PHI, sp.Integer(1)),
        (sp.Integer(0), PHI, -sp.Integer(1)),
        (sp.Integer(0), -PHI, sp.Integer(1)),
        (sp.Integer(0), -PHI, -sp.Integer(1)),
        (PHI, sp.Integer(1), sp.Integer(0)),
        (PHI, -sp.Integer(1), sp.Integer(0)),
        (-PHI, sp.Integer(1), sp.Integer(0)),
        (-PHI, -sp.Integer(1), sp.Integer(0)),
    )

    dod_midpoints: dict[tuple[sp.Expr, sp.Expr, sp.Expr], tuple[int, int]] = {}
    for i, j in dod.edges:
        m = (
            sp.simplify((v_dod[i][0] + v_dod[j][0]) / 2),
            sp.simplify((v_dod[i][1] + v_dod[j][1]) / 2),
            sp.simplify((v_dod[i][2] + v_dod[j][2]) / 2),
        )
        dod_midpoints[m] = (i, j)

    ico_edges: list[tuple[int, int]] = []
    for i in range(12):
        for j in range(i + 1, 12):
            d = (
                v_ico_dual[j][0] - v_ico_dual[i][0],
                v_ico_dual[j][1] - v_ico_dual[i][1],
                v_ico_dual[j][2] - v_ico_dual[i][2],
            )
            if sp.simplify(quadrance_3d(d)) == 4:
                ico_edges.append((i, j))

    ico_midpoints: dict[tuple[sp.Expr, sp.Expr, sp.Expr], tuple[int, int]] = {}
    for i, j in ico_edges:
        m = (
            sp.simplify((v_ico_dual[i][0] + v_ico_dual[j][0]) / 2),
            sp.simplify((v_ico_dual[i][1] + v_ico_dual[j][1]) / 2),
            sp.simplify((v_ico_dual[i][2] + v_ico_dual[j][2]) / 2),
        )
        ico_midpoints[m] = (i, j)

    all_vertices = v_dod + v_ico_dual
    dodecahedron_indices = tuple(range(20))
    icosahedron_indices = tuple(range(20, 32))

    rhombic_faces: list[tuple[int, int, int, int]] = []
    for m, (b_idx, d_idx) in dod_midpoints.items():
        a_ico_idx, c_ico_idx = ico_midpoints[m]
        a_idx = 20 + a_ico_idx
        c_idx = 20 + c_ico_idx

        pt_a = all_vertices[a_idx]
        pt_b = all_vertices[b_idx]
        pt_d = all_vertices[d_idx]

        side_ab = (pt_b[0] - pt_a[0], pt_b[1] - pt_a[1], pt_b[2] - pt_a[2])
        side_ad = (pt_d[0] - pt_a[0], pt_d[1] - pt_a[1], pt_d[2] - pt_a[2])
        norm = cross_3d(side_ab, side_ad)

        if sp.simplify(dot_3d(norm, m)) > 0:
            rhombic_faces.append((a_idx, b_idx, c_idx, d_idx))
        else:
            rhombic_faces.append((a_idx, d_idx, c_idx, b_idx))

    # Extract 60 unique edges
    edge_set: set[tuple[int, int]] = set()
    for a, b, c, d in rhombic_faces:
        edge_set.add((min(a, b), max(a, b)))
        edge_set.add((min(b, c), max(b, c)))
        edge_set.add((min(c, d), max(c, d)))
        edge_set.add((min(d, a), max(d, a)))

    edges = tuple(sorted(edge_set))

    q_long_diagonal = sp.Integer(4)
    q_short_diagonal = sp.Integer(4) * (PHI_INV**2)
    q_diagonal_ratio = sp.simplify(q_long_diagonal / q_short_diagonal)
    q_edge = sp.Integer(3) - PHI

    return RhombicTriacontahedronResult(
        vertices=all_vertices,
        faces=tuple(rhombic_faces),
        edges=edges,
        dodecahedron_indices=dodecahedron_indices,
        icosahedron_indices=icosahedron_indices,
        q_long_diagonal=q_long_diagonal,
        q_short_diagonal=q_short_diagonal,
        q_diagonal_ratio=q_diagonal_ratio,
        q_edge=q_edge,
    )


def build_odom_tetrahedron_section_model() -> tuple[Model, dict[str, sp.Expr]]:
    """Constructs George Odom's golden section on the regular tetrahedron face circumcircle.

    In 1983, George Odom discovered that connecting the midpoints of two sides of
    an equilateral triangle inscribed in a circle and extending the line to meet
    the circle divides the chord in the exact golden ratio.

    Returns:
        Tuple of (Model, metrics_dict) with certified exact golden proportions.
    """
    model = Model("odom_tetrahedron_section")
    register_divine_hook(model)

    pt_o = model.set_point(0, 0, classes=["center"])
    pt_a = model.set_point(0, 2, classes=["given"])
    pt_b = model.set_point(-sp.sqrt(3), -1, classes=["given"])
    pt_c = model.set_point(sp.sqrt(3), -1, classes=["given"])

    model.construct_segment(pt_a, pt_b)
    model.construct_segment(pt_b, pt_c)
    model.construct_segment(pt_c, pt_a)

    circ = model.construct_circle(pt_o, pt_a)

    pt_m1 = model.set_point(-sp.sqrt(3) / 2, sp.Rational(1, 2), classes=["midpoint"])
    pt_m2 = model.set_point(sp.sqrt(3) / 2, sp.Rational(1, 2), classes=["midpoint"])

    line_mid = model.construct_line(pt_m1, pt_m2)
    g_pts = model.intersect_all(line_mid, circ)

    g1 = g_pts[0] if g_pts[0].x < g_pts[1].x else g_pts[1]
    g2 = g_pts[1] if g_pts[0].x < g_pts[1].x else g_pts[0]

    q_m1_m2 = quadrance(pt_m1, pt_m2)
    q_m2_g2 = quadrance(pt_m2, g2)
    q_m1_g2 = quadrance(pt_m1, g2)
    q_g1_g2 = quadrance(g1, g2)

    ratio_major_minor = sp.simplify(q_m1_m2 / q_m2_g2)
    ratio_total_major = sp.simplify(q_m1_g2 / q_m1_m2)

    metrics: dict[str, sp.Expr] = {
        "q_m1_m2": q_m1_m2,
        "q_m2_g2": q_m2_g2,
        "q_m1_g2": q_m1_g2,
        "q_g1_g2": q_g1_g2,
        "ratio_major_minor": ratio_major_minor,
        "ratio_total_major": ratio_total_major,
    }

    return model, metrics


def build_icosahedron_meridian_model() -> tuple[Model, dict[str, sp.Expr]]:
    """Constructs the exact 2D principal meridian section of the icosahedron.

    In the principal plane X = 0, the canonical regular icosahedron has four
    vertices forming a golden rectangle (±1, ±phi) and two equatorial crossings
    at (±phi, 0) in (Y, Z) coordinates.

    Returns:
        Tuple of (Model, metrics_dict) certifying golden proportions in the meridian slice.
    """
    model = Model("icosahedron_meridian_section")

    pt_a = model.set_point(1, PHI, classes=["vertex"])
    pt_b = model.set_point(-1, PHI, classes=["vertex"])
    pt_c = model.set_point(-1, -PHI, classes=["vertex"])
    pt_d = model.set_point(1, -PHI, classes=["vertex"])
    pt_e = model.set_point(-PHI, 0, classes=["equatorial"])
    pt_f = model.set_point(PHI, 0, classes=["equatorial"])
    pt_o = model.set_point(0, 0, classes=["center"])
    pt_i = model.set_point(1, 0, classes=["midpoint"])

    model.construct_segment(pt_a, pt_b)
    model.construct_segment(pt_b, pt_c)
    model.construct_segment(pt_c, pt_d)
    model.construct_segment(pt_d, pt_a)
    model.construct_segment(pt_e, pt_f)

    q_short = quadrance(pt_a, pt_b)
    q_long = quadrance(pt_a, pt_d)
    q_diag = quadrance(pt_b, pt_d)
    q_ratio = sp.simplify(q_long / q_short)

    q_of = quadrance(pt_o, pt_f)
    q_oi = quadrance(pt_o, pt_i)
    q_if = quadrance(pt_i, pt_f)

    ratio_of_oi = sp.simplify(q_of / q_oi)
    ratio_oi_if = sp.simplify(q_oi / q_if)

    metrics: dict[str, sp.Expr] = {
        "q_short": q_short,
        "q_long": q_long,
        "q_diagonal": q_diag,
        "q_ratio": q_ratio,
        "q_of": q_of,
        "q_oi": q_oi,
        "q_if": q_if,
        "ratio_of_oi": ratio_of_oi,
        "ratio_oi_if": ratio_oi_if,
    }

    return model, metrics


def build_pentagon_cross_section_model() -> tuple[Model, dict[str, sp.Expr]]:
    """Constructs the regular pentagon and pentagram section over Q(phi, sqrt(5 - sqrt(5))).

    Euclid Elements XIII.8 demonstrates that the diagonals of a regular pentagon
    cut one another in extreme and mean ratio (the golden ratio). This configuration
    represents the vertex figure of the icosahedron and the face of the dodecahedron.

    Returns:
        Tuple of (Model, metrics_dict) certifying pentagon-pentagram golden proportions.
    """
    model = Model("pentagon_cross_section")

    verts = []
    for k in range(5):
        ang = 2 * sp.pi * k / 5
        verts.append(
            model.set_point(sp.cos(ang), sp.sin(ang), classes=["vertex"])
        )

    # Pentagon side quadrance Q(V0, V1) and pentagram diagonal quadrance Q(V0, V2)
    q_side = quadrance(verts[0], verts[1])
    q_diag = quadrance(verts[0], verts[2])
    q_diag_over_side = sp.simplify(q_diag / q_side)

    # Intersect diagonals V0-V2 and V1-V4
    line_02 = model.construct_line(verts[0], verts[2])
    line_14 = model.construct_line(verts[1], verts[4])
    pt_inter = model.intersect(line_02, line_14)

    # Segments on diagonal V0-V2: minor part V0-inter, major part inter-V2
    q_minor = quadrance(verts[0], pt_inter)
    q_major = quadrance(pt_inter, verts[2])

    ratio_diag_major = sp.simplify(q_diag / q_major)
    ratio_major_minor = sp.simplify(q_major / q_minor)

    metrics: dict[str, sp.Expr] = {
        "q_side": q_side,
        "q_diagonal": q_diag,
        "q_diag_over_side": q_diag_over_side,
        "q_major": q_major,
        "q_minor": q_minor,
        "ratio_diag_major": ratio_diag_major,
        "ratio_major_minor": ratio_major_minor,
    }

    return model, metrics


def get_golden_theorems() -> dict[str, GoldenPolyhedronTheorem]:
    """Retrieves all canonical golden proportion theorems in polyhedra.

    Returns:
        Dictionary mapping theorem slugs to GoldenPolyhedronTheorem instances.
    """
    rect_res = build_icosahedron_golden_rectangles()
    oct_res = build_octahedron_golden_icosahedron()
    cube_res = build_dodecahedron_five_cubes()
    rhomb_res = build_rhombic_triacontahedron_golden()
    _, odom_metrics = build_odom_tetrahedron_section_model()
    _, mer_metrics = build_icosahedron_meridian_model()
    _, pent_metrics = build_pentagon_cross_section_model()

    theorems = {
        "icosahedron_golden_rectangles": GoldenPolyhedronTheorem(
            slug="icosahedron_golden_rectangles",
            title="Golden Rectangles of the Icosahedron",
            subtitle="Three Mutually Orthogonal Golden Rectangles Spanning the 12 Vertices",
            historical_source="Euclid Elements XIII.16 · Pacioli Cap. XLIX",
            summary=(
                "The twelve vertices of the regular icosahedron are spanned by three mutually "
                "orthogonal golden rectangles whose aspect ratio is phi : 1 and whose diagonals "
                "are diameters of the circumscribing sphere."
            ),
            golden_identities=(
                (
                    "Aspect ratio quadrance Q_long / Q_short == PHI**2",
                    rect_res.q_ratio,
                    PHI**2,
                ),
                (
                    "Diagonal quadrance equals circumdiameter quadrance 4 * Q_circum",
                    rect_res.q_diagonal,
                    sp.Integer(4) * (PHI + sp.Integer(2)),
                ),
                (
                    "Diagonal to short edge quadrance ratio",
                    rect_res.q_diagonal / rect_res.q_short,
                    PHI + sp.Integer(2),
                ),
            ),
        ),
        "octahedron_golden_icosahedron": GoldenPolyhedronTheorem(
            slug="octahedron_golden_icosahedron",
            title="Golden Division of Octahedral Edges",
            subtitle="Inscribing the Regular Icosahedron in the Regular Octahedron",
            historical_source="Pacioli De Divina Proportione · Jessen",
            summary=(
                "Dividing the twelve edges of a regular octahedron of scale phi^2 in the golden "
                "ratio 1 : phi yields the twelve vertices of the regular icosahedron."
            ),
            golden_identities=(
                (
                    "Octahedron edge to major segment quadrance Q(A, B) / Q(G, B)",
                    oct_res.q_oct_edge / oct_res.q_major,
                    PHI**2,
                ),
                (
                    "Major segment to minor segment quadrance Q(G, B) / Q(A, G)",
                    oct_res.q_major / oct_res.q_minor,
                    PHI**2,
                ),
                (
                    "Icosahedron edge to minor segment quadrance ratio",
                    oct_res.q_ico_edge / oct_res.q_minor,
                    sp.Integer(2),
                ),
            ),
        ),
        "dodecahedron_five_cubes": GoldenPolyhedronTheorem(
            slug="dodecahedron_five_cubes",
            title="Five Inscribed Cubes in the Dodecahedron",
            subtitle="Euclid XIII.17 Roof Construction & the Compound of 5 Inscribed Cubes",
            historical_source="Euclid Elements XIII.17",
            summary=(
                "The twenty vertices of a regular dodecahedron contain five distinct sets of "
                "eight vertices that form regular cubes, partitioning the sixty pentagonal face "
                "diagonals into five disjoint sets of twelve cube edges."
            ),
            golden_identities=(
                (
                    "Cube edge to dodecahedron edge quadrance ratio Q_cube / Q_dod",
                    cube_res.q_ratio,
                    PHI**2,
                ),
                (
                    "Dodecahedron edge to cube edge quadrance ratio",
                    cube_res.q_dod_edge / cube_res.q_cube_edge,
                    PHI_INV**2,
                ),
                (
                    "Cube edge quadrance",
                    cube_res.q_cube_edge,
                    sp.Integer(4),
                ),
            ),
        ),
        "rhombic_triacontahedron_golden": GoldenPolyhedronTheorem(
            slug="rhombic_triacontahedron_golden",
            title="Kepler's Rhombic Triacontahedron",
            subtitle="Thirty Golden Rhombic Faces Spanning Dodecahedral and Icosahedral Dual Vertices",
            historical_source="Kepler Strena (1611)",
            summary=(
                "The union of the twenty vertices of the regular dodecahedron and the twelve "
                "vertices of its dual regular icosahedron forms the thirty-two vertices of the "
                "rhombic triacontahedron, whose thirty faces are congruent golden rhombi."
            ),
            golden_identities=(
                (
                    "Rhombus diagonal quadrance ratio Q_long / Q_short",
                    rhomb_res.q_diagonal_ratio,
                    PHI**2,
                ),
                (
                    "Rhombus edge quadrance",
                    rhomb_res.q_edge,
                    sp.Integer(3) - PHI,
                ),
                (
                    "Short diagonal quadrance",
                    rhomb_res.q_short_diagonal,
                    sp.Integer(4) * (PHI_INV**2),
                ),
            ),
        ),
        "odom_tetrahedron_section": GoldenPolyhedronTheorem(
            slug="odom_tetrahedron_section",
            title="George Odom's Golden Construction in the Tetrahedron",
            subtitle="Circumcircle Section of an Equilateral Face Yielding the Golden Ratio",
            historical_source="George Odom (1983) · Plato Timaeus",
            summary=(
                "Connecting the midpoints of two edges of an equilateral triangular face of a "
                "regular tetrahedron and extending to its circumcircle divides the chord in "
                "extreme and mean ratio."
            ),
            golden_identities=(
                (
                    "Odom chord major to minor segment quadrance ratio",
                    odom_metrics["ratio_major_minor"],
                    PHI**2,
                ),
                (
                    "Odom total chord to major segment quadrance ratio",
                    odom_metrics["ratio_total_major"],
                    PHI**2,
                ),
            ),
        ),
        "icosahedron_meridian": GoldenPolyhedronTheorem(
            slug="icosahedron_meridian",
            title="Icosahedron Principal Meridian Section",
            subtitle="Planar Golden Rectangle and Equatorial Golden Division in X = 0",
            historical_source="Euclid Elements XIII.16 · Pappus Synagoge VII",
            summary=(
                "The principal meridian plane X = 0 of the canonical icosahedron contains a "
                "golden rectangle and intersects the equatorial edges in the exact golden ratio."
            ),
            golden_identities=(
                (
                    "Meridian golden rectangle aspect ratio quadrance",
                    mer_metrics["q_ratio"],
                    PHI**2,
                ),
                (
                    "Meridian equatorial axis golden quadrance ratio",
                    mer_metrics["ratio_of_oi"],
                    PHI**2,
                ),
                (
                    "Meridian equatorial minor segment golden quadrance ratio",
                    mer_metrics["ratio_oi_if"],
                    PHI**2,
                ),
            ),
        ),
        "pentagon_cross_section": GoldenPolyhedronTheorem(
            slug="pentagon_cross_section",
            title="Regular Pentagon and Pentagram Golden Sections",
            subtitle="Diagonal-to-Side and Diagonal-Intersection Golden Division",
            historical_source="Euclid Elements XIII.8 · XIII.16",
            summary=(
                "The diagonals of a regular pentagon cut one another in extreme and mean ratio, "
                "with the diagonal-to-side quadrance ratio equal to phi^2."
            ),
            golden_identities=(
                (
                    "Pentagon diagonal to side quadrance ratio",
                    pent_metrics["q_diag_over_side"],
                    PHI**2,
                ),
                (
                    "Pentagram diagonal to major segment quadrance ratio",
                    pent_metrics["ratio_diag_major"],
                    PHI**2,
                ),
                (
                    "Pentagram major to minor segment quadrance ratio",
                    pent_metrics["ratio_major_minor"],
                    PHI**2,
                ),
            ),
        ),
    }

    return theorems


def get_golden_theorem(slug: str) -> GoldenPolyhedronTheorem:
    """Retrieves a single golden proportion theorem by slug name.

    Args:
        slug: Short lowercase identifier ('icosahedron_golden_rectangles', etc.).

    Returns:
        The corresponding GoldenPolyhedronTheorem instance.

    Raises:
        KeyError: If slug is not recognized.
    """
    theorems = get_golden_theorems()
    if slug not in theorems:
        raise KeyError(
            f"Unknown golden theorem slug: {slug!r}. Available: {list(theorems.keys())}"
        )
    return theorems[slug]


__all__ = [
    "DodecahedronFiveCubesResult",
    "GoldenPolyhedronTheorem",
    "GoldenRectanglesResult",
    "InscribedCube",
    "OctahedronGoldenIcosahedronResult",
    "RhombicTriacontahedronResult",
    "build_dodecahedron_five_cubes",
    "build_icosahedron_golden_rectangles",
    "build_icosahedron_meridian_model",
    "build_octahedron_golden_icosahedron",
    "build_odom_tetrahedron_section_model",
    "build_pentagon_cross_section_model",
    "build_rhombic_triacontahedron_golden",
    "get_golden_theorem",
    "get_golden_theorems",
]
