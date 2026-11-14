"""Command-line interface for geometor.polyhedra.

Provides rich terminal tables displaying the five Platonic solids, their
exact symbolic invariants, and Leonardo da Vinci's Pacioli woodcut plates.
"""

from __future__ import annotations

import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from geometor.polyhedra.platonic import (
    RegularSolid,
    get_platonic_solids,
)


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
    solids = get_platonic_solids()

    if not argv:
        _render_solids_table(console, solids)
        return 0

    slug = argv[0].lower().strip()
    if slug in solids:
        _render_solid_detail(console, solids[slug])
        return 0

    console.print(
        f"[red]Error: Unknown Platonic solid '{slug}'.[/red]\n"
        f"Available solids: {', '.join(solids.keys())}"
    )
    return 1
