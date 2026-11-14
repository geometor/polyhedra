"""Tests for exact symbolic Platonic solids and 3D Rational Trigonometry."""

from __future__ import annotations

import pytest
import sympy as sp

from geometor.polyhedra import (
    cross_3d,
    dihedral_spread_3d,
    dot_3d,
    face_normal_3d,
    get_platonic_solid,
    get_platonic_solids,
    quadrance_3d,
)
from geometor.polyhedra.cli import main


def test_no_float_atoms() -> None:
    """Verifies that no float or sp.Float atoms exist in vertices or metrics."""
    solids = get_platonic_solids()
    assert len(solids) == 5

    for solid in solids.values():
        # Check vertices
        for v in solid.vertices:
            for coord in v:
                assert not coord.has(sp.Float), f"Float in {solid.slug} vertex {coord}"
                assert not isinstance(coord, float)

        # Check metrics
        for metric in (
            solid.dihedral_spread,
            solid.q_in_over_q_out,
            solid.q_mid_over_q_out,
        ):
            assert not metric.has(sp.Float), f"Float in {solid.slug} metric {metric}"
            assert not isinstance(metric, float)


def test_euler_and_schlafli() -> None:
    """Verifies Euler's formula V - E + F = 2 and Schläfli counts p*F = 2*E = q*V."""
    solids = get_platonic_solids()

    for solid in solids.values():
        v = len(solid.vertices)
        e = len(solid.edges)
        f = len(solid.faces)
        p, q = solid.schlafli

        # Euler's characteristic
        assert v - e + f == 2, f"Euler failed for {solid.slug}"

        # Schläfli regular relation
        assert p * f == 2 * e, f"p*F != 2*E for {solid.slug}"
        assert q * v == 2 * e, f"q*V != 2*E for {solid.slug}"


def test_edge_quadrances() -> None:
    """Verifies that all edges of each solid have identical exact quadrance."""
    solids = get_platonic_solids()

    expected_edge_q = {
        "tetrahedron": sp.Integer(8),
        "hexahedron": sp.Integer(4),
        "octahedron": sp.Integer(2),
        "icosahedron": sp.Integer(4),
        "dodecahedron": sp.simplify(sp.Integer(4) * (sp.Integer(2) - (sp.Integer(1) + sp.sqrt(5)) / 2)),
    }

    for slug, solid in solids.items():
        expected = expected_edge_q[slug]
        for idx1, idx2 in solid.edges:
            v1 = solid.vertices[idx1]
            v2 = solid.vertices[idx2]
            diff = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
            q = quadrance_3d(diff)
            assert sp.simplify(q - expected) == 0, f"Edge ({idx1}, {idx2}) in {slug} mismatch: {q} != {expected}"


def test_quadrances_from_origin() -> None:
    """Verifies circumquadrance, inquadrance, and midquadrance across all solids."""
    solids = get_platonic_solids()

    for solid in solids.values():
        # Check all vertices have identical circumquadrance
        q_out = quadrance_3d(solid.vertices[0])
        for v in solid.vertices:
            assert sp.simplify(quadrance_3d(v) - q_out) == 0

        # Check all face centroids have identical inquadrance
        f0 = solid.faces[0]
        n_face = len(f0)
        c0 = tuple(
            sp.simplify(sum(solid.vertices[idx][k] for idx in f0) / n_face)
            for k in range(3)
        )
        q_in = quadrance_3d(c0)
        for f in solid.faces:
            cf = tuple(
                sp.simplify(sum(solid.vertices[idx][k] for idx in f) / len(f))
                for k in range(3)
            )
            assert sp.simplify(quadrance_3d(cf) - q_in) == 0

        # Check all edge midpoints have identical midquadrance
        e0 = solid.edges[0]
        m0 = tuple(
            sp.simplify((solid.vertices[e0[0]][k] + solid.vertices[e0[1]][k]) / 2)
            for k in range(3)
        )
        q_mid = quadrance_3d(m0)
        for e in solid.edges:
            me = tuple(
                sp.simplify((solid.vertices[e[0]][k] + solid.vertices[e[1]][k]) / 2)
                for k in range(3)
            )
            assert sp.simplify(quadrance_3d(me) - q_mid) == 0

        # Verify recorded ratio invariants
        assert sp.simplify((q_in / q_out) - solid.q_in_over_q_out) == 0
        assert sp.simplify((q_mid / q_out) - solid.q_mid_over_q_out) == 0


def test_coplanarity_and_outward_orientation() -> None:
    """Verifies that all faces are coplanar and oriented counter-clockwise outward."""
    solids = get_platonic_solids()

    for solid in solids.values():
        for face in solid.faces:
            n_vertices = len(face)
            centroid = tuple(
                sp.simplify(sum(solid.vertices[idx][k] for idx in face) / n_vertices)
                for k in range(3)
            )
            normal = face_normal_3d(solid.vertices, face)

            # Outward orientation: dot(centroid, normal) > 0
            orientation_dot = sp.simplify(dot_3d(centroid, normal))
            assert orientation_dot > 0, f"Face {face} in {solid.slug} not outward"

            # Coplanarity: all face vertices lie on plane dot(v - centroid, normal) == 0
            for v_idx in face:
                v = solid.vertices[v_idx]
                disp = (v[0] - centroid[0], v[1] - centroid[1], v[2] - centroid[2])
                assert sp.simplify(dot_3d(disp, normal)) == 0, f"Vertex {v_idx} in face {face} not coplanar"


def test_adjacent_dihedral_spread() -> None:
    """Verifies adjacent face dihedral spreads match the exact Rational Trigonometry values."""
    solids = get_platonic_solids()

    expected_spreads = {
        "tetrahedron": sp.Rational(8, 9),
        "hexahedron": sp.Rational(1, 1),
        "octahedron": sp.Rational(8, 9),
        "icosahedron": sp.Rational(4, 9),
        "dodecahedron": sp.Rational(4, 5),
    }

    for slug, solid in solids.items():
        assert solid.dihedral_spread == expected_spreads[slug]

        # Find adjacent faces sharing an edge (exactly 2 common vertices)
        tested_adjacent = 0
        f0 = solid.faces[0]
        n0 = face_normal_3d(solid.vertices, f0)

        for other_face in solid.faces[1:]:
            common = set(f0) & set(other_face)
            if len(common) == 2:
                n1 = face_normal_3d(solid.vertices, other_face)
                computed_spread = dihedral_spread_3d(n0, n1)
                assert sp.simplify(computed_spread - solid.dihedral_spread) == 0
                tested_adjacent += 1

        assert tested_adjacent > 0


def test_polar_duality() -> None:
    """Verifies polar duality ratios across the five Platonic solids."""
    solids = get_platonic_solids()

    cube = solids["hexahedron"]
    octa = solids["octahedron"]
    dodec = solids["dodecahedron"]
    ico = solids["icosahedron"]
    tetra = solids["tetrahedron"]

    # Cube and Octahedron dual pair
    assert cube.dual_slug == "octahedron"
    assert octa.dual_slug == "hexahedron"
    assert sp.simplify(cube.q_in_over_q_out - octa.q_in_over_q_out) == 0
    assert cube.q_in_over_q_out == sp.Rational(1, 3)

    # Dodecahedron and Icosahedron dual pair
    assert dodec.dual_slug == "icosahedron"
    assert ico.dual_slug == "dodecahedron"
    assert sp.simplify(dodec.q_in_over_q_out - ico.q_in_over_q_out) == 0

    # Tetrahedron self-dual
    assert tetra.dual_slug == "tetrahedron"
    assert tetra.q_in_over_q_out == sp.Rational(1, 9)


def test_vector_helpers() -> None:
    """Tests 3D Rational Trigonometry vector helpers."""
    u = (sp.Integer(1), sp.Integer(2), sp.Integer(3))
    v = (sp.Integer(4), sp.Integer(5), sp.Integer(6))

    # Dot product: 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
    assert dot_3d(u, v) == sp.Integer(32)

    # Quadrance: 1 + 4 + 9 = 14
    assert quadrance_3d(u) == sp.Integer(14)

    # Cross product: (2*6 - 3*5, 3*4 - 1*6, 1*5 - 2*4) = (-3, 6, -3)
    c = cross_3d(u, v)
    assert c == (sp.Integer(-3), sp.Integer(6), sp.Integer(-3))

    # Orthogonality of cross product
    assert dot_3d(u, c) == 0
    assert dot_3d(v, c) == 0


def test_get_platonic_solid_errors() -> None:
    """Verifies KeyError is raised for invalid solid slugs."""
    with pytest.raises(KeyError):
        get_platonic_solid("nonexistent_solid")


def test_cli_execution() -> None:
    """Verifies that the polyhedra CLI runs cleanly."""
    assert main([]) == 0
    assert main(["tetrahedron"]) == 0
    assert main(["dodecahedron"]) == 0
    assert main(["invalid_solid_slug"]) == 1
