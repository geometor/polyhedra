:layout: book
:type: plate
:order: 14
:title: Tabulae XXVII–XXVIII: Dodecahedron Planum Solidum et Vacuum (1509)
:featured_image: leonardo/plates/0243.g1.png
:featured_image_alt: Leonardo da Vinci Tabula XXVII Folio 0243 - Dodecahedron Planum Solidum
:categories: leonardo-1509, platonic
:tags: pacioli, woodcut, solidum, vacuum, dodecahedron, platonic-solids, golden-ratio
:excerpt: Leonardo da Vinci's woodcut studies of the regular dodecahedron, representing the Cosmos or Quintessence in Platonic and Renaissance cosmology, depicted with solid pentagonal facets and as an open wooden cage of genus g = 11.

===================================================================
Tabulae XXVII–XXVIII: Dodecahedron Planum Solidum et Vacuum (1509)
===================================================================

*The Regular Dodecahedron in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Dodecahedron planum solidum est corpus duodecim basibus pentagonalibus aequilateris et aequiangulis contentum...*

   *The solid plane dodecahedron is a body contained by twelve equilateral and equiangular pentagonal bases...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. XXXIX (Venice, 1509)

.. enunciation::

   The regular dodecahedron :math:`\{5, 3\}` possesses 20 vertices, 30 edges, and 12 regular pentagonal faces governed by the divine proportion :math:`\phi`. Leonardo da Vinci illustrates this celestial solid in **Tabula XXVII (Folio 0243)** as *Dodecahedron Planum Solidum* and in **Tabula XXVIII (Folio 0245)** as *Dodecahedron Planum Vacuum*. In hollow form, the twelve open pentagonal windows form a wooden carpentry cage of topological genus :math:`g = F - 1 = 11`.

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0243.g1.png
          :align: center
          :alt: Tabula XXVII (Folio 0243) - Dodecahedron Planum Solidum

          **Tabula XXVII (Folio 0243)**: *Dodecahedron Planum Solidum*.
     - .. figure:: plates/0245.g1.png
          :align: center
          :alt: Tabula XXVIII (Folio 0245) - Dodecahedron Planum Vacuum

          **Tabula XXVIII (Folio 0245)**: *Dodecahedron Planum Vacuum* (:math:`g = 11`).

Cosmology of the Quintessence & The Divine Proportion
-----------------------------------------------------

In Plato's *Timaeus* (55c), the dodecahedron is reserved for the entire cosmos: *"There remained a fifth construction, which God used for embroidering the constellations on the whole heaven."*

Pacioli identifies the dodecahedron with the **Aether** or **Quintessence** (*Quinta Essentia*), because the golden ratio governs its pentagonal face diagonals in accordance with Euclid XIII.17. In exact coordinates over :math:`\mathbb{Q}(\phi)`, its 20 vertices comprise the 8 corners of the cube :math:`(\pm 1, \pm 1, \pm 1)` plus 12 golden roof vertices:

.. math::

   (0, \pm \phi^{-1}, \pm \phi), \quad (\pm \phi^{-1}, \pm \phi, 0), \quad (\pm \phi, 0, \pm \phi^{-1})

In Tabula XXVII, Leonardo depicts the solid dodecahedron tilted so that the pentagonal symmetry is immediately discernible.

In Tabula XXVIII, the hollow carpentry framework features 12 pentagonal window apertures framed by 30 mitered wooden beams. Looking through the top pentagon reveals the floor and rear walls of the inner chamber with breathtaking perspective accuracy.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow dodecahedron framework satisfies:

- **Base Solid Invariants**: :math:`V = 20`, :math:`E = 30`, :math:`F = 12` regular pentagonal faces
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(20) + 4(30) = 160`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(30) = 360`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(30) = 180` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 160 - 360 + 180 = -20`
- **Topological Genus**: :math:`g = F - 1 = 12 - 1 = 11`
- **Coordinate Field**: Quadratic extension field :math:`\mathbb{Q}(\phi)`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}(\phi)`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Regular Dodecahedron </solids/01-platonic/dodecahedron/index>`
