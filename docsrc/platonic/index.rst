The Five Platonic Solids
========================

*Euclidean Constructions, Golden Ratio Coordinates, and 3D Rational Trigonometry*

.. epigraph::

   *No other figure can be constructed from equilateral and equiangular plane figures, except these five solids alone.*

   — :person:`Euclid of Alexandria`, *Elements* Book XIII, Proposition 18a (Porism)

Axiomatic Foundation
--------------------

In Book XIII of the *Elements*, Euclid constructs the five regular convex polyhedra and proves that no other regular solids can exist in Euclidean 3-space:

1. **Proposition XIII.13**: Construction of the regular **Tetrahedron** inside a given sphere.
2. **Proposition XIII.14**: Construction of the regular **Octahedron** inside a given sphere.
3. **Proposition XIII.15**: Construction of the regular **Hexahedron (Cube)** inside a given sphere.
4. **Proposition XIII.16**: Construction of the regular **Icosahedron** inside a given sphere.
5. **Proposition XIII.17**: Construction of the regular **Dodecahedron** inside a given sphere.

In the GEOMETOR formulation, these solids are modeled with **zero floating-point numbers** over the rational field :math:`\mathbb{Q}` and the golden field :math:`\mathbb{Q}(\phi)`, where :math:`\phi = \frac{1 + \sqrt{5}}{2}` satisfies :math:`\phi^2 - \phi - 1 = 0`.

Exact Symbolic Metrics
----------------------

Tetrahedron :math:`\{3, 3\}`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The regular tetrahedron is modeled using four alternating vertices of the cube :math:`[-1, 1]^3`:

.. math::

   V_0 = (1, 1, 1), \quad V_1 = (1, -1, -1), \quad V_2 = (-1, 1, -1), \quad V_3 = (-1, -1, 1)

- **Schläfli Symbol**: :math:`\{3, 3\}` (4 equilateral triangles, 3 meeting at each vertex).
- **Euler Characteristic**: :math:`V - E + F = 4 - 6 + 4 = 2`.
- **Edge Quadrance**: :math:`Q_E = 8` (edge length :math:`2\sqrt{2}`).
- **Circumquadrance**: :math:`Q_{\text{out}} = 3`.
- **Inquadrance**: :math:`Q_{\text{in}} = 1/3`.
- **Midquadrance**: :math:`Q_{\text{mid}} = 1`.
- **Ratio Invariants**: :math:`Q_{\text{in}} / Q_{\text{out}} = 1/9`, :math:`Q_{\text{mid}} / Q_{\text{out}} = 1/3`.
- **Dihedral Spread**: :math:`s = 8/9` (:math:`\cos\theta = 1/3`, :math:`\sin^2\theta = 8/9`).
- **Polar Duality**: The tetrahedron is self-dual (:math:`\{3, 3\}^* = \{3, 3\}`).

Hexahedron (Cube) :math:`\{4, 3\}`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The regular hexahedron (cube) is modeled on the eight canonical corners:

.. math::

   V \in \{(\pm 1, \pm 1, \pm 1)\}

- **Schläfli Symbol**: :math:`\{4, 3\}` (6 squares, 3 meeting at each vertex).
- **Euler Characteristic**: :math:`V - E + F = 8 - 12 + 6 = 2`.
- **Edge Quadrance**: :math:`Q_E = 4` (edge length :math:`2`).
- **Circumquadrance**: :math:`Q_{\text{out}} = 3`.
- **Inquadrance**: :math:`Q_{\text{in}} = 1`.
- **Midquadrance**: :math:`Q_{\text{mid}} = 2`.
- **Ratio Invariants**: :math:`Q_{\text{in}} / Q_{\text{out}} = 1/3`, :math:`Q_{\text{mid}} / Q_{\text{out}} = 2/3`.
- **Dihedral Spread**: :math:`s = 1` (:math:`\theta = 90^\circ`, :math:`\sin^2\theta = 1`).
- **Polar Dual**: Octahedron :math:`\{3, 4\}`.

Octahedron :math:`\{3, 4\}`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The regular octahedron is modeled on the six axial unit vertices:

.. math::

   V \in \{(\pm 1, 0, 0), (0, \pm 1, 0), (0, 0, \pm 1)\}

- **Schläfli Symbol**: :math:`\{3, 4\}` (8 equilateral triangles, 4 meeting at each vertex).
- **Euler Characteristic**: :math:`V - E + F = 6 - 12 + 8 = 2`.
- **Edge Quadrance**: :math:`Q_E = 2` (edge length :math:`\sqrt{2}`).
- **Circumquadrance**: :math:`Q_{\text{out}} = 1`.
- **Inquadrance**: :math:`Q_{\text{in}} = 1/3`.
- **Midquadrance**: :math:`Q_{\text{mid}} = 1/2`.
- **Ratio Invariants**: :math:`Q_{\text{in}} / Q_{\text{out}} = 1/3`, :math:`Q_{\text{mid}} / Q_{\text{out}} = 1/2`.
- **Dihedral Spread**: :math:`s = 8/9` (:math:`\cos\theta = -1/3`, :math:`\sin^2\theta = 8/9`).
- **Polar Dual**: Hexahedron :math:`\{4, 3\}`.

Icosahedron :math:`\{3, 5\}`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The regular icosahedron is modeled on three mutually perpendicular golden rectangles of aspect ratio :math:`1 : \phi`:

.. math::

   V \in \{(0, \pm 1, \pm \phi), (\pm 1, \pm \phi, 0), (\pm \phi, 0, \pm 1)\}

- **Schläfli Symbol**: :math:`\{3, 5\}` (20 equilateral triangles, 5 meeting at each vertex).
- **Euler Characteristic**: :math:`V - E + F = 12 - 30 + 20 = 2`.
- **Edge Quadrance**: :math:`Q_E = 4` (edge length :math:`2`).
- **Circumquadrance**: :math:`Q_{\text{out}} = 1 + \phi^2 = \phi + 2`.
- **Ratio Invariants**:

  .. math::

     \frac{Q_{\text{in}}}{Q_{\text{out}}} = \frac{4\phi + 3}{15} = \frac{1}{3} + \frac{2\sqrt{5}}{15}

  .. math::

     \frac{Q_{\text{mid}}}{Q_{\text{out}}} = \frac{\phi + 2}{5} = \frac{1}{2} + \frac{\sqrt{5}}{10}

- **Dihedral Spread**: :math:`s = 4/9` (:math:`\cos\theta = -\sqrt{5}/3`, :math:`\sin^2\theta = 4/9`).
- **Polar Dual**: Dodecahedron :math:`\{5, 3\}`.

Dodecahedron :math:`\{5, 3\}`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The regular dodecahedron is modeled on twenty vertices: the eight corners of a cube :math:`(\pm 1, \pm 1, \pm 1)` plus twelve vertices on the golden planes:

.. math::

   (0, \pm \phi^{-1}, \pm \phi), \quad (\pm \phi^{-1}, \pm \phi, 0), \quad (\pm \phi, 0, \pm \phi^{-1})

where :math:`\phi^{-1} = \phi - 1`.

- **Schläfli Symbol**: :math:`\{5, 3\}` (12 regular pentagons, 3 meeting at each vertex).
- **Euler Characteristic**: :math:`V - E + F = 20 - 30 + 12 = 2`.
- **Edge Quadrance**: :math:`Q_E = 4\phi^{-2} = 4(2 - \phi) = 6 - 2\sqrt{5}`.
- **Circumquadrance**: :math:`Q_{\text{out}} = 3`.
- **Ratio Invariants**:

  .. math::

     \frac{Q_{\text{in}}}{Q_{\text{out}}} = \frac{4\phi + 3}{15} = \frac{1}{3} + \frac{2\sqrt{5}}{15}

  .. math::

     \frac{Q_{\text{mid}}}{Q_{\text{out}}} = \frac{\phi + 1}{3} = \frac{1}{2} + \frac{\sqrt{5}}{6}

- **Dihedral Spread**: :math:`s = 4/5` (:math:`\cos\theta = -1/\sqrt{5}`, :math:`\sin^2\theta = 4/5`).
- **Polar Dual**: Icosahedron :math:`\{3, 5\}`.

Rational Trigonometry Invariants
--------------------------------

In Norman Wildberger's Rational Trigonometry, angles between faces are measured not in transcendental radians or degrees, but via the **spread** :math:`s = \sin^2\theta`:

.. math::

   s(n_1, n_2) = 1 - \frac{(n_1 \cdot n_2)^2}{Q(n_1) Q(n_2)}

For all five Platonic solids, the dihedral spread is an exact rational number in :math:`\mathbb{Q}`:

.. math::

   s(\text{Tetrahedron}) = \frac{8}{9}, \quad s(\text{Cube}) = 1, \quad s(\text{Octahedron}) = \frac{8}{9}

.. math::

   s(\text{Dodecahedron}) = \frac{4}{5}, \quad s(\text{Icosahedron}) = \frac{4}{9}
