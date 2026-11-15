"""Bridge module connecting 3D polyhedra to 2D GEOMETOR symbolic models.

Provides cross-section planar slicing into exact 2D Model instances and
2D net unfolding for SVG visualization and physical papercraft modeling.
"""

from __future__ import annotations

import math
from collections import deque

import sympy as sp
from geometor.model import Model

from geometor.polyhedra.model3d.primitives import (
    Plane3D,
    Point3D,
    Solid3D,
    Vector3D,
)


def slice_solid_to_model(
    solid: Solid3D,
    plane: Plane3D,
    u_axis: Vector3D,
    v_axis: Vector3D,
    origin: Point3D | None = None,
    name: str = "slice",
    normalize_axes: bool = False,
) -> Model:
    """Computes exact planar cross-section of a Solid3D and constructs a 2D Model.

    Intersects all boundary edges of the solid with the given slicing plane,
    projects the exact intersection points onto the 2D plane defined by u_axis
    and v_axis, sorts them cyclically around their centroid, and constructs
    exact points, segments, and polygon entities in a 2D Model.

    Args:
        solid: Exact 3D polyhedral solid.
        plane: Slicing plane.
        u_axis: Direction vector for 2D X axis.
        v_axis: Direction vector for 2D Y axis.
        origin: Optional 3D point mapped to 2D origin (0, 0). Defaults to (0,0,0).
        name: Name identifier for the constructed Model.
        normalize_axes: If True, divides projections by axis quadrances.

    Returns:
        Exact 2D Model containing the cross-section polygon and boundary segments.
    """
    if origin is None:
        origin = Point3D(sp.Integer(0), sp.Integer(0), sp.Integer(0))

    pts_3d: list[Point3D] = []
    for u_idx, v_idx in solid.edges:
        p1 = solid.vertices[u_idx]
        p2 = solid.vertices[v_idx]
        pt = plane.intersect_segment(p1, p2)
        if pt is not None:
            is_dup = False
            for existing in pts_3d:
                if sp.simplify(existing.quadrance_to(pt)) == 0:
                    is_dup = True
                    break
            if not is_dup:
                pts_3d.append(pt)

    pts_2d_exact: list[tuple[sp.Expr, sp.Expr]] = []
    qu = u_axis.quadrance()
    qv = v_axis.quadrance()

    for pt in pts_3d:
        v_rel = origin.vector_to(pt)
        dot_u = v_rel.dot(u_axis)
        dot_v = v_rel.dot(v_axis)
        if normalize_axes:
            x_2d = sp.simplify(dot_u / qu)
            y_2d = sp.simplify(dot_v / qv)
        else:
            x_2d = sp.simplify(dot_u)
            y_2d = sp.simplify(dot_v)

        is_dup = False
        for ex_x, ex_y in pts_2d_exact:
            if sp.simplify(ex_x - x_2d) == 0 and sp.simplify(ex_y - y_2d) == 0:
                is_dup = True
                break
        if not is_dup:
            pts_2d_exact.append((x_2d, y_2d))

    if len(pts_2d_exact) >= 3:
        cx = sum(p[0] for p in pts_2d_exact) / sp.Integer(len(pts_2d_exact))
        cy = sum(p[1] for p in pts_2d_exact) / sp.Integer(len(pts_2d_exact))
        cx_f = float(cx.evalf())
        cy_f = float(cy.evalf())

        def sort_key(pt: tuple[sp.Expr, sp.Expr]) -> float:
            return math.atan2(float(pt[1].evalf()) - cy_f, float(pt[0].evalf()) - cx_f)

        pts_2d_exact.sort(key=sort_key)

    model = Model(name=name, auto_intersect=False)
    model_pts = []
    for idx, (x, y) in enumerate(pts_2d_exact):
        p = model.set_point(x, y, classes=["given"], label=f"P_{idx}")
        model_pts.append(p)

    n_pts = len(model_pts)
    if n_pts >= 2:
        for i in range(n_pts):
            if n_pts >= 3 or i == 0:
                next_i = (i + 1) % n_pts
                model.construct_segment(model_pts[i], model_pts[next_i])

    if n_pts >= 3:
        model.construct_polygon(model_pts)

    return model


def unfold_net_2d(
    solid: Solid3D,
    root_face: int = 0,
) -> list[dict[str, object]]:
    """Unfolds faces of a Solid3D onto a 2D plane via dual graph BFS spanning tree.

    Starting from root_face, flattens each adjacent face around its shared hinge
    edge without folding backward or overlapping adjacent faces.

    Args:
        solid: Exact 3D polyhedral solid.
        root_face: Index of the base face placed first at 2D origin.

    Returns:
        List of dictionaries with face net layout metadata:
            - face_index: Index of the face in solid.faces.
            - role: Role string from solid.face_roles.
            - pts_2d: List of 2D vertex coordinates as (x, y) floats.
            - parent_face: Index of parent face across hinge, or None for root.
            - hinge_2d: Pair of (start, end) 2D coordinates of hinge, or None for root.
    """
    verts_3d = [
        (float(v.x.evalf()), float(v.y.evalf()), float(v.z.evalf()))
        for v in solid.vertices
    ]
    faces = solid.faces

    def vec_sub(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

    def vec_dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def vec_cross(
        a: tuple[float, float, float], b: tuple[float, float, float]
    ) -> tuple[float, float, float]:
        return (
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        )

    def vec_norm(a: tuple[float, float, float]) -> float:
        return math.sqrt(vec_dot(a, a))

    def vec_unit(a: tuple[float, float, float]) -> tuple[float, float, float]:
        n = vec_norm(a)
        if n == 0:
            return (0.0, 0.0, 0.0)
        return (a[0] / n, a[1] / n, a[2] / n)

    edge_to_faces: dict[tuple[int, int], list[int]] = {}
    for fi, f in enumerate(faces):
        k = len(f)
        for i in range(k):
            e = (min(f[i], f[(i + 1) % k]), max(f[i], f[(i + 1) % k]))
            edge_to_faces.setdefault(e, []).append(fi)

    dual_adj: dict[int, list[tuple[int, tuple[int, int]]]] = {
        fi: [] for fi in range(len(faces))
    }
    for e, flist in edge_to_faces.items():
        if len(flist) == 2:
            dual_adj[flist[0]].append((flist[1], e))
            dual_adj[flist[1]].append((flist[0], e))

    f0 = faces[root_face]
    v0, v1 = verts_3d[f0[0]], verts_3d[f0[1]]
    u3d = vec_unit(vec_sub(v1, v0))
    e1 = vec_sub(v1, v0)
    e2 = vec_sub(verts_3d[f0[2]], v0)
    n3d = vec_unit(vec_cross(e1, e2))
    v3d = vec_cross(n3d, u3d)

    f0_pts_2d: dict[int, tuple[float, float]] = {}
    for vi in f0:
        d = vec_sub(verts_3d[vi], v0)
        f0_pts_2d[vi] = (vec_dot(d, u3d), vec_dot(d, v3d))

    face_vertex_2d: dict[int, dict[int, tuple[float, float]]] = {root_face: f0_pts_2d}
    visited = {root_face}
    queue = deque([root_face])

    net_faces: list[dict[str, object]] = [
        {
            "face_index": root_face,
            "role": solid.face_roles[root_face] if root_face < len(solid.face_roles) else "base",
            "pts_2d": [f0_pts_2d[vi] for vi in f0],
            "parent_face": None,
            "hinge_2d": None,
        }
    ]

    while queue:
        curr = queue.popleft()
        curr_v2d = face_vertex_2d[curr]
        for nxt, e in dual_adj[curr]:
            if nxt not in visited:
                visited.add(nxt)
                u_e, v_e = e[0], e[1]
                p_ue = curr_v2d[u_e]
                p_ve = curr_v2d[v_e]

                fnxt = faces[nxt]
                k = len(fnxt)
                m = -1
                p_start, p_end = p_ue, p_ve
                for i in range(k):
                    if fnxt[i] == u_e and fnxt[(i + 1) % k] == v_e:
                        m = i
                        p_start = p_ue
                        p_end = p_ve
                        break
                    if fnxt[i] == v_e and fnxt[(i + 1) % k] == u_e:
                        m = i
                        p_start = p_ve
                        p_end = p_ue
                        break

                vm_3d = verts_3d[fnxt[m]]
                vm1_3d = verts_3d[fnxt[(m + 1) % k]]
                u_b = vec_unit(vec_sub(vm1_3d, vm_3d))
                eb1 = vec_sub(vm1_3d, vm_3d)
                eb2 = vec_sub(verts_3d[fnxt[(m + 2) % k]], vm_3d)
                nb = vec_unit(vec_cross(eb1, eb2))
                vb = vec_cross(nb, u_b)

                u2d_vec = (p_end[0] - p_start[0], p_end[1] - p_start[1])
                l_dist = math.sqrt(u2d_vec[0] ** 2 + u2d_vec[1] ** 2)
                u2d = (u2d_vec[0] / l_dist, u2d_vec[1] / l_dist)
                v2d = (-u2d[1], u2d[0])

                nxt_v2d: dict[int, tuple[float, float]] = {}
                for vi in fnxt:
                    d = vec_sub(verts_3d[vi], vm_3d)
                    x_loc = vec_dot(d, u_b)
                    y_loc = vec_dot(d, vb)
                    p2d = (
                        p_start[0] + x_loc * u2d[0] + y_loc * v2d[0],
                        p_start[1] + x_loc * u2d[1] + y_loc * v2d[1],
                    )
                    nxt_v2d[vi] = p2d

                face_vertex_2d[nxt] = nxt_v2d
                role_str = solid.face_roles[nxt] if nxt < len(solid.face_roles) else "base"
                net_faces.append(
                    {
                        "face_index": nxt,
                        "role": role_str,
                        "pts_2d": [nxt_v2d[vi] for vi in fnxt],
                        "parent_face": curr,
                        "hinge_2d": (p_start, p_end),
                    }
                )
                queue.append(nxt)

    return net_faces
