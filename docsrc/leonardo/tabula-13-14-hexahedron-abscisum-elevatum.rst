:layout: book
:type: plate
:order: 7
:title: Tabulae XIII–XIIII: Exahedron Abscisum Elevatum Solidum et Vacuum (1509)
:featured_image: leonardo/plates/0211.g1.png
:featured_image_alt: Leonardo da Vinci Tabula XIII Folio 0211 - Exahedron Abscisum Elevatum Solidum
:categories: leonardo-1509, elevated
:tags: pacioli, woodcut, solidum, vacuum, cuboctahedron-elevatum, elevated-solids
:excerpt: Leonardo da Vinci's compound stellation of the cuboctahedron (Exahedron Abscisum Elevatum), erecting pyramids on all 14 rectified facets to generate 48 triangular faces and an open wooden lattice of genus g = 47.

=========================================================================
Tabulae XIII–XIIII: Exahedron Abscisum Elevatum Solidum et Vacuum (1509)
=========================================================================

*The Compound Elevated Cuboctahedron in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Exahedron abscisum elevatum solidum est corpus habens super qualibet base abscisi cubi pyramidem erectam...*

   *The solid elevated truncated hexahedron is a body having erected upon each base of the truncated cube a pyramid...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. XXXII (Venice, 1509)

.. enunciation::

   By erecting regular pyramids over both the 8 triangular and 6 square facets of the cuboctahedron, Leonardo da Vinci constructs the compound stellated solid **Exahedron Abscisum Elevatum** (*Cuboctahedron Elevatum*), consisting of :math:`8 \times 3 + 6 \times 4 = 48` triangular facets and 26 vertices. In Luca Pacioli's *De Divina Proportione* (1509), this body is illustrated in **Tabula XIII (Folio 0211)** as *Exahedron Abscisum Elevatum Solidum* and in **Tabula XIIII (Folio 0217)** as *Exahedron Abscisum Elevatum Vacuum* (genus :math:`g = 47`).

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0211.g1.png
          :align: center
          :alt: Tabula XIII (Folio 0211) - Exahedron Abscisum Elevatum Solidum

          **Tabula XIII (Folio 0211)**: *Exahedron Abscisum Elevatum Solidum*.
     - .. figure:: plates/0217.g1.png
          :align: center
          :alt: Tabula XIIII (Folio 0217) - Exahedron Abscisum Elevatum Vacuum

          **Tabula XIIII (Folio 0217)**: *Exahedron Abscisum Elevatum Vacuum*.

Scholarly Note on Paganini's 1509 Folio Numbering
-------------------------------------------------

In Paganini's 1509 Venetian print edition, folios **0213** and **0215** were allocated to full-page Vitruvian architectural column plates (*Colonna Corinta, Jonica e Pulvinata con Stilobata e Steriobata*). Consequently, the hollow counterpart **Tabula XIIII** was placed on **Folio 0217**, immediately following the architectural treatise plates.

Compound Stellation & Multi-Pyramidal Architecture
--------------------------------------------------

This compound solid illustrates the recursive power of Renaissance constructive operations: starting from the cube, edge-midpoint truncation generates the 14-faced cuboctahedron, upon which 14 distinct pyramids (8 triangular pyramids and 6 square pyramids) are erected.

In Tabula XIII, the multi-faceted star body sparkles with alternating illuminated and shaded planes.

In Tabula XIIII, the hollow carpentry cage becomes a triumph of wooden craftsmanship: 48 triangular window openings reveal the intricate interior cage, yielding a manifold of topological genus :math:`g = 47`.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow elevated cuboctahedron satisfies:

- **Base Solid Invariants**: :math:`V = 12 + 8 + 6 = 26`, :math:`E = 24 + 24 + 24 = 72`, :math:`F = 24 + 24 = 48` triangular facets
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(26) + 4(72) = 340`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(72) = 864`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(72) = 432` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 340 - 864 + 432 = -92`
- **Topological Genus**: :math:`g = F - 1 = 48 - 1 = 47`
- **Coordinate Field**: Pure rational field :math:`\mathbb{Q}`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Cuboctahedron Elevatum </solids/04-elevated/cuboctahedron-elevatum/index>`
