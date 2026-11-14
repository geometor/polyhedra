"""Demonstration of the five Platonic solids and 3D Rational Trigonometry.

Exhibits exact symbolic algebra over Z and Q(phi), Euler characteristics,
Schläfli counts, inquadrance-to-circumquadrance ratios, and dihedral spreads.
"""

from __future__ import annotations

import sympy as sp

from geometor.polyhedra import (
    RegularSolid,
    dihedral_spread_3d,
    dot_3d,
    face_normal_3d,
    get_platonic_solids,
    quadrance_3d,
)


def run_platonic_demo() -> None:
    """Runs the demonstration across all five Platonic solids."""
    print("=" * 72)
    print("GEOMETOR • Platonic Solids & Exact Symbolic 3D Rational Trigonometry")
    print("=" * 72)

    solids: dict[str, RegularSolid] = get_platonic_solids()

    for slug, solid in solids.items():
        v_count = len(solid.vertices)
        e_count = len(solid.edges)
        f_count = len(solid.faces)
        euler = v_count - e_count + f_count
        p, q = solid.schlafli

        print(f"\n[{solid.name.upper()}] {{{p}, {q}}} — Element: {solid.element}")
        print(f"  Greek / Latin : {solid.greek_name} / {solid.latin_name}")
        print(f"  Euclid Canon  : {solid.euclid_prop} ({solid.g_index})")
        print(f"  Euler Formula : V - E + F = {v_count} - {e_count} + {f_count} = {euler}")
        assert euler == 2, f"Euler failed for {solid.name}"

        # Check Schläfli counts: p*F = 2*E = q*V
        assert p * f_count == 2 * e_count == q * v_count, f"Schläfli failed for {solid.name}"
        print(f"  Schläfli Count: p·F = 2·E = q·V ({p*f_count} = {2*e_count} = {q*v_count})")

        # Circumquadrance from origin
        q_out = quadrance_3d(solid.vertices[0])
        for v in solid.vertices:
            assert sp.simplify(quadrance_3d(v) - q_out) == 0

        # Edge quadrance
        e0 = solid.edges[0]
        v0, v1 = solid.vertices[e0[0]], solid.vertices[e0[1]]
        edge_q = quadrance_3d((v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]))
        for e in solid.edges:
            va, vb = solid.vertices[e[0]], solid.vertices[e[1]]
            eq = quadrance_3d((vb[0] - va[0], vb[1] - va[1], vb[2] - va[2]))
            assert sp.simplify(eq - edge_q) == 0

        # Face inquadrance and normal check
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
            # Outward normal orientation
            nf = face_normal_3d(solid.vertices, f)
            assert dot_3d(cf, nf) > 0

        # Midquadrance
        m0 = tuple(
            sp.simplify((solid.vertices[e0[0]][k] + solid.vertices[e0[1]][k]) / 2)
            for k in range(3)
        )
        q_mid = quadrance_3d(m0)

        # Dihedral spread between adjacent faces
        adjacent_spread = None
        for other_face in solid.faces[1:]:
            if len(set(f0) & set(other_face)) == 2:
                n0 = face_normal_3d(solid.vertices, f0)
                n1 = face_normal_3d(solid.vertices, other_face)
                adjacent_spread = dihedral_spread_3d(n0, n1)
                break

        print(f"  Edge Quadrance: {edge_q}")
        print(f"  Q_out / Q_in  : {q_out} / {q_in}")
        print(f"  Q_mid         : {q_mid}")
        print(f"  Spread s      : {adjacent_spread} (recorded: {solid.dihedral_spread})")
        assert sp.simplify(adjacent_spread - solid.dihedral_spread) == 0

        print(f"  Q_in / Q_out  : {solid.q_in_over_q_out}")
        print(f"  Q_mid / Q_out : {solid.q_mid_over_q_out}")
        print(f"  Dual Solid    : {solid.dual_slug}")

    # Verify Polar Duality
    print("\n" + "=" * 72)
    print("VERIFYING POLAR DUALITY:")
    cube = solids["hexahedron"]
    octa = solids["octahedron"]
    dodec = solids["dodecahedron"]
    ico = solids["icosahedron"]
    tetra = solids["tetrahedron"]

    assert sp.simplify(cube.q_in_over_q_out - octa.q_in_over_q_out) == 0
    print(f"  ✓ Cube == Octahedron (Q_in / Q_out = {cube.q_in_over_q_out})")

    assert sp.simplify(dodec.q_in_over_q_out - ico.q_in_over_q_out) == 0
    print(f"  ✓ Dodecahedron == Icosahedron (Q_in / Q_out = {dodec.q_in_over_q_out})")

    assert tetra.dual_slug == "tetrahedron"
    print(f"  ✓ Tetrahedron is self-dual (Q_in / Q_out = {tetra.q_in_over_q_out})")
    print("=" * 72)


if __name__ == "__main__":
    run_platonic_demo()
