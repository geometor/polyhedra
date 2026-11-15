"""Tests for exact symbolic 3D primitives, bridge, and polyhedral operators."""

from __future__ import annotations

import math

import pytest
import sympy as sp

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
from geometor.polyhedra.platonic import PHI, get_platonic_solids


def test_vector3d_primitives() -> None:
    """Tests exact Vector3D construction, operations, and float rejection."""
    v1 = Vector3D(sp.Integer(1), sp.Integer(2), sp.Integer(3))
    v2 = Vector3D(sp.Integer(4), sp.Integer(5), sp.Integer(6))

    # Float rejections
    with pytest.raises(TypeError):
        Vector3D(1.0, 2, 3)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        Vector3D(sp.Float(1.0), sp.Integer(2), sp.Integer(3))

    # Algebra
    v_add = v1 + v2
    assert v_add == Vector3D(sp.Integer(5), sp.Integer(7), sp.Integer(9))

    v_sub = v2 - v1
    assert v_sub == Vector3D(sp.Integer(3), sp.Integer(3), sp.Integer(3))

    v_neg = -v1
    assert v_neg == Vector3D(sp.Integer(-1), sp.Integer(-2), sp.Integer(-3))

    v_mul = v1 * sp.Rational(2, 3)
    assert v_mul == Vector3D(sp.Rational(2, 3), sp.Rational(4, 3), sp.Integer(2))
    assert sp.Rational(2, 3) * v1 == v_mul

    # Dot, cross, quadrance
    dot = v1.dot(v2)
    assert dot == sp.Integer(32)

    cross = v1.cross(v2)
    assert cross == Vector3D(sp.Integer(-3), sp.Integer(6), sp.Integer(-3))
    assert cross.dot(v1) == 0
    assert cross.dot(v2) == 0

    assert v1.quadrance() == sp.Integer(14)
    assert v1.to_tuple() == (sp.Integer(1), sp.Integer(2), sp.Integer(3))


def test_point3d_primitives() -> None:
    """Tests exact Point3D construction, displacement, lerp, and float rejection."""
    p1 = Point3D(sp.Integer(0), sp.Integer(0), sp.Integer(0))
    p2 = Point3D(sp.Integer(2), sp.Integer(4), sp.Integer(6))

    with pytest.raises(TypeError):
        Point3D(0.5, 0, 0)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        p1.scale(1.5)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        p1.lerp(p2, 0.5)  # type: ignore[arg-type]

    disp = p1.vector_to(p2)
    assert disp == Vector3D(sp.Integer(2), sp.Integer(4), sp.Integer(6))
    assert p1.quadrance_to(p2) == sp.Integer(56)

    mid = p1.lerp(p2, sp.Rational(1, 2))
    assert mid == Point3D(sp.Integer(1), sp.Integer(2), sp.Integer(3))

    scaled = mid.scale(sp.Integer(3))
    assert scaled == Point3D(sp.Integer(3), sp.Integer(6), sp.Integer(9))

    translated = p1 + disp
    assert translated == p2
    assert p2.to_tuple() == (sp.Integer(2), sp.Integer(4), sp.Integer(6))
    assert p2.to_vector() == disp


def test_line_plane_sphere_primitives() -> None:
    """Tests Line3D, Plane3D, and Sphere3D exact intersections and containment."""
    p1 = Point3D(sp.Integer(0), sp.Integer(0), sp.Integer(0))
    p2 = Point3D(sp.Integer(0), sp.Integer(0), sp.Integer(2))
    line = Line3D(p1, p2)
    assert line.direction() == Vector3D(sp.Integer(0), sp.Integer(0), sp.Integer(2))

    # Plane from points
    p_x = Point3D(sp.Integer(1), sp.Integer(0), sp.Integer(1))
    p_y = Point3D(sp.Integer(0), sp.Integer(1), sp.Integer(1))
    p_z = Point3D(sp.Integer(0), sp.Integer(0), sp.Integer(1))
    plane = Plane3D.from_points(p_x, p_y, p_z)
    assert plane.contains(p_x)
    assert plane.contains(p_y)
    assert plane.contains(p_z)

    with pytest.raises(ValueError):
        Plane3D.from_points(p1, p2, Point3D(sp.Integer(0), sp.Integer(0), sp.Integer(3)))

    # Intersect segment
    hit = plane.intersect_segment(p1, p2)
    assert hit is not None
    assert hit == Point3D(sp.Integer(0), sp.Integer(0), sp.Integer(1))

    # Non-intersecting segment
    p_above1 = Point3D(sp.Integer(0), sp.Integer(0), sp.Integer(2))
    p_above2 = Point3D(sp.Integer(0), sp.Integer(0), sp.Integer(4))
    assert plane.intersect_segment(p_above1, p_above2) is None

    # Sphere
    sphere = Sphere3D(p1, sp.Integer(4))
    assert sphere.contains(Point3D(sp.Integer(2), sp.Integer(0), sp.Integer(0)))
    assert sphere.contains(Point3D(sp.Integer(0), sp.Integer(2), sp.Integer(0)))
    assert not sphere.contains(Point3D(sp.Integer(1), sp.Integer(1), sp.Integer(1)))


def test_solid3d_from_platonic() -> None:
    """Verifies that all 5 Platonic solids instantiate exact Solid3D instances."""
    solids = get_platonic_solids()
    for solid_raw in solids.values():
        solid = Solid3D.from_regular_solid(solid_raw)
        assert solid.euler_characteristic == 2
        assert solid.genus == 0
        assert solid.are_faces_coplanar()
        assert solid.is_outward_oriented()
        assert len(solid.edges) == len(solid_raw.edges)
        assert len(solid.faces) == len(solid_raw.faces)
        assert len(solid.vertices) == len(solid_raw.vertices)


def test_slice_solid_to_model() -> None:
    """Tests exact planar slicing of Cube and Octahedron into 2D GEOMETOR Model."""
    solids = get_platonic_solids()
    cube = Solid3D.from_regular_solid(solids["hexahedron"])

    # Slice cube with horizontal plane z = 0
    slice_plane = Plane3D(sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(0))
    u_axis = Vector3D(sp.Integer(1), sp.Integer(0), sp.Integer(0))
    v_axis = Vector3D(sp.Integer(0), sp.Integer(1), sp.Integer(0))

    model = slice_solid_to_model(cube, slice_plane, u_axis, v_axis, name="cube_slice")
    assert len(model.points) == 4
    assert len(model.polygons) == 1
    assert len(model.segments) == 4

    # Points should have exact coordinates in {-1, 1}
    for pt in model.points:
        assert not pt.x.has(sp.Float)
        assert not pt.y.has(sp.Float)
        assert abs(pt.x) == 1
        assert abs(pt.y) == 1


def _sat_polygons_overlap(
    poly1: list[tuple[float, float]],
    poly2: list[tuple[float, float]],
    eps: float = 1e-5,
) -> bool:
    """Checks if interiors of two 2D convex polygons overlap via Separating Axis Theorem."""
    for poly in (poly1, poly2):
        n = len(poly)
        for i in range(n):
            p_a = poly[i]
            p_b = poly[(i + 1) % n]
            edge = (p_b[0] - p_a[0], p_b[1] - p_a[1])
            normal = (-edge[1], edge[0])
            norm = math.hypot(normal[0], normal[1])
            if norm < 1e-12:
                continue
            axis = (normal[0] / norm, normal[1] / norm)

            proj1 = [pt[0] * axis[0] + pt[1] * axis[1] for pt in poly1]
            proj2 = [pt[0] * axis[0] + pt[1] * axis[1] for pt in poly2]
            min1, max1 = min(proj1), max(proj1)
            min2, max2 = min(proj2), max(proj2)

            if max1 <= min2 + eps or max2 <= min1 + eps:
                return False
    return True


def test_unfold_net_2d_platonic_no_overlaps() -> None:
    """Verifies that 2D net unfolding produces zero overlapping faces for all 5 Platonic solids."""
    solids = get_platonic_solids()
    for slug, solid_raw in solids.items():
        solid = Solid3D.from_regular_solid(solid_raw)
        net = unfold_net_2d(solid)

        assert len(net) == solid.num_faces
        assert net[0]["parent_face"] is None
        assert net[0]["hinge_2d"] is None

        for idx in range(1, len(net)):
            assert net[idx]["parent_face"] is not None
            assert net[idx]["hinge_2d"] is not None

        # Overlap check
        for i in range(len(net)):
            pts_i = net[i]["pts_2d"]
            assert isinstance(pts_i, list)
            for j in range(i + 1, len(net)):
                pts_j = net[j]["pts_2d"]
                assert isinstance(pts_j, list)
                overlaps = _sat_polygons_overlap(pts_i, pts_j)
                assert not overlaps, f"Faces {i} and {j} overlap in {slug} net!"


def test_vacuate_platonic() -> None:
    """Verifies Leonardo's vacuate operator on all 5 Platonic solids."""
    solids = get_platonic_solids()
    for slug, solid_raw in solids.items():
        solid = Solid3D.from_regular_solid(solid_raw)
        vac = vacuate(solid)

        v = solid.num_vertices
        e = solid.num_edges
        f = solid.num_faces

        assert vac.num_vertices == 2 * v + 4 * e
        assert vac.num_faces == 6 * e
        assert vac.num_edges == 12 * e
        assert vac.euler_characteristic == 4 - 2 * f
        assert vac.genus == f - 1
        assert vac.are_faces_coplanar(), f"Not all quads coplanar in vacuate {slug}"
        assert vac.is_outward_oriented(), f"Orientation mismatch in vacuate {slug}"

    # Float rejection
    with pytest.raises(TypeError):
        vacuate(Solid3D.from_regular_solid(solids["tetrahedron"]), aperture=0.5)  # type: ignore[arg-type]


def test_rectify_platonic() -> None:
    """Verifies Pacioli's rectify operator producing Archimedean core polyhedra."""
    solids = get_platonic_solids()

    # Tetrahedron -> Octahedron
    tet = Solid3D.from_regular_solid(solids["tetrahedron"])
    rec_tet = rectify(tet)
    assert rec_tet.num_vertices == 6
    assert rec_tet.num_faces == 8
    assert rec_tet.num_edges == 12
    assert rec_tet.euler_characteristic == 2
    assert rec_tet.are_faces_coplanar()
    assert rec_tet.is_outward_oriented()

    # Hexahedron -> Cuboctahedron
    cube = Solid3D.from_regular_solid(solids["hexahedron"])
    rec_cube = rectify(cube)
    assert rec_cube.num_vertices == 12
    assert rec_cube.num_faces == 14  # 6 squares + 8 triangles
    assert rec_cube.num_edges == 24
    assert rec_cube.euler_characteristic == 2
    assert rec_cube.are_faces_coplanar()
    assert rec_cube.is_outward_oriented()

    # Octahedron -> Cuboctahedron
    octa = Solid3D.from_regular_solid(solids["octahedron"])
    rec_octa = rectify(octa)
    assert rec_octa.num_vertices == 12
    assert rec_octa.num_faces == 14
    assert rec_octa.num_edges == 24
    assert rec_octa.euler_characteristic == 2
    assert rec_octa.are_faces_coplanar()
    assert rec_octa.is_outward_oriented()

    # Dodecahedron -> Icosidodecahedron
    dodec = Solid3D.from_regular_solid(solids["dodecahedron"])
    rec_dodec = rectify(dodec)
    assert rec_dodec.num_vertices == 30
    assert rec_dodec.num_faces == 32  # 12 pentagons + 20 triangles
    assert rec_dodec.num_edges == 60
    assert rec_dodec.euler_characteristic == 2
    assert rec_dodec.are_faces_coplanar()
    assert rec_dodec.is_outward_oriented()

    # Icosahedron -> Icosidodecahedron
    ico = Solid3D.from_regular_solid(solids["icosahedron"])
    rec_ico = rectify(ico)
    assert rec_ico.num_vertices == 30
    assert rec_ico.num_faces == 32
    assert rec_ico.num_edges == 60
    assert rec_ico.euler_characteristic == 2
    assert rec_ico.are_faces_coplanar()
    assert rec_ico.is_outward_oriented()


def test_truncate_platonic() -> None:
    """Verifies truncate operator producing Archimedean truncated solids."""
    solids = get_platonic_solids()
    for slug, solid_raw in solids.items():
        solid = Solid3D.from_regular_solid(solid_raw)
        trunc = truncate(solid, ratio=sp.Rational(1, 3))

        e = solid.num_edges
        f = solid.num_faces
        v = solid.num_vertices

        assert trunc.num_vertices == 2 * e
        assert trunc.num_faces == f + v
        assert trunc.num_edges == 3 * e
        assert trunc.euler_characteristic == 2
        assert trunc.are_faces_coplanar(), f"Truncated {slug} faces not coplanar"
        assert trunc.is_outward_oriented(), f"Truncated {slug} not outward oriented"

    with pytest.raises(TypeError):
        truncate(Solid3D.from_regular_solid(solids["tetrahedron"]), ratio=0.33)  # type: ignore[arg-type]


def test_elevate_equilateral() -> None:
    """Verifies elevate operator producing exact equilateral face pyramids."""
    solids = get_platonic_solids()

    # Test all 5 Platonic solids
    for slug, solid_raw in solids.items():
        solid = Solid3D.from_regular_solid(solid_raw)
        el = elevate(solid)
        assert el.num_faces == sum(len(f) for f in solid.faces)
        assert el.num_vertices == solid.num_vertices + solid.num_faces
        assert el.are_faces_coplanar()
        assert el.is_outward_oriented()

        # Check equilateral property: lateral edges must equal base edge
        f0 = solid.faces[0]
        s2 = solid.vertices[f0[0]].quadrance_to(solid.vertices[f0[1]])
        apex = el.vertices[solid.num_vertices]
        for vi in f0:
            dist2 = apex.quadrance_to(solid.vertices[vi])
            assert sp.simplify(dist2 - s2) == 0, f"Apex distance mismatch in elevate {slug}"

    # Octahedron Stella Octangula: 24 equilateral triangles, 14 vertices
    octa = Solid3D.from_regular_solid(solids["octahedron"])
    stella = elevate(octa)
    assert stella.num_faces == 24
    assert stella.num_vertices == 14
    assert stella.num_edges == 36

    # Test on rectified solids (Cuboctahedron and Icosidodecahedron)
    cube = Solid3D.from_regular_solid(solids["hexahedron"])
    cubocta = rectify(cube)
    el_cubocta = elevate(cubocta)
    assert el_cubocta.num_faces == 6 * 4 + 8 * 3  # 48 triangles
    assert el_cubocta.are_faces_coplanar()

    dodec = Solid3D.from_regular_solid(solids["dodecahedron"])
    icosidodec = rectify(dodec)
    el_icosidodec = elevate(icosidodec)
    assert el_icosidodec.num_faces == 12 * 5 + 20 * 3  # 120 triangles
    assert el_icosidodec.are_faces_coplanar()


def test_polar_dual_rhombic_solids() -> None:
    """Verifies polar_dual on Cuboctahedron and Icosidodecahedron."""
    solids = get_platonic_solids()

    # Rhombic Dodecahedron from rectify(cube)
    cube = Solid3D.from_regular_solid(solids["hexahedron"])
    cubocta = rectify(cube)
    rd = polar_dual(cubocta)

    assert rd.num_faces == 12
    assert rd.num_vertices == 14
    assert rd.num_edges == 24
    assert rd.euler_characteristic == 2
    assert rd.are_faces_coplanar()
    assert rd.is_outward_oriented()

    # Verify all 12 faces are congruent rhombi with diagonal ratio sqrt(2)
    for f in rd.faces:
        assert len(f) == 4
        p0, p1, p2, p3 = [rd.vertices[idx] for idx in f]
        d1_q = p0.quadrance_to(p2)
        d2_q = p1.quadrance_to(p3)
        ratio_q = sp.simplify(max(d1_q, d2_q) / min(d1_q, d2_q))
        assert ratio_q == sp.Integer(2)
        assert sp.simplify(sp.sqrt(ratio_q) - sp.sqrt(2)) == 0

    # Rhombic Triacontahedron from rectify(dodecahedron)
    dodec = Solid3D.from_regular_solid(solids["dodecahedron"])
    icosidodec = rectify(dodec)
    rt = polar_dual(icosidodec)

    assert rt.num_faces == 30
    assert rt.num_vertices == 32
    assert rt.num_edges == 60
    assert rt.euler_characteristic == 2
    assert rt.are_faces_coplanar()
    assert rt.is_outward_oriented()

    # Verify all 30 faces are congruent Golden Rhombi with diagonal ratio PHI
    for f in rt.faces:
        assert len(f) == 4
        p0, p1, p2, p3 = [rt.vertices[idx] for idx in f]
        d1_q = p0.quadrance_to(p2)
        d2_q = p1.quadrance_to(p3)
        ratio_q = sp.simplify(max(d1_q, d2_q) / min(d1_q, d2_q))
        assert sp.simplify(ratio_q - PHI**2) == 0
        assert sp.simplify(sp.sqrt(ratio_q) - PHI) == 0
