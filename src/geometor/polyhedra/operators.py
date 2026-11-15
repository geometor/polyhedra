"""Exact symbolic polyhedral operators over algebraic number fields.

Provides five exact geometric operators preserving 100% symbolic coordinates
over Q(phi, sqrt(d)):

- ``vacuate``: Leonardo da Vinci's hollow manifold (*Corpus Vacuum*).
- ``rectify``: Pacioli's edge-midpoint truncation (*Abscisum*).
- ``truncate``: Archimedean corner-cutting at rational edge ratios.
- ``elevate``: Pacioli/Leonardo's equilateral face stellations (*Elevatum* / *kis*).
- ``polar_dual``: Reciprocal face-polar duality across concentric spheres.
"""

from __future__ import annotations

import math

import sympy as sp

from geometor.polyhedra.model3d.primitives import (
    Point3D,
    Solid3D,
    _validate_exact,
)


def _order_polygon_around_axis(
    pts: list[Point3D],
    axis_pt: Point3D,
) -> list[int]:
    """Orders a list of coplanar 3D points cyclically around an outward axis.

    Args:
        pts: List of 3D points forming a convex polygon.
        axis_pt: Outward reference point from origin establishing normal orientation.

    Returns:
        List of indices into pts ordered counter-clockwise relative to axis_pt.
    """
    n_pts = len(pts)
    if n_pts <= 2:
        return list(range(n_pts))

    w_dir = [float(axis_pt.to_vector().to_tuple()[c].evalf()) for c in range(3)]
    w_norm = math.hypot(*w_dir)
    if w_norm == 0:
        w = [0.0, 0.0, 1.0]
    else:
        w = [c / w_norm for c in w_dir]

    if abs(w[0]) < 0.8:
        u_raw = (0.0, -w[2], w[1])
    else:
        u_raw = (-w[1], w[0], 0.0)
    u_norm = math.hypot(*u_raw)
    u_vec = [c / u_norm for c in u_raw]
    v_vec = [
        w[1] * u_vec[2] - w[2] * u_vec[1],
        w[2] * u_vec[0] - w[0] * u_vec[2],
        w[0] * u_vec[1] - w[1] * u_vec[0],
    ]

    cx_f = sum(float(pt.x.evalf()) for pt in pts) / n_pts
    cy_f = sum(float(pt.y.evalf()) for pt in pts) / n_pts
    cz_f = sum(float(pt.z.evalf()) for pt in pts) / n_pts

    def angle(idx: int) -> float:
        pt = pts[idx]
        dx = float(pt.x.evalf()) - cx_f
        dy = float(pt.y.evalf()) - cy_f
        dz = float(pt.z.evalf()) - cz_f
        proj_u = dx * u_vec[0] + dy * u_vec[1] + dz * u_vec[2]
        proj_v = dx * v_vec[0] + dy * v_vec[1] + dz * v_vec[2]
        return math.atan2(proj_v, proj_u)

    sorted_indices = sorted(range(n_pts), key=angle)

    p0 = [float(pts[sorted_indices[0]].to_tuple()[c].evalf()) for c in range(3)]
    p1 = [float(pts[sorted_indices[1]].to_tuple()[c].evalf()) for c in range(3)]
    p2 = [float(pts[sorted_indices[2]].to_tuple()[c].evalf()) for c in range(3)]
    d1 = [p1[c] - p0[c] for c in range(3)]
    d2 = [p2[c] - p0[c] for c in range(3)]
    nx = d1[1] * d2[2] - d1[2] * d2[1]
    ny = d1[2] * d2[0] - d1[0] * d2[2]
    nz = d1[0] * d2[1] - d1[1] * d2[0]
    dot_out = nx * w[0] + ny * w[1] + nz * w[2]

    if dot_out < 0:
        sorted_indices = sorted_indices[::-1]

    return sorted_indices


def vacuate(
    solid: Solid3D,
    aperture: sp.Expr = sp.Rational(3, 5),
    shell: sp.Expr = sp.Rational(4, 5),
) -> Solid3D:
    """Constructs Leonardo da Vinci's hollow manifold (Corpus Vacuum).

    Generates outer and inner concentric shell vertices and mitered frame
    quadrilaterals around window openings for each face of the solid.

    Args:
        solid: Exact 3D polyhedral solid.
        aperture: Shrink factor for face window opening in (0, 1). Defaults to 3/5.
        shell: Shrink factor for inner concentric shell in (0, 1). Defaults to 4/5.

    Returns:
        Exact Solid3D representing the 2-manifold hollow cage polyhedron.
    """
    _validate_exact(aperture, shell)
    v_orig = solid.num_vertices

    verts: list[Point3D] = list(solid.vertices)
    for v in solid.vertices:
        verts.append(v.scale(shell))

    faces: list[tuple[int, ...]] = []
    face_roles: list[str] = []

    for fi, f in enumerate(solid.faces):
        k = len(f)
        c_f = solid.face_centroid(fi)

        w_indices: list[int] = []
        iw_indices: list[int] = []
        for m in range(k):
            vm = solid.vertices[f[m]]
            w_pt = c_f.lerp(vm, aperture)
            w_idx = len(verts)
            verts.append(w_pt)
            w_indices.append(w_idx)

            iw_pt = w_pt.scale(shell)
            iw_idx = len(verts)
            verts.append(iw_pt)
            iw_indices.append(iw_idx)

        for m in range(k):
            m_next = (m + 1) % k
            v_im = f[m]
            v_im1 = f[m_next]
            w_m = w_indices[m]
            w_m1 = w_indices[m_next]
            faces.append((v_im, v_im1, w_m1, w_m))
            face_roles.append("outer_frame")

            iv_im = v_orig + v_im
            iv_im1 = v_orig + v_im1
            iw_m = iw_indices[m]
            iw_m1 = iw_indices[m_next]
            faces.append((iv_im1, iv_im, iw_m, iw_m1))
            face_roles.append("inner_frame")

            faces.append((w_m, w_m1, iw_m1, iw_m))
            face_roles.append("window_reveal")

    return Solid3D(
        slug=f"{solid.slug}_vacuate",
        title=f"Vacuate {solid.title}",
        vertices=tuple(verts),
        faces=tuple(faces),
        face_roles=tuple(face_roles),
    )


def rectify(solid: Solid3D) -> Solid3D:
    """Constructs Pacioli's edge-midpoint truncation (Abscisum).

    Places vertices at exact midpoints of all edges, yielding shrunk faces
    on original faces and vertex-figure polygons at all original vertices.

    Args:
        solid: Exact 3D polyhedral solid.

    Returns:
        Exact rectified Solid3D instance.
    """
    midpoints: list[Point3D] = []
    edge_map: dict[tuple[int, int], int] = {}

    for idx, (u, v) in enumerate(solid.edges):
        m = solid.vertices[u].lerp(solid.vertices[v], sp.Rational(1, 2))
        midpoints.append(m)
        edge_map[(min(u, v), max(u, v))] = idx

    base_faces: list[tuple[int, ...]] = []
    for f in solid.faces:
        k = len(f)
        bface = [
            edge_map[(min(f[i], f[(i + 1) % k]), max(f[i], f[(i + 1) % k]))]
            for i in range(k)
        ]
        base_faces.append(tuple(bface))

    trunc_faces: list[tuple[int, ...]] = []
    for vi, v_pt in enumerate(solid.vertices):
        inc_edges = [
            edge_map[(min(vi, u), max(vi, u))]
            for u in range(solid.num_vertices)
            if (min(vi, u), max(vi, u)) in edge_map
        ]
        sub_pts = [midpoints[e_idx] for e_idx in inc_edges]
        ordered_sub = _order_polygon_around_axis(sub_pts, v_pt)
        trunc_faces.append(tuple(inc_edges[i] for i in ordered_sub))

    all_faces = base_faces + trunc_faces
    all_roles = ["base"] * len(base_faces) + ["truncation"] * len(trunc_faces)

    return Solid3D(
        slug=f"{solid.slug}_rectified",
        title=f"Rectified {solid.title}",
        vertices=tuple(midpoints),
        faces=tuple(all_faces),
        face_roles=tuple(all_roles),
    )


def truncate(
    solid: Solid3D,
    ratio: sp.Expr = sp.Rational(1, 3),
) -> Solid3D:
    """Constructs Archimedean corner truncation at an exact rational ratio.

    Divides each directed edge at parameter ratio, creating 2k-gons on original
    k-gon faces and q-gon vertex-figure faces at vertices of degree q.

    Args:
        solid: Exact 3D polyhedral solid.
        ratio: Truncation ratio in (0, 1/2). Defaults to 1/3.

    Returns:
        Exact truncated Solid3D instance.
    """
    _validate_exact(ratio)

    verts: list[Point3D] = []
    dir_edge_map: dict[tuple[int, int], int] = {}

    for u, v in solid.edges:
        pu, pv = solid.vertices[u], solid.vertices[v]
        p_uv = pu.lerp(pv, ratio)
        idx_uv = len(verts)
        verts.append(p_uv)
        dir_edge_map[(u, v)] = idx_uv

        p_vu = pu.lerp(pv, sp.Integer(1) - ratio)
        idx_vu = len(verts)
        verts.append(p_vu)
        dir_edge_map[(v, u)] = idx_vu

    base_faces: list[tuple[int, ...]] = []
    for f in solid.faces:
        k = len(f)
        bface: list[int] = []
        for i in range(k):
            u, v = f[i], f[(i + 1) % k]
            bface.append(dir_edge_map[(u, v)])
            bface.append(dir_edge_map[(v, u)])
        base_faces.append(tuple(bface))

    trunc_faces: list[tuple[int, ...]] = []
    for vi, v_pt in enumerate(solid.vertices):
        neighbors = [nbr for (u, nbr) in dir_edge_map.keys() if u == vi]
        sub_pts = [verts[dir_edge_map[(vi, nbr)]] for nbr in neighbors]
        ordered_sub = _order_polygon_around_axis(sub_pts, v_pt)
        tface = [dir_edge_map[(vi, neighbors[i])] for i in ordered_sub]
        trunc_faces.append(tuple(tface))

    all_faces = base_faces + trunc_faces
    all_roles = ["base"] * len(base_faces) + ["truncation"] * len(trunc_faces)

    return Solid3D(
        slug=f"{solid.slug}_truncated",
        title=f"Truncated {solid.title}",
        vertices=tuple(verts),
        faces=tuple(all_faces),
        face_roles=tuple(all_roles),
    )


def elevate(
    solid: Solid3D,
    height_scale: sp.Expr | None = None,
) -> Solid3D:
    """Constructs Pacioli/Leonardo's stellation (Elevatum / Conway kis).

    Replaces each k-gon face with k triangular pyramid faces meeting at an apex
    above the face centroid. When height_scale is None, calculates the exact
    algebraic height making all lateral triangular faces equilateral.

    Args:
        solid: Exact 3D polyhedral solid.
        height_scale: Optional exact height scaling factor. When None, calculates
            exact equilateral pyramid height.

    Returns:
        Exact elevated Solid3D instance.

    Raises:
        ValueError: If face circumradius exceeds edge length for equilateral pyramid.
    """
    if height_scale is not None:
        _validate_exact(height_scale)

    verts: list[Point3D] = list(solid.vertices)
    pyramid_faces: list[tuple[int, ...]] = []

    for fi, f in enumerate(solid.faces):
        k = len(f)
        c_f = solid.face_centroid(fi)
        v0 = solid.vertices[f[0]]
        v1 = solid.vertices[f[1]]

        s2 = v0.quadrance_to(v1)
        r2 = c_f.quadrance_to(v0)
        h2 = sp.simplify(s2 - r2)

        if height_scale is None:
            if float(h2.evalf()) <= 0:
                raise ValueError(
                    f"Face {fi} circumradius squared {r2} exceeds edge quadrance {s2}; "
                    "cannot form equilateral pyramid."
                )
        else:
            h2 = sp.simplify((height_scale ** 2) * h2)

        n = solid.face_normal(fi)
        qn = n.quadrance()
        alpha = sp.sqrt(h2 / qn)

        apex = Point3D(
            sp.simplify(c_f.x + alpha * n.x),
            sp.simplify(c_f.y + alpha * n.y),
            sp.simplify(c_f.z + alpha * n.z),
        )
        apex_idx = len(verts)
        verts.append(apex)

        for m in range(k):
            m_next = (m + 1) % k
            pyramid_faces.append((f[m], f[m_next], apex_idx))

    return Solid3D(
        slug=f"{solid.slug}_elevated",
        title=f"Elevated {solid.title}",
        vertices=tuple(verts),
        faces=tuple(pyramid_faces),
        face_roles=("pyramid",) * len(pyramid_faces),
    )


def polar_dual(
    solid: Solid3D,
    sphere_quadrance: sp.Expr | None = None,
) -> Solid3D:
    """Constructs exact polar dual of an origin-centered polyhedral solid.

    Reciprocates every face plane across a concentric sphere of quadrance
    sphere_quadrance, producing dual vertices at poles of face planes and dual
    faces corresponding to original vertices.

    Args:
        solid: Exact origin-centered Solid3D instance.
        sphere_quadrance: Optional exact sphere quadrance. Defaults to midquadrance
            of the first edge.

    Returns:
        Exact dual Solid3D instance.
    """
    if sphere_quadrance is not None:
        _validate_exact(sphere_quadrance)
    else:
        u_idx, v_idx = solid.edges[0]
        m = solid.vertices[u_idx].lerp(solid.vertices[v_idx], sp.Rational(1, 2))
        sphere_quadrance = m.to_vector().quadrance()

    dual_verts: list[Point3D] = []
    for fi, _ in enumerate(solid.faces):
        c_f = solid.face_centroid(fi)
        n = solid.face_normal(fi)
        dot_nc = n.dot(c_f.to_vector())
        scale = sp.simplify(sphere_quadrance / dot_nc)
        v_star = Point3D(
            sp.simplify(scale * n.x),
            sp.simplify(scale * n.y),
            sp.simplify(scale * n.z),
        )
        dual_verts.append(v_star)

    dual_faces: list[tuple[int, ...]] = []
    for vi, v_pt in enumerate(solid.vertices):
        inc_faces = [fi for fi, f in enumerate(solid.faces) if vi in f]
        sub_pts = [dual_verts[fi] for fi in inc_faces]
        ordered_sub = _order_polygon_around_axis(sub_pts, v_pt)
        dual_faces.append(tuple(inc_faces[i] for i in ordered_sub))

    return Solid3D(
        slug=f"{solid.slug}_dual",
        title=f"Dual {solid.title}",
        vertices=tuple(dual_verts),
        faces=tuple(dual_faces),
        face_roles=("base",) * len(dual_faces),
    )
