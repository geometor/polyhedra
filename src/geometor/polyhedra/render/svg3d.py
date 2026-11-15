"""SVG 3D projection and publication-grade geometric renderers.

Provides three theme-adaptive SVG renderers for polyhedra and 2D models:
    - render_solid_svg: Perspective projection of 3D solids with depth sorting,
      directional lighting, back-face culling, and Renaissance woodcut or
      elemental styling.
    - render_net_svg: Unfolded 2D net layout with hinge folds and cut boundaries.
    - render_model2d_svg: 2D GEOMETOR symbolic models with golden sections and
      dark-mode theme adaptation.
"""

from __future__ import annotations

import html
import math
import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from geometor.model import Model

    from geometor.polyhedra.model3d.primitives import Solid3D


def _vec3_sub(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> tuple[float, float, float]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _vec3_dot(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _vec3_cross(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _vec3_norm(a: tuple[float, float, float]) -> float:
    return math.sqrt(_vec3_dot(a, a))


def _vec3_unit(a: tuple[float, float, float]) -> tuple[float, float, float]:
    n = _vec3_norm(a)
    if n <= 1e-12:
        return (0.0, 0.0, 0.0)
    return (a[0] / n, a[1] / n, a[2] / n)


def _shade_hex(hex_code: str, intensity: float) -> str:
    """Modulates a hex color string by a lighting intensity factor.

    Args:
        hex_code: Hex color string (e.g. '#efe2c6').
        intensity: Lighting factor in [0.0, 1.0].

    Returns:
        Shaded hex color string.
    """
    clean_hex = hex_code.lstrip("#")
    r = int(clean_hex[0:2], 16)
    g = int(clean_hex[2:4], 16)
    b = int(clean_hex[4:6], 16)
    factor = 0.48 + 0.52 * intensity
    r_sh = max(0, min(255, int(r * factor)))
    g_sh = max(0, min(255, int(g * factor)))
    b_sh = max(0, min(255, int(b * factor)))
    return f"#{r_sh:02x}{g_sh:02x}{b_sh:02x}"


def render_solid_svg(
    solid: Solid3D,
    *,
    yaw_deg: float = 32.0,
    pitch_deg: float = 22.0,
    roll_deg: float = 0.0,
    camera_dist: float = 5.2,
    focal_length: float = 4.4,
    width: int = 520,
    height: int = 480,
    style: str = "elemental",
    show_hidden_edges: bool = True,
    golden_polygons_3d: list[list[tuple[float, float, float]]] | None = None,
    graphic_id: str = "g1",
) -> str:
    """Renders a 3D polyhedral solid to publication-grade theme-adaptive SVG.

    Uses orbit camera perspective projection with depth-sorted painter's
    algorithm, back-face culling, and directional lighting.

    Args:
        solid: Exact symbolic Solid3D polyhedral model.
        yaw_deg: Horizontal orbit yaw angle in degrees.
        pitch_deg: Vertical orbit pitch angle in degrees.
        roll_deg: Camera roll angle in degrees.
        camera_dist: Orbit distance from model center.
        focal_length: Perspective camera focal length.
        width: SVG viewport width in pixels.
        height: SVG viewport height in pixels.
        style: Visual style ('elemental', 'woodcut_vacuum', 'woodcut_solidum').
        show_hidden_edges: Whether to render dashed back-facing edges.
        golden_polygons_3d: Optional list of 3D polygon vertex loops to render
            as translucent golden planes depth-interleaved with faces.
        graphic_id: Unique identifier for data-graphic-id attribute.

    Returns:
        Valid XML SVG string with class 'euclid-graphic'.

    Raises:
        ValueError: If style is unknown or solid has no vertices.
    """
    if not solid.vertices:
        raise ValueError("Cannot render Solid3D with no vertices.")

    # 1. Evaluate vertices to float and compute center / bounding radius
    verts_f = [
        (float(v.x.evalf()), float(v.y.evalf()), float(v.z.evalf()))
        for v in solid.vertices
    ]
    n_v = len(verts_f)
    cx = sum(v[0] for v in verts_f) / n_v
    cy = sum(v[1] for v in verts_f) / n_v
    cz = sum(v[2] for v in verts_f) / n_v
    center = (cx, cy, cz)

    max_r = max(_vec3_norm(_vec3_sub(v, center)) for v in verts_f)
    if max_r <= 1e-9:
        max_r = 1.0

    # Normalized 3D vertices (radius 1.0, centered at origin)
    verts_norm = [
        (
            (v[0] - center[0]) / max_r,
            (v[1] - center[1]) / max_r,
            (v[2] - center[2]) / max_r,
        )
        for v in verts_f
    ]

    # Normalize golden polygons if provided
    golden_polys_norm: list[list[tuple[float, float, float]]] = []
    if golden_polygons_3d:
        for poly in golden_polygons_3d:
            poly_norm = [
                (
                    (p[0] - center[0]) / max_r,
                    (p[1] - center[1]) / max_r,
                    (p[2] - center[2]) / max_r,
                )
                for p in poly
            ]
            golden_polys_norm.append(poly_norm)

    # 2. Camera setup in orbit coordinates around origin
    yaw = math.radians(yaw_deg)
    pitch = math.radians(pitch_deg)
    roll = math.radians(roll_deg)

    cam_x = camera_dist * math.cos(pitch) * math.sin(yaw)
    cam_y = -camera_dist * math.cos(pitch) * math.cos(yaw)
    cam_z = camera_dist * math.sin(pitch)
    cam_pos = (cam_x, cam_y, cam_z)

    forward = _vec3_unit((0.0 - cam_x, 0.0 - cam_y, 0.0 - cam_z))
    world_up = (0.0, 0.0, 1.0)
    if abs(_vec3_dot(forward, world_up)) > 0.99:
        world_up = (0.0, 1.0, 0.0)

    right = _vec3_unit(_vec3_cross(forward, world_up))
    up = _vec3_cross(right, forward)

    cos_r = math.cos(roll)
    sin_r = math.sin(roll)
    right_r = (
        cos_r * right[0] + sin_r * up[0],
        cos_r * right[1] + sin_r * up[1],
        cos_r * right[2] + sin_r * up[2],
    )
    up_r = (
        -sin_r * right[0] + cos_r * up[0],
        -sin_r * right[1] + cos_r * up[1],
        -sin_r * right[2] + cos_r * up[2],
    )

    def project_3d(pt: tuple[float, float, float]) -> tuple[float, float]:
        d = _vec3_sub(pt, cam_pos)
        xc = _vec3_dot(d, right_r)
        yc = _vec3_dot(d, up_r)
        zc = max(_vec3_dot(d, forward), 1e-4)
        return (focal_length * xc / zc, focal_length * yc / zc)

    # 3. Perspective projection of all vertices
    proj_pts = [project_3d(vn) for vn in verts_norm]

    # Include golden polygon projected points in bounding box calculation
    all_proj_pts = list(proj_pts)
    proj_golden_polys: list[list[tuple[float, float]]] = []
    for gpoly in golden_polys_norm:
        pg = [project_3d(gp) for gp in gpoly]
        proj_golden_polys.append(pg)
        all_proj_pts.extend(pg)

    u_min = min(p[0] for p in all_proj_pts)
    u_max = max(p[0] for p in all_proj_pts)
    v_min = min(p[1] for p in all_proj_pts)
    v_max = max(p[1] for p in all_proj_pts)

    span_u = max(u_max - u_min, 1e-6)
    span_v = max(v_max - v_min, 1e-6)

    margin = 0.12
    target_w = width * (1.0 - 2.0 * margin)
    target_h = height * (1.0 - 2.0 * margin)
    scale = min(target_w / span_u, target_h / span_v)

    mid_u = (u_min + u_max) / 2.0
    mid_v = (v_min + v_max) / 2.0

    def to_screen(u_val: float, v_val: float) -> tuple[float, float]:
        px = width / 2.0 + (u_val - mid_u) * scale
        py = height / 2.0 - (v_val - mid_v) * scale
        return (px, py)

    screen_pts = [to_screen(p[0], p[1]) for p in proj_pts]

    # 4. Face normals, visibility test, and directional lighting
    # Directional light source from upper-left-front in camera space
    l_cam = _vec3_unit((-0.45, 0.55, 0.70))
    l_dir = _vec3_unit((
        l_cam[0] * right_r[0] + l_cam[1] * up_r[0] + l_cam[2] * forward[0],
        l_cam[0] * right_r[1] + l_cam[1] * up_r[1] + l_cam[2] * forward[1],
        l_cam[0] * right_r[2] + l_cam[1] * up_r[2] + l_cam[2] * forward[2],
    ))

    face_visible: list[bool] = []
    face_dist: list[float] = []
    face_light: list[float] = []

    for fi, f in enumerate(solid.faces):
        k = len(f)
        # Newell's method for normal from normalized vertices
        nx = 0.0
        ny = 0.0
        nz = 0.0
        for i in range(k):
            p1 = verts_norm[f[i]]
            p2 = verts_norm[f[(i + 1) % k]]
            nx += p1[1] * p2[2] - p1[2] * p2[1]
            ny += p1[2] * p2[0] - p1[0] * p2[2]
            nz += p1[0] * p2[1] - p1[1] * p2[0]
        n_face = (nx, ny, nz)

        # Centroid of face in normalized space
        cx_f = sum(verts_norm[vi][0] for vi in f) / k
        cy_f = sum(verts_norm[vi][1] for vi in f) / k
        cz_f = sum(verts_norm[vi][2] for vi in f) / k
        c_face = (cx_f, cy_f, cz_f)

        v_to_cam = _vec3_sub(cam_pos, c_face)
        dot_cam = _vec3_dot(n_face, v_to_cam)
        is_vis = dot_cam > 1e-9

        face_visible.append(is_vis)
        face_dist.append(_vec3_norm(v_to_cam))

        n_unit = _vec3_unit(n_face)
        cos_l = max(0.0, _vec3_dot(n_unit, l_dir))
        face_light.append(0.38 + 0.62 * cos_l)

    # 5. Hidden edges identification
    edge_to_faces: dict[tuple[int, int], list[int]] = {}
    for fi, f in enumerate(solid.faces):
        k = len(f)
        for i in range(k):
            u_idx = min(f[i], f[(i + 1) % k])
            v_idx = max(f[i], f[(i + 1) % k])
            edge_to_faces.setdefault((u_idx, v_idx), []).append(fi)

    hidden_edge_lines: list[tuple[tuple[float, float], tuple[float, float]]] = []
    if show_hidden_edges:
        for (u_idx, v_idx), flist in edge_to_faces.items():
            # An edge is back-facing if ALL adjacent faces are back-facing
            if all(not face_visible[fi] for fi in flist):
                hidden_edge_lines.append((screen_pts[u_idx], screen_pts[v_idx]))

    # 6. Style-specific role color maps
    if style == "woodcut_vacuum":
        stroke_color = "#2b2116"
        stroke_width = 1.2
        role_base_colors = {
            "outer_frame": "#efe2c6",
            "window_reveal": "#c8ad7f",
            "inner_frame": "#8a6f47",
            "base": "#efe2c6",
            "truncation": "#d8bf97",
            "pyramid": "#e8d6b5",
        }
        fill_opacity = 1.0
    elif style == "woodcut_solidum":
        stroke_color = "#2b2116"
        stroke_width = 1.4
        role_base_colors = {
            "base": "#f4ede0",
            "outer_frame": "#f4ede0",
            "truncation": "#dfd2bc",
            "pyramid": "#ebdcc5",
            "window_reveal": "#d8caa8",
            "inner_frame": "#a89270",
        }
        fill_opacity = 1.0
    elif style == "elemental":
        stroke_color = "#1e3a8a"
        stroke_width = 1.3
        role_base_colors = {
            "base": "#93c5fd",
            "outer_frame": "#60a5fa",
            "window_reveal": "#3b82f6",
            "inner_frame": "#1d4ed8",
            "truncation": "#a5b4fc",
            "pyramid": "#7dd3fc",
        }
        fill_opacity = 0.22 if golden_polygons_3d else 0.88
    else:
        raise ValueError(
            f"Unknown render style: {style!r}. "
            "Supported: 'elemental', 'woodcut_vacuum', 'woodcut_solidum'."
        )

    # 7. Collect items for depth sorting (back to front by distance to camera)
    render_queue: list[tuple[float, str, int]] = []
    for fi, is_vis in enumerate(face_visible):
        if is_vis:
            render_queue.append((face_dist[fi], "face", fi))

    # Add golden polygons to queue
    for gi, gpoly in enumerate(golden_polys_norm):
        k_g = len(gpoly)
        cgx = sum(p[0] for p in gpoly) / k_g
        cgy = sum(p[1] for p in gpoly) / k_g
        cgz = sum(p[2] for p in gpoly) / k_g
        dist_g = _vec3_norm(_vec3_sub(cam_pos, (cgx, cgy, cgz)))
        render_queue.append((dist_g, "golden", gi))

    # Sort descending by distance: farthest rendered first
    render_queue.sort(key=lambda item: item[0], reverse=True)

    # 8. Build SVG Elements
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" class="euclid-graphic" '
        f'data-graphic-id="{html.escape(graphic_id)}">',
        "  <style>",
        "    .euclid-graphic {",
        "      font-family: 'Fira Sans Condensed', 'Fira Sans', sans-serif;",
        "    }",
        "    .poly-stroke {",
        f"      stroke: {stroke_color};",
        "      stroke-linejoin: round;",
        "      stroke-linecap: round;",
        "    }",
        "    .poly-hidden {",
        "      stroke: #94a3b8;",
        "      stroke-dasharray: 3 3;",
        "      stroke-width: 1.0;",
        "      opacity: 0.5;",
        "      fill: none;",
        "    }",
        "    .poly-gold {",
        "      fill: #f59e0b;",
        "      fill-opacity: 0.30;",
        "      stroke: #b45309;",
        "      stroke-width: 2.5;",
        "      stroke-linejoin: round;",
        "    }",
        "    @media (prefers-color-scheme: dark) {",
        "      .poly-stroke {",
        f"        stroke: {'#e8dec8' if 'woodcut' in style else '#93c5fd'};",
        "      }",
        "      .poly-hidden {",
        "        stroke: #64748b;",
        "        opacity: 0.6;",
        "      }",
        "    }",
        "    html[data-theme=\"dark\"] .poly-stroke {",
        f"      stroke: {'#e8dec8' if 'woodcut' in style else '#93c5fd'};",
        "    }",
        "    html[data-theme=\"dark\"] .poly-hidden {",
        "      stroke: #64748b;",
        "      opacity: 0.6;",
        "    }",
        "  </style>",
        "  <defs />",
    ]

    # Hidden dashed edges
    svg_lines.append('  <g id="hidden-edges">')
    for p1, p2 in hidden_edge_lines:
        svg_lines.append(
            f'    <line x1="{p1[0]:.2f}" y1="{p1[1]:.2f}" '
            f'x2="{p2[0]:.2f}" y2="{p2[1]:.2f}" class="poly-hidden" />'
        )
    svg_lines.append("  </g>")

    # Depth-sorted visible faces and golden polygons
    svg_lines.append('  <g id="faces">')
    for _, item_type, idx in render_queue:
        if item_type == "face":
            f = solid.faces[idx]
            role = solid.face_roles[idx] if idx < len(solid.face_roles) else "base"
            base_col = role_base_colors.get(role, "#efe2c6")
            shaded_col = _shade_hex(base_col, face_light[idx])

            pts_str = " ".join(
                f"{screen_pts[vi][0]:.2f},{screen_pts[vi][1]:.2f}" for vi in f
            )
            opac_str = f' fill-opacity="{fill_opacity}"' if fill_opacity < 1.0 else ""
            svg_lines.append(
                f'    <polygon points="{pts_str}" fill="{shaded_col}"{opac_str} '
                f'stroke="{stroke_color}" stroke-width="{stroke_width}" '
                f'class="poly-stroke" data-face-role="{role}" data-face-idx="{idx}" />'
            )
        elif item_type == "golden":
            gpoly_pts = proj_golden_polys[idx]
            screen_gpts = [to_screen(gp[0], gp[1]) for gp in gpoly_pts]
            pts_str = " ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in screen_gpts)
            svg_lines.append(
                f'    <polygon points="{pts_str}" class="poly-gold" '
                f'data-type="golden-polygon" data-gold-idx="{idx}" />'
            )
    svg_lines.append("  </g>")
    svg_lines.append("</svg>")

    result = "\n".join(svg_lines)
    # Verify XML validity
    ET.fromstring(result)
    return result


def render_net_svg(
    solid: Solid3D,
    *,
    width: int = 520,
    height: int = 420,
    graphic_id: str = "net",
) -> str:
    """Renders unfolded 2D papercraft net layout of a Solid3D to SVG.

    Uses dual graph BFS unfolding from geometor.polyhedra.model3d.bridge,
    drawing filled face polygons, dashed interior hinge folds, solid boundary
    cut lines, and centered face index labels.

    Args:
        solid: Exact symbolic Solid3D polyhedral model.
        width: SVG viewport width in pixels.
        height: SVG viewport height in pixels.
        graphic_id: Unique identifier for data-graphic-id attribute.

    Returns:
        Valid XML SVG string with class 'euclid-graphic'.
    """
    from geometor.polyhedra.model3d.bridge import unfold_net_2d

    net_faces = unfold_net_2d(solid)

    all_x = [pt[0] for f in net_faces for pt in f["pts_2d"]]  # type: ignore[union-attr]
    all_y = [pt[1] for f in net_faces for pt in f["pts_2d"]]  # type: ignore[union-attr]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    span_x = max(max_x - min_x, 1e-6)
    span_y = max(max_y - min_y, 1e-6)

    margin = 0.12
    target_w = width * (1.0 - 2.0 * margin)
    target_h = height * (1.0 - 2.0 * margin)
    scale = min(target_w / span_x, target_h / span_y)

    mid_x = (min_x + max_x) / 2.0
    mid_y = (min_y + max_y) / 2.0

    def to_screen(x: float, y: float) -> tuple[float, float]:
        px = width / 2.0 + (x - mid_x) * scale
        py = height / 2.0 - (y - mid_y) * scale
        return (px, py)

    # Classify edges into interior hinges vs outer boundary cuts
    edge_counts: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
    quantized_to_screen: dict[
        tuple[tuple[int, int], tuple[int, int]],
        tuple[tuple[float, float], tuple[float, float]],
    ] = {}

    for f_data in net_faces:
        pts = f_data["pts_2d"]  # type: ignore[index]
        k = len(pts)
        for i in range(k):
            p1 = pts[i]
            p2 = pts[(i + 1) % k]
            q1 = (round(p1[0] * 1000), round(p1[1] * 1000))
            q2 = (round(p2[0] * 1000), round(p2[1] * 1000))
            ekey = (min(q1, q2), max(q1, q2))
            edge_counts[ekey] = edge_counts.get(ekey, 0) + 1
            if ekey not in quantized_to_screen:
                quantized_to_screen[ekey] = (to_screen(p1[0], p1[1]), to_screen(p2[0], p2[1]))

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" class="euclid-graphic" '
        f'data-graphic-id="{html.escape(graphic_id)}">',
        "  <style>",
        "    .euclid-graphic {",
        "      font-family: 'Fira Sans Condensed', 'Fira Sans', sans-serif;",
        "    }",
        "    .net-face {",
        "      fill: #fdfbf7;",
        "      stroke: none;",
        "    }",
        "    .net-hinge {",
        "      stroke: #d97706;",
        "      stroke-width: 1.5;",
        "      stroke-dasharray: 5 3.5;",
        "      stroke-linecap: round;",
        "      fill: none;",
        "    }",
        "    .net-cut {",
        "      stroke: #1e293b;",
        "      stroke-width: 1.8;",
        "      stroke-linecap: round;",
        "      stroke-linejoin: round;",
        "      fill: none;",
        "    }",
        "    .geom-label {",
        "      font-family: 'Fira Sans Condensed', 'Fira Sans', sans-serif;",
        "      font-size: 13px;",
        "      font-weight: 700;",
        "      fill: #1e293b;",
        "    }",
        "    @media (prefers-color-scheme: dark) {",
        "      .net-face { fill: #1c2128; }",
        "      .net-cut { stroke: #e2d5b8; }",
        "      .net-hinge { stroke: #fbbf24; }",
        "      .geom-label { fill: #f1f5f9; }",
        "    }",
        "    html[data-theme=\"dark\"] .net-face { fill: #1c2128; }",
        "    html[data-theme=\"dark\"] .net-cut { stroke: #e2d5b8; }",
        "    html[data-theme=\"dark\"] .net-hinge { stroke: #fbbf24; }",
        "    html[data-theme=\"dark\"] .geom-label { fill: #f1f5f9; }",
        "  </style>",
        "  <defs />",
    ]

    # Draw face polygons
    svg_lines.append('  <g id="net-faces">')
    for f_data in net_faces:
        pts = f_data["pts_2d"]  # type: ignore[index]
        screen_pts = [to_screen(p[0], p[1]) for p in pts]
        pts_str = " ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in screen_pts)
        svg_lines.append(
            f'    <polygon points="{pts_str}" class="net-face" '
            f'data-face-idx="{f_data["face_index"]}" />'  # type: ignore[index]
        )
    svg_lines.append("  </g>")

    # Draw interior hinge edges (shared edges)
    svg_lines.append('  <g id="net-hinges">')
    for ekey, count in edge_counts.items():
        if count >= 2:
            p1, p2 = quantized_to_screen[ekey]
            svg_lines.append(
                f'    <line x1="{p1[0]:.2f}" y1="{p1[1]:.2f}" '
                f'x2="{p2[0]:.2f}" y2="{p2[1]:.2f}" class="net-hinge" />'
            )
    svg_lines.append("  </g>")

    # Draw outer boundary cut edges
    svg_lines.append('  <g id="net-cuts">')
    for ekey, count in edge_counts.items():
        if count == 1:
            p1, p2 = quantized_to_screen[ekey]
            svg_lines.append(
                f'    <line x1="{p1[0]:.2f}" y1="{p1[1]:.2f}" '
                f'x2="{p2[0]:.2f}" y2="{p2[1]:.2f}" class="net-cut" />'
            )
    svg_lines.append("  </g>")

    # Draw face index labels
    svg_lines.append('  <g id="net-labels">')
    for f_data in net_faces:
        pts = f_data["pts_2d"]  # type: ignore[index]
        k = len(pts)
        screen_pts = [to_screen(p[0], p[1]) for p in pts]
        cx_lbl = sum(p[0] for p in screen_pts) / k
        cy_lbl = sum(p[1] for p in screen_pts) / k
        lbl_text = f"F{int(f_data['face_index']) + 1}"  # type: ignore[call-overload]
        svg_lines.append(
            f'    <text x="{cx_lbl:.2f}" y="{cy_lbl:.2f}" text-anchor="middle" '
            f'dominant-baseline="central" class="geom-label">{lbl_text}</text>'
        )
    svg_lines.append("  </g>")
    svg_lines.append("</svg>")

    result = "\n".join(svg_lines)
    ET.fromstring(result)
    return result


def render_model2d_svg(
    model: Model,
    *,
    golden_segments: list[tuple[str, str, str]] | None = None,
    width: int = 520,
    height: int = 480,
    graphic_id: str = "slice",
) -> str:
    """Renders a 2D GEOMETOR symbolic Model to publication-grade SVG.

    Renders circles, polygons, 3-vertex midpoint path segments, points, and
    labels with data-ref attributes using luminous gold and sky-blue theme
    colors with full dark-mode adaptation.

    Args:
        model: Exact symbolic 2D geometor.model.Model instance.
        golden_segments: Optional list of (pt1_label, pt2_label, role) triples
            designating golden ratio segments to highlight in gold or terracotta.
        width: SVG viewport width in pixels.
        height: SVG viewport height in pixels.
        graphic_id: Unique identifier for data-graphic-id attribute.

    Returns:
        Valid XML SVG string with class 'euclid-graphic'.
    """
    # 1. Collect points and compute 2D bounding box
    pts_dict: dict[object, tuple[float, float, str]] = {}
    label_to_pt: dict[str, object] = {}

    all_x: list[float] = []
    all_y: list[float] = []

    for pt in model.points:
        xf = float(pt.x.evalf())
        yf = float(pt.y.evalf())
        elem = model.get(pt)
        lbl = str(elem.ID) if elem is not None and hasattr(elem, "ID") else ""
        pts_dict[pt] = (xf, yf, lbl)
        if lbl:
            label_to_pt[lbl] = pt
        all_x.append(xf)
        all_y.append(yf)

    # Include circle extents in bounding box
    circles_data: list[tuple[float, float, float, str]] = []
    for c in model.circles:
        c_xf = float(c.center.x.evalf())
        c_yf = float(c.center.y.evalf())
        c_rf = float(c.radius.evalf())
        elem = model.get(c)
        c_lbl = str(elem.ID) if elem is not None and hasattr(elem, "ID") else ""
        circles_data.append((c_xf, c_yf, c_rf, c_lbl))
        all_x.extend([c_xf - c_rf, c_xf + c_rf])
        all_y.extend([c_yf - c_rf, c_yf + c_rf])

    if not all_x:
        all_x = [-1.0, 1.0]
        all_y = [-1.0, 1.0]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    span_x = max(max_x - min_x, 1e-6)
    span_y = max(max_y - min_y, 1e-6)

    margin = 0.12
    target_w = width * (1.0 - 2.0 * margin)
    target_h = height * (1.0 - 2.0 * margin)
    scale = min(target_w / span_x, target_h / span_y)

    mid_x = (min_x + max_x) / 2.0
    mid_y = (min_y + max_y) / 2.0

    def to_screen(x: float, y: float) -> tuple[float, float]:
        px = width / 2.0 + (x - mid_x) * scale
        py = height / 2.0 - (y - mid_y) * scale
        return (px, py)

    # Build golden segment lookup set
    golden_map: dict[tuple[str, str], str] = {}
    if golden_segments:
        for p1_lbl, p2_lbl, role in golden_segments:
            golden_map[(p1_lbl, p2_lbl)] = role
            golden_map[(p2_lbl, p1_lbl)] = role

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" class="euclid-graphic" '
        f'data-graphic-id="{html.escape(graphic_id)}">',
        "  <style>",
        "    .euclid-graphic {",
        "      font-family: 'Fira Sans Condensed', 'Fira Sans', sans-serif;",
        "    }",
        "    .geom-poly {",
        "      fill: #0284c7;",
        "      fill-opacity: 0.08;",
        "      stroke: #0284c7;",
        "      stroke-width: 1.6;",
        "      stroke-linejoin: round;",
        "    }",
        "    .geom-circle {",
        "      stroke: #64748b;",
        "      stroke-width: 1.2;",
        "      stroke-dasharray: 4 3;",
        "      fill: none;",
        "    }",
        "    .geom-seg {",
        "      stroke: #0284c7;",
        "      stroke-width: 1.8;",
        "      stroke-linecap: round;",
        "      stroke-linejoin: round;",
        "      fill: none;",
        "    }",
        "    .geom-gold-major {",
        "      stroke: #d4af37;",
        "      stroke-width: 2.5;",
        "      stroke-linecap: round;",
        "      stroke-linejoin: round;",
        "      fill: none;",
        "    }",
        "    .geom-gold-minor {",
        "      stroke: #c2410c;",
        "      stroke-width: 2.2;",
        "      stroke-linecap: round;",
        "      stroke-linejoin: round;",
        "      fill: none;",
        "    }",
        "    .geom-point {",
        "      fill: #0f172a;",
        "      stroke: #ffffff;",
        "      stroke-width: 1.2;",
        "    }",
        "    .geom-label {",
        "      font-family: 'Fira Sans Condensed', 'Fira Sans', sans-serif;",
        "      font-size: 13px;",
        "      font-weight: 700;",
        "      fill: #0f172a;",
        "    }",
        "    @media (prefers-color-scheme: dark) {",
        "      .geom-poly { fill: #38bdf8; fill-opacity: 0.12; stroke: #38bdf8; }",
        "      .geom-seg { stroke: #38bdf8; }",
        "      .geom-gold-major { stroke: #fbbf24; }",
        "      .geom-gold-minor { stroke: #ea580c; }",
        "      .geom-point { fill: #f8fafc; stroke: #0f172a; }",
        "      .geom-label { fill: #f8fafc; }",
        "      .geom-circle { stroke: #94a3b8; }",
        "    }",
        "    html[data-theme=\"dark\"] .geom-poly { fill: #38bdf8; fill-opacity: 0.12; stroke: #38bdf8; }",
        "    html[data-theme=\"dark\"] .geom-seg { stroke: #38bdf8; }",
        "    html[data-theme=\"dark\"] .geom-gold-major { stroke: #fbbf24; }",
        "    html[data-theme=\"dark\"] .geom-gold-minor { stroke: #ea580c; }",
        "    html[data-theme=\"dark\"] .geom-point { fill: #f8fafc; stroke: #0f172a; }",
        "    html[data-theme=\"dark\"] .geom-label { fill: #f8fafc; }",
        "    html[data-theme=\"dark\"] .geom-circle { stroke: #94a3b8; }",
        "  </style>",
        "  <defs />",
    ]

    # Draw Polygons
    svg_lines.append('  <g id="polygons">')
    for poly in model.polygons:
        poly_pts = [to_screen(float(v.x.evalf()), float(v.y.evalf())) for v in poly.vertices]
        pts_str = " ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in poly_pts)
        elem = model.get(poly)
        poly_id = str(elem.ID) if elem is not None and hasattr(elem, "ID") else ""
        svg_lines.append(
            f'    <polygon points="{pts_str}" class="geom-poly" '
            f'data-ref="{html.escape(poly_id)}" />'
        )
    svg_lines.append("  </g>")

    # Draw Circles
    svg_lines.append('  <g id="circles">')
    for c_xf, c_yf, c_rf, c_lbl in circles_data:
        spx, spy = to_screen(c_xf, c_yf)
        s_r = c_rf * scale
        svg_lines.append(
            f'    <circle cx="{spx:.2f}" cy="{spy:.2f}" r="{s_r:.2f}" '
            f'class="geom-circle" data-ref="{html.escape(c_lbl)}" />'
        )
    svg_lines.append("  </g>")

    # Draw 3-vertex midpoint path segments
    svg_lines.append('  <g id="segments">')
    for seg in model.segments:
        p1 = seg.p1
        p2 = seg.p2
        p1_x, p1_y, p1_lbl = pts_dict.get(p1, (float(p1.x.evalf()), float(p1.y.evalf()), ""))
        p2_x, p2_y, p2_lbl = pts_dict.get(p2, (float(p2.x.evalf()), float(p2.y.evalf()), ""))

        pm_x = (p1_x + p2_x) / 2.0
        pm_y = (p1_y + p2_y) / 2.0

        sp1 = to_screen(p1_x, p1_y)
        spm = to_screen(pm_x, pm_y)
        sp2 = to_screen(p2_x, p2_y)

        # Check golden highlighting
        role = golden_map.get((p1_lbl, p2_lbl))
        if role == "major":
            seg_class = "geom-gold-major"
        elif role == "minor":
            seg_class = "geom-gold-minor"
        elif role:
            seg_class = "geom-gold-major"
        else:
            seg_class = "geom-seg"

        elem = model.get(seg)
        seg_id = str(elem.ID) if elem is not None and hasattr(elem, "ID") else ""
        d_path = f"M {sp1[0]:.2f} {sp1[1]:.2f} L {spm[0]:.2f} {spm[1]:.2f} L {sp2[0]:.2f} {sp2[1]:.2f}"
        svg_lines.append(
            f'    <path d="{d_path}" class="{seg_class}" '
            f'data-ref="{html.escape(seg_id)}" data-type="segment" />'
        )
    svg_lines.append("  </g>")

    # Draw Points
    svg_lines.append('  <g id="points">')
    for pt, (xf, yf, lbl) in pts_dict.items():
        spx, spy = to_screen(xf, yf)
        svg_lines.append(
            f'    <circle cx="{spx:.2f}" cy="{spy:.2f}" r="3.2" '
            f'class="geom-point" data-ref="{html.escape(lbl)}" data-type="point" />'
        )
    svg_lines.append("  </g>")

    # Draw Labels
    svg_lines.append('  <g id="labels">')
    for pt, (xf, yf, lbl) in pts_dict.items():
        if lbl:
            spx, spy = to_screen(xf, yf)
            svg_lines.append(
                f'    <text x="{spx + 6.0:.2f}" y="{spy - 6.0:.2f}" '
                f'class="geom-label" data-ref="{html.escape(lbl)}">{html.escape(lbl)}</text>'
            )
    svg_lines.append("  </g>")
    svg_lines.append("</svg>")

    result = "\n".join(svg_lines)
    ET.fromstring(result)
    return result
