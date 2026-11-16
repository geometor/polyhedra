:layout: book
:type: plate
:order: 1
:title: Tabulae I–II: Tetrahedron Planum Solidum et Vacuum (1509)
:featured_image: leonardo/plates/0187.g1.png
:featured_image_alt: Leonardo da Vinci Tabula I Folio 0187 - Tetrahedron Planum Solidum
:categories: leonardo-1509, platonic
:tags: pacioli, woodcut, solidum, vacuum, tetrahedron, platonic-solids
:excerpt: Leonardo da Vinci's opening woodcut studies for Luca Pacioli's De Divina Proportione (1509), depicting the regular tetrahedron as both an opaque solid body and an open mitered wooden framework of genus g = 3.

=========================================================
Tabulae I–II: Tetrahedron Planum Solidum et Vacuum (1509)
=========================================================

*The Regular Tetrahedron in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Tetrahedron planum solidum est corpus quatuor basibus triangularibus aequilateris contentum... vacuum vero est quando bases aperiuntur lignea trabecula circumdata.*

   *The solid plane tetrahedron is a body contained by four equilateral triangular bases... but the vacuum is when the bases are opened, surrounded by wooden beams.*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. XXVI (Venice, 1509)

.. enunciation::

   To illustrate Luca Pacioli's *De Divina Proportione* (1509), Leonardo da Vinci constructed the regular tetrahedron :math:`\{3, 3\}` in two foundational aspects: **Tabula I (Folio 0187)** as an opaque solid body with directional shading (*Planum Solidum*), and **Tabula II (Folio 0189)** as an open mitered wooden lattice (*Planum Vacuum*). Through the Vacuate Manifold Theorem, hollowing the four triangular faces produces a closed orientable 2-manifold of topological genus :math:`g = F - 1 = 3`.

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0187.g1.png
          :align: center
          :alt: Tabula I (Folio 0187) - Tetrahedron Planum Solidum

          **Tabula I (Folio 0187)**: *Tetrahedron Planum Solidum* (Τετράεδρον ἐπίπεδον στερεόν).
     - .. figure:: plates/0189.g1.png
          :align: center
          :alt: Tabula II (Folio 0189) - Tetrahedron Planum Vacuum

          **Tabula II (Folio 0189)**: *Tetrahedron Planum Vacuum* (Τετράεδρον ἐπίπεδον κενόν).

Historical & Iconographic Analysis
----------------------------------

In the Platonic cosmology of the *Timaeus* (54d–55a), the regular tetrahedron is assigned to **Fire** (*Ignis*) because of its penetrating sharpness, minimal number of bounding facets, and agile mobility.

Leonardo's rendering of Tabula I establishes the lighting conventions utilized across all sixty woodcuts: an illumination source located above and to the left of the spectator, casting crisp diagonal hatchings across the rightmost facets.

In Tabula II, Leonardo strips away the opaque faces to construct the hollow wooden lattice framework (*Corpus Vacuum*). These hollow models were crafted in boxwood and hung from the ceiling of Duke Ludovico Sforza's banquet hall in Milan.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow lattice framework replaces each triangular face with an open window reveal framed by mitered boundary beams:

- **Base Solid Invariants**: :math:`V = 4`, :math:`E = 6`, :math:`F = 4`
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(4) + 4(6) = 32`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(6) = 72`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(6) = 36` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 32 - 72 + 36 = -4`
- **Topological Genus**: :math:`g = F - 1 = 4 - 1 = 3`
- **Coordinate Field**: Pure rational field :math:`\mathbb{Q}`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Regular Tetrahedron </solids/01-platonic/tetrahedron/index>`
