"""Command-line interface for geometor.polyhedra.

Provides rich terminal tables displaying the 26 canonical polyhedra across five
thematic families, exact symbolic Rational Trigonometry invariants, and Leonardo
da Vinci's Pacioli woodcut plates.
"""

from __future__ import annotations

import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from geometor.polyhedra.catalog import (
    PolyhedronEntry,
    PolyhedronFamily,
    get_polyhedra_catalog,
    get_polyhedra_families,
    get_polyhedron_entry,
)
from geometor.polyhedra.platonic import (
    RegularSolid,
    get_platonic_solids,
)


def _format_field(field_latex: str) -> str:
    r"""Formats LaTeX field expression for clean terminal display.

    Args:
        field_latex: Raw LaTeX number field string (e.g. r"\\mathbb{Q}(\\phi)").

    Returns:
        Clean Unicode string for terminal output (e.g. "ℚ(ϕ)").
    """
    return (
        field_latex.replace(r"\mathbb{Z}", "ℤ")
        .replace(r"\mathbb{Q}", "ℚ")
        .replace(r"\phi", "ϕ")
        .replace(r"\sqrt", "√")
        .replace("{", "")
        .replace("}", "")
    )


def _render_catalog_table(
    console: Console,
    catalog: dict[str, PolyhedronEntry],
    families: dict[str, PolyhedronFamily],
) -> None:
    """Renders a comprehensive Rich table of all 26 cataloged polyhedra by family.

    Args:
        console: Rich Console instance for terminal output.
        catalog: Dictionary mapping slugs to PolyhedronEntry instances.
        families: Dictionary mapping family slugs to PolyhedronFamily instances.
    """
    table = Table(
        title="[bold gold1]GEOMETOR • Canonical Polyhedra Catalog[/bold gold1]",
        caption="26 Exact Symbolic 3D Manifolds · 5 Families · Euclid · Pacioli (1509) · Kepler (1619)",
        header_style="bold cyan",
        show_lines=False,
    )

    table.add_column("ID", style="bold cyan", justify="center", no_wrap=True)
    table.add_column("Solid", style="bold")
    table.add_column("Latin Name", style="italic")
    table.add_column("Field", justify="center")
    table.add_column("V", justify="right")
    table.add_column("E", justify="right")
    table.add_column("F", justify="right")
    table.add_column("Genus", justify="right", style="magenta")
    table.add_column("Spread", justify="center", style="yellow")
    table.add_column("Dual", style="green")

    for fam_slug, fam in families.items():
        table.add_section()
        table.add_row(
            f"[bold gold1]{fam.order}[/bold gold1]",
            f"[bold gold1]{fam.title.upper()}[/bold gold1]",
            f"[dim]{fam.subtitle}[/dim]",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        )
        fam_entries = [e for e in catalog.values() if e.family == fam_slug]
        for e in fam_entries:
            dual_str = e.dual_slug if e.dual_slug else "—"
            spread_str = (
                str(e.primary_dihedral_spread)
                if e.primary_dihedral_spread is not None
                else "—"
            )
            table.add_row(
                e.canonical_id,
                e.title,
                e.latin_name,
                _format_field(e.number_field),
                str(e.vertices_count),
                str(e.edges_count),
                str(e.faces_count),
                str(e.vacuum_genus),
                spread_str,
                dual_str,
            )

    console.print(table)


def _render_entry_detail(console: Console, entry: PolyhedronEntry) -> None:
    """Renders a detailed Rich view of a single cataloged polyhedron.

    Args:
        console: Rich Console instance for terminal output.
        entry: PolyhedronEntry instance to display.
    """
    convex_str = "Convex" if entry.is_convex else "Non-Convex (Stellated)"
    dual_str = entry.dual_slug if entry.dual_slug else "None"
    spread_str = (
        str(entry.primary_dihedral_spread)
        if entry.primary_dihedral_spread is not None
        else "N/A"
    )

    console.print(
        Panel(
            f"[bold cyan]ID:[/bold cyan] {entry.canonical_id}    "
            f"[bold cyan]Family:[/bold cyan] {entry.family}    "
            f"[bold cyan]Type:[/bold cyan] {convex_str}\n"
            f"[bold cyan]Latin:[/bold cyan] {entry.latin_name}\n"
            f"[bold cyan]Enunciation:[/bold cyan] {entry.enunciation}\n\n"
            f"[bold cyan]Field:[/bold cyan] {_format_field(entry.number_field)}    "
            f"[bold cyan]Symmetry:[/bold cyan] {entry.symmetry_group}    "
            f"[bold cyan]Dual:[/bold cyan] {dual_str}\n"
            f"[bold cyan]Topology:[/bold cyan] V={entry.vertices_count}, "
            f"E={entry.edges_count}, F={entry.faces_count} "
            f"(Euler χ={entry.vertices_count - entry.edges_count + entry.faces_count})\n"
            f"[bold cyan]Faces:[/bold cyan] {entry.face_summary}\n"
            f"[bold cyan]Hollow Vacuum Genus:[/bold cyan] g={entry.vacuum_genus}    "
            f"[bold cyan]Dihedral Spread:[/bold cyan] {spread_str}\n"
            f"[bold cyan]Edge Quadrances:[/bold cyan] {entry.edge_quadrances}\n"
            f"[bold cyan]Vertex Quadrances:[/bold cyan] {entry.vertex_quadrances}\n\n"
            f"[bold cyan]Source:[/bold cyan] {entry.historical_source}",
            title=f"[bold gold1]{entry.canonical_id} • {entry.title}[/bold gold1]",
            border_style="gold1",
        )
    )

    if entry.leonardo_plates:
        plates_table = Table(
            title=f"Leonardo da Vinci Plates (Pacioli 1509) — {entry.title}",
            header_style="bold magenta",
            show_lines=False,
        )
        plates_table.add_column("Plate", justify="center", style="cyan")
        plates_table.add_column("Folio", justify="center", style="yellow")
        plates_table.add_column("Caption", style="italic")

        for plate, folio, caption in entry.leonardo_plates:
            plates_table.add_row(plate, folio, caption)

        console.print(plates_table)


def _render_solids_table(console: Console, solids: dict[str, RegularSolid]) -> None:
    """Renders a Rich overview table of all five Platonic solids.

    Args:
        console: Rich Console instance for terminal output.
        solids: Dictionary of slug to RegularSolid instances.
    """
    table = Table(
        title="[bold gold1]GEOMETOR • The Five Platonic Solids[/bold gold1]",
        caption="Exact symbolic metrics over ℤ and ℚ(ϕ) · Euclid Elements XIII · Pacioli 1509",
        header_style="bold cyan",
        show_lines=True,
    )

    table.add_column("Solid", style="bold")
    table.add_column("Greek / Latin", style="italic")
    table.add_column("Element", style="green")
    table.add_column("{p, q}", justify="center", style="magenta")
    table.add_column("V", justify="right")
    table.add_column("E", justify="right")
    table.add_column("F", justify="right")
    table.add_column("Euclid", justify="center")
    table.add_column("Spread", justify="center", style="yellow")
    table.add_column("Q_in / Q_out", justify="center")
    table.add_column("Q_mid / Q_out", justify="center")

    for solid in solids.values():
        table.add_row(
            solid.name,
            f"{solid.greek_name}\n{solid.latin_name}",
            solid.element,
            f"{{{solid.schlafli[0]}, {solid.schlafli[1]}}}",
            str(len(solid.vertices)),
            str(len(solid.edges)),
            str(len(solid.faces)),
            f"{solid.euclid_prop}\n({solid.g_index})",
            str(solid.dihedral_spread),
            str(solid.q_in_over_q_out),
            str(solid.q_mid_over_q_out),
        )

    console.print(table)


def _render_solid_detail(console: Console, solid: RegularSolid) -> None:
    """Renders a detailed Rich view of a single Platonic solid.

    Args:
        console: Rich Console instance for terminal output.
        solid: RegularSolid instance to display.
    """
    title = f"{solid.name} {{{solid.schlafli[0]}, {solid.schlafli[1]}}} — {solid.element}"
    console.print(
        Panel(
            f"[bold cyan]Greek:[/bold cyan] {solid.greek_name}    "
            f"[bold cyan]Latin:[/bold cyan] {solid.latin_name}\n"
            f"[bold cyan]Euclid:[/bold cyan] {solid.euclid_prop} ({solid.g_index})    "
            f"[bold cyan]Dual:[/bold cyan] {solid.dual_slug}\n"
            f"[bold cyan]Dihedral Spread:[/bold cyan] {solid.dihedral_spread}    "
            f"[bold cyan]Q_in / Q_out:[/bold cyan] {solid.q_in_over_q_out}    "
            f"[bold cyan]Q_mid / Q_out:[/bold cyan] {solid.q_mid_over_q_out}",
            title=f"[bold gold1]{title}[/bold gold1]",
            border_style="gold1",
        )
    )

    plates_table = Table(
        title=f"Leonardo da Vinci Plates (Pacioli 1509) — {solid.name}",
        header_style="bold magenta",
        show_lines=False,
    )
    plates_table.add_column("Variant", style="bold")
    plates_table.add_column("Plate", justify="center", style="cyan")
    plates_table.add_column("Folio", justify="center", style="yellow")

    for variant, (plate, folio) in solid.leonardo_plates.items():
        plates_table.add_row(variant, plate, folio)

    console.print(plates_table)


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point for the polyhedra command.

    Args:
        argv: Optional list of command-line arguments.

    Returns:
        Exit code (0 on success, non-zero on error).
    """
    if argv is None:
        argv = sys.argv[1:]

    console = Console()
    catalog = get_polyhedra_catalog()
    families = get_polyhedra_families()
    platonic_solids = get_platonic_solids()

    if not argv:
        _render_catalog_table(console, catalog, families)
        return 0

    arg = argv[0].lower().strip()

    if arg in ("--platonic", "-p"):
        _render_solids_table(console, platonic_solids)
        return 0

    if arg in catalog:
        _render_entry_detail(console, get_polyhedron_entry(arg))
        if arg in platonic_solids:
            _render_solid_detail(console, platonic_solids[arg])
        return 0

    console.print(
        f"[red]Error: Unknown polyhedron slug '{arg}'.[/red]\n"
        f"Available solids: {', '.join(catalog.keys())}"
    )
    return 1
