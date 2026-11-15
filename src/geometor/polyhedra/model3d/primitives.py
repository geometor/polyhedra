"""Exact symbolic 3D geometric primitives and polyhedral models.

Provides 100% exact algebraic representations of vectors, points, lines, planes,
spheres, and polyhedral solids over Q, Q(phi), and radical extensions, with zero
float or sp.Float coordinates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import sympy as sp

if TYPE_CHECKING:
    from geometor.polyhedra.platonic import RegularSolid


def _validate_exact(*values: object) -> None:
    """Validates that values contain no floats or sp.Float atoms.

    Args:
        *values: Symbolic expressions or numbers to validate.

    Raises:
        TypeError: If any value is a Python float or contains sp.Float atoms.
    """
    for val in values:
        if isinstance(val, (float, sp.Float)):
            raise TypeError(f"Float instances prohibited in exact symbolic geometry: {val!r}")
        if isinstance(val, sp.Basic) and val.atoms(sp.Float):
            raise TypeError(f"sp.Float atoms prohibited in exact symbolic geometry: {val!r}")


@dataclass(frozen=True)
class Vector3D:
    """Exact 3D symbolic vector over algebraic number fields.

    Attributes:
        x: Exact X component.
        y: Exact Y component.
        z: Exact Z component.
    """

    x: sp.Expr
    y: sp.Expr
    z: sp.Expr

    def __post_init__(self) -> None:
        """Validates exact algebraic coordinates."""
        for name in ("x", "y", "z"):
            val = getattr(self, name)
            _validate_exact(val)
            sym = sp.sympify(val)
            _validate_exact(sym)
            object.__setattr__(self, name, sym)

    def __add__(self, other: Vector3D) -> Vector3D:
        """Adds two 3D vectors."""
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3D) -> Vector3D:
        """Subtracts two 3D vectors."""
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self) -> Vector3D:
        """Negates vector coordinates."""
        return Vector3D(-self.x, -self.y, -self.z)

    def __mul__(self, scalar: sp.Expr | int) -> Vector3D:
        """Multiplies vector by exact scalar."""
        _validate_exact(scalar)
        s = sp.sympify(scalar)
        _validate_exact(s)
        return Vector3D(self.x * s, self.y * s, self.z * s)

    def __rmul__(self, scalar: sp.Expr | int) -> Vector3D:
        """Multiplies vector by exact scalar from left."""
        return self.__mul__(scalar)

    def dot(self, other: Vector3D) -> sp.Expr:
        """Computes exact dot product with another vector."""
        return sp.simplify(self.x * other.x + self.y * other.y + self.z * other.z)

    def cross(self, other: Vector3D) -> Vector3D:
        """Computes exact cross product with another vector."""
        return Vector3D(
            sp.simplify(self.y * other.z - self.z * other.y),
            sp.simplify(self.z * other.x - self.x * other.z),
            sp.simplify(self.x * other.y - self.y * other.x),
        )

    def quadrance(self) -> sp.Expr:
        """Computes exact quadrance (squared norm) of vector."""
        return self.dot(self)

    def to_tuple(self) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
        """Returns coordinate 3-tuple."""
        return (self.x, self.y, self.z)


@dataclass(frozen=True)
class Point3D:
    """Exact 3D symbolic point over algebraic number fields.

    Attributes:
        x: Exact X coordinate.
        y: Exact Y coordinate.
        z: Exact Z coordinate.
        label: Optional symbolic label.
    """

    x: sp.Expr
    y: sp.Expr
    z: sp.Expr
    label: str = ""

    def __post_init__(self) -> None:
        """Validates exact algebraic coordinates."""
        for name in ("x", "y", "z"):
            val = getattr(self, name)
            _validate_exact(val)
            sym = sp.sympify(val)
            _validate_exact(sym)
            object.__setattr__(self, name, sym)

    def vector_to(self, other: Point3D) -> Vector3D:
        """Returns displacement vector from self to other."""
        return Vector3D(other.x - self.x, other.y - self.y, other.z - self.z)

    def quadrance_to(self, other: Point3D) -> sp.Expr:
        """Returns exact quadrance (squared Euclidean distance) to other."""
        return self.vector_to(other).quadrance()

    def lerp(self, other: Point3D, t: sp.Expr | int) -> Point3D:
        """Computes exact linear interpolation (1 - t)*self + t*other."""
        _validate_exact(t)
        st = sp.sympify(t)
        _validate_exact(st)
        one_minus_t = sp.Integer(1) - st
        return Point3D(
            sp.simplify(one_minus_t * self.x + st * other.x),
            sp.simplify(one_minus_t * self.y + st * other.y),
            sp.simplify(one_minus_t * self.z + st * other.z),
        )

    def scale(self, factor: sp.Expr | int) -> Point3D:
        """Scales point coordinates from origin by exact factor."""
        _validate_exact(factor)
        sf = sp.sympify(factor)
        _validate_exact(sf)
        return Point3D(
            sp.simplify(self.x * sf),
            sp.simplify(self.y * sf),
            sp.simplify(self.z * sf),
        )

    def to_tuple(self) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
        """Returns coordinate 3-tuple."""
        return (self.x, self.y, self.z)

    def to_vector(self) -> Vector3D:
        """Returns position vector from origin to this point."""
        return Vector3D(self.x, self.y, self.z)

    def __add__(self, vec: Vector3D) -> Point3D:
        """Translates point by a vector."""
        return Point3D(self.x + vec.x, self.y + vec.y, self.z + vec.z)


@dataclass(frozen=True)
class Line3D:
    """Exact 3D line passing through two distinct points.

    Attributes:
        p1: First point on line.
        p2: Second point on line.
    """

    p1: Point3D
    p2: Point3D

    def direction(self) -> Vector3D:
        """Returns direction vector from p1 to p2."""
        return self.p1.vector_to(self.p2)


@dataclass(frozen=True)
class Plane3D:
    """Exact 3D plane represented by algebraic equation a*x + b*y + c*z + d = 0.

    Attributes:
        a: Coefficient for x.
        b: Coefficient for y.
        c: Coefficient for z.
        d: Constant term.
    """

    a: sp.Expr
    b: sp.Expr
    c: sp.Expr
    d: sp.Expr

    def __post_init__(self) -> None:
        """Validates exact algebraic coefficients."""
        for name in ("a", "b", "c", "d"):
            val = getattr(self, name)
            _validate_exact(val)
            sym = sp.sympify(val)
            _validate_exact(sym)
            object.__setattr__(self, name, sym)

    @classmethod
    def from_points(cls, p1: Point3D, p2: Point3D, p3: Point3D) -> Plane3D:
        """Constructs plane passing through three non-collinear points.

        Args:
            p1: First point.
            p2: Second point.
            p3: Third point.

        Returns:
            Plane3D passing through p1, p2, and p3.

        Raises:
            ValueError: If points are collinear.
        """
        v12 = p1.vector_to(p2)
        v13 = p1.vector_to(p3)
        n = v12.cross(v13)
        if sp.simplify(n.quadrance()) == 0:
            raise ValueError("Collinear points cannot define a unique plane.")
        d = sp.simplify(-(n.x * p1.x + n.y * p1.y + n.z * p1.z))
        return cls(sp.simplify(n.x), sp.simplify(n.y), sp.simplify(n.z), d)

    @classmethod
    def from_normal_point(cls, normal: Vector3D, point: Point3D) -> Plane3D:
        """Constructs plane from normal vector and point on plane.

        Args:
            normal: Non-zero normal vector.
            point: Point lying on plane.

        Returns:
            Plane3D with given normal containing point.

        Raises:
            ValueError: If normal vector is zero.
        """
        if sp.simplify(normal.quadrance()) == 0:
            raise ValueError("Normal vector cannot be zero.")
        d = sp.simplify(-(normal.x * point.x + normal.y * point.y + normal.z * point.z))
        return cls(sp.simplify(normal.x), sp.simplify(normal.y), sp.simplify(normal.z), d)

    def normal(self) -> Vector3D:
        """Returns normal vector (a, b, c)."""
        return Vector3D(self.a, self.b, self.c)

    def eval_point(self, pt: Point3D) -> sp.Expr:
        """Evaluates linear form a*pt.x + b*pt.y + c*pt.z + d."""
        return sp.simplify(self.a * pt.x + self.b * pt.y + self.c * pt.z + self.d)

    def contains(self, pt: Point3D) -> bool:
        """Tests whether point lies exactly on plane."""
        return sp.simplify(self.eval_point(pt)) == 0

    def intersect_segment(self, p1: Point3D, p2: Point3D) -> Point3D | None:
        """Computes exact intersection point of segment [p1, p2] with plane.

        Args:
            p1: Segment start point.
            p2: Segment end point.

        Returns:
            Exact Point3D if segment intersects plane, or None otherwise.
        """
        e1 = self.eval_point(p1)
        e2 = self.eval_point(p2)
        denom = sp.simplify(e2 - e1)
        if denom == 0:
            if sp.simplify(e1) == 0:
                return p1
            return None
        t = sp.simplify(-e1 / denom)
        t_float = float(t.evalf())
        if t_float < -1e-9 or t_float > 1.0 + 1e-9:
            return None
        if t_float <= 1e-9 and sp.simplify(t) == 0:
            return p1
        if t_float >= 1.0 - 1e-9 and sp.simplify(t - 1) == 0:
            return p2
        try:
            if bool(t >= 0) and bool(1 - t >= 0):
                return p1.lerp(p2, t)
        except TypeError:
            pass
        if 0.0 <= t_float <= 1.0:
            return p1.lerp(p2, t)
        return None


@dataclass(frozen=True)
class Sphere3D:
    """Exact 3D sphere defined by center and quadrance.

    Attributes:
        center: Center point of sphere.
        quadrance: Exact squared radius Q = R^2.
    """

    center: Point3D
    quadrance: sp.Expr

    def __post_init__(self) -> None:
        """Validates exact algebraic parameters."""
        _validate_exact(self.quadrance)
        sym = sp.sympify(self.quadrance)
        _validate_exact(sym)
        object.__setattr__(self, "quadrance", sym)

    def contains(self, pt: Point3D) -> bool:
        """Tests whether point lies exactly on sphere surface."""
        return sp.simplify(self.center.quadrance_to(pt) - self.quadrance) == 0


@dataclass(frozen=True)
class Solid3D:
    """Exact 3D polyhedral manifold with oriented face cycles and metadata.

    Attributes:
        slug: Short lowercase identifier.
        title: Descriptive human-readable title.
        vertices: Sequence of exact 3D vertices.
        faces: Sequence of oriented face cycles (indices in counter-clockwise order).
        edges: Sorted sequence of unique undirected edge index pairs (i, j) with i < j.
        face_roles: Role tags corresponding to each face in faces sequence.
    """

    slug: str
    title: str
    vertices: tuple[Point3D, ...]
    faces: tuple[tuple[int, ...], ...]
    edges: tuple[tuple[int, int], ...] = ()
    face_roles: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Normalizes edges and face roles."""
        if not self.edges:
            edge_set = set()
            for face in self.faces:
                k = len(face)
                for i in range(k):
                    u = face[i]
                    v = face[(i + 1) % k]
                    edge_set.add((min(u, v), max(u, v)))
            object.__setattr__(self, "edges", tuple(sorted(edge_set)))
        if not self.face_roles:
            object.__setattr__(self, "face_roles", ("base",) * len(self.faces))

    @classmethod
    def from_regular_solid(cls, solid: RegularSolid) -> Solid3D:
        """Constructs Solid3D from a RegularSolid instance.

        Args:
            solid: Exact symbolic RegularSolid instance.

        Returns:
            Corresponding Solid3D instance.
        """
        pts = tuple(Point3D(v[0], v[1], v[2]) for v in solid.vertices)
        return cls(
            slug=solid.slug,
            title=solid.name,
            vertices=pts,
            faces=solid.faces,
            edges=solid.edges,
            face_roles=("base",) * len(solid.faces),
        )

    @property
    def num_vertices(self) -> int:
        """Returns number of vertices."""
        return len(self.vertices)

    @property
    def num_edges(self) -> int:
        """Returns number of edges."""
        return len(self.edges)

    @property
    def num_faces(self) -> int:
        """Returns number of faces."""
        return len(self.faces)

    @property
    def euler_characteristic(self) -> int:
        """Returns Euler characteristic V - E + F."""
        return self.num_vertices - self.num_edges + self.num_faces

    @property
    def genus(self) -> int:
        """Returns topological genus (2 - chi) // 2."""
        return (2 - self.euler_characteristic) // 2

    def face_centroid(self, face_idx: int) -> Point3D:
        """Computes exact centroid of a face.

        Args:
            face_idx: Index of face in faces tuple.

        Returns:
            Point3D representing the centroid.
        """
        face = self.faces[face_idx]
        k = len(face)
        cx = sp.simplify(sum(self.vertices[i].x for i in face) / sp.Integer(k))
        cy = sp.simplify(sum(self.vertices[i].y for i in face) / sp.Integer(k))
        cz = sp.simplify(sum(self.vertices[i].z for i in face) / sp.Integer(k))
        return Point3D(cx, cy, cz)

    def face_normal(self, face_idx: int) -> Vector3D:
        """Computes unnormalized outward normal vector of a face.

        Args:
            face_idx: Index of face in faces tuple.

        Returns:
            Vector3D normal vector via cycle cross product sum.
        """
        face = self.faces[face_idx]
        k = len(face)
        nx = sp.Integer(0)
        ny = sp.Integer(0)
        nz = sp.Integer(0)
        for i in range(k):
            p1 = self.vertices[face[i]]
            p2 = self.vertices[face[(i + 1) % k]]
            nx += p1.y * p2.z - p1.z * p2.y
            ny += p1.z * p2.x - p1.x * p2.z
            nz += p1.x * p2.y - p1.y * p2.x
        return Vector3D(sp.simplify(nx), sp.simplify(ny), sp.simplify(nz))

    def are_faces_coplanar(self) -> bool:
        """Verifies that all vertices of every face are strictly coplanar.

        Returns:
            True if all faces are planar, False otherwise.
        """
        for idx, face in enumerate(self.faces):
            if len(face) <= 3:
                continue
            n = self.face_normal(idx)
            if sp.simplify(n.quadrance()) == 0:
                return False
            plane = Plane3D.from_normal_point(n, self.vertices[face[0]])
            for vi in face[3:]:
                if not plane.contains(self.vertices[vi]):
                    return False
        return True

    def is_outward_oriented(self) -> bool:
        """Checks consistent outward orientation relative to origin or cavity.

        Returns:
            True if all face normal orientations match expected outwards conventions.
        """
        for idx in range(len(self.faces)):
            n = self.face_normal(idx)
            c = self.face_centroid(idx)
            dot_val = n.dot(c.to_vector())
            role = self.face_roles[idx] if idx < len(self.face_roles) else "base"
            if role in ("base", "outer_frame", "truncation", "pyramid"):
                if float(dot_val.evalf()) <= 0:
                    return False
            elif role == "inner_frame":
                if float(dot_val.evalf()) >= 0:
                    return False
            elif role == "window_reveal" and sp.simplify(n.quadrance()) == 0:
                return False
        return True
