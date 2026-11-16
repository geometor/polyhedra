:layout: book
:type: plate
:order: 10
:title: Tabulae XIX–XX: Octahedron Elevatum — Stella Octangula (1509)
:featured_image: leonardo/plates/0227.g1.png
:featured_image_alt: Leonardo da Vinci Tabula XIX Folio 0227 - Octahedron Elevatum Solidum
:categories: leonardo-1509, elevated
:tags: pacioli, woodcut, solidum, vacuum, stella-octangula, octahedron-elevatum, elevated-solids
:excerpt: Leonardo da Vinci's 1509 woodcuts of the Stella Octangula (Octahedron Elevatum), depicting the compound of two dual tetrahedra with rigorous perspective depth 110 years prior to Johannes Kepler's 1619 treatise.

=====================================================================
Tabulae XIX–XX: Octahedron Elevatum — Stella Octangula (1509)
=====================================================================

*The Compound of Two Dual Tetrahedra in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Octahedron elevatum solidum est quando super qualibet octo basium octahedri erigitur una pyramis triangularis...*

   *The solid elevated octahedron is when upon each of the eight bases of the octahedron a triangular pyramid is erected...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. XXXV (Venice, 1509)

.. enunciation::

   By erecting regular triangular pyramids over each of the 8 triangular faces of an octahedron, Leonardo da Vinci constructs the celebrated **Stella Octangula** (*Octahedron Elevatum*), consisting of :math:`8 \times 3 = 24` equilateral triangular faces and :math:`6 + 8 = 14` vertices. In Luca Pacioli's *De Divina Proportione* (1509), this masterpiece of geometric art is illustrated in **Tabula XIX (Folio 0227)** as *Octahedron Elevatum Solidum* and in **Tabula XX (Folio 0229)** as *Octahedron Elevatum Vacuum* (genus :math:`g = 23`).

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0227.g1.png
          :align: center
          :alt: Tabula XIX (Folio 0227) - Octahedron Elevatum Solidum

          **Tabula XIX (Folio 0227)**: *Octahedron Elevatum Solidum* (*Stella Octangula*).
     - .. figure:: plates/0229.g1.png
          :align: center
          :alt: Tabula XX (Folio 0229) - Octahedron Elevatum Vacuum

          **Tabula XX (Folio 0229)**: *Octahedron Elevatum Vacuum*.

Historical Discovery: Leonardo Before Kepler
--------------------------------------------

In astronomical and mathematical history, credit for discovering the **Stella Octangula** (the compound of two interpenetrating regular tetrahedra) is almost universally accorded to **Johannes Kepler**, who coined the term in *Harmonices Mundi* (Linz, 1619, Book II).

However, **Leonardo da Vinci drew both the solid and hollow Stella Octangula with rigorous perspective and chiaroscuro modeling in 1497**, published in Pacioli's *De Divina Proportione* in **1509**—more than **110 years before Kepler**!

Geometric Structure of the Stella Octangula
-------------------------------------------

When equilateral pyramids are erected over the 8 triangular faces of an octahedron, the apex of each pyramid forms an equilateral tetrahedron sharing an octahedral face. In exact integer coordinates, the 8 pyramid apices are precisely the 8 corners of a cube :math:`(\pm 1, \pm 1, \pm 1)`.

The 8 triangular pyramids combine in groups of four to form **two interpenetrating regular tetrahedra**:

.. math::

   T_1: (1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)

.. math::

   T_2: (-1, -1, -1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)

- **Apex Vertices**: 8 (corners of cube)
- **Octahedral Core Vertices**: 6 (centers of cube faces)
- **Total Vertices**: :math:`V = 8 + 6 = 14`
- **Edges**: :math:`E = 36`
- **Faces**: :math:`F = 24` equilateral triangular facets
- **Shared Intersection Core**: An exact regular octahedron

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow elevated octahedron framework satisfies:

- **Base Solid Invariants**: :math:`V = 14`, :math:`E = 36`, :math:`F = 24` triangular faces
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(14) + 4(36) = 172`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(36) = 432`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(36) = 216` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 172 - 432 + 216 = -44`
- **Topological Genus**: :math:`g = F - 1 = 24 - 1 = 23`
- **Coordinate Field**: Pure integer lattice :math:`\mathbb{Z}` / rational field :math:`\mathbb{Q}`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Stella Octangula </solids/04-elevated/stella-octangula/index>`
