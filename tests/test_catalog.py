"""Tests for exact symbolic polyhedra catalog, builders, invariants, and CLI."""

from __future__ import annotations

import pytest
import sympy as sp

from geometor.polyhedra.catalog import (
    PolyhedronEntry,
    PolyhedronFamily,
    build_catalog_solid,
    build_pentagonal_pyramid_solid,
    build_rhombicuboctahedron_solid,
    get_polyhedra_catalog,
    get_polyhedra_families,
    get_polyhedron_entry,
)
from geometor.polyhedra.cli import main
from geometor.polyhedra.operators import vacuate

EXPECTED_FAMILIES = (
    "01-platonic",
    "02-archimedean",
    "03-catalan",
    "04-elevated",
    "05-pyramids",
)

EXPECTED_SLUGS = (
    # 01-platonic (5)
    "tetrahedron",
    "hexahedron",
    "octahedron",
    "icosahedron",
    "dodecahedron",
    # 02-archimedean (8)
    "truncated-tetrahedron",
    "cuboctahedron",
    "truncated-hexahedron",
    "truncated-octahedron",
    "rhombicuboctahedron",
    "icosidodecahedron",
    "truncated-icosahedron",
    "truncated-dodecahedron",
    # 03-catalan (2)
    "rhombic-dodecahedron",
    "rhombic-triacontahedron",
    # 04-elevated (7)
    "tetrahedron-elevatum",
    "hexahedron-elevatum",
    "stella-octangula",
    "icosahedron-elevatum",
    "dodecahedron-elevatum",
    "cuboctahedron-elevatum",
    "icosidodecahedron-elevatum",
    # 05-pyramids (4)
    "kepler-pyramid",
    "seked-pyramid",
    "golden-bipyramid",
    "pentagonal-pyramid",
)


def test_catalog_families_and_slugs() -> None:
    """Verifies that all 5 families and 26 canonical slugs exist with valid IDs."""
    families = get_polyhedra_families()
    assert tuple(families.keys()) == EXPECTED_FAMILIES
    for order, (fam_slug, fam) in enumerate(families.items(), start=1):
        assert isinstance(fam, PolyhedronFamily)
        assert fam.slug == fam_slug
        assert fam.order == order

    catalog = get_polyhedra_catalog()
    assert tuple(catalog.keys()) == EXPECTED_SLUGS
    assert len(catalog) == 26

    # Verify canonical IDs and order within families
    counts: dict[str, int] = {}
    for slug, entry in catalog.items():
        assert isinstance(entry, PolyhedronEntry)
        assert entry.slug == slug
        fam_idx = EXPECTED_FAMILIES.index(entry.family) + 1
        counts[entry.family] = counts.get(entry.family, 0) + 1
        expected_id = f"P-{fam_idx:02d}.{counts[entry.family]:02d}"
        assert entry.canonical_id == expected_id
        assert entry.order == counts[entry.family]

    assert counts["01-platonic"] == 5
    assert counts["02-archimedean"] == 8
    assert counts["03-catalan"] == 2
    assert counts["04-elevated"] == 7
    assert counts["05-pyramids"] == 4

    # Test single lookup
    entry = get_polyhedron_entry("rhombicuboctahedron")
    assert entry.canonical_id == "P-02.05"
    assert entry.title == "Rhombicuboctahedron"

    with pytest.raises(KeyError):
        get_polyhedron_entry("non-existent-solid")


def test_no_floats_in_entries_and_solids() -> None:
    """Verifies strict 100% exact symbolic algebra with zero float or sp.Float atoms."""
    catalog = get_polyhedra_catalog()

    for slug, entry in catalog.items():
        # Test entry symbolic metrics
        for q in entry.edge_quadrances:
            assert not isinstance(q, (float, sp.Float))
            assert not q.atoms(sp.Float)
        for vq in entry.vertex_quadrances:
            assert not isinstance(vq, (float, sp.Float))
            assert not vq.atoms(sp.Float)
        if entry.primary_dihedral_spread is not None:
            s = entry.primary_dihedral_spread
            assert not isinstance(s, (float, sp.Float))
            assert not s.atoms(sp.Float)

        # Test Solid3D vertices
        solid = build_catalog_solid(slug)
        for pt in solid.vertices:
            for coord in (pt.x, pt.y, pt.z):
                assert not isinstance(coord, (float, sp.Float))
                assert not coord.atoms(sp.Float)


def test_euler_characteristics_and_topology() -> None:
    """Verifies (V, E, F) counts, Euler characteristic chi == 2, and vacuum genus."""
    catalog = get_polyhedra_catalog()

    for slug, entry in catalog.items():
        solid = build_catalog_solid(slug)
        assert solid.num_vertices == entry.vertices_count
        assert solid.num_edges == entry.edges_count
        assert solid.num_faces == entry.faces_count

        # All 26 base solids are closed topological 2-spheres
        assert solid.euler_characteristic == 2
        assert solid.genus == 0

        # Vacuum genus is always F - 1
        assert entry.vacuum_genus == solid.num_faces - 1

        # Convexity matches family specification
        if entry.family == "04-elevated":
            assert not entry.is_convex
        else:
            assert entry.is_convex


def test_coplanarity_and_outward_orientation() -> None:
    """Verifies coplanarity and consistent outward orientation across all 26 solids."""
    catalog = get_polyhedra_catalog()

    for slug, _ in catalog.items():
        solid = build_catalog_solid(slug)

        # Fast exact coplanarity using algebraic sp.expand
        for f in solid.faces:
            if len(f) <= 3:
                continue
            p0, p1, p2 = solid.vertices[f[0]], solid.vertices[f[1]], solid.vertices[f[2]]
            d1x, d1y, d1z = p1.x - p0.x, p1.y - p0.y, p1.z - p0.z
            d2x, d2y, d2z = p2.x - p0.x, p2.y - p0.y, p2.z - p0.z
            nx = d1y * d2z - d1z * d2y
            ny = d1z * d2x - d1x * d2z
            nz = d1x * d2y - d1y * d2x
            for vi in f[3:]:
                pv = solid.vertices[vi]
                dot_cop = sp.expand(nx * (pv.x - p0.x) + ny * (pv.y - p0.y) + nz * (pv.z - p0.z))
                assert dot_cop == 0, f"Face vertex not coplanar in {slug}"

        # Fast outward orientation check
        for fi, f in enumerate(solid.faces):
            p0, p1, p2 = solid.vertices[f[0]], solid.vertices[f[1]], solid.vertices[f[2]]
            d1x, d1y, d1z = p1.x - p0.x, p1.y - p0.y, p1.z - p0.z
            d2x, d2y, d2z = p2.x - p0.x, p2.y - p0.y, p2.z - p0.z
            nx = d1y * d2z - d1z * d2y
            ny = d1z * d2x - d1x * d2z
            nz = d1x * d2y - d1y * d2x
            k = len(f)
            cx = sum(solid.vertices[i].x for i in f) / k
            cy = sum(solid.vertices[i].y for i in f) / k
            cz = sum(solid.vertices[i].z for i in f) / k
            dot_val = float((nx * cx + ny * cy + nz * cz).evalf())
            assert dot_val > 0, f"Face {fi} not outward oriented in {slug}"


def test_uniform_edge_quadrances() -> None:
    """Verifies uniform single edge quadrances on all Platonic, Archimedean, Catalan, Elevated, and J2."""
    catalog = get_polyhedra_catalog()

    uniform_slugs = [
        # All 5 Platonic
        "tetrahedron",
        "hexahedron",
        "octahedron",
        "icosahedron",
        "dodecahedron",
        # All 8 Archimedean
        "truncated-tetrahedron",
        "cuboctahedron",
        "truncated-hexahedron",
        "truncated-octahedron",
        "rhombicuboctahedron",
        "icosidodecahedron",
        "truncated-icosahedron",
        "truncated-dodecahedron",
        # Both Catalan
        "rhombic-dodecahedron",
        "rhombic-triacontahedron",
        # All 7 Elevated
        "tetrahedron-elevatum",
        "hexahedron-elevatum",
        "stella-octangula",
        "icosahedron-elevatum",
        "dodecahedron-elevatum",
        "cuboctahedron-elevatum",
        "icosidodecahedron-elevatum",
        # Johnson Pentagonal Pyramid
        "pentagonal-pyramid",
    ]

    for slug in uniform_slugs:
        entry = catalog[slug]
        assert len(entry.edge_quadrances) == 1, f"Expected uniform edge in {slug}"

    # Verify exact edge quadrances for specific celebrated solids
    trunc_hex = catalog["truncated-hexahedron"]
    assert trunc_hex.edge_quadrances[0] == sp.Integer(12) - sp.Integer(8) * sp.sqrt(2)

    trunc_dod = catalog["truncated-dodecahedron"]
    assert trunc_dod.edge_quadrances[0] == sp.Rational(6, 5) - sp.Rational(2, 5) * sp.sqrt(5)

    rho = catalog["rhombicuboctahedron"]
    assert rho.edge_quadrances[0] == sp.Integer(4)

    pyr = catalog["pentagonal-pyramid"]
    assert pyr.edge_quadrances[0] == sp.Integer(4)

    # Non-uniform architectural pyramids
    for pyr_slug in ("kepler-pyramid", "seked-pyramid", "golden-bipyramid"):
        assert len(catalog[pyr_slug].edge_quadrances) == 2


def test_vacuate_manifold_properties() -> None:
    """Verifies Leonardo's vacuate operator across cataloged polyhedral manifolds."""
    catalog = get_polyhedra_catalog()

    # Verify vacuum genus across all 26 solids
    for slug, entry in catalog.items():
        assert entry.vacuum_genus == entry.faces_count - 1

    # Full 3D vacuate manifold construction on fast representative set across all 5 families
    sample_slugs = (
        "tetrahedron",
        "cuboctahedron",
        "rhombicuboctahedron",
        "rhombic-dodecahedron",
        "stella-octangula",
        "kepler-pyramid",
        "pentagonal-pyramid",
    )
    for slug in sample_slugs:
        solid = build_catalog_solid(slug)
        vac = vacuate(solid)

        v = solid.num_vertices
        e = solid.num_edges
        f = solid.num_faces

        assert vac.num_vertices == 2 * v + 4 * e, f"V_vac mismatch in {slug}"
        assert vac.num_edges == 12 * e, f"E_vac mismatch in {slug}"
        assert vac.num_faces == 6 * e, f"F_vac mismatch in {slug}"
        assert vac.euler_characteristic == 4 - 2 * f, f"Euler mismatch in vacuate {slug}"
        assert vac.genus == f - 1, f"Genus mismatch in vacuate {slug}"


def test_rhombicuboctahedron_builder_specifics() -> None:
    """Verifies detailed geometry and face breakdown of Leonardo's Vigintisex Basium."""
    solid = build_rhombicuboctahedron_solid()
    assert solid.num_vertices == 24
    assert solid.num_edges == 48
    assert solid.num_faces == 26
    assert solid.euler_characteristic == 2

    # Check 48 edges all have exact quadrance 4
    for u, v in solid.edges:
        pu, pv = solid.vertices[u], solid.vertices[v]
        dx, dy, dz = pu.x - pv.x, pu.y - pv.y, pu.z - pv.z
        assert sp.expand(dx**2 + dy**2 + dz**2) == 4

    # Face roles: 6 axial squares ("base"), 12 chamfer squares + 8 triangles ("truncation")
    base_roles = [r for r in solid.face_roles if r == "base"]
    trunc_roles = [r for r in solid.face_roles if r == "truncation"]
    assert len(base_roles) == 6
    assert len(trunc_roles) == 20

    assert solid.are_faces_coplanar()
    assert solid.is_outward_oriented()


def test_pentagonal_pyramid_builder_specifics() -> None:
    """Verifies detailed geometry of the equilateral Pentagonal Pyramid (Johnson J2)."""
    # Centered version
    solid_c = build_pentagonal_pyramid_solid(center_origin=True)
    assert solid_c.num_vertices == 6
    assert solid_c.num_edges == 10
    assert solid_c.num_faces == 6
    assert solid_c.euler_characteristic == 2

    for u, v in solid_c.edges:
        pu, pv = solid_c.vertices[u], solid_c.vertices[v]
        dx, dy, dz = pu.x - pv.x, pu.y - pv.y, pu.z - pv.z
        assert sp.expand(dx**2 + dy**2 + dz**2) == 4

    assert solid_c.are_faces_coplanar()
    assert solid_c.is_outward_oriented()

    # Raw icosahedral cap coordinates
    solid_raw = build_pentagonal_pyramid_solid(center_origin=False)
    assert solid_raw.num_vertices == 6
    assert solid_raw.num_edges == 10
    assert solid_raw.num_faces == 6

    for u, v in solid_raw.edges:
        pu, pv = solid_raw.vertices[u], solid_raw.vertices[v]
        dx, dy, dz = pu.x - pv.x, pu.y - pv.y, pu.z - pv.z
        assert sp.expand(dx**2 + dy**2 + dz**2) == 4


def test_catalog_cli_execution(capsys: pytest.CaptureFixture[str]) -> None:
    """Verifies that the CLI entry points execute cleanly without errors."""
    # Overview table
    exit_code = main([])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "GEOMETOR • Canonical Polyhedra Catalog" in out
    assert "P-01.01" in out
    assert "P-02.05" in out
    assert "P-05.04" in out

    # Detail view of Archimedean solid
    exit_code = main(["rhombicuboctahedron"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Vigintisex Basium" in out
    assert "Tabula XXXV" in out

    # Platonic flag view
    exit_code = main(["--platonic"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "The Five Platonic Solids" in out

    # Unknown slug error
    exit_code = main(["invalid-slug"])
    assert exit_code == 1
    err = capsys.readouterr().out
    assert "Unknown polyhedron slug 'invalid-slug'" in err
