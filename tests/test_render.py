"""Tests for polyhedra 3D SVG rendering and CAD export pipelines."""

from __future__ import annotations

import ast
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
import sympy as sp
from geometor.model import Model

from geometor.polyhedra.model3d.bridge import slice_solid_to_model
from geometor.polyhedra.model3d.primitives import (
    Plane3D,
    Solid3D,
    Vector3D,
)
from geometor.polyhedra.operators import vacuate
from geometor.polyhedra.platonic import get_platonic_solid
from geometor.polyhedra.render import (
    export_blender_script,
    export_ingetrazo_script,
    export_obj_mtl,
    render_model2d_svg,
    render_net_svg,
    render_solid_svg,
)

if TYPE_CHECKING:
    pass


def test_render_solid_svg_styles_and_xml() -> None:
    """Verifies render_solid_svg produces valid XML across all styles."""
    oct_solid = Solid3D.from_regular_solid(get_platonic_solid("octahedron"))

    # Elemental style
    svg_elem = render_solid_svg(
        oct_solid,
        style="elemental",
        graphic_id="oct_elem",
        show_hidden_edges=True,
    )
    root_elem = ET.fromstring(svg_elem)
    assert root_elem.tag.endswith("svg")
    assert root_elem.attrib["data-graphic-id"] == "oct_elem"
    assert "class" in root_elem.attrib and "euclid-graphic" in root_elem.attrib["class"]
    assert "poly-stroke" in svg_elem
    assert "poly-hidden" in svg_elem

    # Woodcut solidum
    svg_wood_solid = render_solid_svg(
        oct_solid,
        style="woodcut_solidum",
        graphic_id="oct_wood_solid",
        show_hidden_edges=False,
    )
    root_wood = ET.fromstring(svg_wood_solid)
    assert root_wood.tag.endswith("svg")
    assert "#2b2116" in svg_wood_solid

    # Woodcut vacuum
    oct_vac = vacuate(oct_solid)
    svg_wood_vac = render_solid_svg(
        oct_vac,
        style="woodcut_vacuum",
        graphic_id="oct_wood_vac",
    )
    root_vac = ET.fromstring(svg_wood_vac)
    assert root_vac.tag.endswith("svg")
    assert "outer_frame" in svg_wood_vac
    assert "window_reveal" in svg_wood_vac

    # Invalid style raises ValueError
    with pytest.raises(ValueError, match="Unknown render style"):
        render_solid_svg(oct_solid, style="unknown_style")

    # Empty solid raises ValueError
    empty_solid = Solid3D(slug="empty", title="Empty", vertices=(), faces=())
    with pytest.raises(ValueError, match="no vertices"):
        render_solid_svg(empty_solid)


def test_render_solid_svg_camera_angles() -> None:
    """Verifies camera orbit and projection parameter variations."""
    cube = Solid3D.from_regular_solid(get_platonic_solid("hexahedron"))
    svg_out = render_solid_svg(
        cube,
        yaw_deg=45.0,
        pitch_deg=35.264,
        roll_deg=10.0,
        camera_dist=6.0,
        focal_length=5.0,
        width=600,
        height=500,
        graphic_id="cube_isometric",
    )
    root = ET.fromstring(svg_out)
    assert root.attrib["width"] == "600"
    assert root.attrib["height"] == "500"
    assert root.attrib["viewBox"] == "0 0 600 500"


def test_render_solid_svg_golden_polygons() -> None:
    """Verifies depth-interleaved golden polygons rendering."""
    ico_solid = Solid3D.from_regular_solid(get_platonic_solid("icosahedron"))

    # Define a 3D golden rectangle loop
    golden_loop = [
        (-1.0, 0.0, 1.618),
        (1.0, 0.0, 1.618),
        (1.0, 0.0, -1.618),
        (-1.0, 0.0, -1.618),
    ]

    svg_gold = render_solid_svg(
        ico_solid,
        golden_polygons_3d=[golden_loop],
        graphic_id="ico_gold",
    )
    root = ET.fromstring(svg_gold)
    assert root.tag.endswith("svg")
    assert "poly-gold" in svg_gold
    assert 'data-type="golden-polygon"' in svg_gold


def test_render_net_svg() -> None:
    """Verifies render_net_svg unfolds 2D net with hinges, cuts, and labels."""
    tetra = Solid3D.from_regular_solid(get_platonic_solid("tetrahedron"))
    svg_net = render_net_svg(tetra, graphic_id="tetra_net")

    root = ET.fromstring(svg_net)
    assert root.tag.endswith("svg")
    assert root.attrib["data-graphic-id"] == "tetra_net"
    assert "net-face" in svg_net
    assert "net-hinge" in svg_net
    assert "net-cut" in svg_net
    assert "geom-label" in svg_net
    assert "F1" in svg_net


def test_render_all_platonic_nets() -> None:
    """Verifies unfolding and SVG generation across all 5 Platonic solids."""
    for slug in ("tetrahedron", "hexahedron", "octahedron", "icosahedron", "dodecahedron"):
        solid = Solid3D.from_regular_solid(get_platonic_solid(slug))
        svg_net = render_net_svg(solid, graphic_id=f"{slug}_net")
        root = ET.fromstring(svg_net)
        assert root.tag.endswith("svg")



def test_render_model2d_svg() -> None:
    """Verifies 2D Model rendering with golden segments and 3-vertex paths."""
    cube = Solid3D.from_regular_solid(get_platonic_solid("hexahedron"))
    plane = Plane3D(sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(0))
    u_ax = Vector3D(sp.Integer(1), sp.Integer(0), sp.Integer(0))
    v_ax = Vector3D(sp.Integer(0), sp.Integer(1), sp.Integer(0))

    model_2d = slice_solid_to_model(cube, plane, u_ax, v_ax, name="cube_slice")

    golden_segs = [
        ("P_0", "P_1", "major"),
        ("P_1", "P_2", "minor"),
    ]

    svg_slice = render_model2d_svg(
        model_2d,
        golden_segments=golden_segs,
        graphic_id="test_slice",
    )

    root = ET.fromstring(svg_slice)
    assert root.tag.endswith("svg")
    assert root.attrib["data-graphic-id"] == "test_slice"
    assert "geom-poly" in svg_slice
    assert "geom-gold-major" in svg_slice
    assert "geom-gold-minor" in svg_slice
    assert "geom-point" in svg_slice
    assert "geom-label" in svg_slice
    # Verify 3-vertex midpoint path notation: 'M ... L ... L ...'
    assert "M " in svg_slice
    assert " L " in svg_slice


def test_render_model2d_svg_with_circles() -> None:
    """Verifies 2D Model rendering with circles."""
    m = Model("circle_test", auto_intersect=False)
    p1 = m.set_point(0, 0, label="O")
    p2 = m.set_point(1, 0, label="A")
    m.construct_circle(p1, p2)

    svg_str = render_model2d_svg(m, graphic_id="circ_test")
    root = ET.fromstring(svg_str)
    assert root.tag.endswith("svg")
    assert "geom-circle" in svg_str


def test_export_obj_mtl(tmp_path: Path) -> None:
    """Verifies Wavefront .obj and companion .mtl exports."""
    ico_solid = Solid3D.from_regular_solid(get_platonic_solid("icosahedron"))
    obj_file = tmp_path / "ico.obj"

    obj_out, mtl_out = export_obj_mtl(ico_solid, obj_file)

    assert obj_out.exists()
    assert mtl_out.exists()

    obj_text = obj_out.read_text(encoding="utf-8")
    mtl_text = mtl_out.read_text(encoding="utf-8")

    assert "mtllib ico.mtl" in obj_text
    assert "o icosahedron" in obj_text
    assert "v " in obj_text
    assert "f " in obj_text
    assert "usemtl " in obj_text

    assert "newmtl base" in mtl_text
    assert "newmtl outer_frame" in mtl_text
    assert "Kd " in mtl_text


def test_export_ingetrazo_script(tmp_path: Path) -> None:
    """Verifies IngeTrazo Python script syntax and structure."""
    tetra = Solid3D.from_regular_solid(get_platonic_solid("tetrahedron"))
    vac_tetra = vacuate(tetra)

    script_path = tmp_path / "test_ingetrazo.py"
    export_ingetrazo_script([tetra, vac_tetra], script_path)

    assert script_path.exists()
    content = script_path.read_text(encoding="utf-8")

    # Validate Python syntax via AST
    parsed_ast = ast.parse(content)
    assert parsed_ast is not None

    assert "Mesh()" in content
    assert "Group(" in content
    assert "Layer(" in content
    assert "QVector3D(" in content
    assert "Platonic_Solida" in content
    assert "Leonardo_Vacua" in content


def test_export_blender_script(tmp_path: Path) -> None:
    """Verifies Blender 5.x Python script syntax and structure."""
    cube = Solid3D.from_regular_solid(get_platonic_solid("hexahedron"))
    script_path = tmp_path / "test_blender.py"

    export_blender_script([cube], script_path)

    assert script_path.exists()
    content = script_path.read_text(encoding="utf-8")

    # Validate Python syntax via AST
    parsed_ast = ast.parse(content)
    assert parsed_ast is not None

    assert "import bpy" in content
    assert "bpy.data.meshes.new" in content
    assert "GEOMETOR_Polyhedra" in content
    assert "Key_Light" in content
    assert "Studio_Camera" in content


def test_generated_static_assets_exist_and_valid_xml() -> None:
    """Verifies all required static SVG assets exist and are valid XML."""
    svg_dir = Path("/home/phi/PROJECTS/geometor/polyhedra/docsrc/_static/svg/platonic")
    assert svg_dir.exists()

    expected_svgs = [
        "tetrahedron_solidum.svg",
        "tetrahedron_vacuum.svg",
        "tetrahedron_net.svg",
        "hexahedron_solidum.svg",
        "hexahedron_vacuum.svg",
        "hexahedron_net.svg",
        "octahedron_solidum.svg",
        "octahedron_vacuum.svg",
        "octahedron_net.svg",
        "icosahedron_solidum.svg",
        "icosahedron_vacuum.svg",
        "icosahedron_net.svg",
        "dodecahedron_solidum.svg",
        "dodecahedron_vacuum.svg",
        "dodecahedron_net.svg",
        "octahedron_elevatum.svg",
        "hexahedron_abscisum.svg",
        "dodecahedron_abscisum.svg",
    ]

    for fname in expected_svgs:
        fpath = svg_dir / fname
        assert fpath.exists(), f"Missing required static SVG: {fname}"
        content = fpath.read_text(encoding="utf-8")
        assert len(content) > 100
        root = ET.fromstring(content)
        assert root.tag.endswith("svg")


def test_generated_demos_exports_exist_and_valid() -> None:
    """Verifies generated 3D CAD/Blender showcase exports exist and are valid."""
    demos_dir = Path("/home/phi/PROJECTS/geometor/polyhedra/demos/exports")
    assert demos_dir.exists()

    expected_files = [
        "dodecahedron_vacuum.obj",
        "dodecahedron_vacuum.mtl",
        "icosahedron_solidum.obj",
        "icosahedron_solidum.mtl",
        "build_ingetrazo_polyhedra.py",
        "build_blender_polyhedra.py",
    ]

    for fname in expected_files:
        fpath = demos_dir / fname
        assert fpath.exists(), f"Missing required export file: {fname}"
        assert fpath.stat().st_size > 50

    # AST parse python scripts
    ingetrazo_py = (demos_dir / "build_ingetrazo_polyhedra.py").read_text(encoding="utf-8")
    assert ast.parse(ingetrazo_py) is not None

    blender_py = (demos_dir / "build_blender_polyhedra.py").read_text(encoding="utf-8")
    assert ast.parse(blender_py) is not None
