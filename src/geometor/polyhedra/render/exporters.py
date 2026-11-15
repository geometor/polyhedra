"""Export pipelines for 3D polyhedra into Wavefront CAD, IngeTrazo, and Blender.

Provides three export targets:

- ``export_obj_mtl``: Wavefront ``.obj`` and companion ``.mtl`` with face role materials.
- ``export_ingetrazo_script``: Runnable Python script for IngeTrazo 0.6.0 CAD.
- ``export_blender_script``: Standalone Blender 5.x Python studio generator.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from geometor.polyhedra.model3d.primitives import Solid3D


def export_obj_mtl(solid: Solid3D, obj_path: Path) -> tuple[Path, Path]:
    """Exports a Solid3D to Wavefront .obj and companion .mtl material library.

    Maps face_roles ('base', 'outer_frame', 'window_reveal', 'inner_frame',
    'truncation', 'pyramid') to distinct Renaissance boxwood, alabaster, and
    stone material definitions.

    Args:
        solid: Exact symbolic Solid3D polyhedral model.
        obj_path: Target filesystem path for the .obj file.

    Returns:
        Tuple of (obj_path, mtl_path).
    """
    obj_path = Path(obj_path)
    obj_path.parent.mkdir(parents=True, exist_ok=True)
    mtl_path = obj_path.with_suffix(".mtl")

    # 1. Generate companion .mtl file
    mtl_content = [
        f"# GEOMETOR Polyhedra Material Library: {solid.slug}",
        "# Renaissance Woodcut & Alabaster Palette",
        "",
        "# Alabaster / Parchment Base Solid",
        "newmtl base",
        "Ka 0.20 0.20 0.20",
        "Kd 0.90 0.87 0.82",
        "Ks 0.15 0.15 0.15",
        "Ns 10.0",
        "illum 2",
        "",
        "# Renaissance Boxwood Outer Frame",
        "newmtl outer_frame",
        "Ka 0.22 0.20 0.16",
        "Kd 0.937 0.886 0.776",
        "Ks 0.12 0.12 0.12",
        "Ns 8.0",
        "illum 2",
        "",
        "# Deep Boxwood Window Reveal (Frame Thickness)",
        "newmtl window_reveal",
        "Ka 0.18 0.15 0.10",
        "Kd 0.784 0.678 0.498",
        "Ks 0.10 0.10 0.10",
        "Ns 8.0",
        "illum 2",
        "",
        "# Walnut Tone Inner Frame (Hollow Cavity)",
        "newmtl inner_frame",
        "Ka 0.12 0.10 0.06",
        "Kd 0.541 0.435 0.278",
        "Ks 0.06 0.06 0.06",
        "Ns 6.0",
        "illum 2",
        "",
        "# Sandstone Truncation Facets",
        "newmtl truncation",
        "Ka 0.18 0.18 0.18",
        "Kd 0.85 0.80 0.74",
        "Ks 0.15 0.15 0.15",
        "Ns 12.0",
        "illum 2",
        "",
        "# Ochre Pyramid Facets",
        "newmtl pyramid",
        "Ka 0.20 0.18 0.12",
        "Kd 0.92 0.84 0.71",
        "Ks 0.16 0.16 0.16",
        "Ns 12.0",
        "illum 2",
    ]
    mtl_path.write_text("\n".join(mtl_content) + "\n", encoding="utf-8")

    # 2. Generate .obj file
    obj_lines = [
        f"# GEOMETOR Polyhedra Wavefront OBJ: {solid.title}",
        f"# Slug: {solid.slug}",
        f"# Vertices: {solid.num_vertices}, Faces: {solid.num_faces}, Edges: {solid.num_edges}",
        f"mtllib {mtl_path.name}",
        f"o {solid.slug}",
        "",
    ]

    # Write vertices
    for v in solid.vertices:
        vx = float(v.x.evalf())
        vy = float(v.y.evalf())
        vz = float(v.z.evalf())
        obj_lines.append(f"v {vx:.6f} {vy:.6f} {vz:.6f}")

    # Group faces by role for clean material assignment
    role_groups: dict[str, list[tuple[int, ...]]] = {}
    for fi, f in enumerate(solid.faces):
        role = solid.face_roles[fi] if fi < len(solid.face_roles) else "base"
        role_groups.setdefault(role, []).append(f)

    for role, flist in role_groups.items():
        obj_lines.append("")
        obj_lines.append(f"g {solid.slug}_{role}")
        obj_lines.append(f"usemtl {role}")
        for f in flist:
            # 1-based indexing in Wavefront OBJ
            f_str = " ".join(str(vi + 1) for vi in f)
            obj_lines.append(f"f {f_str}")

    obj_path.write_text("\n".join(obj_lines) + "\n", encoding="utf-8")
    return (obj_path, mtl_path)


def export_ingetrazo_script(
    solids: list[Solid3D],
    script_path: Path,
    spacing: float = 4.5,
) -> Path:
    """Emits a runnable Python script for IngeTrazo 0.6.0 CAD modeler.

    Lays out polyhedra along the X-axis on named layers ('Platonic_Solida',
    'Leonardo_Vacua') with warm boxwood and alabaster materials.

    Args:
        solids: List of Solid3D polyhedral models to include in the scene.
        script_path: Target filesystem path for the emitted Python script.
        spacing: Center-to-center offset along the X axis between models.

    Returns:
        Path to the generated Python script.
    """
    script_path = Path(script_path)
    script_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# ruff: noqa: F821",
        '"""IngeTrazo 0.6.0 Polyhedral Showcase Generator.',
        "",
        "Lays out exact Platonic and Leonardo polyhedra along the X-axis with",
        "distinct layers and materials. Executes inside the IngeTrazo live",
        "Python runtime (Mesh, Group, Layer, QVector3D, groups, layers, viewport).",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "# Ensure layers exist in scene",
        'layer_names = [ly.name for ly in layers if hasattr(ly, "name")]',
        'if "Platonic_Solida" not in layer_names:',
        '    layers.append(Layer("Platonic_Solida"))',
        'if "Leonardo_Vacua" not in layer_names:',
        '    layers.append(Layer("Leonardo_Vacua"))',
        "",
    ]

    for i, solid in enumerate(solids):
        x_off = i * spacing
        is_vacuum = "vacu" in solid.slug
        layer_name = "Leonardo_Vacua" if is_vacuum else "Platonic_Solida"
        mat_color = (0.91, 0.82, 0.65) if is_vacuum else (0.95, 0.93, 0.90)

        lines.append(f"# --- Polyhedron {i + 1}: {solid.title} ---")
        lines.append("m = Mesh()")

        # Add faces to mesh
        for fi, f in enumerate(solid.faces):
            pts_code: list[str] = []
            for vi in f:
                v = solid.vertices[vi]
                vx = float(v.x.evalf()) + x_off
                vy = float(v.y.evalf())
                vz = float(v.z.evalf())
                pts_code.append(f"QVector3D({vx:.4f}, {vy:.4f}, {vz:.4f})")
            pts_str = ", ".join(pts_code)
            lines.append(f"f = m.add_face([{pts_str}])")
            lines.append(f'f.attrs["role"] = "{solid.face_roles[fi]}"')

        grp_var = f"g_{i}"
        lines.append(f'{grp_var} = Group(m, name="{solid.title}")')
        lines.append(f'{grp_var}.layer = "{layer_name}"')
        lines.append(
            f"{grp_var}.material = {{"
            f'"color": ({mat_color[0]:.2f}, {mat_color[1]:.2f}, {mat_color[2]:.2f}), '
            f'"opacity": 1.0}}'
        )
        lines.append(f"groups.append({grp_var})")
        lines.append("")

    # Viewport setup
    mid_x = (len(solids) - 1) * spacing / 2.0 if solids else 0.0
    cam_dist = max(spacing * len(solids), 8.0) if solids else 8.0
    lines.extend([
        "# Configure viewport camera framing",
        f"viewport.camera.target = QVector3D({mid_x:.2f}, 0.0, 0.0)",
        f"viewport.camera.distance = {cam_dist:.2f}",
        "viewport.camera.yaw = 0.55",
        "viewport.camera.pitch = 0.38",
        "viewport.update()",
        f'print("Rendered {len(solids)} polyhedra in IngeTrazo scene.")',
        "",
    ])

    script_path.write_text("\n".join(lines), encoding="utf-8")
    return script_path


def export_blender_script(
    solids: list[Solid3D],
    script_path: Path,
    spacing: float = 4.5,
) -> Path:
    """Emits a standalone Blender 5.x Python script generating a studio showcase.

    Creates collections, meshes, Principled BSDF materials (Boxwood, Alabaster,
    Gold), studio 3-point lighting, and camera framing.

    Args:
        solids: List of Solid3D polyhedral models to include in the scene.
        script_path: Target filesystem path for the emitted Python script.
        spacing: Center-to-center offset along the X axis between models.

    Returns:
        Path to the generated Python script.
    """
    script_path = Path(script_path)
    script_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        '"""Blender 5.x Polyhedral Studio Showcase Generator.',
        "",
        "Generates studio lighting, materials, and polyhedra meshes along the X-axis.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "import bpy",
        "",
        "",
        "def create_material(",
        "    name: str,",
        "    color: tuple[float, float, float, float],",
        "    roughness: float,",
        "    metallic: float = 0.0,",
        ") -> bpy.types.Material:",
        '    """Creates or retrieves a Principled BSDF material."""',
        "    mat = bpy.data.materials.get(name)",
        "    if mat is None:",
        "        mat = bpy.data.materials.new(name=name)",
        "        mat.use_nodes = True",
        "        bsdf = mat.node_tree.nodes.get('Principled BSDF')",
        "        if bsdf:",
        "            bsdf.inputs['Base Color'].default_value = color",
        "            bsdf.inputs['Roughness'].default_value = roughness",
        "            bsdf.inputs['Metallic'].default_value = metallic",
        "    return mat",
        "",
        "",
        "def build_scene() -> None:",
        '    """Builds the complete polyhedral studio showcase scene."""',
        "    # 1. Setup Collection",
        '    col_name = "GEOMETOR_Polyhedra"',
        "    col = bpy.data.collections.get(col_name)",
        "    if col is None:",
        "        col = bpy.data.collections.new(col_name)",
        "        bpy.context.scene.collection.children.link(col)",
        "",
        "    # 2. Setup Materials",
        "    mat_boxwood = create_material('Boxwood', (0.85, 0.72, 0.52, 1.0), 0.45)",
        "    mat_alabaster = create_material('Alabaster', (0.94, 0.92, 0.88, 1.0), 0.25)",
        "    mat_gold = create_material('Gold', (1.0, 0.766, 0.336, 1.0), 0.20, 1.0)",
        "",
    ]

    for i, solid in enumerate(solids):
        x_off = i * spacing
        if "vacu" in solid.slug:
            mat_var = "mat_boxwood"
        elif "elev" in solid.slug or "gold" in solid.slug or "dual" in solid.slug:
            mat_var = "mat_gold"
        else:
            mat_var = "mat_alabaster"

        verts_repr = [
            (
                round(float(v.x.evalf()) + x_off, 4),
                round(float(v.y.evalf()), 4),
                round(float(v.z.evalf()), 4),
            )
            for v in solid.vertices
        ]
        faces_repr = [list(f) for f in solid.faces]

        lines.extend([
            f"    # Polyhedron {i + 1}: {solid.title}",
            f"    verts_{i} = {verts_repr!r}",
            f"    faces_{i} = {faces_repr!r}",
            f'    mesh_{i} = bpy.data.meshes.new(name="{solid.slug}_mesh")',
            f"    mesh_{i}.from_pydata(verts_{i}, [], faces_{i})",
            f"    mesh_{i}.update()",
            f'    obj_{i} = bpy.data.objects.new(name="{solid.slug}", object_data=mesh_{i})',
            f"    obj_{i}.data.materials.append({mat_var})",
            f"    obj_{i}.data.materials.append(mat_gold)",
            f"    col.objects.link(obj_{i})",
            "",
        ])

    mid_x = (len(solids) - 1) * spacing / 2.0 if solids else 0.0
    cam_y = -max(spacing * len(solids) * 0.9, 10.0) if solids else -10.0

    lines.extend([
        "    # 3. Studio 3-Point Lighting",
        '    key_data = bpy.data.lights.new(name="Key_Light", type="AREA")',
        "    key_data.energy = 800.0",
        "    key_data.size = 5.0",
        '    key_obj = bpy.data.objects.new(name="Key_Light", object_data=key_data)',
        f"    key_obj.location = ({mid_x - 6.0:.2f}, {cam_y * 0.5:.2f}, 8.0)",
        "    col.objects.link(key_obj)",
        "",
        '    fill_data = bpy.data.lights.new(name="Fill_Light", type="AREA")',
        "    fill_data.energy = 350.0",
        "    fill_data.size = 4.0",
        '    fill_obj = bpy.data.objects.new(name="Fill_Light", object_data=fill_data)',
        f"    fill_obj.location = ({mid_x + 6.0:.2f}, {cam_y * 0.6:.2f}, 5.0)",
        "    col.objects.link(fill_obj)",
        "",
        '    rim_data = bpy.data.lights.new(name="Rim_Light", type="POINT")',
        "    rim_data.energy = 500.0",
        '    rim_obj = bpy.data.objects.new(name="Rim_Light", object_data=rim_data)',
        f"    rim_obj.location = ({mid_x:.2f}, {-cam_y * 0.6:.2f}, 6.0)",
        "    col.objects.link(rim_obj)",
        "",
        "    # 4. Studio Camera",
        '    cam_data = bpy.data.cameras.new(name="Studio_Camera")',
        "    cam_data.lens = 50.0",
        '    cam_obj = bpy.data.objects.new(name="Studio_Camera", object_data=cam_data)',
        f"    cam_obj.location = ({mid_x:.2f}, {cam_y:.2f}, 5.5)",
        "    cam_obj.rotation_euler = (1.20, 0.0, 0.0)",
        "    col.objects.link(cam_obj)",
        "    bpy.context.scene.camera = cam_obj",
        "",
        "",
        'if __name__ == "__main__":',
        "    build_scene()",
        "",
    ])

    script_path.write_text("\n".join(lines), encoding="utf-8")
    return script_path
