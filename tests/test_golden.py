"""Tests for exact symbolic golden proportions and Keplerian compounds in polyhedra."""

from __future__ import annotations

import pytest
import sympy as sp

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
from geometor.polyhedra.platonic import (
    PHI,
    PHI_INV,
    dot_3d,
    get_platonic_solid,
    quadrance_3d,
)


def _assert_no_float(obj: object, context: str = "") -> None:
    """Recursively asserts that no float or sp.Float instances exist in obj."""
    if isinstance(obj, (int, str, bool)):
        return
    if isinstance(obj, float):
        pytest.fail(f"Found python float {obj!r} in {context}")
    if isinstance(obj, sp.Float):
        pytest.fail(f"Found sp.Float {obj!r} in {context}")
    if isinstance(obj, sp.Basic):
        if obj.has(sp.Float):
            pytest.fail(f"Found sp.Float inside expression {obj!r} in {context}")
        return
    if isinstance(obj, (tuple, list, set)):
        for idx, item in enumerate(obj):
            _assert_no_float(item, f"{context}[{idx}]")
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            _assert_no_float(v, f"{context}[{k!r}]")
        return


def test_no_float_atoms_in_all_theorems_and_constructions() -> None:
    """Verifies that no float or sp.Float atoms exist in any theorem, coordinate, or metric."""
    theorems = get_golden_theorems()
    assert len(theorems) >= 6

    for slug, thm in theorems.items():
        assert isinstance(thm, GoldenPolyhedronTheorem)
        for desc, lhs, rhs in thm.golden_identities:
            _assert_no_float(lhs, f"Theorem {slug} identity {desc} LHS")
            _assert_no_float(rhs, f"Theorem {slug} identity {desc} RHS")

    # Check Golden Rectangles
    rect_res = build_icosahedron_golden_rectangles()
    _assert_no_float(rect_res.rectangles, "GoldenRectangles.rectangles")
    _assert_no_float(rect_res.normals, "GoldenRectangles.normals")
    _assert_no_float(rect_res.q_short, "GoldenRectangles.q_short")
    _assert_no_float(rect_res.q_long, "GoldenRectangles.q_long")
    _assert_no_float(rect_res.q_diagonal, "GoldenRectangles.q_diagonal")

    # Check Octahedron Golden Icosahedron
    oct_res = build_octahedron_golden_icosahedron()
    _assert_no_float(oct_res.octahedron_vertices, "Octahedron.vertices")
    _assert_no_float(oct_res.division_points, "Octahedron.division_points")
    _assert_no_float(oct_res.q_oct_edge, "Octahedron.q_oct_edge")
    _assert_no_float(oct_res.q_major, "Octahedron.q_major")
    _assert_no_float(oct_res.q_minor, "Octahedron.q_minor")

    # Check Dodecahedron Five Cubes
    cube_res = build_dodecahedron_five_cubes()
    _assert_no_float(cube_res.dodecahedron_vertices, "Dodecahedron.vertices")
    for cube in cube_res.cubes:
        _assert_no_float(cube.vertex_coords, f"Cube {cube.cube_index} vertex_coords")
    _assert_no_float(cube_res.q_dod_edge, "Dodecahedron.q_dod_edge")
    _assert_no_float(cube_res.q_cube_edge, "Dodecahedron.q_cube_edge")

    # Check Rhombic Triacontahedron
    rhomb_res = build_rhombic_triacontahedron_golden()
    _assert_no_float(rhomb_res.vertices, "RhombicTriacontahedron.vertices")
    _assert_no_float(rhomb_res.q_long_diagonal, "RhombicTriacontahedron.q_long_diagonal")
    _assert_no_float(rhomb_res.q_short_diagonal, "RhombicTriacontahedron.q_short_diagonal")
    _assert_no_float(rhomb_res.q_edge, "RhombicTriacontahedron.q_edge")

    # Check 2D Models
    m_odom, odom_metrics = build_odom_tetrahedron_section_model()
    _assert_no_float(odom_metrics, "Odom.metrics")
    for pt in m_odom.points:
        _assert_no_float(pt.x, f"Odom point {pt} x")
        _assert_no_float(pt.y, f"Odom point {pt} y")

    m_mer, mer_metrics = build_icosahedron_meridian_model()
    _assert_no_float(mer_metrics, "Meridian.metrics")
    for pt in m_mer.points:
        _assert_no_float(pt.x, f"Meridian point {pt} x")
        _assert_no_float(pt.y, f"Meridian point {pt} y")

    m_pent, pent_metrics = build_pentagon_cross_section_model()
    _assert_no_float(pent_metrics, "Pentagon.metrics")
    for pt in m_pent.points:
        _assert_no_float(pt.x, f"Pentagon point {pt} x")
        _assert_no_float(pt.y, f"Pentagon point {pt} y")


def test_golden_identities_simplify_zero() -> None:
    """Verifies that all golden identities across all registered theorems simplify to exact zero."""
    theorems = get_golden_theorems()

    for slug, thm in theorems.items():
        assert thm.slug == slug
        assert len(thm.title) > 0
        assert len(thm.historical_source) > 0
        assert len(thm.golden_identities) > 0

        for desc, lhs, rhs in thm.golden_identities:
            diff = sp.simplify(lhs - rhs)
            assert diff == 0, (
                f"Identity failed in theorem {slug!r} ({desc}): "
                f"LHS={lhs}, RHS={rhs}, diff={diff}"
            )


def test_icosahedron_golden_rectangles() -> None:
    """Verifies the three mutually orthogonal golden rectangles in the icosahedron."""
    ico = get_platonic_solid("icosahedron")
    res = build_icosahedron_golden_rectangles()

    assert len(res.rectangles) == 3
    assert set(res.rectangles.keys()) == {"R_YZ", "R_ZX", "R_XY"}

    # Quadrance and aspect ratio
    assert res.q_short == 4
    assert sp.simplify(res.q_long - 4 * (PHI**2)) == 0
    assert sp.simplify(res.q_ratio - PHI**2) == 0
    assert sp.simplify(res.q_diagonal - 4 * (PHI + 2)) == 0
    assert sp.simplify(res.q_circumradius - (PHI + 2)) == 0
    assert sp.simplify(res.q_diagonal - 4 * res.q_circumradius) == 0

    # Mutual orthogonality of the three rectangle planes
    n_yz = res.normals["R_YZ"]
    n_zx = res.normals["R_ZX"]
    n_xy = res.normals["R_XY"]
    assert dot_3d(n_yz, n_zx) == 0
    assert dot_3d(n_zx, n_xy) == 0
    assert dot_3d(n_xy, n_yz) == 0

    # All rectangle vertices must belong to canonical icosahedron
    all_rect_verts = [v for rect in res.rectangles.values() for v in rect]
    assert len(all_rect_verts) == 12
    assert set(all_rect_verts) == set(ico.vertices)

    # Short edges: exactly 6 edges belonging to the icosahedron edge topology
    assert len(res.short_edges_in_icosahedron) == 6
    ico_edge_set = set(ico.edges)
    for e in res.short_edges_in_icosahedron:
        assert e in ico_edge_set


def test_octahedron_golden_icosahedron() -> None:
    """Verifies the golden division of the twelve edges of a regular octahedron."""
    res = build_octahedron_golden_icosahedron()
    ico = get_platonic_solid("icosahedron")

    # Parent octahedron counts
    assert len(res.octahedron_vertices) == 6
    assert len(res.octahedron_edges) == 12
    assert len(res.octahedron_faces) == 8

    # Edge division: exactly 12 division points matching canonical icosahedron
    assert len(res.division_points) == 12
    assert res.division_points == ico.vertices

    # Proportions on each octahedron edge: Q(A, B) / Q(G, B) == PHI**2, Q(G, B) / Q(A, G) == PHI**2
    assert sp.simplify(res.q_oct_edge / res.q_major - PHI**2) == 0
    assert sp.simplify(res.q_major / res.q_minor - PHI**2) == 0
    assert res.q_minor == 2
    assert res.q_ico_edge == 4

    # Mutual icosahedral edge quadrance across all 30 edges
    for i, j in res.icosahedron_edges:
        p1 = res.division_points[i]
        p2 = res.division_points[j]
        diff = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
        q = sp.simplify(quadrance_3d(diff))
        assert q == 4, f"Edge ({i}, {j}) has quadrance {q} != 4"


def test_dodecahedron_five_cubes() -> None:
    """Verifies Euclid XIII.17 and Kepler's compound of five inscribed cubes."""
    res = build_dodecahedron_five_cubes()

    assert len(res.dodecahedron_vertices) == 20
    assert len(res.dodecahedron_edges) == 30
    assert len(res.dodecahedron_faces) == 12

    # Euclid XIII.17 edge ratio
    assert res.q_cube_edge == 4
    assert sp.simplify(res.q_dod_edge - 4 * (PHI_INV**2)) == 0
    assert sp.simplify(res.q_ratio - PHI**2) == 0

    # Exactly 5 inscribed regular cubes
    assert len(res.cubes) == 5

    all_cube_edge_set: set[tuple[int, int]] = set()

    for cube in res.cubes:
        assert len(cube.vertices) == 8
        assert len(set(cube.vertices)) == 8
        assert len(cube.edges) == 12
        assert len(cube.faces) == 6

        # Check all 12 cube edges have quadrance 4
        for i, j in cube.edges:
            v1 = res.dodecahedron_vertices[i]
            v2 = res.dodecahedron_vertices[j]
            diff = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
            assert sp.simplify(quadrance_3d(diff)) == 4
            all_cube_edge_set.add((min(i, j), max(i, j)))

        # Check 6 square faces: 4 vertices, 4 edges of Q=4, 2 diagonals of Q=8
        for face in cube.faces:
            assert len(face) == 4
            f_verts = [res.dodecahedron_vertices[idx] for idx in face]
            # Edge quadrances around cycle
            for k in range(4):
                va = f_verts[k]
                vb = f_verts[(k + 1) % 4]
                diff = (vb[0] - va[0], vb[1] - va[1], vb[2] - va[2])
                assert sp.simplify(quadrance_3d(diff)) == 4
            # Diagonal quadrances
            diag1 = (f_verts[2][0] - f_verts[0][0], f_verts[2][1] - f_verts[0][1], f_verts[2][2] - f_verts[0][2])
            diag2 = (f_verts[3][0] - f_verts[1][0], f_verts[3][1] - f_verts[1][1], f_verts[3][2] - f_verts[1][2])
            assert sp.simplify(quadrance_3d(diag1)) == 8
            assert sp.simplify(quadrance_3d(diag2)) == 8

    # The 5 cubes must partition all 60 diagonals (5 * 12 = 60 disjoint edges)
    assert len(all_cube_edge_set) == 60
    assert len(res.all_cube_edges) == 60


def test_rhombic_triacontahedron_golden() -> None:
    """Verifies Kepler's 30-face Rhombic Triacontahedron and golden rhombi."""
    res = build_rhombic_triacontahedron_golden()

    assert len(res.vertices) == 32
    assert len(res.faces) == 30
    assert len(res.edges) == 60
    assert len(res.dodecahedron_indices) == 20
    assert len(res.icosahedron_indices) == 12

    # Euler characteristic V - E + F = 32 - 60 + 30 = 2
    assert len(res.vertices) - len(res.edges) + len(res.faces) == 2

    # Metric ratios
    assert res.q_long_diagonal == 4
    assert sp.simplify(res.q_short_diagonal - 4 * (PHI_INV**2)) == 0
    assert sp.simplify(res.q_diagonal_ratio - PHI**2) == 0
    assert sp.simplify(res.q_edge - (sp.Integer(3) - PHI)) == 0

    # Face verification
    for face in res.faces:
        assert len(face) == 4
        a, b, c, d = face
        # a, c are degree 5 (icosahedral: 20..31); b, d are degree 3 (dodecahedral: 0..19)
        assert a in res.icosahedron_indices
        assert c in res.icosahedron_indices
        assert b in res.dodecahedron_indices
        assert d in res.dodecahedron_indices

        pt_a = res.vertices[a]
        pt_b = res.vertices[b]
        pt_c = res.vertices[c]
        pt_d = res.vertices[d]

        # Diagonals
        diag_ac = (pt_c[0] - pt_a[0], pt_c[1] - pt_a[1], pt_c[2] - pt_a[2])
        diag_bd = (pt_d[0] - pt_b[0], pt_d[1] - pt_b[1], pt_d[2] - pt_b[2])

        assert sp.simplify(quadrance_3d(diag_ac)) == 4
        assert sp.simplify(quadrance_3d(diag_bd) - 4 * (PHI_INV**2)) == 0
        # Perpendicularity
        assert sp.simplify(dot_3d(diag_ac, diag_bd)) == 0

        # Sides
        side_ab = (pt_b[0] - pt_a[0], pt_b[1] - pt_a[1], pt_b[2] - pt_a[2])
        side_bc = (pt_c[0] - pt_b[0], pt_c[1] - pt_b[1], pt_c[2] - pt_b[2])
        side_cd = (pt_d[0] - pt_c[0], pt_d[1] - pt_c[1], pt_d[2] - pt_c[2])
        side_da = (pt_a[0] - pt_d[0], pt_a[1] - pt_d[1], pt_a[2] - pt_d[2])

        assert sp.simplify(quadrance_3d(side_ab) - (3 - PHI)) == 0
        assert sp.simplify(quadrance_3d(side_bc) - (3 - PHI)) == 0
        assert sp.simplify(quadrance_3d(side_cd) - (3 - PHI)) == 0
        assert sp.simplify(quadrance_3d(side_da) - (3 - PHI)) == 0


def test_odom_tetrahedron_section_model() -> None:
    """Verifies George Odom's golden section construction in Model."""
    model, metrics = build_odom_tetrahedron_section_model()

    assert len(model.points) >= 6
    assert sp.simplify(metrics["ratio_major_minor"] - PHI**2) == 0
    assert sp.simplify(metrics["ratio_total_major"] - PHI**2) == 0
    assert metrics["q_m1_m2"] == 3


def test_icosahedron_meridian_model() -> None:
    """Verifies the icosahedron principal meridian section in Model."""
    model, metrics = build_icosahedron_meridian_model()

    assert len(model.points) >= 6
    assert metrics["q_short"] == 4
    assert sp.simplify(metrics["q_long"] - 4 * (PHI**2)) == 0
    assert sp.simplify(metrics["q_ratio"] - PHI**2) == 0
    assert sp.simplify(metrics["ratio_of_oi"] - PHI**2) == 0
    assert sp.simplify(metrics["ratio_oi_if"] - PHI**2) == 0


def test_pentagon_cross_section_model() -> None:
    """Verifies the regular pentagon and pentagram section in Model."""
    model, metrics = build_pentagon_cross_section_model()

    assert len(model.points) >= 6
    assert sp.simplify(metrics["q_diag_over_side"] - PHI**2) == 0
    assert sp.simplify(metrics["ratio_diag_major"] - PHI**2) == 0
    assert sp.simplify(metrics["ratio_major_minor"] - PHI**2) == 0


def test_get_golden_theorem_registry() -> None:
    """Verifies theorem lookup and KeyError on invalid slug."""
    theorems = get_golden_theorems()
    assert len(theorems) >= 6

    for slug in theorems:
        thm = get_golden_theorem(slug)
        assert thm.slug == slug

    with pytest.raises(KeyError):
        get_golden_theorem("non_existent_slug")
