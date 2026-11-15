"""Exact symbolic geometry of the Great Pyramid, Kepler triangle, and circle quadrature.

Provides 100% exact algebraic models over Q, Q(phi), Q(sqrt(phi)), and Q(pi) for:

- The Great Pyramid architectural profiles (Kepler Golden, Pi-Quadrature, Seked 14:11,
  and Half-Octahedron).
- Certified exact algebraic identities connecting the Kepler Pyramid, Herodotus's area law,
  phi harmonics, and the regular icosahedron.
- 3D Solid3D manifold builders (Kepler Pyramid, Seked Pyramid, and Golden Square Bipyramid).
- 2D geometor.model constructions (Kepler Right Triangle and Squaring the Circle Cosmogram).
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp
from geometor.divine import register_divine_hook
from geometor.model import Model, quadrance

from geometor.polyhedra.model3d.primitives import Point3D, Solid3D, _validate_exact
from geometor.polyhedra.platonic import (
    PHI,
    PHI_INV,
    get_platonic_solid,
    quadrance_3d,
)

# Exact root of the golden ratio: zero float or sp.Float
SQRT_PHI: sp.Expr = sp.sqrt(PHI)


@dataclass(frozen=True)
class PyramidModelProfile:
    """Exact symbolic specification of a Great Pyramid architectural or geometric model.

    Attributes:
        slug: Unique identifier ('kepler_golden', 'pi_quadrature', 'seked_14_11', 'half_octahedron').
        title: Descriptive human-readable title.
        historical_source: Primary source or historical citation.
        half_base: Exact half-base length (unit baseline = 1).
        height: Exact vertical apex height h above base.
        apothem: Exact face altitude (slant height) s = sqrt(half_base^2 + height^2).
        lateral_edge: Exact edge length from base corner to apex.
        base_perimeter: Exact perimeter of square base (8 * half_base).
        apex_circle_circumference: Exact circumference 2 * pi * height.
        base_area: Exact base area (4 * half_base^2).
        face_area: Exact area of one triangular lateral face (half_base * apothem).
        lateral_area: Exact total lateral area of the four triangular faces (4 * face_area).
        total_area: Exact total surface area (base_area + lateral_area).
        volume: Exact solid volume (1/3 * base_area * height).
        slope_spread: Exact Rational Trigonometry face slope spread sin^2(alpha) = h^2 / s^2.
        adjacent_dihedral_spread: Exact spread between normals of adjacent lateral faces.
        opposite_apex_spread: Exact spread between opposite meridian apothems.
    """

    slug: str
    title: str
    historical_source: str
    half_base: sp.Expr
    height: sp.Expr
    apothem: sp.Expr
    lateral_edge: sp.Expr
    base_perimeter: sp.Expr
    apex_circle_circumference: sp.Expr
    base_area: sp.Expr
    face_area: sp.Expr
    lateral_area: sp.Expr
    total_area: sp.Expr
    volume: sp.Expr
    slope_spread: sp.Expr
    adjacent_dihedral_spread: sp.Expr | None
    opposite_apex_spread: sp.Expr

    def __post_init__(self) -> None:
        """Validates that all symbolic parameters contain no floats or sp.Float atoms."""
        _validate_exact(
            self.half_base,
            self.height,
            self.apothem,
            self.lateral_edge,
            self.base_perimeter,
            self.apex_circle_circumference,
            self.base_area,
            self.face_area,
            self.lateral_area,
            self.total_area,
            self.volume,
            self.slope_spread,
            self.opposite_apex_spread,
        )
        if self.adjacent_dihedral_spread is not None:
            _validate_exact(self.adjacent_dihedral_spread)


def _make_kepler_golden_profile() -> PyramidModelProfile:
    """Constructs the exact symbolic Kepler Golden Pyramid profile."""
    h = SQRT_PHI
    s = PHI
    e = sp.sqrt(PHI + sp.Integer(2))
    base_perim = sp.Integer(8)
    apex_circ = sp.Integer(2) * sp.pi * h
    b_area = sp.Integer(4)
    f_area = s
    lat_area = sp.Integer(4) * s
    tot_area = b_area + lat_area
    vol = sp.Rational(4, 3) * h
    slope_sp = PHI_INV
    adj_dih = sp.Integer(3) * PHI - sp.Integer(4)
    opp_apex = sp.Integer(4) / PHI**3

    return PyramidModelProfile(
        slug="kepler_golden",
        title="Kepler Golden Pyramid (Phi-Harmonic)",
        historical_source="Johannes Kepler, Epistola ad Mästlinum (1597); Herodotus, Histories II.124",
        half_base=sp.Integer(1),
        height=h,
        apothem=s,
        lateral_edge=e,
        base_perimeter=base_perim,
        apex_circle_circumference=apex_circ,
        base_area=b_area,
        face_area=f_area,
        lateral_area=lat_area,
        total_area=tot_area,
        volume=vol,
        slope_spread=slope_sp,
        adjacent_dihedral_spread=adj_dih,
        opposite_apex_spread=opp_apex,
    )


def _make_pi_quadrature_profile() -> PyramidModelProfile:
    """Constructs the exact symbolic Pi-Quadrature Circle Squaring profile."""
    h = sp.Integer(4) / sp.pi
    s = sp.sqrt(sp.Integer(1) + sp.Integer(16) / sp.pi**2)
    e = sp.sqrt(sp.Integer(2) + sp.Integer(16) / sp.pi**2)
    base_perim = sp.Integer(8)
    apex_circ = sp.Integer(8)
    b_area = sp.Integer(4)
    f_area = s
    lat_area = sp.Integer(4) * s
    tot_area = b_area + lat_area
    vol = sp.Rational(16, 3) / sp.pi
    slope_sp = sp.Integer(16) / (sp.pi**2 + sp.Integer(16))
    adj_dih = sp.Integer(32) * (sp.pi**2 + sp.Integer(8)) / (sp.pi**2 + sp.Integer(16))**2
    opp_apex = sp.Integer(64) * sp.pi**2 / (sp.pi**2 + sp.Integer(16))**2

    return PyramidModelProfile(
        slug="pi_quadrature",
        title="Pi-Quadrature Pyramid (Circle Squaring)",
        historical_source="John Taylor, The Great Pyramid: Why Was It Built? & Who Built It? (1859)",
        half_base=sp.Integer(1),
        height=h,
        apothem=s,
        lateral_edge=e,
        base_perimeter=base_perim,
        apex_circle_circumference=apex_circ,
        base_area=b_area,
        face_area=f_area,
        lateral_area=lat_area,
        total_area=tot_area,
        volume=vol,
        slope_spread=slope_sp,
        adjacent_dihedral_spread=adj_dih,
        opposite_apex_spread=opp_apex,
    )


def _make_seked_14_11_profile() -> PyramidModelProfile:
    """Constructs the exact symbolic Seked 14:11 Khufu Standard profile."""
    h = sp.Rational(14, 11)
    s = sp.sqrt(sp.Rational(317, 121))
    e = sp.sqrt(sp.Rational(438, 121))
    base_perim = sp.Integer(8)
    apex_circ = sp.Rational(28, 11) * sp.pi
    b_area = sp.Integer(4)
    f_area = s
    lat_area = sp.Integer(4) * s
    tot_area = b_area + lat_area
    vol = sp.Rational(56, 33)
    slope_sp = sp.Rational(196, 317)
    adj_dih = sp.Rational(85848, 100489)
    opp_apex = sp.Rational(94864, 100489)

    return PyramidModelProfile(
        slug="seked_14_11",
        title="Seked 5 1/2 Palms Pyramid (14:11 Khufu Standard)",
        historical_source="Rhind Mathematical Papyrus (c. 1550 BCE), Problems 56–60; Petrie (1883)",
        half_base=sp.Integer(1),
        height=h,
        apothem=s,
        lateral_edge=e,
        base_perimeter=base_perim,
        apex_circle_circumference=apex_circ,
        base_area=b_area,
        face_area=f_area,
        lateral_area=lat_area,
        total_area=tot_area,
        volume=vol,
        slope_spread=slope_sp,
        adjacent_dihedral_spread=adj_dih,
        opposite_apex_spread=opp_apex,
    )


def _make_half_octahedron_profile() -> PyramidModelProfile:
    """Constructs the exact symbolic Half-Octahedron profile."""
    h = sp.sqrt(2)
    s = sp.sqrt(3)
    e = sp.Integer(2)
    base_perim = sp.Integer(8)
    apex_circ = sp.Integer(2) * sp.pi * h
    b_area = sp.Integer(4)
    f_area = s
    lat_area = sp.Integer(4) * s
    tot_area = b_area + lat_area
    vol = sp.Rational(4, 3) * h
    slope_sp = sp.Rational(2, 3)
    adj_dih = sp.Rational(8, 9)
    opp_apex = sp.Rational(8, 9)

    return PyramidModelProfile(
        slug="half_octahedron",
        title="Half-Octahedron Pyramid (Equilateral Triangular Faces)",
        historical_source="Euclid, Elements Book XIII.14",
        half_base=sp.Integer(1),
        height=h,
        apothem=s,
        lateral_edge=e,
        base_perimeter=base_perim,
        apex_circle_circumference=apex_circ,
        base_area=b_area,
        face_area=f_area,
        lateral_area=lat_area,
        total_area=tot_area,
        volume=vol,
        slope_spread=slope_sp,
        adjacent_dihedral_spread=adj_dih,
        opposite_apex_spread=opp_apex,
    )


def get_great_pyramid_profiles() -> dict[str, PyramidModelProfile]:
    """Returns mapping of canonical Great Pyramid model profiles.

    Returns:
        Mapping of slug identifiers to PyramidModelProfile specifications.
    """
    return {
        "kepler_golden": _make_kepler_golden_profile(),
        "pi_quadrature": _make_pi_quadrature_profile(),
        "seked_14_11": _make_seked_14_11_profile(),
        "half_octahedron": _make_half_octahedron_profile(),
    }


def get_great_pyramid_profile(slug: str) -> PyramidModelProfile:
    """Retrieves a single Great Pyramid model profile by slug.

    Args:
        slug: Unique identifier ('kepler_golden', 'pi_quadrature', 'seked_14_11', 'half_octahedron').

    Returns:
        Corresponding PyramidModelProfile.

    Raises:
        KeyError: If slug is not recognized.
    """
    profiles = get_great_pyramid_profiles()
    if slug not in profiles:
        raise KeyError(
            f"Unknown pyramid model profile: {slug!r}. Available: {list(profiles.keys())}"
        )
    return profiles[slug]


def verify_kepler_pyramid_identities() -> dict[str, tuple[sp.Expr, sp.Expr]]:
    """Certifies the eleven foundational exact identities of the Great Pyramid models.

    Certifies Herodotus's area law, Kepler's right triangle geometric progression,
    golden ratio area ratios, the icosahedron circumquadrance bridge, Rational
    Trigonometry slope and dihedral spreads, and Rhind Papyrus Seked 14:11 relations.

    Returns:
        Mapping of identity names to exact (lhs, rhs) pairs where
        sp.simplify(lhs - rhs) == 0.
    """
    kepler = get_great_pyramid_profile("kepler_golden")
    ico = get_platonic_solid("icosahedron")
    ico_circumquadrance = quadrance_3d(ico.vertices[0])

    return {
        "pythagorean_geometric_mean": (sp.Integer(1) + PHI, PHI**2),
        "herodotus_face_area_equals_height_squared": (kepler.face_area, kepler.height**2),
        "golden_area_ratio_lateral_to_base": (kepler.lateral_area / kepler.base_area, PHI),
        "golden_area_ratio_total_to_lateral": (kepler.total_area / kepler.lateral_area, PHI),
        "golden_area_additive_law": (kepler.base_area + kepler.lateral_area, kepler.total_area),
        "icosahedron_circumradius_edge_bridge": (kepler.lateral_edge**2, ico_circumquadrance),
        "kepler_slope_spread_equals_inv_phi": (kepler.slope_spread, PHI_INV),
        "kepler_adjacent_dihedral_spread": (
            kepler.adjacent_dihedral_spread,
            sp.Integer(3) * PHI - sp.Integer(4),
        ),
        "seked_archimedes_pi_22_7_perimeter": (
            sp.Integer(2) * sp.Rational(22, 7) * sp.Rational(14, 11),
            sp.Integer(8),
        ),
        "khufu_royal_cubits_ratio": (sp.Rational(280, 220), sp.Rational(14, 11)),
        "earth_moon_seked_radius_ratio": (
            sp.Rational(14, 11) - sp.Integer(1),
            sp.Rational(3, 11),
        ),
    }


def build_kepler_pyramid_solid(*, center_origin: bool = False) -> Solid3D:
    """Constructs the exact 3D Solid3D model of the Kepler Golden Pyramid over Q(sqrt(phi)).

    When center_origin is False (default), the square base rests on z = 0 with corners
    (±1, ±1, 0) and apex at (0, 0, sqrt(phi)).
    When center_origin is True, the Z coordinates are shifted downward by h/4 = sqrt(phi)/4
    so that the centroid is at (0, 0, 0), placing the origin strictly inside the solid.
    This guarantees is_outward_oriented(), vacuate(), and polar_dual() behave as valid 3D manifolds.

    Args:
        center_origin: If True, shifts vertices along Z by -h/4 to center the solid.

    Returns:
        Exact symbolic Solid3D instance.
    """
    h = SQRT_PHI
    z0 = -h / sp.Integer(4) if center_origin else sp.Integer(0)
    za = sp.Integer(3) * h / sp.Integer(4) if center_origin else h

    verts = (
        Point3D(sp.Integer(1), sp.Integer(-1), z0),
        Point3D(sp.Integer(1), sp.Integer(1), z0),
        Point3D(sp.Integer(-1), sp.Integer(1), z0),
        Point3D(sp.Integer(-1), sp.Integer(-1), z0),
        Point3D(sp.Integer(0), sp.Integer(0), za),
    )
    faces = (
        (0, 3, 2, 1),
        (0, 1, 4),
        (1, 2, 4),
        (2, 3, 4),
        (3, 0, 4),
    )
    face_roles = ("base", "pyramid", "pyramid", "pyramid", "pyramid")
    slug = "kepler_pyramid_centered" if center_origin else "kepler_pyramid"
    title = (
        "Kepler Golden Pyramid (Centered)"
        if center_origin
        else "Kepler Golden Pyramid"
    )
    return Solid3D(
        slug=slug,
        title=title,
        vertices=verts,
        faces=faces,
        face_roles=face_roles,
    )


def build_seked_pyramid_solid(
    *,
    royal_cubits: bool = False,
    center_origin: bool = False,
) -> Solid3D:
    """Constructs the exact 3D Solid3D model of the Seked 14:11 Khufu Pyramid.

    When royal_cubits is True, half-base is 220 and height is 280 (base 440 x 440 cubits,
    height 280 cubits).
    When royal_cubits is False (default), unit half-base 1 and height 14/11 are used.
    When center_origin is True, vertices are shifted along Z by -h/4 so the origin
    is at the solid's interior centroid.

    Args:
        royal_cubits: If True, uses historical Khufu dimensions (220, 280 cubits).
        center_origin: If True, shifts vertices along Z by -h/4 to center the solid.

    Returns:
        Exact symbolic Solid3D instance.
    """
    b = sp.Integer(220) if royal_cubits else sp.Integer(1)
    h = sp.Integer(280) if royal_cubits else sp.Rational(14, 11)
    z0 = -h / sp.Integer(4) if center_origin else sp.Integer(0)
    za = sp.Integer(3) * h / sp.Integer(4) if center_origin else h

    verts = (
        Point3D(b, -b, z0),
        Point3D(b, b, z0),
        Point3D(-b, b, z0),
        Point3D(-b, -b, z0),
        Point3D(sp.Integer(0), sp.Integer(0), za),
    )
    faces = (
        (0, 3, 2, 1),
        (0, 1, 4),
        (1, 2, 4),
        (2, 3, 4),
        (3, 0, 4),
    )
    face_roles = ("base", "pyramid", "pyramid", "pyramid", "pyramid")
    slug = (
        f"seked_pyramid_{'cubits' if royal_cubits else 'unit'}"
        f"{'_centered' if center_origin else ''}"
    )
    title = (
        f"Seked 14:11 Pyramid ({'Royal Cubits' if royal_cubits else 'Unit'}"
        f"{', Centered' if center_origin else ''})"
    )
    return Solid3D(
        slug=slug,
        title=title,
        vertices=verts,
        faces=faces,
        face_roles=face_roles,
    )


def build_kepler_bipyramid_solid() -> Solid3D:
    """Constructs the exact 3D Golden Square Bipyramid over Q(sqrt(phi)).

    Formed by reflecting the Kepler Golden Pyramid across its square base z = 0,
    producing an 8-faced convex polyhedron with 6 vertices:
    (±1, ±1, 0), (0, 0, sqrt(phi)), and (0, 0, -sqrt(phi)).

    Returns:
        Exact symbolic Solid3D instance centered at (0, 0, 0).
    """
    h = SQRT_PHI
    verts = (
        Point3D(sp.Integer(1), sp.Integer(-1), sp.Integer(0)),
        Point3D(sp.Integer(1), sp.Integer(1), sp.Integer(0)),
        Point3D(sp.Integer(-1), sp.Integer(1), sp.Integer(0)),
        Point3D(sp.Integer(-1), sp.Integer(-1), sp.Integer(0)),
        Point3D(sp.Integer(0), sp.Integer(0), h),
        Point3D(sp.Integer(0), sp.Integer(0), -h),
    )
    faces = (
        (0, 1, 4),
        (1, 2, 4),
        (2, 3, 4),
        (3, 0, 4),
        (1, 0, 5),
        (2, 1, 5),
        (3, 2, 5),
        (0, 3, 5),
    )
    face_roles = ("pyramid",) * 8
    return Solid3D(
        slug="kepler_bipyramid",
        title="Kepler Golden Square Bipyramid",
        vertices=verts,
        faces=faces,
        face_roles=face_roles,
    )


def build_kepler_triangle_model() -> tuple[Model, dict[str, sp.Expr]]:
    """Constructs the exact 2D Kepler Right Triangle model over Q(sqrt(phi)).

    Constructs unit base O(0, 0), A(1, 0), W(-1, 0), midpoint E(1/2, 0),
    north point N(0, 1), golden section point P(phi, 0), midpoint K((phi - 1)/2, 0),
    Thales circle cutting positive Y-axis at B(0, sqrt(phi)), Kepler Right Triangle
    OAB, and altitude foot H dividing hypotenuse AB into golden major BH = 1
    and minor HA = phi - 1 = 1/phi.

    Returns:
        Tuple of (Model, metrics_dict) with certified exact SymPy quadrances.
    """
    model = Model("kepler_triangle", auto_intersect=False)
    register_divine_hook(model)

    pt_o = model.set_point(sp.Integer(0), sp.Integer(0), classes=["center"], ID="O")
    pt_a = model.set_point(sp.Integer(1), sp.Integer(0), classes=["given"], ID="A")
    pt_w = model.set_point(sp.Integer(-1), sp.Integer(0), classes=["given"], ID="W")
    pt_e = model.set_point(sp.Rational(1, 2), sp.Integer(0), classes=["midpoint"], ID="E")
    pt_n = model.set_point(sp.Integer(0), sp.Integer(1), classes=["given"], ID="N")
    pt_p = model.set_point(PHI, sp.Integer(0), classes=["golden"], ID="P")
    pt_k = model.set_point(
        (PHI - sp.Integer(1)) / sp.Integer(2),
        sp.Integer(0),
        classes=["midpoint"],
        ID="K",
    )
    pt_b = model.set_point(sp.Integer(0), SQRT_PHI, classes=["vertex"], ID="B")
    pt_h = model.set_point(
        PHI - sp.Integer(1),
        (sp.Integer(2) - PHI) * SQRT_PHI,
        classes=["altitude"],
        ID="H",
    )

    model.construct_circle(pt_e, pt_n, classes=["golden_swing"], ID="cEN")
    model.construct_circle(pt_k, pt_p, classes=["thales"], ID="cThales")

    model.construct_segment(pt_w, pt_p, classes=["baseline"], ID="sWP")
    model.construct_segment(pt_o, pt_a, classes=["kepler_triangle"], ID="sOA")
    model.construct_segment(pt_o, pt_b, classes=["kepler_triangle"], ID="sOB")
    model.construct_segment(pt_a, pt_b, classes=["kepler_triangle"], ID="sAB")
    model.construct_segment(pt_o, pt_h, classes=["altitude"], ID="sOH")
    model.construct_segment(pt_b, pt_h, classes=["golden_major"], ID="sBH")
    model.construct_segment(pt_h, pt_a, classes=["golden_minor"], ID="sHA")

    model.construct_polygon([pt_o, pt_a, pt_b], classes=["kepler_triangle"], ID="triOAB")

    q_oa = quadrance(pt_o, pt_a)
    q_ob = quadrance(pt_o, pt_b)
    q_ab = quadrance(pt_a, pt_b)
    q_bh = quadrance(pt_b, pt_h)
    q_ha = quadrance(pt_h, pt_a)
    q_oh = quadrance(pt_o, pt_h)
    ratio_bh_ha = sp.simplify(q_bh / q_ha)

    metrics: dict[str, sp.Expr] = {
        "Q_OA": q_oa,
        "Q_OB": q_ob,
        "Q_AB": q_ab,
        "Q_BH": q_bh,
        "Q_HA": q_ha,
        "Q_OH": q_oh,
        "ratio_BH_HA": ratio_bh_ha,
        "Q_BH_over_Q_HA": ratio_bh_ha,
    }

    return model, metrics


def build_pyramid_squaring_circle_model() -> tuple[Model, dict[str, sp.Expr]]:
    """Constructs the Great Pyramid Squaring the Circle & Earth-Moon Cosmogram in 2D.

    Constructs:

    - Base square corners SW(-1, -1), SE(1, -1), NE(1, 1), NW(-1, 1) of side 2,
      perimeter 8, and area 4.
    - Meridian pyramid triangle on base W(-1, 0) to E(1, 0) with apex S(0, sqrt(phi)).
    - Apex circle centered at O(0, 0) passing through S(0, sqrt(phi)) with radius
      R = sqrt(phi) and circumference 2 * pi * sqrt(phi) ≈ 8.
    - Inscribed Earth circle centered at O(0, 0) passing through T(0, 1) and E(1, 0)
      tangent to the square of side 2 (radius 1).
    - Tangent Moon circle centered at apex S(0, sqrt(phi)) tangent to the Earth circle
      at T(0, 1) with radius sqrt(phi) - 1 ≈ 3/11.

    Returns:
        Tuple of (Model, metrics_dict) certifying exact symbolic circle-squaring metrics.
    """
    model = Model("pyramid_squaring_circle", auto_intersect=False)

    pt_o = model.set_point(sp.Integer(0), sp.Integer(0), classes=["center"], ID="O")
    pt_sw = model.set_point(sp.Integer(-1), sp.Integer(-1), classes=["square_vertex"], ID="SW")
    pt_se = model.set_point(sp.Integer(1), sp.Integer(-1), classes=["square_vertex"], ID="SE")
    pt_ne = model.set_point(sp.Integer(1), sp.Integer(1), classes=["square_vertex"], ID="NE")
    pt_nw = model.set_point(sp.Integer(-1), sp.Integer(1), classes=["square_vertex"], ID="NW")

    pt_w = model.set_point(sp.Integer(-1), sp.Integer(0), classes=["base_point"], ID="W")
    pt_e = model.set_point(sp.Integer(1), sp.Integer(0), classes=["base_point"], ID="E")
    pt_t = model.set_point(sp.Integer(0), sp.Integer(1), classes=["tangent_point"], ID="T")
    pt_s = model.set_point(sp.Integer(0), SQRT_PHI, classes=["apex"], ID="S")

    model.construct_polygon(
        [pt_sw, pt_se, pt_ne, pt_nw], classes=["square"], ID="poly_Square"
    )
    model.construct_segment(pt_sw, pt_se, ID="s_SW_SE")
    model.construct_segment(pt_se, pt_ne, ID="s_SE_NE")
    model.construct_segment(pt_ne, pt_nw, ID="s_NE_NW")
    model.construct_segment(pt_nw, pt_sw, ID="s_NW_SW")

    model.construct_polygon(
        [pt_w, pt_e, pt_s], classes=["meridian_triangle"], ID="poly_Pyramid"
    )
    model.construct_segment(pt_w, pt_e, ID="s_WE")
    model.construct_segment(pt_e, pt_s, ID="s_ES")
    model.construct_segment(pt_s, pt_w, ID="s_SW")
    model.construct_segment(pt_o, pt_s, classes=["altitude"], ID="s_OS")

    model.construct_circle(pt_o, pt_s, classes=["apex_circle"], ID="c_Apex")
    model.construct_circle(pt_o, pt_t, classes=["earth_circle"], ID="c_Earth")
    model.construct_circle(pt_s, pt_t, classes=["moon_circle"], ID="c_Moon")

    q_meridian_edge = quadrance(pt_e, pt_s)

    metrics: dict[str, sp.Expr] = {
        "square_side": sp.Integer(2),
        "square_perimeter": sp.Integer(8),
        "square_area": sp.Integer(4),
        "apex_circle_radius": SQRT_PHI,
        "apex_circle_circumference": sp.Integer(2) * sp.pi * SQRT_PHI,
        "earth_radius": sp.Integer(1),
        "earth_circumference": sp.Integer(2) * sp.pi,
        "moon_radius": SQRT_PHI - sp.Integer(1),
        "moon_circumference": sp.Integer(2) * sp.pi * (SQRT_PHI - sp.Integer(1)),
        "moon_to_earth_radius_ratio": SQRT_PHI - sp.Integer(1),
        "seked_moon_earth_ratio": sp.Rational(3, 11),
        "quadrature_perimeter_diff": sp.Integer(2) * sp.pi * SQRT_PHI - sp.Integer(8),
        "meridian_edge_quadrance": q_meridian_edge,
    }

    return model, metrics


__all__ = [
    "PyramidModelProfile",
    "SQRT_PHI",
    "build_kepler_bipyramid_solid",
    "build_kepler_pyramid_solid",
    "build_kepler_triangle_model",
    "build_pyramid_squaring_circle_model",
    "build_seked_pyramid_solid",
    "get_great_pyramid_profile",
    "get_great_pyramid_profiles",
    "verify_kepler_pyramid_identities",
]
