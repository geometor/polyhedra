"""Tests for exact symbolic Great Pyramid models, identities, and 3D solids.

Verifies 100% exact algebraic geometry over Q, Q(phi), Q(sqrt(phi)), and Q(pi) with zero
float or sp.Float atoms across profiles, identities, 3D solids, and 2D models.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest
import sympy as sp

from geometor.polyhedra.model3d.bridge import unfold_net_2d
from geometor.polyhedra.model3d.primitives import Point3D, Solid3D
from geometor.polyhedra.operators import vacuate
from geometor.polyhedra.platonic import PHI, PHI_INV
from geometor.polyhedra.pyramid import (
    SQRT_PHI,
    PyramidModelProfile,
    build_kepler_bipyramid_solid,
    build_kepler_pyramid_solid,
    build_kepler_triangle_model,
    build_pyramid_squaring_circle_model,
    build_seked_pyramid_solid,
    get_great_pyramid_profile,
    get_great_pyramid_profiles,
    verify_kepler_pyramid_identities,
)
from geometor.polyhedra.render.svg3d import render_model2d_svg


def _assert_no_float(obj: object, context: str = "") -> None:
    """Recursively asserts that no float or sp.Float instances exist in obj.

    Args:
        obj: Object, expression, collection, or dataclass to inspect.
        context: Breadcrumb context string for failure reporting.
    """
    if isinstance(obj, (int, str, bool)):
        return
    if isinstance(obj, float):
        pytest.fail(f"Found Python float {obj!r} in {context}")
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
    if isinstance(obj, Point3D):
        _assert_no_float(obj.x, f"{context}.x")
        _assert_no_float(obj.y, f"{context}.y")
        _assert_no_float(obj.z, f"{context}.z")
        return
    if isinstance(obj, Solid3D):
        _assert_no_float(obj.vertices, f"{context}.vertices")
        return
    if isinstance(obj, PyramidModelProfile):
        for field in (
            "half_base",
            "height",
            "apothem",
            "lateral_edge",
            "base_perimeter",
            "apex_circle_circumference",
            "base_area",
            "face_area",
            "lateral_area",
            "total_area",
            "volume",
            "slope_spread",
            "adjacent_dihedral_spread",
            "opposite_apex_spread",
        ):
            val = getattr(obj, field)
            if val is not None:
                _assert_no_float(val, f"{context}.{field}")
        return


def test_zero_float_atoms_in_all_pyramid_profiles() -> None:
    """Verifies that no float or sp.Float atoms exist in any profile parameters."""
    profiles = get_great_pyramid_profiles()
    assert len(profiles) == 4
    assert set(profiles.keys()) == {
        "kepler_golden",
        "pi_quadrature",
        "seked_14_11",
        "half_octahedron",
    }

    for slug, profile in profiles.items():
        assert isinstance(profile, PyramidModelProfile)
        assert profile.slug == slug
        _assert_no_float(profile, f"Profile({slug})")


def test_get_great_pyramid_profile_lookup() -> None:
    """Verifies profile lookup by slug and KeyError on invalid slugs."""
    kepler = get_great_pyramid_profile("kepler_golden")
    assert kepler.slug == "kepler_golden"
    assert kepler.height == SQRT_PHI

    with pytest.raises(KeyError, match="Unknown pyramid model profile"):
        get_great_pyramid_profile("nonexistent_pyramid")


def test_all_kepler_pyramid_identities_certify_to_zero() -> None:
    """Verifies all eleven exact symbolic identities simplify identically to zero."""
    identities = verify_kepler_pyramid_identities()
    assert len(identities) == 11

    expected_keys = {
        "pythagorean_geometric_mean",
        "herodotus_face_area_equals_height_squared",
        "golden_area_ratio_lateral_to_base",
        "golden_area_ratio_total_to_lateral",
        "golden_area_additive_law",
        "icosahedron_circumradius_edge_bridge",
        "kepler_slope_spread_equals_inv_phi",
        "kepler_adjacent_dihedral_spread",
        "seked_archimedes_pi_22_7_perimeter",
        "khufu_royal_cubits_ratio",
        "earth_moon_seked_radius_ratio",
    }
    assert set(identities.keys()) == expected_keys

    for name, (lhs, rhs) in identities.items():
        _assert_no_float(lhs, f"Identity {name} LHS")
        _assert_no_float(rhs, f"Identity {name} RHS")
        diff = sp.simplify(lhs - rhs)
        assert diff == 0, f"Identity {name} failed: {lhs} - {rhs} = {diff} != 0"


def test_specific_profile_exact_values() -> None:
    """Verifies exact algebraic properties across all four pyramid models."""
    kepler = get_great_pyramid_profile("kepler_golden")
    assert kepler.half_base == sp.Integer(1)
    assert kepler.height == SQRT_PHI
    assert kepler.apothem == PHI
    assert kepler.face_area == PHI
    assert kepler.base_area == sp.Integer(4)
    assert kepler.lateral_area == sp.Integer(4) * PHI
    assert kepler.total_area == sp.Integer(4) + sp.Integer(4) * PHI
    assert kepler.slope_spread == PHI_INV
    assert sp.simplify(kepler.adjacent_dihedral_spread - (sp.Integer(3) * PHI - sp.Integer(4))) == 0
    assert sp.simplify(kepler.opposite_apex_spread - sp.Integer(4) / PHI**3) == 0

    pi_prof = get_great_pyramid_profile("pi_quadrature")
    assert pi_prof.height == sp.Integer(4) / sp.pi
    assert pi_prof.apex_circle_circumference == sp.Integer(8)
    assert pi_prof.base_perimeter == sp.Integer(8)
    assert sp.simplify(pi_prof.slope_spread - sp.Integer(16) / (sp.pi**2 + sp.Integer(16))) == 0

    seked = get_great_pyramid_profile("seked_14_11")
    assert seked.height == sp.Rational(14, 11)
    assert seked.volume == sp.Rational(56, 33)
    assert seked.slope_spread == sp.Rational(196, 317)
    assert seked.adjacent_dihedral_spread == sp.Rational(85848, 100489)
    assert seked.opposite_apex_spread == sp.Rational(94864, 100489)

    oct_prof = get_great_pyramid_profile("half_octahedron")
    assert oct_prof.height == sp.sqrt(2)
    assert oct_prof.apothem == sp.sqrt(3)
    assert oct_prof.lateral_edge == sp.Integer(2)
    assert oct_prof.slope_spread == sp.Rational(2, 3)
    assert oct_prof.adjacent_dihedral_spread == sp.Rational(8, 9)
    assert oct_prof.opposite_apex_spread == sp.Rational(8, 9)


def test_build_kepler_pyramid_solid_baseline_and_centered() -> None:
    """Verifies Kepler pyramid construction, orientation, vacuation, and net unfolding."""
    # Baseline on z = 0
    s_base = build_kepler_pyramid_solid(center_origin=False)
    assert s_base.num_vertices == 5
    assert s_base.num_edges == 8
    assert s_base.num_faces == 5
    assert s_base.euler_characteristic == 2
    assert s_base.are_faces_coplanar()
    _assert_no_float(s_base, "s_base")
    # Base face has normal (0, 0, -4) pointing downward
    n_base = s_base.face_normal(0)
    assert n_base.x == 0 and n_base.y == 0 and n_base.z < 0

    # Centered origin at z = -h/4
    s_cent = build_kepler_pyramid_solid(center_origin=True)
    assert s_cent.num_vertices == 5
    assert s_cent.num_edges == 8
    assert s_cent.num_faces == 5
    assert s_cent.euler_characteristic == 2
    assert s_cent.are_faces_coplanar()
    assert s_cent.is_outward_oriented()
    _assert_no_float(s_cent, "s_cent")

    # Leonardo da Vinci hollow cage vacuate: V=42, E=96, F=48, genus=4
    s_vac = vacuate(s_cent)
    assert s_vac.num_vertices == 42
    assert s_vac.num_edges == 96
    assert s_vac.num_faces == 48
    assert s_vac.euler_characteristic == -6
    assert s_vac.genus == 4
    assert s_vac.are_faces_coplanar()
    _assert_no_float(s_vac, "s_vac")

    # 2D Net Unfolding: 5 faces (1 square base + 4 triangles)
    net_faces = unfold_net_2d(s_cent)
    assert len(net_faces) == 5
    polygon_lengths = sorted(len(f["pts_2d"]) for f in net_faces)  # type: ignore[union-attr]
    assert polygon_lengths == [3, 3, 3, 3, 4]


def test_build_seked_pyramid_solid_unit_and_royal_cubits() -> None:
    """Verifies Seked pyramid dimensions in unit baseline and historical royal cubits."""
    # Unit baseline
    s_unit = build_seked_pyramid_solid(royal_cubits=False, center_origin=False)
    assert s_unit.num_vertices == 5
    assert s_unit.are_faces_coplanar()
    _assert_no_float(s_unit, "s_unit")

    # Unit centered
    s_unit_c = build_seked_pyramid_solid(royal_cubits=False, center_origin=True)
    assert s_unit_c.is_outward_oriented()

    # Historical Khufu Dimensions: 220 cubits half-base, 280 cubits height
    s_cubits = build_seked_pyramid_solid(royal_cubits=True, center_origin=False)
    assert s_cubits.num_vertices == 5
    assert s_cubits.are_faces_coplanar()
    _assert_no_float(s_cubits, "s_cubits")

    v0 = s_cubits.vertices[0]
    assert v0.x == sp.Integer(220)
    assert v0.y == sp.Integer(-220)
    assert v0.z == sp.Integer(0)

    apex = s_cubits.vertices[4]
    assert apex.x == sp.Integer(0)
    assert apex.y == sp.Integer(0)
    assert apex.z == sp.Integer(280)

    # Base edge length is 440 cubits, base area is 440^2 = 193600
    e_sq = (s_cubits.vertices[1].x - s_cubits.vertices[0].x) ** 2 + (
        s_cubits.vertices[1].y - s_cubits.vertices[0].y
    ) ** 2
    assert e_sq == sp.Integer(440) ** 2

    # Centered cubits
    s_cubits_c = build_seked_pyramid_solid(royal_cubits=True, center_origin=True)
    assert s_cubits_c.is_outward_oriented()
    assert s_cubits_c.vertices[4].z == sp.Integer(210)
    assert s_cubits_c.vertices[0].z == sp.Integer(-70)


def test_build_kepler_bipyramid_solid() -> None:
    """Verifies the Golden Square Bipyramid (octahedron-analog) topology and geometry."""
    bip = build_kepler_bipyramid_solid()
    assert bip.num_vertices == 6
    assert bip.num_edges == 12
    assert bip.num_faces == 8
    assert bip.euler_characteristic == 2
    assert bip.genus == 0
    assert bip.are_faces_coplanar()
    assert bip.is_outward_oriented()
    _assert_no_float(bip, "kepler_bipyramid")

    # Equator edge quadrance
    q_eq = (bip.vertices[1].x - bip.vertices[0].x) ** 2 + (
        bip.vertices[1].y - bip.vertices[0].y
    ) ** 2
    assert q_eq == sp.Integer(4)

    # Lateral edge quadrance = 1^2 + 1^2 + SQRT_PHI^2 = PHI + 2
    v_base = bip.vertices[1]
    v_apex_north = bip.vertices[4]
    q_lat = (
        (v_apex_north.x - v_base.x) ** 2
        + (v_apex_north.y - v_base.y) ** 2
        + (v_apex_north.z - v_base.z) ** 2
    )
    assert sp.simplify(q_lat - (PHI + sp.Integer(2))) == 0

    # Apex to apex distance squared = (2*sqrt(phi))^2 = 4*phi
    v_apex_south = bip.vertices[5]
    q_axis = (v_apex_north.z - v_apex_south.z) ** 2
    assert sp.simplify(q_axis - sp.Integer(4) * PHI) == 0


def test_build_kepler_triangle_model_quadrances_and_svg() -> None:
    """Verifies the 2D Kepler Right Triangle construction, metrics, and SVG rendering."""
    model, metrics = build_kepler_triangle_model()
    _assert_no_float(metrics, "kepler_triangle_metrics")

    assert metrics["Q_OA"] == sp.Integer(1)
    assert sp.simplify(metrics["Q_OB"] - PHI) == 0
    assert sp.simplify(metrics["Q_AB"] - (PHI + sp.Integer(1))) == 0
    assert metrics["Q_BH"] == sp.Integer(1)
    assert sp.simplify(metrics["Q_HA"] - (sp.Integer(2) - PHI)) == 0
    assert sp.simplify(metrics["Q_OH"] - (PHI - sp.Integer(1))) == 0
    assert sp.simplify(metrics["ratio_BH_HA"] - PHI**2) == 0

    # Check SVG generation
    svg_str = render_model2d_svg(model, graphic_id="kepler_tri")
    root = ET.fromstring(svg_str)
    assert root.tag.endswith("svg")
    assert root.attrib["data-graphic-id"] == "kepler_tri"
    assert "geom-poly" in svg_str
    assert "geom-circle" in svg_str
    assert "geom-point" in svg_str
    assert "geom-label" in svg_str


def test_build_pyramid_squaring_circle_model_metrics_and_svg() -> None:
    """Verifies the 2D Great Pyramid Squaring the Circle Cosmogram and SVG rendering."""
    model, metrics = build_pyramid_squaring_circle_model()
    _assert_no_float(metrics, "squaring_circle_metrics")

    assert metrics["square_perimeter"] == sp.Integer(8)
    assert metrics["square_area"] == sp.Integer(4)
    assert metrics["apex_circle_radius"] == SQRT_PHI
    assert metrics["earth_radius"] == sp.Integer(1)
    assert metrics["moon_radius"] == SQRT_PHI - sp.Integer(1)
    assert metrics["seked_moon_earth_ratio"] == sp.Rational(3, 11)
    assert (
        metrics["quadrature_perimeter_diff"]
        == sp.Integer(2) * sp.pi * SQRT_PHI - sp.Integer(8)
    )
    assert sp.simplify(metrics["meridian_edge_quadrance"] - (PHI + sp.Integer(1))) == 0

    # Check SVG generation
    svg_str = render_model2d_svg(model, graphic_id="pyramid_squaring_circle")
    root = ET.fromstring(svg_str)
    assert root.tag.endswith("svg")
    assert root.attrib["data-graphic-id"] == "pyramid_squaring_circle"
    assert "geom-poly" in svg_str
    assert "geom-circle" in svg_str
    assert "geom-point" in svg_str
