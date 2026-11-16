GEOMETOR • polyhedra
====================

**Visit the Online Archive:** https://geometor.github.io/polyhedra/

**Polyhedra • Platonic, Archimedean, Keplerian Solids & Leonardo Plates • semantic digital archive**

Mission
-------

``geometor/polyhedra`` is part of the interconnected `GEOMETOR <https://geometor.com>`_ semantic digital archive. It models three-dimensional constructive geometry, regular and semi-regular polyhedra, and spatial proportion in 100% exact symbolic algebra over :math:`\mathbb{Z}`, :math:`\mathbb{Q}(\phi)`, and radical field extensions. Grounded in Euclid's *Elements* Book XIII, Plato's *Timaeus*, Luca Pacioli and Leonardo da Vinci's *De Divina Proportione* (1509), and Johannes Kepler's *Harmonices Mundi* (1619), the repository liberates 26 canonical solids into addressable semantic monographs featuring interactive 3D HTML5 viewports, theme-adaptive vector diagrams, and exact dihedral spread calculations across the GEOMETOR corpus.

Catalogs in This Archive
------------------------

- **`Catalog of Polyhedra <https://geometor.github.io/polyhedra/solids/>`_** — Twenty-six exact symbolic solids across five geometric families (Platonic, Archimedean, Catalan, Elevated, and Pyramids) with interactive 3D viewports and comparative metrics.
- **`Leonardo da Vinci's Polyhedral Plates (1509) <https://geometor.github.io/polyhedra/leonardo/>`_** — Twenty paired woodcut folio studies from Luca Pacioli's *De Divina Proportione* paired with exact genus :math:`g = F - 1` *Corpora Vacua* proofs.
- **`Golden Proportions in Polyhedra <https://geometor.github.io/polyhedra/golden/>`_** — Certified golden ratio (:math:`\phi`) theorems across 3D solids and 2D cross-sections.
- **`Kepler, Squaring the Circle & the Great Pyramid <https://geometor.github.io/polyhedra/pyramid/>`_** — Exact symbolic investigations of the 1597 Kepler right triangle, circle quadrature, and 14:11 Seked geometry.
- **`3D Symbolic Infrastructure & Multi-Engine Pipeline <https://geometor.github.io/polyhedra/pipeline/>`_** — Exact 3D modeling kernel, Conway/Pacioli operators, and multi-target export architecture to SVG, OBJ, IngeTrazo, and Blender.

The Five Platonic Solids
------------------------

All five regular solids :math:`\{p, q\}` are modeled symbolically over :math:`\mathbb{Z}` and :math:`\mathbb{Q}(\phi)` with pure rational dihedral spreads:

.. list-table::
   :header-rows: 1
   :widths: 16 10 8 8 8 10 12 14 14

   * - Solid
     - Element
     - :math:`\{p, q\}`
     - :math:`V`
     - :math:`E`
     - :math:`F`
     - Euclid
     - Spread
     - :math:`Q_{\text{in}} / Q_{\text{out}}`
   * - **Tetrahedron**
     - Fire
     - :math:`\{3, 3\}`
     - 4
     - 6
     - 4
     - XIII.13
     - :math:`8/9`
     - :math:`1/9`
   * - **Hexahedron**
     - Earth
     - :math:`\{4, 3\}`
     - 8
     - 12
     - 6
     - XIII.15
     - :math:`1`
     - :math:`1/3`
   * - **Octahedron**
     - Air
     - :math:`\{3, 4\}`
     - 6
     - 12
     - 8
     - XIII.14
     - :math:`8/9`
     - :math:`1/3`
   * - **Icosahedron**
     - Water
     - :math:`\{3, 5\}`
     - 12
     - 30
     - 20
     - XIII.16
     - :math:`4/9`
     - :math:`(4\phi+3)/15`
   * - **Dodecahedron**
     - Aether
     - :math:`\{5, 3\}`
     - 20
     - 30
     - 12
     - XIII.17
     - :math:`4/5`
     - :math:`(4\phi+3)/15`

Repository Contents
-------------------

- ``docsrc/`` — RST catalog tracks, monographs, and 3D studios compiled by `PHOTON publish <https://github.com/photon-platform/publish>`_.
- ``src/geometor/polyhedra/`` — Exact 3D modeling kernel, Conway/Pacioli operators, catalog definitions, and renderers.

Local Build & Verification
--------------------------

.. code-block:: bash

   publish build
   uv run --no-sync pytest

Part of the GEOMETOR Knowledge Archive
--------------------------------------

Explore all **74 Book Codices** and **11 Mathematical Catalogs** at https://geometor.com/books/.
