/* =========================================================================
   GEOMETOR • polyhedra — Interactive 3D Studio Engine
   Exact symbolic geometry, 3-point studio lighting, wireframe, opacity & vertex nodes
   Auto-mounts onto every <div class="polyhedra-3d-mount" ...>
   ========================================================================= */

(function () {
  'use strict';

  // --- Mathematical Constants ---
  const PHI = (1 + Math.sqrt(5)) / 2;       // ~1.618033988749895
  const INV_PHI = PHI - 1;                 // ~0.618033988749895 (1 / PHI)
  const PHI_SQ = PHI + 1;                  // ~2.618033988749895 (PHI^2)

  // --- Luminous Studio & Mineral Palettes ---
  const PAL = {
    // Theme backgrounds & surfaces
    bgDark: '#0d1117',
    panelDark: '#161b22',
    borderDark: '#30363d',
    textDark: '#e6edf3',
    subtextDark: '#8b949e',

    bgLight: '#f6f8fa',
    panelLight: '#ffffff',
    borderLight: '#d0d7de',
    textLight: '#1f2328',
    subtextLight: '#656d76',

    // Studio Beveled Frame Materials (Outer, Reveal Jamb, Inner Cavity)
    frameOuter: [238, 214, 168],   // Warm brushed champagne-gold outer frame
    frameReveal: [164, 184, 212],  // Crisp cool titanium-slate window reveal
    frameInner: [118, 138, 168],   // Sculpted architectural slate inner cavity

    // Luminous Elemental & Mineral Base Tones
    fire: [248, 113, 113],         // Tetrahedron (Coral / Ruby)
    earth: [251, 191, 36],         // Hexahedron (Radiant Gold)
    air: [56, 189, 248],           // Octahedron (Cerulean Sky)
    water: [96, 165, 250],         // Icosahedron (Sapphire)
    aether: [192, 132, 252],       // Dodecahedron (Amethyst)

    // Golden Ratio accents
    gold: '#f59e0b',
    goldGlow: 'rgba(245, 158, 11, 0.35)',
    goldFill: 'rgba(245, 158, 11, 0.18)',

    // Five Cubes Jewel Palette (Euclid XIII.17)
    cubeColors: [
      { name: 'Cube 1', hex: '#fbbf24', rgb: [251, 191, 36] }, // Gold
      { name: 'Cube 2', hex: '#34d399', rgb: [52, 211, 153] }, // Emerald
      { name: 'Cube 3', hex: '#22d3ee', rgb: [34, 211, 238] }, // Cyan
      { name: 'Cube 4', hex: '#a78bfa', rgb: [167, 139, 250] }, // Violet
      { name: 'Cube 5', hex: '#fb7185', rgb: [251, 113, 133] }  // Rose
    ]
  };

  // --- Vector Math Utilities ---
  function vAdd(a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; }
  function vSub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
  function vScale(a, s) { return [a[0] * s, a[1] * s, a[2] * s]; }
  function vDot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function vCross(a, b) {
    return [
      a[1] * b[2] - a[2] * b[1],
      a[2] * b[0] - a[0] * b[2],
      a[0] * b[1] - a[1] * b[0]
    ];
  }
  function vMag(a) { return Math.hypot(a[0], a[1], a[2]); }
  function vNorm(a) {
    const m = vMag(a);
    return m > 1e-9 ? [a[0] / m, a[1] / m, a[2] / m] : [0, 0, 0];
  }
  function vLerp(a, b, t) {
    return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
  }

  // Extract unique undirected edges from faces
  function getEdgesFromFaces(faces) {
    const edgeMap = new Map();
    const edges = [];
    faces.forEach((f, fIdx) => {
      const len = f.length;
      for (let i = 0; i < len; i++) {
        const a = f[i];
        const b = f[(i + 1) % len];
        const key = a < b ? `${a}_${b}` : `${b}_${a}`;
        if (!edgeMap.has(key)) {
          edgeMap.set(key, edges.length);
          edges.push({ a, b, faces: [fIdx] });
        } else {
          edges[edgeMap.get(key)].faces.push(fIdx);
        }
      }
    });
    return { edges, edgeMap };
  }

  // Auto-Scale Normalization: normalizes bounding radius cleanly to visual target (~1.80)
  function normalizeSolid(solid, targetRadius = 1.80) {
    let maxR = 0;
    solid.vertices.forEach(v => {
      const r = vMag(v);
      if (r > maxR) maxR = r;
    });
    if (maxR > 1e-6) {
      const scale = targetRadius / maxR;
      solid.vertices = solid.vertices.map(v => vScale(v, scale));
      if (solid.parentSolid) {
        solid.parentSolid.vertices = solid.parentSolid.vertices.map(v => vScale(v, scale));
      }
    }
    return solid;
  }

  // --- Platonic Solid Base Generators ---
  function getTetrahedron() {
    const s = 1.25;
    const vertices = [
      [ s,  s,  s],
      [ s, -s, -s],
      [-s,  s, -s],
      [-s, -s,  s]
    ];
    const faces = [
      [0, 1, 2],
      [0, 2, 3],
      [0, 3, 1],
      [1, 3, 2]
    ];
    return { name: 'tetrahedron', title: 'Tetrahedron', element: 'Fire', vertices, faces, color: PAL.fire };
  }

  function getHexahedron() {
    const s = 1.0;
    const vertices = [
      [ s,  s,  s], [ s, -s,  s], [-s, -s,  s], [-s,  s,  s],
      [ s,  s, -s], [ s, -s, -s], [-s, -s, -s], [-s,  s, -s]
    ];
    const faces = [
      [0, 3, 2, 1], // +Z front
      [4, 5, 6, 7], // -Z back
      [0, 4, 7, 3], // +Y top
      [1, 2, 6, 5], // -Y bottom
      [0, 1, 5, 4], // +X right
      [2, 3, 7, 6]  // -X left
    ];
    return { name: 'hexahedron', title: 'Hexahedron (Cube)', element: 'Earth', vertices, faces, color: PAL.earth };
  }

  function getOctahedron() {
    const s = 1.45;
    const vertices = [
      [ s,  0,  0], [-s,  0,  0],
      [ 0,  s,  0], [ 0, -s,  0],
      [ 0,  0,  s], [ 0,  0, -s]
    ];
    const faces = [
      [0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2],
      [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]
    ];
    return { name: 'octahedron', title: 'Octahedron', element: 'Air', vertices, faces, color: PAL.air };
  }

  function getIcosahedron() {
    const s = 0.88;
    const raw = [
      [0, 1, PHI], [0, -1, PHI], [0, 1, -PHI], [0, -1, -PHI],
      [PHI, 0, 1], [-PHI, 0, 1], [PHI, 0, -1], [-PHI, 0, -1],
      [1, PHI, 0], [-1, PHI, 0], [1, -PHI, 0], [-1, -PHI, 0]
    ];
    const vertices = raw.map(v => vScale(v, s));
    const faces = [];
    for (let i = 0; i < 12; i++) {
      for (let j = i + 1; j < 12; j++) {
        for (let k = j + 1; k < 12; k++) {
          const d1 = vMag(vSub(vertices[i], vertices[j]));
          const d2 = vMag(vSub(vertices[j], vertices[k]));
          const d3 = vMag(vSub(vertices[k], vertices[i]));
          const target = 2 * s;
          if (Math.abs(d1 - target) < 1e-3 && Math.abs(d2 - target) < 1e-3 && Math.abs(d3 - target) < 1e-3) {
            const v0 = vertices[i], v1 = vertices[j], v2 = vertices[k];
            const c = vScale(vAdd(vAdd(v0, v1), v2), 1 / 3);
            const n = vCross(vSub(v1, v0), vSub(v2, v0));
            if (vDot(n, c) > 0) {
              faces.push([i, j, k]);
            } else {
              faces.push([i, k, j]);
            }
          }
        }
      }
    }
    return { name: 'icosahedron', title: 'Icosahedron', element: 'Water', vertices, faces, color: PAL.water };
  }

  function getDodecahedron() {
    const s = 0.82;
    const rawIco = [
      [0, 1, PHI], [0, -1, PHI], [0, 1, -PHI], [0, -1, -PHI],
      [PHI, 0, 1], [-PHI, 0, 1], [PHI, 0, -1], [-PHI, 0, -1],
      [1, PHI, 0], [-1, PHI, 0], [1, -PHI, 0], [-1, -PHI, 0]
    ];
    const rawDodeca = [
      [ 1,  1,  1], [ 1,  1, -1], [ 1, -1,  1], [ 1, -1, -1],
      [-1,  1,  1], [-1,  1, -1], [-1, -1,  1], [-1, -1, -1],
      [0, PHI, INV_PHI], [0, PHI, -INV_PHI], [0, -PHI, INV_PHI], [0, -PHI, -INV_PHI],
      [INV_PHI, 0, PHI], [-INV_PHI, 0, PHI], [INV_PHI, 0, -PHI], [-INV_PHI, 0, -PHI],
      [PHI, INV_PHI, 0], [PHI, -INV_PHI, 0], [-PHI, INV_PHI, 0], [-PHI, -INV_PHI, 0]
    ];
    const vertices = rawDodeca.map(v => vScale(v, s));

    const faces = [];
    for (let ic = 0; ic < rawIco.length; ic++) {
      const dir = vNorm(rawIco[ic]);
      const scored = vertices.map((v, idx) => ({ idx, dot: vDot(v, dir) }));
      scored.sort((a, b) => b.dot - a.dot);
      const top5 = scored.slice(0, 5).map(x => x.idx);

      const c = top5.reduce((acc, idx) => vAdd(acc, vScale(vertices[idx], 0.2)), [0, 0, 0]);
      let u = Math.abs(dir[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0];
      const uDotD = vDot(u, dir);
      u = vNorm(vSub(u, vScale(dir, uDotD)));
      const v = vCross(dir, u);

      top5.sort((a, b) => {
        const da = vSub(vertices[a], c);
        const db = vSub(vertices[b], c);
        const anga = Math.atan2(vDot(da, v), vDot(da, u));
        const angb = Math.atan2(vDot(db, v), vDot(db, u));
        return anga - angb;
      });
      faces.push(top5);
    }
    return { name: 'dodecahedron', title: 'Dodecahedron', element: 'Aether', vertices, faces, color: PAL.aether };
  }

  // --- Truncation & Rectification Helpers ---
  function truncateSolid(base, ratio, name, title) {
    const { vertices, faces } = base;
    const { edges } = getEdgesFromFaces(faces);
    const cutMap = new Map();
    const newVertices = [];

    function getCutIdx(u, v) {
      const key = `${u}_${v}`;
      if (cutMap.has(key)) return cutMap.get(key);
      const pt = vLerp(vertices[u], vertices[v], ratio);
      const idx = newVertices.length;
      newVertices.push(pt);
      cutMap.set(key, idx);
      return idx;
    }

    const newFaces = [];
    const faceRoles = [];

    // 1. Base face 2k-gons
    faces.forEach(f => {
      const k = f.length;
      const poly = [];
      for (let i = 0; i < k; i++) {
        const u = f[i];
        const v = f[(i + 1) % k];
        poly.push(getCutIdx(u, v));
        poly.push(getCutIdx(v, u));
      }
      const p0 = newVertices[poly[0]], p1 = newVertices[poly[1]], p2 = newVertices[poly[2]];
      const c = poly.reduce((acc, idx) => vAdd(acc, vScale(newVertices[idx], 1 / poly.length)), [0, 0, 0]);
      const norm = vCross(vSub(p1, p0), vSub(p2, p0));
      if (vDot(norm, c) < 0) poly.reverse();
      newFaces.push(poly);
      faceRoles.push('base');
    });

    // 2. Vertex truncation q-gons
    for (let u = 0; u < vertices.length; u++) {
      const neighbors = [];
      edges.forEach(e => {
        if (e.a === u) neighbors.push(e.b);
        else if (e.b === u) neighbors.push(e.a);
      });
      const norm = vNorm(vertices[u]);
      const cutIndices = neighbors.map(w => ({
        idx: getCutIdx(u, w),
        pt: newVertices[getCutIdx(u, w)]
      }));
      const c = cutIndices.reduce((acc, x) => vAdd(acc, vScale(x.pt, 1 / cutIndices.length)), [0, 0, 0]);
      let uAxis = Math.abs(norm[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0];
      uAxis = vNorm(vSub(uAxis, vScale(norm, vDot(uAxis, norm))));
      const vAxis = vCross(norm, uAxis);

      cutIndices.sort((a, b) => {
        const da = vSub(a.pt, c);
        const db = vSub(b.pt, c);
        return Math.atan2(vDot(da, vAxis), vDot(da, uAxis)) - Math.atan2(vDot(db, vAxis), vDot(db, uAxis));
      });
      const poly = cutIndices.map(x => x.idx);
      const p0 = newVertices[poly[0]], p1 = newVertices[poly[1]], p2 = newVertices[poly[2]];
      const n = vCross(vSub(p1, p0), vSub(p2, p0));
      if (vDot(n, norm) < 0) poly.reverse();
      newFaces.push(poly);
      faceRoles.push('truncation');
    }

    return {
      name: name || ('truncated-' + base.name),
      title: title || ('Truncated ' + base.title),
      vertices: newVertices,
      faces: newFaces,
      faceRoles
    };
  }

  function rectifySolid(base, name, title) {
    const { vertices, faces } = base;
    const { edges, edgeMap } = getEdgesFromFaces(faces);
    const newVertices = edges.map(e => vScale(vAdd(vertices[e.a], vertices[e.b]), 0.5));
    const newFaces = [];
    const faceRoles = [];

    // 1. Face truncations
    faces.forEach(f => {
      const k = f.length;
      const poly = [];
      for (let i = 0; i < k; i++) {
        const a = f[i];
        const b = f[(i + 1) % k];
        const key = a < b ? `${a}_${b}` : `${b}_${a}`;
        poly.push(edgeMap.get(key));
      }
      const p0 = newVertices[poly[0]], p1 = newVertices[poly[1]], p2 = newVertices[poly[2]];
      const c = poly.reduce((acc, idx) => vAdd(acc, vScale(newVertices[idx], 1 / poly.length)), [0, 0, 0]);
      const norm = vCross(vSub(p1, p0), vSub(p2, p0));
      if (vDot(norm, c) < 0) poly.reverse();
      newFaces.push(poly);
      faceRoles.push('base');
    });

    // 2. Vertex truncations
    for (let u = 0; u < vertices.length; u++) {
      const incidentEdgeIndices = [];
      edges.forEach((e, eIdx) => {
        if (e.a === u || e.b === u) incidentEdgeIndices.push(eIdx);
      });
      const norm = vNorm(vertices[u]);
      const c = incidentEdgeIndices.reduce((acc, idx) => vAdd(acc, vScale(newVertices[idx], 1 / incidentEdgeIndices.length)), [0, 0, 0]);
      let uAxis = Math.abs(norm[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0];
      uAxis = vNorm(vSub(uAxis, vScale(norm, vDot(uAxis, norm))));
      const vAxis = vCross(norm, uAxis);

      incidentEdgeIndices.sort((a, b) => {
        const da = vSub(newVertices[a], c);
        const db = vSub(newVertices[b], c);
        return Math.atan2(vDot(da, vAxis), vDot(da, uAxis)) - Math.atan2(vDot(db, vAxis), vDot(db, uAxis));
      });
      const poly = incidentEdgeIndices;
      const p0 = newVertices[poly[0]], p1 = newVertices[poly[1]], p2 = newVertices[poly[2]];
      const n = vCross(vSub(p1, p0), vSub(p2, p0));
      if (vDot(n, norm) < 0) poly.reverse();
      newFaces.push(poly);
      faceRoles.push('truncation');
    }

    return {
      name: name || ('rectified-' + base.name),
      title: title || ('Rectified ' + base.title),
      vertices: newVertices,
      faces: newFaces,
      faceRoles
    };
  }

  function getRhombicuboctahedron() {
    const xi = 1 + Math.SQRT2;
    const rawVerts = [];
    const signs = [-1, 1];

    const basePerms = [
      (s1, s2, s3) => [s1, s2, s3 * xi],
      (s1, s2, s3) => [s1, s2 * xi, s3],
      (s1, s2, s3) => [s1 * xi, s2, s3]
    ];

    basePerms.forEach(perm => {
      signs.forEach(s1 => {
        signs.forEach(s2 => {
          signs.forEach(s3 => {
            rawVerts.push(perm(s1, s2, s3));
          });
        });
      });
    });

    const vertices = rawVerts;
    const faces = [];
    const faceRoles = [];

    function addFace(indices, role) {
      const pts = indices.map(i => vertices[i]);
      const c = pts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / pts.length)), [0, 0, 0]);
      const norm = vNorm(c);
      let uAxis = Math.abs(norm[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0];
      uAxis = vNorm(vSub(uAxis, vScale(norm, vDot(uAxis, norm))));
      const vAxis = vCross(norm, uAxis);

      indices.sort((a, b) => {
        const da = vSub(vertices[a], c);
        const db = vSub(vertices[b], c);
        return Math.atan2(vDot(da, vAxis), vDot(da, uAxis)) - Math.atan2(vDot(db, vAxis), vDot(db, uAxis));
      });

      const p0 = vertices[indices[0]], p1 = vertices[indices[1]], p2 = vertices[indices[2]];
      const n = vCross(vSub(p1, p0), vSub(p2, p0));
      if (vDot(n, norm) < 0) indices.reverse();
      faces.push(indices);
      faceRoles.push(role);
    }

    // 6 Axial Squares
    [-xi, xi].forEach(val => {
      const sq = [];
      vertices.forEach((v, idx) => { if (Math.abs(v[2] - val) < 1e-4) sq.push(idx); });
      addFace(sq, 'axial_square');
    });
    [-xi, xi].forEach(val => {
      const sq = [];
      vertices.forEach((v, idx) => { if (Math.abs(v[1] - val) < 1e-4) sq.push(idx); });
      addFace(sq, 'axial_square');
    });
    [-xi, xi].forEach(val => {
      const sq = [];
      vertices.forEach((v, idx) => { if (Math.abs(v[0] - val) < 1e-4) sq.push(idx); });
      addFace(sq, 'axial_square');
    });

    // 8 Octant Triangles
    signs.forEach(sx => {
      signs.forEach(sy => {
        signs.forEach(sz => {
          const tri = [];
          vertices.forEach((v, idx) => {
            if (Math.sign(v[0]) === sx && Math.sign(v[1]) === sy && Math.sign(v[2]) === sz) {
              tri.push(idx);
            }
          });
          if (tri.length === 3) addFace(tri, 'octant_triangle');
        });
      });
    });

    // 12 Chamfer Squares
    signs.forEach(sx => {
      signs.forEach(sy => {
        const sq = [];
        vertices.forEach((v, idx) => {
          if (Math.sign(v[0]) === sx && Math.sign(v[1]) === sy && Math.abs(Math.abs(v[2]) - 1) < 1e-4) {
            sq.push(idx);
          }
        });
        if (sq.length === 4) addFace(sq, 'chamfer_square');
      });
    });
    signs.forEach(sy => {
      signs.forEach(sz => {
        const sq = [];
        vertices.forEach((v, idx) => {
          if (Math.sign(v[1]) === sy && Math.sign(v[2]) === sz && Math.abs(Math.abs(v[0]) - 1) < 1e-4) {
            sq.push(idx);
          }
        });
        if (sq.length === 4) addFace(sq, 'chamfer_square');
      });
    });
    signs.forEach(sz => {
      signs.forEach(sx => {
        const sq = [];
        vertices.forEach((v, idx) => {
          if (Math.sign(v[2]) === sz && Math.sign(v[0]) === sx && Math.abs(Math.abs(v[1]) - 1) < 1e-4) {
            sq.push(idx);
          }
        });
        if (sq.length === 4) addFace(sq, 'chamfer_square');
      });
    });

    return {
      name: 'rhombicuboctahedron',
      title: 'Rhombicuboctahedron',
      vertices,
      faces,
      faceRoles
    };
  }

  // --- Polar Dual Solid Generator (Catalan Duals) ---
  function polarDualSolid(base, name, title) {
    const { vertices, faces } = base;
    const { edges } = getEdgesFromFaces(faces);

    let rMidSqSum = 0;
    edges.forEach(e => {
      const mid = vScale(vAdd(vertices[e.a], vertices[e.b]), 0.5);
      rMidSqSum += vDot(mid, mid);
    });
    const rMidSq = edges.length > 0 ? (rMidSqSum / edges.length) : 1.5;

    const dualVertices = faces.map(f => {
      const pts = f.map(idx => vertices[idx]);
      const c = pts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / pts.length)), [0, 0, 0]);
      const cSq = vDot(c, c);
      return cSq > 1e-6 ? vScale(c, rMidSq / cSq) : [0, 0, 0];
    });

    const dualFaces = [];
    const faceRoles = [];

    for (let u = 0; u < vertices.length; u++) {
      const incidentFaceIndices = [];
      faces.forEach((f, fIdx) => {
        if (f.includes(u)) incidentFaceIndices.push(fIdx);
      });

      const norm = vNorm(vertices[u]);
      const c = incidentFaceIndices.reduce((acc, fIdx) => vAdd(acc, vScale(dualVertices[fIdx], 1 / incidentFaceIndices.length)), [0, 0, 0]);
      let uAxis = Math.abs(norm[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0];
      uAxis = vNorm(vSub(uAxis, vScale(norm, vDot(uAxis, norm))));
      const vAxis = vCross(norm, uAxis);

      incidentFaceIndices.sort((a, b) => {
        const da = vSub(dualVertices[a], c);
        const db = vSub(dualVertices[b], c);
        return Math.atan2(vDot(da, vAxis), vDot(da, uAxis)) - Math.atan2(vDot(db, vAxis), vDot(db, uAxis));
      });

      const poly = incidentFaceIndices;
      const p0 = dualVertices[poly[0]], p1 = dualVertices[poly[1]], p2 = dualVertices[poly[2]];
      const n = vCross(vSub(p1, p0), vSub(p2, p0));
      if (vDot(n, norm) < 0) poly.reverse();
      dualFaces.push(poly);
      faceRoles.push('rhombus');
    }

    return {
      name: name || ('dual-' + base.name),
      title: title || ('Dual of ' + base.title),
      vertices: dualVertices,
      faces: dualFaces,
      faceRoles,
      dualOf: base.title,
      color: [234, 179, 8] // Warm golden amber for Catalan duals
    };
  }

  // --- Leonardo & Kepler Elevated Solid Generator ---
  function elevateSolid(base, name, title) {
    const { vertices, faces } = base;
    const newVertices = [...vertices.map(v => [...v])];
    const newFaces = [];
    const faceRoles = [];

    faces.forEach((f, fIdx) => {
      const k = f.length;
      const pts = f.map(idx => vertices[idx]);
      const c = pts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / k)), [0, 0, 0]);
      let norm = vCross(vSub(pts[1], pts[0]), vSub(pts[2], pts[0]));
      norm = vNorm(norm);
      if (vDot(norm, c) < 0) norm = vScale(norm, -1);

      const s = vMag(vSub(pts[1], pts[0]));
      let h;
      if (k === 3) {
        h = s * Math.sqrt(6) / 3;
      } else if (k === 4) {
        h = s * Math.SQRT2 / 2;
      } else if (k === 5) {
        h = s * Math.sqrt((5 - Math.sqrt(5)) / 10);
      } else {
        h = s * 0.5;
      }

      const apex = vAdd(c, vScale(norm, h));
      const apexIdx = newVertices.length;
      newVertices.push(apex);

      for (let j = 0; j < k; j++) {
        const u = f[j];
        const v = f[(j + 1) % k];
        const tri = [u, v, apexIdx];
        const p0 = newVertices[tri[0]], p1 = newVertices[tri[1]], p2 = newVertices[tri[2]];
        const triNorm = vCross(vSub(p1, p0), vSub(p2, p0));
        const triCenter = vScale(vAdd(vAdd(p0, p1), p2), 1 / 3);
        if (vDot(triNorm, triCenter) < 0) tri.reverse();
        newFaces.push(tri);
        faceRoles.push('elevated_pyramid');
      }
    });

    return {
      name: name || ('augmented-' + base.name),
      title: title || ('Augmented ' + base.title),
      vertices: newVertices,
      faces: newFaces,
      faceRoles,
      parentSolid: base,
      color: [251, 165, 48] // Luminous amber-gold for augmented stellation pyramids
    };
  }

  // --- Canonical Pyramids & Bipyramids ---
  function getPyramid(h, name, title) {
    const yBase = -h * 0.25;
    const yApex = h * 0.75;
    const vertices = [
      [ 1, yBase,  1],
      [-1, yBase,  1],
      [-1, yBase, -1],
      [ 1, yBase, -1],
      [ 0, yApex,  0]
    ];
    const faces = [
      [0, 1, 2, 3], // Base (normal pointing down -Y)
      [0, 4, 1],    // South
      [3, 4, 0],    // East
      [2, 4, 3],    // North
      [1, 4, 2]     // West
    ];
    return {
      name,
      title,
      vertices,
      faces,
      h,
      color: [244, 224, 186] // Luminous alabaster-gold
    };
  }

  function getGoldenBipyramid() {
    const h = Math.sqrt(PHI);
    const vertices = [
      [ 1,  0,  1],
      [-1,  0,  1],
      [-1,  0, -1],
      [ 1,  0, -1],
      [ 0,  h,  0],
      [ 0, -h,  0]
    ];
    const faces = [
      [0, 4, 1], [3, 4, 0], [2, 4, 3], [1, 4, 2],
      [1, 5, 0], [0, 5, 3], [3, 5, 2], [2, 5, 1]
    ];
    return {
      name: 'golden-bipyramid',
      title: 'Golden Square Bipyramid',
      vertices,
      faces,
      h,
      color: [251, 191, 36] // Luminous 24k gold
    };
  }

  function getPentagonalPyramid() {
    const s = 2.0;
    const R5 = s / (2 * Math.sin(Math.PI / 5));
    const h = s * Math.sqrt((5 - Math.sqrt(5)) / 10);
    const yBase = -h / 6;
    const yApex = 5 * h / 6;

    const vertices = [];
    for (let k = 0; k < 5; k++) {
      const angle = (k * 2 * Math.PI) / 5;
      vertices.push([R5 * Math.cos(angle), yBase, R5 * Math.sin(angle)]);
    }
    vertices.push([0, yApex, 0]); // Apex is index 5

    const faces = [
      [0, 1, 2, 3, 4], // Base pentagon (normal pointing down -Y)
      [1, 0, 5],
      [2, 1, 5],
      [3, 2, 5],
      [4, 3, 5],
      [0, 4, 5]
    ];
    return {
      name: 'pentagonal-pyramid',
      title: 'Pentagonal Pyramid (J₂)',
      vertices,
      faces,
      h,
      s,
      R5,
      color: [192, 132, 252] // Luminous amethyst
    };
  }

  // --- Solid Categorization & Master Registry ---
  function getSolidCategory(rawSlug) {
    const slug = (rawSlug || '').trim().toLowerCase().replace(/_/g, '-');
    const platonic = ['tetrahedron', 'hexahedron', 'cube', 'octahedron', 'icosahedron', 'dodecahedron'];
    const archimedean = [
      'truncated-tetrahedron', 'cuboctahedron', 'truncated-hexahedron',
      'truncated-octahedron', 'rhombicuboctahedron', 'icosidodecahedron',
      'truncated-icosahedron', 'truncated-dodecahedron'
    ];
    const catalan = ['rhombic-dodecahedron', 'rhombic-triacontahedron'];
    const elevated = [
      'tetrahedron-elevatum', 'hexahedron-elevatum', 'stella-octangula',
      'icosahedron-elevatum', 'dodecahedron-elevatum',
      'cuboctahedron-elevatum', 'icosidodecahedron-elevatum'
    ];
    const pyramid = ['kepler-pyramid', 'seked-pyramid', 'golden-bipyramid', 'pentagonal-pyramid'];

    if (platonic.includes(slug)) return 'platonic';
    if (archimedean.includes(slug)) return 'archimedean';
    if (catalan.includes(slug)) return 'catalan';
    if (elevated.includes(slug)) return 'elevated';
    if (pyramid.includes(slug)) return 'pyramid';
    return 'unknown';
  }

  function getSolid(rawSlug) {
    const slug = (rawSlug || '').trim().toLowerCase().replace(/_/g, '-');
    let solid = null;

    switch (slug) {
      // 1. Platonic Solids
      case 'tetrahedron':
        solid = getTetrahedron();
        break;
      case 'hexahedron':
      case 'cube':
        solid = getHexahedron();
        break;
      case 'octahedron':
        solid = getOctahedron();
        break;
      case 'icosahedron':
        solid = getIcosahedron();
        break;
      case 'dodecahedron':
        solid = getDodecahedron();
        break;

      // 2. Archimedean Solids
      case 'truncated-tetrahedron':
        solid = truncateSolid(getTetrahedron(), 1/3, 'truncated-tetrahedron', 'Truncated Tetrahedron');
        break;
      case 'cuboctahedron':
        solid = rectifySolid(getHexahedron(), 'cuboctahedron', 'Cuboctahedron');
        break;
      case 'truncated-hexahedron':
        solid = truncateSolid(getHexahedron(), 1 - Math.SQRT2 / 2, 'truncated-hexahedron', 'Truncated Hexahedron');
        break;
      case 'truncated-octahedron':
        solid = truncateSolid(getOctahedron(), 1/3, 'truncated-octahedron', 'Truncated Octahedron');
        break;
      case 'rhombicuboctahedron':
        solid = getRhombicuboctahedron();
        break;
      case 'icosidodecahedron':
        solid = rectifySolid(getDodecahedron(), 'icosidodecahedron', 'Icosidodecahedron');
        break;
      case 'truncated-icosahedron':
        solid = truncateSolid(getIcosahedron(), 1/3, 'truncated-icosahedron', 'Truncated Icosahedron');
        break;
      case 'truncated-dodecahedron':
        solid = truncateSolid(getDodecahedron(), (3 - PHI) / 5, 'truncated-dodecahedron', 'Truncated Dodecahedron');
        break;

      // 3. Catalan Duals
      case 'rhombic-dodecahedron':
        solid = polarDualSolid(rectifySolid(getHexahedron()), 'rhombic-dodecahedron', 'Rhombic Dodecahedron');
        break;
      case 'rhombic-triacontahedron':
        solid = polarDualSolid(rectifySolid(getDodecahedron()), 'rhombic-triacontahedron', 'Rhombic Triacontahedron');
        break;

      // 4. Augmented & Stellated Solids
      case 'tetrahedron-elevatum':
        solid = elevateSolid(getTetrahedron(), 'tetrahedron-elevatum', 'Triakis Tetrahedron');
        break;
      case 'hexahedron-elevatum':
        solid = elevateSolid(getHexahedron(), 'hexahedron-elevatum', 'Tetrakis Hexahedron');
        break;
      case 'stella-octangula':
        solid = elevateSolid(getOctahedron(), 'stella-octangula', 'Stella Octangula');
        break;
      case 'icosahedron-elevatum':
        solid = elevateSolid(getIcosahedron(), 'icosahedron-elevatum', 'Triakis Icosahedron');
        break;
      case 'dodecahedron-elevatum':
        solid = elevateSolid(getDodecahedron(), 'dodecahedron-elevatum', 'Pentakis Dodecahedron');
        break;
      case 'cuboctahedron-elevatum':
        solid = elevateSolid(rectifySolid(getHexahedron()), 'cuboctahedron-elevatum', 'Augmented Cuboctahedron');
        break;
      case 'icosidodecahedron-elevatum':
        solid = elevateSolid(rectifySolid(getDodecahedron()), 'icosidodecahedron-elevatum', 'Augmented Icosidodecahedron');
        break;

      // 5. Canonical Pyramids & Bipyramids
      case 'kepler-pyramid':
        solid = getPyramid(Math.sqrt(PHI), 'kepler-pyramid', 'Kepler Golden Pyramid');
        break;
      case 'seked-pyramid':
        solid = getPyramid(14 / 11, 'seked-pyramid', 'Seked 14:11 Pyramid');
        break;
      case 'golden-bipyramid':
        solid = getGoldenBipyramid();
        break;
      case 'pentagonal-pyramid':
        solid = getPentagonalPyramid();
        break;

      default:
        solid = getIcosahedron();
    }

    return normalizeSolid(solid, 1.80);
  }

  function getPlatonicSolid(name) {
    return getSolid(name);
  }


  // --- Procedural Polyhedral Mesh Builders ---

  // 1. Planar Surface Mesh
  function buildSolidumMesh(base) {
    const { vertices, faces, color } = base;
    const polygons = faces.map(f => {
      const pts = f.map(idx => vertices[idx]);
      const c = pts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / pts.length)), [0, 0, 0]);
      let norm = vNorm(vCross(vSub(pts[1], pts[0]), vSub(pts[2], pts[0])));
      if (vDot(norm, c) < 0) norm = vScale(norm, -1);

      let faceCol = color;
      if (!faceCol) {
        const k = f.length;
        if (k === 3) faceCol = [72, 198, 250];       // Cerulean (Triangles)
        else if (k === 4) faceCol = [251, 191, 36];  // Radiant Gold (Squares)
        else if (k === 5) faceCol = [192, 132, 252]; // Amethyst (Pentagons)
        else if (k === 6) faceCol = [96, 165, 250];  // Sapphire (Hexagons)
        else if (k === 8) faceCol = [52, 211, 153];  // Emerald (Octagons)
        else if (k === 10) faceCol = [251, 113, 133];// Rose (Decagons)
        else faceCol = [245, 172, 56];               // Amber
      }

      return {
        pts,
        centroid: c,
        norm,
        baseColor: faceCol,
        type: 'face',
        wireColor: '#1e293b'
      };
    });
    return {
      polygons,
      V: vertices.length,
      E: getEdgesFromFaces(faces).edges.length,
      F: faces.length,
      genus: 0,
      label: `${base.title} • Faceted Surfaces`
    };
  }

  // 2. Beveled Hollow Frame (6 * E mitered quads: outer, inner, window jamb)
  function buildVacuumMesh(base, mu, frameThickness) {
    const { vertices, faces } = base;
    const { edges } = getEdgesFromFaces(faces);
    const E = edges.length;
    const V = vertices.length;
    const F = faces.length;
    const R_in = 1.0 - (frameThickness || 0.14);

    const polygons = [];

    faces.forEach(f => {
      const k = f.length;
      const faceVerts = f.map(idx => vertices[idx]);
      const cFace = faceVerts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / k)), [0, 0, 0]);
      let faceNorm = vNorm(vCross(vSub(faceVerts[1], faceVerts[0]), vSub(faceVerts[2], faceVerts[0])));
      if (vDot(faceNorm, cFace) < 0) faceNorm = vScale(faceNorm, -1);

      const wOut = faceVerts.map(v => vLerp(v, cFace, mu));
      const vIn = faceVerts.map(v => vScale(v, R_in));
      const wIn = wOut.map(w => vScale(w, R_in));

      for (let i = 0; i < k; i++) {
        const next = (i + 1) % k;

        const outerQuad = [faceVerts[i], faceVerts[next], wOut[next], wOut[i]];
        const cOuter = outerQuad.reduce((acc, p) => vAdd(acc, vScale(p, 0.25)), [0, 0, 0]);
        polygons.push({
          pts: outerQuad,
          centroid: cOuter,
          norm: faceNorm,
          baseColor: PAL.frameOuter,
          type: 'frame_outer'
        });

        const innerQuad = [vIn[next], vIn[i], wIn[i], wIn[next]];
        const cInner = innerQuad.reduce((acc, p) => vAdd(acc, vScale(p, 0.25)), [0, 0, 0]);
        polygons.push({
          pts: innerQuad,
          centroid: cInner,
          norm: vScale(faceNorm, -1),
          baseColor: PAL.frameInner,
          type: 'frame_inner'
        });

        const revealQuad = [wOut[i], wOut[next], wIn[next], wIn[i]];
        const cReveal = revealQuad.reduce((acc, p) => vAdd(acc, vScale(p, 0.25)), [0, 0, 0]);
        const revealNorm = vNorm(vCross(vSub(wOut[next], wOut[i]), vSub(wIn[next], wOut[next])));
        polygons.push({
          pts: revealQuad,
          centroid: cReveal,
          norm: revealNorm,
          baseColor: PAL.frameReveal,
          type: 'frame_reveal'
        });
      }
    });

    return {
      polygons,
      V_vac: 2 * V + 4 * E,
      E_vac: 12 * E,
      F_vac: 6 * E,
      genus: F - 1,
      label: `${base.title} • Hollow Frame (Aperture ${mu.toFixed(2)})`
    };
  }

  // 3. Abscisum (Rectified Midpoint Solid)
  function buildAbscisumMesh(base) {
    const { vertices, faces } = base;
    const { edges } = getEdgesFromFaces(faces);
    const midpoints = edges.map(e => vScale(vAdd(vertices[e.a], vertices[e.b]), 0.5));

    const polygons = [];

    // Face truncations: for each original face, connect consecutive edge midpoints
    faces.forEach(f => {
      const k = f.length;
      const faceMids = [];
      for (let i = 0; i < k; i++) {
        const a = f[i];
        const b = f[(i + 1) % k];
        const key = a < b ? `${a}_${b}` : `${b}_${a}`;
        const eIdx = edges.findIndex(e => (e.a === a && e.b === b) || (e.a === b && e.b === a));
        faceMids.push(midpoints[eIdx]);
      }
      const c = faceMids.reduce((acc, p) => vAdd(acc, vScale(p, 1 / k)), [0, 0, 0]);
      const norm = vNorm(vCross(vSub(faceMids[1], faceMids[0]), vSub(faceMids[2], faceMids[0])));
      polygons.push({
        pts: faceMids,
        centroid: c,
        norm,
        baseColor: [59, 130, 246], // Deep lapis
        type: 'abscisum_face'
      });
    });

    // Vertex truncations: for each original vertex, connect midpoints of incident edges
    for (let vIdx = 0; vIdx < vertices.length; vIdx++) {
      const incidentEdges = [];
      edges.forEach((e, eIdx) => {
        if (e.a === vIdx || e.b === vIdx) incidentEdges.push(eIdx);
      });
      const incidentMids = incidentEdges.map(idx => midpoints[idx]);
      const c = incidentMids.reduce((acc, p) => vAdd(acc, vScale(p, 1 / incidentMids.length)), [0, 0, 0]);
      const norm = vNorm(vertices[vIdx]);

      // Sort midpoints cyclically around vertex normal
      let u = Math.abs(norm[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0];
      const un = vDot(u, norm);
      u = vNorm(vSub(u, vScale(norm, un)));
      const v = vCross(norm, u);

      incidentMids.sort((p1, p2) => {
        const d1 = vSub(p1, c);
        const d2 = vSub(p2, c);
        return Math.atan2(vDot(d1, v), vDot(d1, u)) - Math.atan2(vDot(d2, v), vDot(d2, u));
      });

      polygons.push({
        pts: incidentMids,
        centroid: c,
        norm,
        baseColor: [245, 158, 11], // Radiant gold
        type: 'abscisum_corner'
      });
    }

    return {
      polygons,
      V: edges.length,
      E: edges.length * 2,
      F: faces.length + vertices.length,
      genus: 0,
      label: 'Abscisum (Archimedean Rectification)'
    };
  }

  // 4. Elevatum (Stellated / Pyramidal Augmentation)
  function buildElevatumMesh(base) {
    const { vertices, faces } = base;
    const { edges } = getEdgesFromFaces(faces);
    const polygons = [];

    faces.forEach(f => {
      const k = f.length;
      const pts = f.map(idx => vertices[idx]);
      const c = pts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / k)), [0, 0, 0]);
      const norm = vNorm(vCross(vSub(pts[1], pts[0]), vSub(pts[2], pts[0])));
      const edgeLen = vMag(vSub(pts[1], pts[0]));

      // Stellation height based on regular polygon geometry
      let h = edgeLen * Math.sqrt(2 / 3);
      if (k === 4) h = edgeLen * 0.7071;
      if (k === 5) h = edgeLen * 1.15; // Golden stellation

      const apex = vAdd(c, vScale(norm, h));

      // Erect k triangular faces
      for (let i = 0; i < k; i++) {
        const next = (i + 1) % k;
        const tri = [pts[i], pts[next], apex];
        const triCenter = vScale(vAdd(vAdd(pts[i], pts[next]), apex), 1 / 3);
        const triNorm = vNorm(vCross(vSub(pts[next], pts[i]), vSub(apex, pts[i])));
        polygons.push({
          pts: tri,
          centroid: triCenter,
          norm: triNorm,
          baseColor: [217, 119, 6], // Amber bronze
          type: 'elevatum_pyramid'
        });
      }
    });

    return {
      polygons,
      V: vertices.length + faces.length,
      E: edges.length + faces.length * (faces[0].length),
      F: faces.reduce((acc, f) => acc + f.length, 0),
      genus: 0,
      label: 'Elevatum (Stellated Pyramids)'
    };
  }

  // --- Exact Face-Center Dual & Golden Sections / Golden Rectangles ---

  function orderQuadInPlane(pts4) {
    const c = pts4.reduce((acc, p) => vAdd(acc, vScale(p, 0.25)), [0, 0, 0]);
    const u = vNorm(vSub(pts4[0], c));
    let n = [0, 0, 0];
    for (let i = 1; i < pts4.length; i++) {
      const cand = vCross(u, vSub(pts4[i], c));
      if (vMag(cand) > 1e-5) {
        n = vNorm(cand);
        break;
      }
    }
    const v = vNorm(vCross(n, u));
    return pts4.slice().sort((a, b) => {
      const da = vSub(a, c);
      const db = vSub(b, c);
      return Math.atan2(vDot(da, v), vDot(da, u)) - Math.atan2(vDot(db, v), vDot(db, u));
    });
  }

  function extractCoordPlaneGoldenRects(verts12) {
    const rects = [];
    const xy = verts12.filter(p => Math.abs(p[2]) < 1e-3);
    const yz = verts12.filter(p => Math.abs(p[0]) < 1e-3);
    const zx = verts12.filter(p => Math.abs(p[1]) < 1e-3);
    if (xy.length === 4) {
      rects.push({ pts: orderQuadInPlane(xy), fill: 'rgba(251, 191, 36, 0.20)', stroke: '#fbbf24', label: 'XY (1:φ)' });
    }
    if (yz.length === 4) {
      rects.push({ pts: orderQuadInPlane(yz), fill: 'rgba(251, 146, 60, 0.20)', stroke: '#fb923c', label: 'YZ (1:φ)' });
    }
    if (zx.length === 4) {
      rects.push({ pts: orderQuadInPlane(zx), fill: 'rgba(192, 132, 252, 0.20)', stroke: '#c084fc', label: 'ZX (1:φ)' });
    }
    return rects;
  }

  function addPentagonGoldenSections(pentPts, sections, allFive = false) {
    if (pentPts.length !== 5) return;
    if (allFive) {
      for (let i = 0; i < 5; i++) {
        const pA = pentPts[i];
        const pB = pentPts[(i + 2) % 5];
        sections.push({ a: pA, g: vLerp(pA, pB, INV_PHI), b: pB });
      }
    } else {
      const p0 = pentPts[0], p1 = pentPts[1], p2 = pentPts[2], p3 = pentPts[3];
      const g = vLerp(p0, p2, INV_PHI); // Exact intersection of diagonals p0-p2 and p3-p1
      sections.push({ a: p0, g, b: p2 });
      sections.push({ a: p3, g, b: p1 });
    }
  }

  // Face-Center Dual: vertices are the exact centers (centroids) of every side
  function buildFaceCenterDual(solidNameOrBase, maybeBase) {
    const base = maybeBase || (typeof solidNameOrBase === 'object' ? solidNameOrBase : getSolid(solidNameOrBase));
    const { vertices, faces } = base;
    const { edges } = getEdgesFromFaces(faces);

    const dualVertices = faces.map(f => {
      const pts = f.map(idx => vertices[idx]);
      return pts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / pts.length)), [0, 0, 0]);
    });

    const dualEdges = [];
    edges.forEach(e => {
      if (e.faces.length === 2) {
        dualEdges.push([e.faces[0], e.faces[1]]);
      }
    });

    return {
      vertices: dualVertices,
      edges: dualEdges
    };
  }

  function getPolarDualWireframe(solidNameOrBase, maybeBase) {
    const dual = buildFaceCenterDual(solidNameOrBase, maybeBase);
    return dual.edges.map(([f0, f1]) => ({
      pts: [dual.vertices[f0], dual.vertices[f1]],
      color: '#38bdf8',
      width: 2.0,
      dashed: false
    }));
  }

  function buildGoldenOverlay(rawSlug, base) {
    const slug = (rawSlug || base.name || '').trim().toLowerCase().replace(/_/g, '-');
    const rects = [];     // Exact 1:φ Golden Rectangles: { pts: [P0,P1,P2,P3], fill, stroke, label }
    const sections = [];  // Exact φ:1 Golden Sections: { a, g, b } where |a-g| / |g-b| = φ
    const circles = [];   // 3D Circles: { center, u, v, r, color }
    const pols = [];      // Auxiliary polygons (e.g. Kepler meridian triangle)
    const lines = [];     // Auxiliary reference segments
    const labels = [];

    const V = base.vertices;
    const F = base.faces;

    // 1. Icosahedron & Triakis Icosahedron
    if (slug === 'icosahedron' || slug === 'icosahedron-elevatum') {
      const icoVerts = V.slice(0, 12);
      extractCoordPlaneGoldenRects(icoVerts).forEach(r => rects.push(r));

      // Equatorial pentagon around top-most vertex -> exact pentagram Golden Section
      let topIdx = 0;
      for (let i = 1; i < 12; i++) {
        if (icoVerts[i][1] > icoVerts[topIdx][1]) topIdx = i;
      }
      const srcFaces = (slug === 'icosahedron-elevatum' && base.parentSolid) ? base.parentSolid.faces : F;
      const nbrSet = new Set();
      srcFaces.forEach(f => {
        if (f.includes(topIdx)) f.forEach(vi => { if (vi !== topIdx && vi < 12) nbrSet.add(vi); });
      });
      const nbrs = Array.from(nbrSet).map(i => icoVerts[i]);
      if (nbrs.length === 5) {
        const cPent = nbrs.reduce((acc, p) => vAdd(acc, vScale(p, 0.2)), [0, 0, 0]);
        const axis = vNorm(icoVerts[topIdx]);
        const uAxis = vNorm(vSub(nbrs[0], cPent));
        const vAxis = vNorm(vCross(axis, uAxis));
        nbrs.sort((a, b) => Math.atan2(vDot(vSub(a, cPent), vAxis), vDot(vSub(a, cPent), uAxis)) -
                            Math.atan2(vDot(vSub(b, cPent), vAxis), vDot(vSub(b, cPent), uAxis)));
        addPentagonGoldenSections(nbrs, sections, false);
      }
    }
    // 2. Rhombic Triacontahedron (Kepler's 30 Golden Rhombi)
    else if (slug === 'rhombic-triacontahedron') {
      const deg = new Array(V.length).fill(0);
      F.forEach(f => f.forEach(vi => { deg[vi]++; }));
      const ico12 = V.filter((_, vi) => deg[vi] === 5);
      extractCoordPlaneGoldenRects(ico12).forEach(r => rects.push(r));

      // Highlight Golden Rhombus diagonals (L : S = φ : 1) and φ:1 Golden Section on front rhombi
      F.forEach((f, fi) => {
        if (f.length === 4) {
          const p0 = V[f[0]], p1 = V[f[1]], p2 = V[f[2]], p3 = V[f[3]];
          const d02 = vMag(vSub(p2, p0));
          const d13 = vMag(vSub(p3, p1));
          const longD = d02 > d13 ? [p0, p2] : [p1, p3];
          const shortD = d02 > d13 ? [p1, p3] : [p0, p2];
          if (fi < 2) {
            sections.push({ a: longD[0], g: vLerp(longD[0], longD[1], INV_PHI), b: longD[1] });
            lines.push({ pts: shortD, color: 'rgba(251, 191, 36, 0.65)', width: 1.6, dashed: true });
          }
        }
      });
    }
    // 3. Pentagonal-Face Icosahedral Solids (Dodecahedron, Icosidodecahedron, Truncated Icosa/Dodeca, & Elevata)
    else if (
      slug === 'dodecahedron' || slug === 'dodecahedron-elevatum' ||
      slug === 'icosidodecahedron' || slug === 'icosidodecahedron-elevatum' ||
      slug === 'truncated-icosahedron' || slug === 'truncated-dodecahedron'
    ) {
      const srcSolid = (base.parentSolid && (slug === 'dodecahedron-elevatum' || slug === 'icosidodecahedron-elevatum'))
        ? base.parentSolid
        : base;
      const pentFaces = srcSolid.faces.filter(f => f.length === 5 || f.length === 10);

      // For truncated-dodecahedron, 10-gon centroids are the 12 icosahedral axes; otherwise 5-gon centroids!
      const fiveGons = srcSolid.faces.filter(f => f.length === 5);
      const axisFaces = fiveGons.length === 12 ? fiveGons : pentFaces.filter(f => f.length === 10);
      if (axisFaces.length === 12) {
        const centers12 = axisFaces.map(f => {
          const pts = f.map(idx => srcSolid.vertices[idx]);
          return pts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / pts.length)), [0, 0, 0]);
        });
        extractCoordPlaneGoldenRects(centers12).forEach(r => rects.push(r));
      }

      if (fiveGons.length > 0) {
        // Add exact pentagram Golden Sections on 2 opposite pentagonal faces
        const pPts0 = fiveGons[0].map(idx => srcSolid.vertices[idx]);
        addPentagonGoldenSections(pPts0, sections, false);
        const c0 = pPts0.reduce((acc, p) => vAdd(acc, vScale(p, 0.2)), [0, 0, 0]);
        let oppIdx = -1, minDot = 1e9;
        fiveGons.forEach((f, idx) => {
          const cf = f.map(vi => srcSolid.vertices[vi]).reduce((acc, p) => vAdd(acc, vScale(p, 0.2)), [0, 0, 0]);
          const d = vDot(c0, cf);
          if (d < minDot) { minDot = d; oppIdx = idx; }
        });
        if (oppIdx > 0) {
          addPentagonGoldenSections(fiveGons[oppIdx].map(idx => srcSolid.vertices[idx]), sections, false);
        }
      } else {
        // Truncated dodecahedron (decagonal faces): divide 2 prominent edges in exact Golden Section
        const { edges } = getEdgesFromFaces(srcSolid.faces);
        edges.slice(0, 2).forEach(e => {
          const a = srcSolid.vertices[e.a], b = srcSolid.vertices[e.b];
          sections.push({ a, g: vLerp(a, b, INV_PHI), b });
        });
      }
    }
    // 4. Octahedron & Stella Octangula (12 Edge Golden Sections -> 3 Orthogonal Golden Rectangles!)
    else if (slug === 'octahedron' || slug === 'stella-octangula') {
      const ox = V.slice(0, 6); // [+R,0,0], [-R,0,0], [0,+R,0], [0,-R,0], [0,0,+R], [0,0,-R]
      const pairs = [
        [0, 2], [0, 3], [1, 2], [1, 3], // ±X -> ±Y (lies in XY)
        [2, 4], [2, 5], [3, 4], [3, 5], // ±Y -> ±Z (lies in YZ)
        [4, 0], [4, 1], [5, 0], [5, 1]  // ±Z -> ±X (lies in ZX)
      ];
      const gPts12 = [];
      pairs.forEach(([uIdx, vIdx]) => {
        const u = ox[uIdx];
        const v = ox[vIdx];
        const g = vLerp(u, v, INV_PHI); // |u - g| = φ⁻¹ |v - u| (major), |g - v| = φ⁻² |v - u| (minor) => |u-g|/|g-v| = φ!
        sections.push({ a: u, g, b: v });
        gPts12.push(g);
      });
      extractCoordPlaneGoldenRects(gPts12).forEach(r => rects.push(r));
    }
    // 5. Hexahedron (Cube) & Tetrakis Hexahedron (3 Orthogonal Golden Rectangles Flush on 6 Cube Faces!)
    else if (slug === 'hexahedron' || slug === 'cube' || slug === 'hexahedron-elevatum') {
      const a = Math.abs(V[0][0]);
      const b = a * INV_PHI;
      rects.push({
        pts: [[ b,  a, 0], [-b,  a, 0], [-b, -a, 0], [ b, -a, 0]],
        fill: 'rgba(251, 191, 36, 0.20)', stroke: '#fbbf24', label: 'XY (1:φ)'
      });
      rects.push({
        pts: [[0,  b,  a], [0, -b,  a], [0, -b, -a], [0,  b, -a]],
        fill: 'rgba(251, 146, 60, 0.20)', stroke: '#fb923c', label: 'YZ (1:φ)'
      });
      rects.push({
        pts: [[ a, 0,  b], [ a, 0, -b], [-a, 0, -b], [-a, 0,  b]],
        fill: 'rgba(192, 132, 252, 0.20)', stroke: '#c084fc', label: 'ZX (1:φ)'
      });
      // Face midline Golden Sections
      const mTopA = [-a, a, 0], mTopB = [a, a, 0];
      sections.push({ a: mTopA, g: vLerp(mTopA, mTopB, INV_PHI), b: mTopB });
      const mFrontA = [0, -a, a], mFrontB = [0, a, a];
      sections.push({ a: mFrontA, g: vLerp(mFrontA, mFrontB, INV_PHI), b: mFrontB });
    }
    // 6. Tetrahedron, Triakis Tetrahedron & Truncated Tetrahedron (George Odom's 1983 Golden Section + 1:φ Rect)
    else if (slug === 'tetrahedron' || slug === 'tetrahedron-elevatum' || slug === 'truncated-tetrahedron') {
      const srcSolid = (slug === 'tetrahedron-elevatum' && base.parentSolid) ? base.parentSolid : base;
      const triFaces = srcSolid.faces.filter(f => f.length === 3);
      let triFace = triFaces[0] || srcSolid.faces[0];
      let bestScore = -1e9;
      triFaces.forEach(f => {
        const p0 = srcSolid.vertices[f[0]], p1 = srcSolid.vertices[f[1]], p2 = srcSolid.vertices[f[2]];
        const cf = vScale(vAdd(vAdd(p0, p1), p2), 1 / 3);
        let nf = vNorm(vCross(vSub(p1, p0), vSub(p2, p0)));
        if (vDot(nf, cf) < 0) nf = vScale(nf, -1);
        const score = vDot(nf, [-0.42, -0.33, -0.85]);
        if (score > bestScore) { bestScore = score; triFace = f; }
      });
      const A = srcSolid.vertices[triFace[0]];
      const B = srcSolid.vertices[triFace[1]];
      const C = srcSolid.vertices[triFace[2]];
      const Of = vScale(vAdd(vAdd(A, B), C), 1 / 3);
      const Rf = vMag(vSub(A, Of));
      let nf = vNorm(vCross(vSub(B, A), vSub(C, A)));
      if (vDot(nf, Of) < 0) nf = vScale(nf, -1);
      const uCirc = vNorm(vSub(A, Of));
      const vCirc = vNorm(vCross(nf, uCirc));

      circles.push({ center: Of, u: uCirc, v: vCirc, r: Rf, color: 'rgba(56, 189, 248, 0.72)' });

      const M1 = vScale(vAdd(A, B), 0.5);
      const M2 = vScale(vAdd(A, C), 0.5);
      const halfSide = vMag(vSub(M2, M1));
      const uDir = vNorm(vSub(M2, M1));
      const G2 = vAdd(M2, vScale(uDir, halfSide * INV_PHI));
      const G1 = vSub(M1, vScale(uDir, halfSide * INV_PHI));

      lines.push({ pts: [G1, M1], color: 'rgba(251, 191, 36, 0.50)', width: 1.5, dashed: true });
      sections.push({ a: M1, g: M2, b: G2 });

      // Exact 1:φ Golden Rectangle erected on Odom chord M1-G2 (length = halfSide * φ, height = halfSide)
      const vPerp = vNorm(vCross(nf, uDir));
      const R2 = vAdd(G2, vScale(vPerp, -halfSide));
      const R3 = vAdd(M1, vScale(vPerp, -halfSide));
      rects.push({
        pts: [M1, G2, R2, R3],
        fill: 'rgba(251, 191, 36, 0.20)',
        stroke: '#fbbf24',
        label: 'Odom (1:φ)'
      });
    }
    // 7. Pyramids & Golden Bipyramid
    else if (slug === 'kepler-pyramid' || slug === 'seked-pyramid' || slug === 'golden-bipyramid') {
      const O = vScale(vAdd(vAdd(V[0], V[1]), vAdd(V[2], V[3])), 0.25);
      const ME = vScale(vAdd(V[0], V[3]), 0.5);
      const MW = vScale(vAdd(V[1], V[2]), 0.5);
      const A = V[4];
      const a = vMag(vSub(ME, O));
      const b = a * INV_PHI;

      // Meridian right triangle / lozenge
      if (slug === 'golden-bipyramid') {
        pols.push({
          pts: [ME, A, MW, V[5]],
          color: 'rgba(251, 191, 36, 0.16)',
          stroke: 'rgba(251, 191, 36, 0.65)',
          width: 1.8
        });
      } else {
        pols.push({
          pts: [O, ME, A],
          color: 'rgba(251, 191, 36, 0.18)',
          stroke: 'rgba(251, 191, 36, 0.70)',
          width: 2.0
        });
      }

      // Base / Equatorial 1:φ Golden Rectangle
      rects.push({
        pts: [
          [O[0] + b, O[1], O[2] + a],
          [O[0] - b, O[1], O[2] + a],
          [O[0] - b, O[1], O[2] - a],
          [O[0] + b, O[1], O[2] - a]
        ],
        fill: 'rgba(192, 132, 252, 0.18)',
        stroke: '#c084fc',
        label: 'Base (1:φ)'
      });

      // On Kepler Pyramid & Golden Bipyramid, half-edge ME->V[0] (a) and apothem ME->A (a·φ) form an exact 1:φ Slant Golden Rectangle!
      if (slug === 'kepler-pyramid' || slug === 'golden-bipyramid') {
        const zVec = vSub(V[0], ME);
        rects.push({
          pts: [ME, V[0], vAdd(A, zVec), A],
          fill: 'rgba(251, 191, 36, 0.22)',
          stroke: '#fbbf24',
          label: 'Apothem (1:φ)'
        });
      }

      // Exact φ:1 Golden Section on slant apothem A -> ME (for Kepler, H is the exact perpendicular foot from O!)
      const H = vLerp(A, ME, INV_PHI);
      sections.push({ a: A, g: H, b: ME });
      if (slug === 'kepler-pyramid' || slug === 'golden-bipyramid') {
        lines.push({ pts: [O, H], color: 'rgba(251, 191, 36, 0.65)', width: 1.6, dashed: true });
      }
    }
    // 8. Pentagonal Pyramid (J2 — Icosahedral Cap)
    else if (slug === 'pentagonal-pyramid') {
      const pent = [V[0], V[1], V[2], V[3], V[4]];
      addPentagonGoldenSections(pent, sections, true);

      const s = vMag(vSub(pent[1], pent[0]));
      const cb = pent.reduce((acc, p) => vAdd(acc, vScale(p, 0.2)), [0, 0, 0]);
      const nb = vNorm(vCross(vSub(pent[1], pent[0]), vSub(pent[2], pent[0])));
      const u = vNorm(vSub(pent[1], pent[0]));
      const v = vNorm(vCross(nb, u));
      const hw = s * 0.5;
      const hl = s * PHI * 0.5;
      rects.push({
        pts: [
          vAdd(cb, vAdd(vScale(u,  hw), vScale(v,  hl))),
          vAdd(cb, vAdd(vScale(u, -hw), vScale(v,  hl))),
          vAdd(cb, vAdd(vScale(u, -hw), vScale(v, -hl))),
          vAdd(cb, vAdd(vScale(u,  hw), vScale(v, -hl)))
        ],
        fill: 'rgba(251, 191, 36, 0.20)',
        stroke: '#fbbf24',
        label: 'Pentagon (1:φ)'
      });
    }
    // 9. Remaining Octahedral Archimedean, Catalan & Elevated Solids
    else {
      let maxCoord = 0;
      V.forEach(p => {
        maxCoord = Math.max(maxCoord, Math.abs(p[0]), Math.abs(p[1]), Math.abs(p[2]));
      });
      const b = maxCoord * INV_PHI;
      const L = b * PHI;
      rects.push({
        pts: [[ b,  L, 0], [-b,  L, 0], [-b, -L, 0], [ b, -L, 0]],
        fill: 'rgba(251, 191, 36, 0.18)', stroke: '#fbbf24', label: 'XY (1:φ)'
      });
      rects.push({
        pts: [[0,  b,  L], [0, -b,  L], [0, -b, -L], [0,  b, -L]],
        fill: 'rgba(251, 146, 60, 0.18)', stroke: '#fb923c', label: 'YZ (1:φ)'
      });
      rects.push({
        pts: [[ L, 0,  b], [ L, 0, -b], [-L, 0, -b], [-L, 0,  b]],
        fill: 'rgba(192, 132, 252, 0.18)', stroke: '#c084fc', label: 'ZX (1:φ)'
      });

      const { edges } = getEdgesFromFaces(F);
      edges.slice(0, 2).forEach(e => {
        const pA = V[e.a], pB = V[e.b];
        sections.push({ a: pA, g: vLerp(pA, pB, INV_PHI), b: pB });
      });
    }

    return { rects, sections, circles, pols, lines, labels };
  }

  function getGoldenOverlay(solidName, base) {
    return buildGoldenOverlay(solidName, base || getSolid(solidName));
  }

  function getParentCoreWireframe(elevatedSolid) {
    const lines = [];
    if (!elevatedSolid || !elevatedSolid.parentSolid) return lines;
    const parent = elevatedSolid.parentSolid;
    const { edges } = getEdgesFromFaces(parent.faces);
    edges.forEach(e => {
      lines.push({
        pts: [parent.vertices[e.a], parent.vertices[e.b]],
        color: '#f59e0b',
        width: 2.2,
        dashed: false
      });
    });
    return lines;
  }

  // --- Dedicated Scene Generators ---

  // Scene 1: 3 Mutually Orthogonal Golden Rectangles inside Icosahedron
  function buildSceneIcosaGoldenRects(shellOpacity) {
    const s = 1.15;
    const ico = getIcosahedron();
    const icoVerts = ico.vertices.map(v => vScale(v, s / 0.88));
    const icoMesh = buildSolidumMesh({ ...ico, vertices: icoVerts });

    const rXY = [[ s,  s*PHI, 0], [-s,  s*PHI, 0], [-s, -s*PHI, 0], [ s, -s*PHI, 0]];
    const rYZ = [[0,  s,  s*PHI], [0, -s,  s*PHI], [0, -s, -s*PHI], [0,  s, -s*PHI]];
    const rZX = [[ s*PHI, 0,  s], [ s*PHI, 0, -s], [-s*PHI, 0, -s], [-s*PHI, 0,  s]];

    const rects = [
      { pts: rXY, fill: 'rgba(245, 158, 11, 0.45)', stroke: '#f59e0b', label: 'XY (Gold • 1:φ)', color: '#f59e0b' },
      { pts: rYZ, fill: 'rgba(251, 146, 60, 0.45)', stroke: '#fb923c', label: 'YZ (Amber • 1:φ)', color: '#fb923c' },
      { pts: rZX, fill: 'rgba(56, 189, 248, 0.45)', stroke: '#38bdf8', label: 'ZX (Sky • 1:φ)', color: '#38bdf8' }
    ];

    return { icoMesh, rects, shellOpacity };
  }

  // Scene 2: Octahedron to Icosahedron continuous edge division
  function buildSceneOctaToIcosa(tau) {
    const s = 1.0;
    const R = PHI_SQ * s;
    const ox = [
      [ R,  0,  0], [-R,  0,  0],
      [ 0,  R,  0], [ 0, -R,  0],
      [ 0,  0,  R], [ 0,  0, -R]
    ];

    // Octahedron 12 edges
    const octaEdges = [
      [0, 2], [0, 3], [0, 4], [0, 5],
      [1, 2], [1, 3], [1, 4], [1, 5],
      [2, 4], [2, 5], [3, 4], [3, 5]
    ];

    // 12 points sliding along edges
    const pts = [
      [0, (1 - tau) * R, tau * R],
      [0, -(1 - tau) * R, tau * R],
      [0, (1 - tau) * R, -tau * R],
      [0, -(1 - tau) * R, -tau * R],
      [tau * R, 0, (1 - tau) * R],
      [-tau * R, 0, (1 - tau) * R],
      [tau * R, 0, -(1 - tau) * R],
      [-tau * R, 0, -(1 - tau) * R],
      [(1 - tau) * R, tau * R, 0],
      [-(1 - tau) * R, tau * R, 0],
      [(1 - tau) * R, -tau * R, 0],
      [-(1 - tau) * R, -tau * R, 0]
    ];

    // 20 triangular faces formed by the 12 sliding points
    const ico = getIcosahedron();
    const triangles = ico.faces.map(f => {
      const p = f.map(idx => pts[idx]);
      const c = vScale(vAdd(vAdd(p[0], p[1]), p[2]), 1 / 3);
      const norm = vNorm(vCross(vSub(p[1], p[0]), vSub(p[2], p[0])));
      const isGold = Math.abs(tau - INV_PHI) < 0.015;
      return {
        pts: p,
        centroid: c,
        norm,
        baseColor: isGold ? [245, 158, 11] : (Math.abs(tau - 0.5) < 0.015 ? [56, 189, 248] : [148, 163, 184]),
        stroke: isGold ? '#f59e0b' : '#334155'
      };
    });

    return { ox, octaEdges, pts, triangles, tau };
  }

  // Scene 3: Euclid XIII.17 — All 5 Inscribed Cubes in Regular Dodecahedron
  function buildSceneDodecaFiveCubes(activeCubes, showRoofWedge) {
    const s = 0.95;
    const rawDodeca = [
      // 0-7: (+-1, +-1, +-1)
      [ 1,  1,  1], [ 1,  1, -1], [ 1, -1,  1], [ 1, -1, -1],
      [-1,  1,  1], [-1,  1, -1], [-1, -1,  1], [-1, -1, -1],
      // 8-11: (0, +-PHI, +-INV_PHI)
      [0,  PHI,  INV_PHI], [0,  PHI, -INV_PHI], [0, -PHI,  INV_PHI], [0, -PHI, -INV_PHI],
      // 12-15: (+-INV_PHI, 0, +-PHI)
      [ INV_PHI, 0,  PHI], [-INV_PHI, 0,  PHI], [ INV_PHI, 0, -PHI], [-INV_PHI, 0, -PHI],
      // 16-19: (+-PHI, +-INV_PHI, 0)
      [ PHI,  INV_PHI, 0], [ PHI, -INV_PHI, 0], [-PHI,  INV_PHI, 0], [-PHI, -INV_PHI, 0]
    ];
    const vertices = rawDodeca.map(v => vScale(v, s));

    // The 5 Exact Regular Inscribed Cubes
    const cubeVertIndices = [
      [0, 1, 2, 3, 4, 5, 6, 7],           // Cube 1 (Canonical Cube)
      [0, 7, 9, 10, 13, 14, 17, 18],       // Cube 2
      [1, 6, 8, 11, 12, 15, 17, 18],       // Cube 3
      [2, 5, 8, 11, 13, 14, 16, 19],       // Cube 4
      [3, 4, 9, 10, 12, 15, 16, 19]        // Cube 5
    ];

    // Compute edges of each cube (pairs at distance 2 * s)
    const cubes = cubeVertIndices.map((indices, cIdx) => {
      const cEdges = [];
      for (let i = 0; i < 8; i++) {
        for (let j = i + 1; j < 8; j++) {
          const d = vMag(vSub(vertices[indices[i]], vertices[indices[j]]));
          if (Math.abs(d - 2 * s) < 1e-3) {
            cEdges.push([indices[i], indices[j]]);
          }
        }
      }
      return {
        id: cIdx + 1,
        colorInfo: PAL.cubeColors[cIdx],
        indices,
        edges: cEdges,
        active: activeCubes[cIdx]
      };
    });

    // Dodecahedron subtle cage
    const dodeca = getDodecahedron();
    const dodecaEdges = getEdgesFromFaces(dodeca.faces).edges;

    // Roof Wedge on Cube 1 (+Z face)
    const roof = [];
    if (showRoofWedge) {
      // Ridge: between v12 and v13
      const ridgeA = vertices[12];
      const ridgeB = vertices[13];
      const c1A = vertices[0];
      const c1B = vertices[4];
      const c1C = vertices[6];
      const c1D = vertices[2];

      roof.push({
        pts: [ridgeA, ridgeB, c1B, c1A],
        fill: 'rgba(245, 158, 11, 0.35)',
        stroke: '#f59e0b'
      });
      roof.push({
        pts: [ridgeA, ridgeB, c1C, c1D],
        fill: 'rgba(245, 158, 11, 0.35)',
        stroke: '#f59e0b'
      });
      roof.push({
        pts: [ridgeA, c1A, c1D],
        fill: 'rgba(251, 146, 60, 0.40)',
        stroke: '#fb923c'
      });
      roof.push({
        pts: [ridgeB, c1B, c1C],
        fill: 'rgba(251, 146, 60, 0.40)',
        stroke: '#fb923c'
      });
    }

    return { vertices, cubes, dodecaEdges, roof, showRoofWedge };
  }

  // Scene 4: Kepler's Rhombic Triacontahedron (30 Golden Rhombi)
  function buildSceneRhombicTriacontahedron(showDodeca, showIcosa, showDiagonals, solidShading) {
    const s = 1.0;
    const rawIco = [
      [0, 1, PHI], [0, -1, PHI], [0, 1, -PHI], [0, -1, -PHI],
      [PHI, 0, 1], [-PHI, 0, 1], [PHI, 0, -1], [-PHI, 0, -1],
      [1, PHI, 0], [-1, PHI, 0], [1, -PHI, 0], [-1, -PHI, 0]
    ];
    // 12 Acute Vertices (Icosahedron)
    const acuteVerts = rawIco.map(v => vScale(v, s));

    // 20 Icosahedron Faces
    const icoFaces = [];
    for (let i = 0; i < 12; i++) {
      for (let j = i + 1; j < 12; j++) {
        for (let k = j + 1; k < 12; k++) {
          const d1 = vMag(vSub(acuteVerts[i], acuteVerts[j]));
          const d2 = vMag(vSub(acuteVerts[j], acuteVerts[k]));
          const d3 = vMag(vSub(acuteVerts[k], acuteVerts[i]));
          if (Math.abs(d1 - 2*s) < 1e-3 && Math.abs(d2 - 2*s) < 1e-3 && Math.abs(d3 - 2*s) < 1e-3) {
            icoFaces.push([i, j, k]);
          }
        }
      }
    }

    // 20 Obtuse Vertices (Dual Dodecahedron)
    const scaleObtuse = PHI / (1 + 2 * PHI);
    const obtuseVerts = icoFaces.map(f => {
      const sum = vAdd(vAdd(acuteVerts[f[0]], acuteVerts[f[1]]), acuteVerts[f[2]]);
      return vScale(sum, scaleObtuse);
    });

    // 30 Golden Rhombic Faces
    const rhombi = [];
    const diagLines = [];

    for (let i = 0; i < 12; i++) {
      for (let j = i + 1; j < 12; j++) {
        const d = vMag(vSub(acuteVerts[i], acuteVerts[j]));
        if (Math.abs(d - 2*s) < 1e-3) {
          const shared = [];
          icoFaces.forEach((f, idx) => {
            if (f.includes(i) && f.includes(j)) shared.push(idx);
          });
          if (shared.length === 2) {
            const vA1 = acuteVerts[i];
            const vA2 = acuteVerts[j];
            const vO1 = obtuseVerts[shared[0]];
            const vO2 = obtuseVerts[shared[1]];

            let quad = [vA1, vO1, vA2, vO2];
            const c = vScale(vAdd(vAdd(vA1, vA2), vAdd(vO1, vO2)), 0.25);
            let norm = vNorm(vCross(vSub(vO1, vA1), vSub(vA2, vA1)));
            if (vDot(norm, c) < 0) {
              quad = [vA1, vO2, vA2, vO1];
              norm = vScale(norm, -1);
            }

            rhombi.push({
              pts: quad,
              centroid: c,
              norm,
              baseColor: solidShading ? [234, 179, 8] : [245, 158, 11],
              opacity: solidShading ? 0.92 : 0.40
            });

            if (showDiagonals) {
              // Long diagonal (Acute to Acute) in radiant gold
              diagLines.push({ pts: [vA1, vA2], color: '#f59e0b', width: 2.0 });
              // Short diagonal (Obtuse to Obtuse) in turquoise/amber
              diagLines.push({ pts: [vO1, vO2], color: '#38bdf8', width: 1.6, dashed: true });
            }
          }
        }
      }
    }

    return { acuteVerts, obtuseVerts, rhombi, diagLines, showDodeca, showIcosa, showDiagonals, solidShading };
  }

  // Scene 5 Helper: Leonardo da Vinci 1509 Vacuum Frame for Square Pyramid (Pyramis Quadrata Vacua)
  function buildPyramidVacuumMesh(H, showBipyramid, mu, frameThickness) {
    const polygons = [];
    const t = frameThickness || 0.12;
    const m = mu || 0.58;

    const C0 = [ 1, 0,  1];
    const C1 = [-1, 0,  1];
    const C2 = [-1, 0, -1];
    const C3 = [ 1, 0, -1];
    const A_top = [0, H, 0];
    const A_bot = [0, -H, 0];

    // Upper pyramid faces
    const upperFaces = [
      { name: 'south', pts: [C1, C0, A_top] },
      { name: 'east',  pts: [C0, C3, A_top] },
      { name: 'north', pts: [C3, C2, A_top] },
      { name: 'west',  pts: [C2, C1, A_top] }
    ];

    if (!showBipyramid) {
      upperFaces.push({ name: 'base', pts: [C0, C1, C2, C3] });
    }

    const cPyrTop = [0, H * 0.25, 0];

    function processFace(facePts, cCenter, isBase) {
      const k = facePts.length;
      const cFace = facePts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / k)), [0, 0, 0]);
      let faceNorm = vNorm(vCross(vSub(facePts[1], facePts[0]), vSub(facePts[2], facePts[0])));
      if (isBase && faceNorm[1] > 0) faceNorm = vScale(faceNorm, -1);

      // Outer aperture vertices
      const wOut = facePts.map(v => vLerp(v, cFace, m));
      // Inner shell vertices (shrunk toward pyramid centroid)
      const vIn = facePts.map(v => vLerp(v, cCenter, t));
      const wIn = wOut.map(w => vLerp(w, cCenter, t));

      for (let i = 0; i < k; i++) {
        const next = (i + 1) % k;

        const outerQuad = [facePts[i], facePts[next], wOut[next], wOut[i]];
        const cOuter = outerQuad.reduce((acc, p) => vAdd(acc, vScale(p, 0.25)), [0, 0, 0]);
        polygons.push({
          pts: outerQuad,
          centroid: cOuter,
          norm: faceNorm,
          baseColor: PAL.frameOuter,
          type: 'frame_outer'
        });

        const innerQuad = [vIn[next], vIn[i], wIn[i], wIn[next]];
        const cInner = innerQuad.reduce((acc, p) => vAdd(acc, vScale(p, 0.25)), [0, 0, 0]);
        polygons.push({
          pts: innerQuad,
          centroid: cInner,
          norm: vScale(faceNorm, -1),
          baseColor: PAL.frameInner,
          type: 'frame_inner'
        });

        const revealQuad = [wOut[i], wOut[next], wIn[next], wIn[i]];
        const cReveal = revealQuad.reduce((acc, p) => vAdd(acc, vScale(p, 0.25)), [0, 0, 0]);
        const revealNorm = vNorm(vCross(vSub(wOut[next], wOut[i]), vSub(wIn[next], wOut[next])));
        polygons.push({
          pts: revealQuad,
          centroid: cReveal,
          norm: revealNorm,
          baseColor: PAL.frameReveal,
          type: 'frame_reveal'
        });
      }
    }

    upperFaces.forEach(f => processFace(f.pts, cPyrTop, f.name === 'base'));

    if (showBipyramid) {
      const cPyrBot = [0, -H * 0.25, 0];
      const lowerFaces = [
        { name: 'south_bot', pts: [C0, C1, A_bot] },
        { name: 'east_bot',  pts: [C3, C0, A_bot] },
        { name: 'north_bot', pts: [C2, C3, A_bot] },
        { name: 'west_bot',  pts: [C1, C2, A_bot] }
      ];
      lowerFaces.forEach(f => processFace(f.pts, cPyrBot, false));
    }

    return polygons;
  }

  // --- Projection & 3D Camera Engine ---
  class Camera3D {
    constructor(preset) {
      this.yaw = preset ? preset.yaw : 0.44;
      this.pitch = preset ? preset.pitch : 0.34;
      this.zoom = preset ? preset.zoom : 1.0;
      this.persp = preset ? preset.persp : 0.30;
      this.target = { yaw: this.yaw, pitch: this.pitch, zoom: this.zoom, persp: this.persp };
    }

    update() {
      this.yaw += (this.target.yaw - this.yaw) * 0.12;
      this.pitch += (this.target.pitch - this.pitch) * 0.12;
      this.zoom += (this.target.zoom - this.zoom) * 0.14;
      this.persp += (this.target.persp - this.persp) * 0.12;
    }

    rotateVec(v) {
      const cy = Math.cos(this.yaw), sy = Math.sin(this.yaw);
      const cp = Math.cos(this.pitch), sp = Math.sin(this.pitch);
      const x1 = v[0] * cy - v[2] * sy;
      const z1 = v[0] * sy + v[2] * cy;
      const y2 = v[1] * cp - z1 * sp;
      const z2 = v[1] * sp + z1 * cp;
      return [x1, y2, z2];
    }

    eyeDirectionFrom(camPt) {
      if (this.persp > 0.01) {
        const zEye = -1.0 / (this.persp * 0.28);
        return vNorm([-camPt[0], -camPt[1], zEye - camPt[2]]);
      }
      return [0, 0, -1];
    }

    classifyFace(worldNorm, worldCentroid) {
      const nCam = this.rotateVec(worldNorm);
      const cCam = this.rotateVec(worldCentroid);
      const toEye = this.eyeDirectionFrom(cCam);
      const isFront = vDot(nCam, toEye) > 0;
      return { nCam, cCam, toEye, isFront };
    }

    project(pt, w, h, baseScale) {
      const [x1, y2, z2] = this.rotateVec(pt);
      const fov = 1.0 / Math.max(0.25, 1.0 + this.persp * z2 * 0.28);
      const s = baseScale * this.zoom * fov;

      return [
        w * 0.5 + x1 * s,
        h * 0.52 - y2 * s,
        z2,
        fov
      ];
    }
  }

  // --- Camera-Locked 3-Point Studio Lighting + Specular + Rim ---
  // In camera space: +X right, +Y up, -Z toward the viewer.
  const STUDIO_KEY  = vNorm([-0.50,  0.62, -0.60]); // Warm upper-left-front key light
  const STUDIO_FILL = vNorm([ 0.64, -0.36, -0.68]); // Cool lower-right-front sculptural fill
  const STUDIO_RIM  = vNorm([ 0.14,  0.86,  0.49]); // Top-back rim separation light

  function shadeStudioFacet(cam, baseRgb, worldNorm, worldCentroid, opacity) {
    const { nCam, toEye, isFront } = cam.classifyFace(worldNorm, worldCentroid);
    const N = isFront ? nCam : vScale(nCam, -1);

    const dKey  = Math.max(0, vDot(N, STUDIO_KEY));
    const dFill = Math.max(0, vDot(N, STUDIO_FILL));
    const dRim  = Math.max(0, vDot(N, STUDIO_RIM));
    const ndotv = Math.max(0, vDot(N, toEye));
    const fresnel = Math.pow(1.0 - ndotv, 2.3);

    const halfVec = vNorm(vAdd(STUDIO_KEY, toEye));
    const spec = isFront ? Math.pow(Math.max(0, vDot(N, halfVec)), 26) : 0.0;

    // Bright, high-clarity diffuse range so shadow facets never turn muddy brown/black
    const diff = isFront
      ? (0.48 + 0.50 * dKey + 0.24 * dFill + 0.12 * dRim)
      : (0.38 + 0.28 * dKey + 0.22 * dFill);

    // Subtle cool sky tint in non-key-lit shadow facets for crisp facet separation
    const coolTint = (1.0 - dKey) * (isFront ? 0.14 : 0.18);
    const sheen = isFront ? (255 * (0.28 * spec + 0.11 * fresnel)) : (255 * 0.04 * fresnel);

    const r = Math.min(255, Math.round(baseRgb[0] * diff * (1 - coolTint) + 150 * coolTint + sheen));
    const g = Math.min(255, Math.round(baseRgb[1] * diff * (1 - coolTint) + 190 * coolTint + sheen * 0.97));
    const b = Math.min(255, Math.round(baseRgb[2] * diff * (1 - coolTint) + 245 * coolTint + sheen * 0.92));

    const alpha = opacity !== undefined ? opacity : 1.0;
    return {
      fill: `rgba(${r},${g},${b},${alpha.toFixed(3)})`,
      isFront
    };
  }

  function drawVertexSphere(ctx, px, py, radius, isFront, isDark, palette = 'gold') {
    ctx.save();
    const alpha = isFront ? 1.0 : 0.45;
    ctx.globalAlpha = alpha;

    let halo = 'rgba(251, 191, 36, 0.22)';
    let mid = '#fde68a';
    let rim = '#d97706';
    if (palette === 'cyan') {
      halo = 'rgba(56, 189, 248, 0.28)';
      mid = '#bae6fd';
      rim = '#0284c7';
    } else if (palette === 'rose') {
      halo = 'rgba(251, 113, 133, 0.32)';
      mid = '#fecdd3';
      rim = '#e11d48';
    }

    // Subtle outer halo on front vertices in dark mode
    if (isFront && isDark) {
      ctx.beginPath();
      ctx.arc(px, py, radius + 2.4, 0, Math.PI * 2);
      ctx.fillStyle = halo;
      ctx.fill();
    }

    // 3D radial gradient sphere
    const grad = ctx.createRadialGradient(
      px - radius * 0.32, py - radius * 0.32, radius * 0.12,
      px, py, radius
    );
    if (isFront) {
      grad.addColorStop(0, '#ffffff');
      grad.addColorStop(0.45, mid);
      grad.addColorStop(1, rim);
    } else {
      grad.addColorStop(0, palette === 'cyan' ? '#bae6fd' : '#cbd5e1');
      grad.addColorStop(1, palette === 'cyan' ? '#0369a1' : '#64748b');
    }

    ctx.beginPath();
    ctx.arc(px, py, radius, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();
    ctx.strokeStyle = isDark ? 'rgba(15, 23, 42, 0.90)' : 'rgba(15, 23, 42, 0.75)';
    ctx.lineWidth = 1.1;
    ctx.stroke();
    ctx.restore();
  }

  function normalizeDisplayMode(raw) {
    const v = (raw || 'wireframe').trim().toLowerCase();
    if (v === 'surfaces' || v === 'surface' || v === 'solid' || v === 'solidum') return 'surfaces';
    if (v === 'frame' || v === 'vacuum') return 'frame';
    return 'wireframe';
  }

  // --- Main Polyhedra 3D Widget Controller ---
  class PolyhedraWidget {
    constructor(container) {
      this.container = container;
      this.solidName = (container.getAttribute('data-solid') || '').trim().toLowerCase();
      this.sceneName = (container.getAttribute('data-scene') || '').trim();
      this.variant = normalizeDisplayMode(
        container.getAttribute('data-mode') || container.getAttribute('data-initial-variant') || 'wireframe'
      );

      const rawOp = parseFloat(container.getAttribute('data-opacity') || '');
      this.surfaceOpacity = !isNaN(rawOp) ? Math.max(0, Math.min(1, rawOp)) : 0.86;
      const rawVerts = (container.getAttribute('data-vertices') || '').trim().toLowerCase();
      this.showVertices = rawVerts === '' ? true : rawVerts !== 'false';

      // State
      this.mu = 0.62;                  // Frame aperture ratio
      this.tau = INV_PHI;              // Octa to Icosa division ratio
      this.shellOpacity = 0.38;        // Icosa shell opacity
      this.showGoldenOverlay = container.getAttribute('data-golden') === 'true';
      this.showDual = container.getAttribute('data-dual') === 'true';
      this.showParentCore = false;     // Parent Core Wireframe for augmented solids
      this.showDiagonals = false;
      this.autoOrbit = true;
      this.activeCubes = [true, true, true, true, true];
      this.showRoofWedge = false;
      this.rtShowDodeca = false;
      this.rtShowIcosa = false;
      this.rtShowDiagonals = true;
      this.rtSolid = false;

      // Great Pyramid & Kepler Scene State
      this.pyramidH = Math.sqrt(PHI);  // Height of pyramid (a = 1.0)
      this.showKeplerTriangle = true;  // Kepler Right Triangle (1 : √φ : φ)
      this.showQuadrature = true;      // Squaring the Circle (2πh = 8)
      this.showCosmogram = false;      // Earth & Moon Cosmogram
      this.pyramidVacuum = false;      // Hollow Frame (genus 4)
      this.showBipyramid = false;      // Reflected Golden Bipyramid

      // Camera presets
      this.presets = {
        perspective: { yaw: 0.46, pitch: 0.34, zoom: 1.0, persp: 0.30 },
        isometric:   { yaw: 0.615, pitch: 0.46, zoom: 1.0, persp: 0.0 },
        front:       { yaw: 0.0, pitch: 0.0, zoom: 1.05, persp: 0.15 },
        top:         { yaw: 0.0, pitch: 1.54, zoom: 1.05, persp: 0.0 }
      };

      this.cam = new Camera3D(this.presets.perspective);

      this.initDOM();
      this.bindEvents();
      this.startLoop();
    }

    initDOM() {
      this.container.classList.add('polyhedra-mounted');

      let title = 'GEOMETOR • 3D Polyhedra Studio';
      let subtitle = 'Drag to orbit • Scroll to zoom • Exact Symbolic Geometry';

      if (this.solidName) {
        const solid = getSolid(this.solidName);
        const cat = getSolidCategory(this.solidName);
        if (cat === 'platonic') {
          title = `REGULAR ${solid.title.toUpperCase()}`;
          subtitle = 'Platonic Regular Polyhedron • Exact Symbolic Geometry';
        } else if (cat === 'archimedean') {
          title = `${solid.title.toUpperCase()}`;
          subtitle = 'Archimedean Semi-Regular Polyhedron • Exact Symbolic Geometry';
        } else if (cat === 'catalan') {
          title = `${solid.title.toUpperCase()}`;
          subtitle = `Catalan Face-Transitive Dual (${solid.dualOf || 'Archimedean'}) • Exact Symbolic Geometry`;
        } else if (cat === 'elevated') {
          title = `${solid.title.toUpperCase()}`;
          subtitle = 'Equilateral Pyramidal Stellation • Exact Symbolic Geometry';
        } else if (cat === 'pyramid') {
          title = `${solid.title.toUpperCase()}`;
          subtitle = 'Canonical Pyramid & Bipyramid Geometry • Exact Symbolic Modeling';
        } else {
          title = solid.title.toUpperCase();
          subtitle = 'Polyhedral Manifold • Exact Symbolic Geometry';
        }
      } else if (this.sceneName === 'icosa_golden_rects') {
        title = 'THREE ORTHOGONAL GOLDEN RECTANGLES (1:φ)';
        subtitle = 'Euclid XIII.16 • 3 Intersecting Rectangles Generating the 12 Vertices of the Regular Icosahedron';
      } else if (this.sceneName === 'octa_to_icosa') {
        title = 'CONTINUOUS MORPHISM • REGULAR OCTAHEDRON TO REGULAR ICOSAHEDRON';
        subtitle = 'Edge Division τ: Midpoint (1/2 → Cuboctahedron) ↔ Golden Section (1/φ → Icosahedron)';
      } else if (this.sceneName === 'dodeca_five_cubes') {
        title = 'EUCLID XIII.17 • ALL FIVE INSCRIBED CUBES IN REGULAR DODECAHEDRON';
        subtitle = '20 Vertices Partitioned into 5 Inscribed Cubes • Face Diagonals Form Cube Edges of Length 2';
      } else if (this.sceneName === 'rhombic_triacontahedron') {
        title = 'KEPLER • RHOMBIC TRIACONTAHEDRON (30 GOLDEN RHOMBI)';
        subtitle = '32 Vertices (20 Dodecahedron + 12 Icosahedron) • Diagonal Ratio Long:Short = φ : 1';
      } else if (this.sceneName === 'great_pyramid_kepler') {
        title = 'KEPLER, SQUARING THE CIRCLE & THE GREAT PYRAMID';
        subtitle = 'Kepler Right Triangle (1 : √φ : φ) • Exact Perimeter Quadrature (2πh = 8) • Earth & Moon Cosmogram';
      }

      this.container.innerHTML = `
        <div class="polyhedra-header">
          <div>
            <div class="polyhedra-title">${title}</div>
            <div class="polyhedra-subtitle">${subtitle}</div>
          </div>
          <div class="polyhedra-presets">
            <button class="polyhedra-btn btn-preset" data-preset="perspective">Perspective</button>
            <button class="polyhedra-btn btn-preset" data-preset="isometric">Isometric</button>
            <button class="polyhedra-btn btn-preset" data-preset="front">Front</button>
            <button class="polyhedra-btn btn-preset" data-preset="top">Top</button>
          </div>
        </div>

        <div class="polyhedra-ctrl-bar">
          <div class="polyhedra-btn-group variant-group"></div>
          <div class="polyhedra-btn-group scene-toggles"></div>
          <div class="polyhedra-slider-wrap"></div>
        </div>

        <div class="polyhedra-telemetry-bar" style="display:none;"></div>

        <div class="polyhedra-canvas-container">
          <canvas class="polyhedra-canvas"></canvas>
        </div>

        <div class="polyhedra-footer">
          <span class="polyhedra-status">Loading exact symbolic model...</span>
          <span class="polyhedra-pill euler-pill">V - E + F = 2</span>
        </div>
      `;

      this.canvas = this.container.querySelector('.polyhedra-canvas');
      this.ctx = this.canvas.getContext('2d');
      this.statusEl = this.container.querySelector('.polyhedra-status');
      this.eulerEl = this.container.querySelector('.euler-pill');
      this.telemetryBar = this.container.querySelector('.polyhedra-telemetry-bar');

      this.populateControls();
    }

    populateControls() {
      const varGroup = this.container.querySelector('.variant-group');
      const togGroup = this.container.querySelector('.scene-toggles');
      const sliderWrap = this.container.querySelector('.polyhedra-slider-wrap');

      varGroup.innerHTML = '';
      togGroup.innerHTML = '';
      sliderWrap.innerHTML = '';

      if (this.solidName) {
        const cat = getSolidCategory(this.solidName);

        // Clean Geometric Display Modes (unified across all 26 solids)
        const modes = [
          ['wireframe', 'Wireframe'],
          ['surfaces',  'Surfaces'],
          ['frame',     'Frame']
        ];

        if (!modes.some(([k]) => k === this.variant)) {
          this.variant = 'wireframe';
        }

        modes.forEach(([mKey, mLabel]) => {
          const btn = document.createElement('button');
          btn.className = `polyhedra-btn ${this.variant === mKey ? 'active' : ''}`;
          btn.textContent = mLabel;
          btn.addEventListener('click', () => {
            this.variant = mKey;
            varGroup.querySelectorAll('.polyhedra-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            this.updateSliderVisibility();
          });
          varGroup.appendChild(btn);
        });

        // 1. Vertex Points Toggle (default ON)
        const togVerts = document.createElement('button');
        togVerts.className = `polyhedra-btn ${this.showVertices ? 'active' : ''}`;
        togVerts.textContent = 'Vertices';
        togVerts.title = 'Show 3D Vertex Points';
        togVerts.addEventListener('click', () => {
          this.showVertices = !this.showVertices;
          togVerts.classList.toggle('active', this.showVertices);
        });
        togGroup.appendChild(togVerts);

        // 2. Face-Center Dual Toggle (vertices at exact centers of the sides — universal on all 26 solids)
        const togDual = document.createElement('button');
        togDual.className = `polyhedra-btn ${this.showDual ? 'active' : ''}`;
        togDual.textContent = 'Dual';
        togDual.title = 'Show Face-Center Dual (Vertices at Centers of the Sides)';
        togDual.addEventListener('click', () => {
          this.showDual = !this.showDual;
          togDual.classList.toggle('active', this.showDual);
        });
        togGroup.appendChild(togDual);

        // 3. Golden Sections & Golden Rectangles Toggle (universal on all 26 solids)
        const togGold = document.createElement('button');
        togGold.className = `polyhedra-btn ${this.showGoldenOverlay ? 'active' : ''}`;
        togGold.textContent = 'Golden φ';
        togGold.title = 'Show Golden Sections (φ:1) & Golden Rectangles (1:φ)';
        togGold.addEventListener('click', () => {
          this.showGoldenOverlay = !this.showGoldenOverlay;
          togGold.classList.toggle('active', this.showGoldenOverlay);
        });
        togGroup.appendChild(togGold);

        // Optional Parent Core toggle on augmented solids
        if (cat === 'elevated') {
          const togCore = document.createElement('button');
          togCore.className = `polyhedra-btn ${this.showParentCore ? 'active' : ''}`;
          togCore.textContent = 'Core';
          togCore.title = 'Show Parent Polyhedron Core Edges';
          togCore.addEventListener('click', () => {
            this.showParentCore = !this.showParentCore;
            togCore.classList.toggle('active', this.showParentCore);
          });
          togGroup.appendChild(togCore);
        }

        const togSpin = document.createElement('button');
        togSpin.className = `polyhedra-btn ${this.autoOrbit ? 'active' : ''}`;
        togSpin.textContent = 'Auto-Spin';
        togSpin.addEventListener('click', () => {
          this.autoOrbit = !this.autoOrbit;
          togSpin.classList.toggle('active', this.autoOrbit);
        });
        togGroup.appendChild(togSpin);

        // Surface Opacity + Frame Aperture Sliders
        sliderWrap.innerHTML = `
          <div class="polyhedra-slider-row surface-opacity-row" style="${this.variant !== 'wireframe' ? 'display:flex;' : 'display:none;'}">
            <span class="polyhedra-label">Opacity:</span>
            <input type="range" class="polyhedra-slider surf-op-slider" min="0" max="100" step="1" value="${Math.round(this.surfaceOpacity * 100)}" />
            <span class="polyhedra-val surf-op-val">${Math.round(this.surfaceOpacity * 100)}%</span>
          </div>
          <div class="polyhedra-slider-row frame-slider-row" style="${this.variant === 'frame' ? 'display:flex;' : 'display:none;'}">
            <span class="polyhedra-label">Aperture:</span>
            <input type="range" class="polyhedra-slider ap-slider" min="0.25" max="0.85" step="0.01" value="${this.mu}" />
            <span class="polyhedra-val ap-val">${this.mu.toFixed(2)}</span>
          </div>
        `;
        const surfOpSlider = sliderWrap.querySelector('.surf-op-slider');
        const surfOpVal = sliderWrap.querySelector('.surf-op-val');
        if (surfOpSlider) {
          surfOpSlider.addEventListener('input', e => {
            this.surfaceOpacity = parseInt(e.target.value, 10) / 100;
            surfOpVal.textContent = `${e.target.value}%`;
          });
        }
        const apSlider = sliderWrap.querySelector('.ap-slider');
        const apVal = sliderWrap.querySelector('.ap-val');
        if (apSlider) {
          apSlider.addEventListener('input', e => {
            this.mu = parseFloat(e.target.value);
            apVal.textContent = this.mu.toFixed(2);
          });
        }
      } else if (this.sceneName === 'icosa_golden_rects') {
        sliderWrap.innerHTML = `
          <div class="polyhedra-slider-row">
            <span class="polyhedra-label">Shell Opacity:</span>
            <input type="range" class="polyhedra-slider opacity-slider" min="0" max="100" step="1" value="${Math.round(this.shellOpacity * 100)}" />
            <span class="polyhedra-val opacity-val">${Math.round(this.shellOpacity * 100)}%</span>
          </div>
        `;
        const opSlider = sliderWrap.querySelector('.opacity-slider');
        const opVal = sliderWrap.querySelector('.opacity-val');
        opSlider.addEventListener('input', e => {
          this.shellOpacity = parseInt(e.target.value, 10) / 100;
          opVal.textContent = `${e.target.value}%`;
        });
      } else if (this.sceneName === 'octa_to_icosa') {
        const btnMid = document.createElement('button');
        btnMid.className = 'polyhedra-btn';
        btnMid.textContent = 'Midpoint (1/2 → Cuboctahedron)';
        btnMid.addEventListener('click', () => {
          this.tau = 0.5;
          const sl = sliderWrap.querySelector('.tau-slider');
          const sv = sliderWrap.querySelector('.tau-val');
          if (sl) sl.value = '0.500';
          if (sv) sv.textContent = '0.500';
        });
        varGroup.appendChild(btnMid);

        const btnGold = document.createElement('button');
        btnGold.className = 'polyhedra-btn active';
        btnGold.textContent = 'Golden Section (1/φ → Icosahedron)';
        btnGold.addEventListener('click', () => {
          this.tau = INV_PHI;
          const sl = sliderWrap.querySelector('.tau-slider');
          const sv = sliderWrap.querySelector('.tau-val');
          if (sl) sl.value = INV_PHI.toFixed(3);
          if (sv) sv.textContent = INV_PHI.toFixed(3);
        });
        varGroup.appendChild(btnGold);

        sliderWrap.innerHTML = `
          <div class="polyhedra-slider-row">
            <span class="polyhedra-label">Edge Division τ:</span>
            <input type="range" class="polyhedra-slider tau-slider" min="0.05" max="0.95" step="0.005" value="${this.tau.toFixed(3)}" />
            <span class="polyhedra-val tau-val">${this.tau.toFixed(3)}</span>
          </div>
        `;
        const tauSlider = sliderWrap.querySelector('.tau-slider');
        const tauVal = sliderWrap.querySelector('.tau-val');
        tauSlider.addEventListener('input', e => {
          this.tau = parseFloat(e.target.value);
          tauVal.textContent = this.tau.toFixed(3);
        });
      } else if (this.sceneName === 'dodeca_five_cubes') {
        PAL.cubeColors.forEach((c, idx) => {
          const btn = document.createElement('button');
          btn.className = `polyhedra-btn active`;
          btn.style.borderColor = c.hex;
          btn.textContent = c.name;
          btn.addEventListener('click', () => {
            this.activeCubes[idx] = !this.activeCubes[idx];
            btn.classList.toggle('active', this.activeCubes[idx]);
          });
          varGroup.appendChild(btn);
        });

        const btnAll = document.createElement('button');
        btnAll.className = 'polyhedra-btn';
        btnAll.textContent = 'Toggle All 5';
        btnAll.addEventListener('click', () => {
          const allActive = this.activeCubes.every(x => x);
          this.activeCubes = this.activeCubes.map(() => !allActive);
          varGroup.querySelectorAll('.polyhedra-btn').forEach((b, i) => {
            if (i < 5) b.classList.toggle('active', this.activeCubes[i]);
          });
        });
        varGroup.appendChild(btnAll);

        const btnRoof = document.createElement('button');
        btnRoof.className = `polyhedra-btn ${this.showRoofWedge ? 'active' : ''}`;
        btnRoof.textContent = 'Roof Wedge (XIII.17)';
        btnRoof.addEventListener('click', () => {
          this.showRoofWedge = !this.showRoofWedge;
          btnRoof.classList.toggle('active', this.showRoofWedge);
        });
        togGroup.appendChild(btnRoof);
      } else if (this.sceneName === 'rhombic_triacontahedron') {
        const btnDodeca = document.createElement('button');
        btnDodeca.className = `polyhedra-btn ${this.rtShowDodeca ? 'active' : ''}`;
        btnDodeca.textContent = 'Dodecahedron (20 Obtuse)';
        btnDodeca.addEventListener('click', () => {
          this.rtShowDodeca = !this.rtShowDodeca;
          btnDodeca.classList.toggle('active', this.rtShowDodeca);
        });
        varGroup.appendChild(btnDodeca);

        const btnIco = document.createElement('button');
        btnIco.className = `polyhedra-btn ${this.rtShowIcosa ? 'active' : ''}`;
        btnIco.textContent = 'Icosahedron (12 Acute)';
        btnIco.addEventListener('click', () => {
          this.rtShowIcosa = !this.rtShowIcosa;
          btnIco.classList.toggle('active', this.rtShowIcosa);
        });
        varGroup.appendChild(btnIco);

        const btnDiag = document.createElement('button');
        btnDiag.className = `polyhedra-btn ${this.rtShowDiagonals ? 'active' : ''}`;
        btnDiag.textContent = 'Diagonals (φ : 1)';
        btnDiag.addEventListener('click', () => {
          this.rtShowDiagonals = !this.rtShowDiagonals;
          btnDiag.classList.toggle('active', this.rtShowDiagonals);
        });
        varGroup.appendChild(btnDiag);

        const btnSolid = document.createElement('button');
        btnSolid.className = `polyhedra-btn ${this.rtSolid ? 'active' : ''}`;
        btnSolid.textContent = 'Opaque / Translucent';
        btnSolid.addEventListener('click', () => {
          this.rtSolid = !this.rtSolid;
          btnSolid.classList.toggle('active', this.rtSolid);
        });
        togGroup.appendChild(btnSolid);
      } else if (this.sceneName === 'great_pyramid_kepler') {
        if (this.telemetryBar) {
          this.telemetryBar.style.display = 'flex';
        }

        const presets = [
          { id: 'kepler', label: 'Kepler φ (h = √φ ≈ 1.2720)', h: Math.sqrt(PHI) },
          { id: 'seked', label: 'Seked 14:11 (Khufu 280/220 ≈ 1.2727)', h: 14 / 11 },
          { id: 'pi_quad', label: 'True π Quadrature (h = 4/π ≈ 1.2732)', h: 4 / Math.PI },
          { id: 'half_octa', label: 'Half-Octahedron (h = √2 ≈ 1.4142)', h: Math.SQRT2 }
        ];

        const presetBtns = [];
        presets.forEach(p => {
          const btn = document.createElement('button');
          btn.className = `polyhedra-btn pyramid-preset-btn ${Math.abs(this.pyramidH - p.h) < 0.001 ? 'active' : ''}`;
          btn.textContent = p.label;
          btn.addEventListener('click', () => {
            this.pyramidH = p.h;
            const sl = sliderWrap.querySelector('.h-slider');
            const sv = sliderWrap.querySelector('.h-val');
            if (sl) sl.value = p.h.toFixed(4);
            if (sv) sv.textContent = p.h.toFixed(4);
            presetBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            this.updatePyramidTelemetry();
          });
          varGroup.appendChild(btn);
          presetBtns.push(btn);
        });

        const btnKepler = document.createElement('button');
        btnKepler.className = `polyhedra-btn ${this.showKeplerTriangle ? 'active' : ''}`;
        btnKepler.textContent = 'Kepler (1, √φ, φ)';
        btnKepler.title = 'Interior Right Triangle from Base Center to East Edge Midpoint to Apex';
        btnKepler.addEventListener('click', () => {
          this.showKeplerTriangle = !this.showKeplerTriangle;
          btnKepler.classList.toggle('active', this.showKeplerTriangle);
        });
        togGroup.appendChild(btnKepler);

        const btnQuad = document.createElement('button');
        btnQuad.className = `polyhedra-btn ${this.showQuadrature ? 'active' : ''}`;
        btnQuad.textContent = 'Squaring the Circle (2πh = 8)';
        btnQuad.title = 'Base Plane & Vertical Meridian Quadrature Circles (Radius = h)';
        btnQuad.addEventListener('click', () => {
          this.showQuadrature = !this.showQuadrature;
          btnQuad.classList.toggle('active', this.showQuadrature);
        });
        togGroup.appendChild(btnQuad);

        const btnCosmo = document.createElement('button');
        btnCosmo.className = `polyhedra-btn ${this.showCosmogram ? 'active' : ''}`;
        btnCosmo.textContent = 'Earth & Moon';
        btnCosmo.title = 'Inscribed Earth Sphere (r=1) and Tangent Moon Sphere (r=h-1)';
        btnCosmo.addEventListener('click', () => {
          this.showCosmogram = !this.showCosmogram;
          btnCosmo.classList.toggle('active', this.showCosmogram);
        });
        togGroup.appendChild(btnCosmo);

        const btnVac = document.createElement('button');
        btnVac.className = `polyhedra-btn ${this.pyramidVacuum ? 'active' : ''}`;
        btnVac.textContent = 'Hollow Frame';
        btnVac.title = 'Beveled Hollow Frame (genus g = 4)';
        btnVac.addEventListener('click', () => {
          this.pyramidVacuum = !this.pyramidVacuum;
          btnVac.classList.toggle('active', this.pyramidVacuum);
        });
        togGroup.appendChild(btnVac);

        const btnBi = document.createElement('button');
        btnBi.className = `polyhedra-btn ${this.showBipyramid ? 'active' : ''}`;
        btnBi.textContent = 'Golden Bipyramid';
        btnBi.title = 'Reflect 4 Lateral Faces Downward to Compare Against Regular Octahedron';
        btnBi.addEventListener('click', () => {
          this.showBipyramid = !this.showBipyramid;
          btnBi.classList.toggle('active', this.showBipyramid);
        });
        togGroup.appendChild(btnBi);

        const btnSpin = document.createElement('button');
        btnSpin.className = `polyhedra-btn ${this.autoOrbit ? 'active' : ''}`;
        btnSpin.textContent = 'Auto-Spin';
        btnSpin.addEventListener('click', () => {
          this.autoOrbit = !this.autoOrbit;
          btnSpin.classList.toggle('active', this.autoOrbit);
        });
        togGroup.appendChild(btnSpin);

        sliderWrap.innerHTML = `
          <div class="polyhedra-slider-row pyramid-slider-row">
            <span class="polyhedra-label">Apex Height (h):</span>
            <input type="range" class="polyhedra-slider h-slider" min="0.75" max="1.60" step="0.001" value="${this.pyramidH.toFixed(4)}" />
            <span class="polyhedra-val h-val">${this.pyramidH.toFixed(4)}</span>
          </div>
        `;
        const hSlider = sliderWrap.querySelector('.h-slider');
        const hVal = sliderWrap.querySelector('.h-val');
        if (hSlider) {
          hSlider.addEventListener('input', e => {
            this.pyramidH = parseFloat(e.target.value);
            if (hVal) hVal.textContent = this.pyramidH.toFixed(4);
            presetBtns.forEach((b, idx) => {
              b.classList.toggle('active', Math.abs(this.pyramidH - presets[idx].h) < 0.001);
            });
            this.updatePyramidTelemetry();
          });
        }

        this.updatePyramidTelemetry();
      }
    }

    updatePyramidTelemetry() {
      if (this.sceneName !== 'great_pyramid_kepler') return;
      const h = this.pyramidH;
      const a = 1.0;
      const s = Math.hypot(a, h);
      const isKepler = Math.abs(h - Math.sqrt(PHI)) < 0.002;
      const isSeked = Math.abs(h - 14 / 11) < 0.002;
      const isPiQuad = Math.abs(h - 4 / Math.PI) < 0.002;
      const isOcta = Math.abs(h - Math.SQRT2) < 0.002;

      // Slope Angle α in degrees, minutes, seconds
      const alphaRad = Math.atan2(h, a);
      const alphaDeg = (alphaRad * 180) / Math.PI;
      const d = Math.floor(alphaDeg);
      const mRem = (alphaDeg - d) * 60;
      const m = Math.floor(mRem);
      const sec = Math.round((mRem - m) * 60);
      const slopeDMS = `${d}° ${m}' ${sec < 10 ? '0' : ''}${sec}"`;

      // Quadrature: Base perimeter = 8.0000, Circle Circumference = 2 * π * h
      const circleCirc = 2 * Math.PI * h;
      const circDiff = Math.abs(circleCirc - 8.0);
      const circErrPct = (circDiff / 8.0) * 100;

      // Face Area: lateral triangle base=2, height=s => Area = s
      // Apex height squared: h^2
      const faceArea = s;
      const hSq = h * h;
      const areaDiff = Math.abs(faceArea - hSq);

      if (this.telemetryBar) {
        this.telemetryBar.innerHTML = `
          <div class="polyhedra-telemetry-item">
            <span class="polyhedra-telemetry-label">h / a:</span>
            <span class="polyhedra-telemetry-val">${h.toFixed(4)}</span>
            <span class="polyhedra-telemetry-label">Slope α:</span>
            <span class="polyhedra-telemetry-val">${slopeDMS} (${alphaDeg.toFixed(3)}°)</span>
          </div>
          <div class="polyhedra-telemetry-item">
            <span class="polyhedra-telemetry-label">Apothem s:</span>
            <span class="polyhedra-telemetry-val ${isKepler ? 'match' : ''}">${s.toFixed(4)}${isKepler ? ' = φ ✨' : ''}</span>
          </div>
          <div class="polyhedra-telemetry-item">
            <span class="polyhedra-telemetry-label">Base P (8.0000) vs 2πh:</span>
            <span class="polyhedra-telemetry-val ${isPiQuad || circErrPct < 0.1 ? 'match' : ''}">${circleCirc.toFixed(4)} (${circErrPct < 0.01 ? '0.00%' : circErrPct.toFixed(2) + '% err'})</span>
          </div>
          <div class="polyhedra-telemetry-item">
            <span class="polyhedra-telemetry-label">Face Area s vs h²:</span>
            <span class="polyhedra-telemetry-val ${isKepler || areaDiff < 0.005 ? 'match' : ''}">${faceArea.toFixed(4)} vs ${hSq.toFixed(4)}${isKepler ? ' (φ = φ ✨)' : ''}</span>
          </div>
        `;
      }

      if (this.eulerEl) {
        if (isKepler) {
          this.eulerEl.textContent = '✨ KEPLER TRIANGLE • a=1, h=√φ, s=φ • 1 + φ = φ² • Face Area = h² = φ';
          this.eulerEl.style.borderColor = '#f59e0b';
        } else if (isSeked) {
          this.eulerEl.textContent = '🏛️ SEKED 14:11 (KHUFU) • Rise 280 / Run 220 • Archimedean π ≈ 22/7 Quadrature';
          this.eulerEl.style.borderColor = '#10b981';
        } else if (isPiQuad) {
          this.eulerEl.textContent = '⭕ TRUE π QUADRATURE • h = 4/π ≈ 1.2732 • Exact 2πh = 8.0000 (Equal Perimeter)';
          this.eulerEl.style.borderColor = '#38bdf8';
        } else if (isOcta) {
          this.eulerEl.textContent = '🔷 HALF-OCTAHEDRON • h = √2 ≈ 1.4142 • Equilateral Lateral Faces (Edge = 2)';
          this.eulerEl.style.borderColor = '#a78bfa';
        } else {
          this.eulerEl.textContent = `Pyramid: h = ${h.toFixed(4)} • Slope = ${alphaDeg.toFixed(2)}° • V = 5, E = 8, F = 5`;
          this.eulerEl.style.borderColor = '';
        }
      }

      if (this.statusEl) {
        if (isKepler) {
          this.statusEl.textContent = 'Kepler (1596): "Geometry has two great treasures: Pythagorean theorem & Golden ratio." Here combined in one!';
        } else if (isSeked) {
          this.statusEl.textContent = 'Rhind Papyrus Seked 5½ palms/cubit gives slope 14/11; circle of radius h has perimeter = 8!';
        } else if (isPiQuad) {
          this.statusEl.textContent = 'Perimeter Squaring of Circle: Vertical height circle circumference 2πh = 8.0000 exactly matches square base!';
        } else if (isOcta) {
          this.statusEl.textContent = 'Half-Octahedron: Equilateral triangular lateral faces of edge 2; golden bipyramid becomes Regular Octahedron!';
        } else {
          this.statusEl.textContent = 'Interactive Great Pyramid & Kepler Proportions • Drag to orbit, scroll to zoom';
        }
      }
    }

    updateSliderVisibility() {
      const opRow = this.container.querySelector('.surface-opacity-row');
      if (opRow) {
        opRow.style.display = this.variant !== 'wireframe' ? 'flex' : 'none';
      }
      const fRow = this.container.querySelector('.frame-slider-row');
      if (fRow) {
        fRow.style.display = this.variant === 'frame' ? 'flex' : 'none';
      }
    }

    bindEvents() {
      // Presets bar
      this.container.querySelectorAll('.btn-preset').forEach(b => {
        b.addEventListener('click', e => {
          const key = e.target.getAttribute('data-preset');
          const p = this.presets[key];
          if (p) {
            this.autoOrbit = false;
            this.cam.target = { ...p };
          }
        });
      });

      // Pointer drag navigation
      let dragging = false;
      let lx = 0, ly = 0;

      this.canvas.addEventListener('pointerdown', e => {
        dragging = true;
        lx = e.clientX;
        ly = e.clientY;
        this.canvas.setPointerCapture(e.pointerId);
      });

      this.canvas.addEventListener('pointermove', e => {
        if (!dragging) return;
        this.autoOrbit = false;
        const dx = e.clientX - lx;
        const dy = e.clientY - ly;
        this.cam.target.yaw += dx * 0.008;
        this.cam.target.pitch = Math.max(-1.54, Math.min(1.54, this.cam.target.pitch + dy * 0.008));
        this.cam.yaw = this.cam.target.yaw;
        this.cam.pitch = this.cam.target.pitch;
        lx = e.clientX;
        ly = e.clientY;
      });

      const stopDrag = () => { dragging = false; };
      this.canvas.addEventListener('pointerup', stopDrag);
      this.canvas.addEventListener('pointercancel', stopDrag);

      // Mouse wheel zoom
      this.canvas.addEventListener('wheel', e => {
        e.preventDefault();
        const factor = e.deltaY < 0 ? 1.09 : 0.91;
        this.cam.target.zoom = Math.max(0.40, Math.min(2.8, this.cam.target.zoom * factor));
      }, { passive: false });

      // Resize observer for crisp high-DPI scaling
      if (window.ResizeObserver) {
        new ResizeObserver(() => this.resizeCanvas()).observe(this.container);
      } else {
        window.addEventListener('resize', () => this.resizeCanvas());
      }
      this.resizeCanvas();
    }

    resizeCanvas() {
      const rect = this.canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      const w = Math.floor(rect.width);
      const h = Math.floor(rect.height || 460);
      if (w > 0 && h > 0) {
        this.canvas.width = w * dpr;
        this.canvas.height = h * dpr;
        this.scaleDpr = dpr;
        this.viewW = w;
        this.viewH = h;
      }
    }

    startLoop() {
      const renderFrame = () => {
        this.cam.update();
        if (this.autoOrbit) {
          this.cam.target.yaw += 0.004;
        }
        this.render();
        requestAnimationFrame(renderFrame);
      };
      requestAnimationFrame(renderFrame);
    }

    isDarkTheme() {
      const attr = document.documentElement.getAttribute('data-theme');
      if (attr === 'light') return false;
      if (attr === 'dark') return true;
      return !window.matchMedia || !window.matchMedia('(prefers-color-scheme: light)').matches;
    }

    render() {
      const ctx = this.ctx;
      const dpr = this.scaleDpr || 1;
      const w = this.viewW || 600;
      const h = this.viewH || 460;

      ctx.save();
      ctx.scale(dpr, dpr);
      ctx.clearRect(0, 0, w, h);

      const isDark = this.isDarkTheme();

      // Subtle radial studio stage backdrop
      const bgGrad = ctx.createRadialGradient(
        w * 0.5, h * 0.48, Math.min(w, h) * 0.04,
        w * 0.5, h * 0.52, Math.max(w, h) * 0.68
      );
      if (isDark) {
        bgGrad.addColorStop(0, '#172236');
        bgGrad.addColorStop(0.58, '#0d1320');
        bgGrad.addColorStop(1, '#080b12');
      } else {
        bgGrad.addColorStop(0, '#ffffff');
        bgGrad.addColorStop(0.65, '#f4f7fb');
        bgGrad.addColorStop(1, '#e8eef5');
      }
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, w, h);

      // Render items queue for depth sorting
      const renderQueue = [];
      const baseScale = Math.min(w, h) * (this.solidName ? 0.215 : 0.35);

      if (this.solidName) {
        this.renderSolid(renderQueue, w, h, baseScale, isDark);
      } else if (this.sceneName === 'icosa_golden_rects') {
        this.renderSceneIcosaGoldenRects(renderQueue, w, h, baseScale, isDark);
      } else if (this.sceneName === 'octa_to_icosa') {
        this.renderSceneOctaToIcosa(renderQueue, w, h, baseScale, isDark);
      } else if (this.sceneName === 'dodeca_five_cubes') {
        this.renderSceneDodecaFiveCubes(renderQueue, w, h, baseScale, isDark);
      } else if (this.sceneName === 'rhombic_triacontahedron') {
        this.renderSceneRhombicTriacontahedron(renderQueue, w, h, baseScale, isDark);
      } else if (this.sceneName === 'great_pyramid_kepler') {
        this.renderSceneGreatPyramidKepler(renderQueue, w, h, baseScale, isDark);
      }

      // Sort by camera depth Z (Painter's algorithm: farthest +Z first, closest -Z last)
      renderQueue.sort((a, b) => b.z - a.z);

      // Draw all items
      renderQueue.forEach(item => item.draw(ctx));

      ctx.restore();
    }

    // --- Scene Renderers ---

    renderSolid(q, w, h, sc, isDark) {
      const base = getSolid(this.solidName);
      const cat = getSolidCategory(this.solidName);
      const { edges } = getEdgesFromFaces(base.faces);

      // Classify front/back status of base faces for depth-cued wireframes & vertex points
      const faceFront = base.faces.map(f => {
        const pts = f.map(idx => base.vertices[idx]);
        const c = pts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / pts.length)), [0, 0, 0]);
        let norm = vNorm(vCross(vSub(pts[1], pts[0]), vSub(pts[2], pts[0])));
        if (vDot(norm, c) < 0) norm = vScale(norm, -1);
        return this.cam.classifyFace(norm, c).isFront;
      });

      const vertFront = new Array(base.vertices.length).fill(false);
      base.faces.forEach((f, fi) => {
        if (faceFront[fi]) {
          f.forEach(vi => { vertFront[vi] = true; });
        }
      });

      const op = this.surfaceOpacity;
      const frontStroke = isDark ? 'rgba(248, 250, 252, 0.76)' : 'rgba(15, 23, 42, 0.74)';
      const backStroke  = isDark ? 'rgba(148, 163, 184, 0.28)' : 'rgba(71, 85, 105, 0.26)';

      if (this.variant === 'surfaces') {
        const mesh = buildSolidumMesh(base);
        this.eulerEl.textContent = `V = ${mesh.V} • E = ${mesh.E} • F = ${mesh.F} • χ = 2`;
        this.statusEl.textContent = `${base.title} • Surface Opacity ${Math.round(op * 100)}%${this.showVertices ? ' • Vertex Points' : ''}`;

        mesh.polygons.forEach(p => {
          const projPts = p.pts.map(v => this.cam.project(v, w, h, sc));
          const pCentroid = this.cam.project(p.centroid, w, h, sc);

          const faceAlpha = op >= 0.995 ? 1.0 : op;
          const shaded = shadeStudioFacet(
            this.cam,
            p.baseColor,
            p.norm,
            p.centroid,
            faceAlpha
          );

          // Skip invisible backfaces when 100% opaque on convex solids
          if (op >= 0.995 && !shaded.isFront && cat !== 'elevated') {
            return;
          }

          const effectiveFillAlpha = shaded.isFront ? faceAlpha : (faceAlpha * 0.50);
          const rearShaded = !shaded.isFront
            ? shadeStudioFacet(this.cam, p.baseColor, p.norm, p.centroid, effectiveFillAlpha)
            : shaded;

          q.push({
            z: pCentroid[2] + (shaded.isFront ? 0 : 0.02),
            draw: ctx => {
              ctx.save();
              ctx.lineJoin = 'round';
              ctx.lineCap = 'round';
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              if (effectiveFillAlpha > 0.005) {
                ctx.fillStyle = rearShaded.fill;
                ctx.fill();
              }
              ctx.strokeStyle = shaded.isFront ? frontStroke : backStroke;
              ctx.lineWidth = shaded.isFront ? 1.35 : 0.95;
              ctx.stroke();
              ctx.restore();
            }
          });
        });
      } else if (this.variant === 'wireframe') {
        const V = base.vertices.length;
        const E = edges.length;
        const F = base.faces.length;
        this.eulerEl.textContent = `V = ${V} • E = ${E} • F = ${F} • χ = 2`;
        this.statusEl.textContent = `${base.title} • Depth-Cued 3D Wireframe (${E} Edges)${this.showVertices ? ' • Vertex Points' : ''}`;

        const wireRgb = base.color || [96, 165, 250];
        const frontWireHex = isDark
          ? `rgba(${Math.min(255, wireRgb[0] + 35)}, ${Math.min(255, wireRgb[1] + 35)}, ${Math.min(255, wireRgb[2] + 35)}, 0.96)`
          : `rgba(${Math.round(wireRgb[0] * 0.72)}, ${Math.round(wireRgb[1] * 0.72)}, ${Math.round(wireRgb[2] * 0.72)}, 0.95)`;
        const backWireCol = isDark ? 'rgba(148, 163, 184, 0.32)' : 'rgba(100, 116, 139, 0.34)';

        edges.forEach(e => {
          const p1 = this.cam.project(base.vertices[e.a], w, h, sc);
          const p2 = this.cam.project(base.vertices[e.b], w, h, sc);
          const isFrontEdge = e.faces.some(fi => faceFront[fi]);
          const midZ = (p1[2] + p2[2]) * 0.5;

          q.push({
            z: midZ + (isFrontEdge ? -0.01 : 0.02),
            draw: ctx => {
              ctx.save();
              ctx.lineCap = 'round';
              ctx.beginPath();
              if (!isFrontEdge) {
                ctx.setLineDash([4, 4]);
              } else if (isDark) {
                ctx.shadowColor = frontWireHex;
                ctx.shadowBlur = 5;
              }
              ctx.moveTo(p1[0], p1[1]);
              ctx.lineTo(p2[0], p2[1]);
              ctx.strokeStyle = isFrontEdge ? frontWireHex : backWireCol;
              ctx.lineWidth = isFrontEdge ? 2.15 : 1.15;
              ctx.stroke();
              ctx.restore();
            }
          });
        });
      } else if (this.variant === 'frame') {
        const mesh = buildVacuumMesh(base, this.mu);
        this.eulerEl.textContent = `V = ${mesh.V_vac} • E = ${mesh.E_vac} • F = ${mesh.F_vac} • genus g = ${mesh.genus}`;
        this.statusEl.textContent = `${base.title} • Beveled Hollow Frame (Aperture ${this.mu.toFixed(2)} • Opacity ${Math.round(op * 100)}%)`;

        const frameStrokeFront = isDark ? 'rgba(15, 23, 42, 0.72)' : 'rgba(15, 23, 42, 0.65)';
        const frameStrokeBack  = isDark ? 'rgba(148, 163, 184, 0.20)' : 'rgba(100, 116, 139, 0.20)';

        mesh.polygons.forEach(p => {
          const projPts = p.pts.map(v => this.cam.project(v, w, h, sc));
          const pCentroid = this.cam.project(p.centroid, w, h, sc);
          const shaded = shadeStudioFacet(this.cam, p.baseColor, p.norm, p.centroid, op);

          // Cull interior solid-wall backfaces when nearly opaque so hollow bevels stay razor-clean
          if (op > 0.92 && !shaded.isFront) {
            return;
          }

          const alpha = shaded.isFront ? op : op * 0.38;
          const finalShade = shaded.isFront
            ? shaded
            : shadeStudioFacet(this.cam, p.baseColor, p.norm, p.centroid, alpha);

          q.push({
            z: pCentroid[2],
            draw: ctx => {
              ctx.save();
              ctx.lineJoin = 'round';
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              if (alpha > 0.005) {
                ctx.fillStyle = finalShade.fill;
                ctx.fill();
              }
              ctx.strokeStyle = shaded.isFront ? frameStrokeFront : frameStrokeBack;
              ctx.lineWidth = shaded.isFront ? 0.95 : 0.65;
              ctx.stroke();
              ctx.restore();
            }
          });
        });
      }

      // 3D Vertex Points Option (depth-interleaved sphere nodes)
      if (this.showVertices) {
        const vCount = base.vertices.length;
        const baseRad = vCount > 45 ? 3.3 : (vCount > 20 ? 4.0 : 4.7);
        base.vertices.forEach((v, vIdx) => {
          const proj = this.cam.project(v, w, h, sc);
          const isFrontV = vertFront[vIdx];
          // Hide occluded back vertices only when Surfaces mode is completely opaque
          if (this.variant === 'surfaces' && op >= 0.98 && !isFrontV && cat !== 'elevated') {
            return;
          }
          const r = baseRad * Math.max(0.75, Math.min(1.25, proj[3] || 1.0)) * (isFrontV ? 1.0 : 0.80);
          q.push({
            z: proj[2] - (isFrontV ? 0.045 : 0.01),
            draw: ctx => drawVertexSphere(ctx, proj[0], proj[1], r, isFrontV, isDark)
          });
        });
      }

      // Universal Golden Sections (φ:1) & Golden Rectangles (1:φ)
      if (this.showGoldenOverlay) {
        const overlay = buildGoldenOverlay(this.solidName, base);

        // 1. 1:φ Golden Rectangles
        overlay.rects.forEach(r => {
          const projPts = r.pts.map(v => this.cam.project(v, w, h, sc));
          const avgZ = projPts.reduce((acc, pt) => acc + pt[2], 0) / projPts.length;
          q.push({
            z: avgZ - 0.02,
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = r.fill;
              ctx.fill();
              ctx.strokeStyle = r.stroke;
              ctx.lineWidth = 2.1;
              ctx.stroke();
            }
          });
        });

        // 2. Auxiliary Polygons (e.g. Kepler Meridian)
        overlay.pols.forEach(p => {
          const projPts = p.pts.map(v => this.cam.project(v, w, h, sc));
          const avgZ = projPts.reduce((acc, pt) => acc + pt[2], 0) / projPts.length;
          q.push({
            z: avgZ - 0.03,
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = p.color;
              ctx.fill();
              ctx.strokeStyle = p.stroke;
              ctx.lineWidth = p.width || 1.8;
              ctx.stroke();
            }
          });
        });

        // 3. 3D Circles (e.g. Odom Face Circumcircle)
        overlay.circles.forEach(c => {
          const steps = 64;
          const pts2d = [];
          let sumZ = 0;
          for (let i = 0; i <= steps; i++) {
            const ang = (i / steps) * Math.PI * 2;
            const p3 = vAdd(
              c.center,
              vAdd(vScale(c.u, Math.cos(ang) * c.r), vScale(c.v, Math.sin(ang) * c.r))
            );
            const pr = this.cam.project(p3, w, h, sc);
            pts2d.push(pr);
            sumZ += pr[2];
          }
          q.push({
            z: (sumZ / (steps + 1)) - 0.04,
            draw: ctx => {
              ctx.beginPath();
              pts2d.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.strokeStyle = c.color || 'rgba(56, 189, 248, 0.72)';
              ctx.lineWidth = 1.8;
              ctx.stroke();
            }
          });
        });

        // 4. Auxiliary Reference Lines
        overlay.lines.forEach(l => {
          const p1 = this.cam.project(l.pts[0], w, h, sc);
          const p2 = this.cam.project(l.pts[1], w, h, sc);
          q.push({
            z: (p1[2] + p2[2]) * 0.5 - 0.05,
            draw: ctx => {
              ctx.beginPath();
              if (l.dashed) ctx.setLineDash([5, 4]);
              ctx.moveTo(p1[0], p1[1]);
              ctx.lineTo(p2[0], p2[1]);
              ctx.strokeStyle = l.color;
              ctx.lineWidth = l.width || 1.6;
              ctx.stroke();
              if (l.dashed) ctx.setLineDash([]);
            }
          });
        });

        // 5. Exact φ:1 Golden Sections (Gold major a->g + Coral-Rose minor g->b + Rose-Gold pearl at g)
        overlay.sections.forEach(sec => {
          const pA = this.cam.project(sec.a, w, h, sc);
          const pG = this.cam.project(sec.g, w, h, sc);
          const pB = this.cam.project(sec.b, w, h, sc);

          q.push({
            z: (pA[2] + pG[2]) * 0.5 - 0.065,
            draw: ctx => {
              ctx.beginPath();
              ctx.moveTo(pA[0], pA[1]);
              ctx.lineTo(pG[0], pG[1]);
              ctx.strokeStyle = isDark ? '#fde047' : '#d97706';
              ctx.lineWidth = 3.2;
              ctx.lineCap = 'round';
              ctx.stroke();
            }
          });

          q.push({
            z: (pG[2] + pB[2]) * 0.5 - 0.065,
            draw: ctx => {
              ctx.beginPath();
              ctx.moveTo(pG[0], pG[1]);
              ctx.lineTo(pB[0], pB[1]);
              ctx.strokeStyle = isDark ? '#fb7185' : '#e11d48';
              ctx.lineWidth = 3.2;
              ctx.lineCap = 'round';
              ctx.stroke();
            }
          });

          const rG = 4.6 * Math.max(0.8, Math.min(1.2, pG[3] || 1.0));
          q.push({
            z: pG[2] - 0.08,
            draw: ctx => drawVertexSphere(ctx, pG[0], pG[1], rG, true, isDark, 'rose')
          });
        });

        overlay.labels.forEach(lb => {
          const p = this.cam.project(lb.pos, w, h, sc);
          q.push({
            z: p[2] - 0.12,
            draw: ctx => {
              ctx.font = '700 12px sans-serif';
              ctx.textAlign = 'center';
              ctx.fillStyle = lb.color || '#fbbf24';
              ctx.fillText(lb.text, p[0], p[1]);
            }
          });
        });
      }

      // Universal Face-Center Dual (vertices are exact centers of the sides; Tetrahedron -> Tetrahedron)
      if (this.showDual) {
        const dual = buildFaceCenterDual(base);
        const dualFrontCol = isDark ? 'rgba(56, 189, 248, 0.94)' : 'rgba(2, 132, 199, 0.92)';
        const dualBackCol = isDark ? 'rgba(56, 189, 248, 0.35)' : 'rgba(2, 132, 199, 0.32)';

        dual.edges.forEach(([f0, f1]) => {
          const p1 = this.cam.project(dual.vertices[f0], w, h, sc);
          const p2 = this.cam.project(dual.vertices[f1], w, h, sc);
          const isFrontDualEdge = faceFront[f0] || faceFront[f1];
          q.push({
            z: (p1[2] + p2[2]) * 0.5 - (isFrontDualEdge ? 0.03 : 0.0),
            draw: ctx => {
              ctx.beginPath();
              if (!isFrontDualEdge) ctx.setLineDash([4, 4]);
              ctx.moveTo(p1[0], p1[1]);
              ctx.lineTo(p2[0], p2[1]);
              ctx.strokeStyle = isFrontDualEdge ? dualFrontCol : dualBackCol;
              ctx.lineWidth = isFrontDualEdge ? 2.2 : 1.25;
              ctx.lineCap = 'round';
              ctx.stroke();
              if (!isFrontDualEdge) ctx.setLineDash([]);
            }
          });
        });

        const dualBaseRad = dual.vertices.length > 32 ? 3.6 : (dual.vertices.length > 16 ? 4.3 : 5.1);
        dual.vertices.forEach((dv, fi) => {
          const proj = this.cam.project(dv, w, h, sc);
          const isFrontD = faceFront[fi];
          const r = dualBaseRad * Math.max(0.75, Math.min(1.25, proj[3] || 1.0)) * (isFrontD ? 1.0 : 0.80);
          q.push({
            z: proj[2] - (isFrontD ? 0.038 : 0.008),
            draw: ctx => drawVertexSphere(ctx, proj[0], proj[1], r, isFrontD, isDark, 'cyan')
          });
        });
      }

      // Parent core wireframe (for augmented solids)
      if (this.showParentCore && cat === 'elevated' && base.parentSolid) {
        const coreLines = getParentCoreWireframe(base);
        coreLines.forEach(l => {
          const p1 = this.cam.project(l.pts[0], w, h, sc);
          const p2 = this.cam.project(l.pts[1], w, h, sc);
          q.push({
            z: (p1[2] + p2[2]) * 0.5 - 0.06,
            draw: ctx => {
              ctx.beginPath();
              ctx.moveTo(p1[0], p1[1]);
              ctx.lineTo(p2[0], p2[1]);
              ctx.strokeStyle = l.color;
              ctx.lineWidth = l.width;
              ctx.stroke();
            }
          });
        });
      }
    }

    renderPlatonicSolid(q, w, h, sc, isDark) {
      this.renderSolid(q, w, h, sc, isDark);
    }

    renderSceneIcosaGoldenRects(q, w, h, sc, isDark) {
      const data = buildSceneIcosaGoldenRects(this.shellOpacity);
      this.eulerEl.textContent = 'V = 12 • 3 Golden Rectangles • Ratio = 1 : φ';
      this.statusEl.textContent = `Three Orthogonal Golden Rectangles (1:φ) inside Regular Icosahedron (Shell Opacity: ${Math.round(this.shellOpacity * 100)}%)`;

      data.rects.forEach(r => {
        const projPts = r.pts.map(v => this.cam.project(v, w, h, sc));
        const avgZ = projPts.reduce((acc, pt) => acc + pt[2], 0) / projPts.length;

        q.push({
          z: avgZ - 0.05,
          draw: ctx => {
            ctx.beginPath();
            projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
            ctx.closePath();
            ctx.fillStyle = r.fill;
            ctx.fill();
            ctx.strokeStyle = r.stroke;
            ctx.lineWidth = 2.4;
            ctx.stroke();
          }
        });

        const midShort = vScale(vAdd(r.pts[0], r.pts[1]), 0.5);
        const midLong = vScale(vAdd(r.pts[1], r.pts[2]), 0.5);
        const pShort = this.cam.project(midShort, w, h, sc);
        const pLong = this.cam.project(midLong, w, h, sc);

        q.push({
          z: pShort[2] - 0.1,
          draw: ctx => {
            ctx.font = '600 11px sans-serif';
            ctx.fillStyle = r.color;
            ctx.fillText('2', pShort[0], pShort[1]);
          }
        });
        q.push({
          z: pLong[2] - 0.1,
          draw: ctx => {
            ctx.font = '600 11px sans-serif';
            ctx.fillStyle = r.color;
            ctx.fillText('2φ', pLong[0], pLong[1]);
          }
        });
      });

      if (this.shellOpacity > 0.01) {
        data.icoMesh.polygons.forEach(p => {
          const projPts = p.pts.map(v => this.cam.project(v, w, h, sc));
          const pCentroid = this.cam.project(p.centroid, w, h, sc);
          const shaded = shadeStudioFacet(this.cam, [96, 165, 250], p.norm, p.centroid, this.shellOpacity);

          q.push({
            z: pCentroid[2] + 0.05,
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = shaded.fill;
              ctx.fill();
              ctx.strokeStyle = `rgba(125, 211, 252, ${Math.min(0.95, this.shellOpacity * 1.6)})`;
              ctx.lineWidth = 1.25;
              ctx.stroke();
            }
          });
        });
      }
    }

    renderSceneOctaToIcosa(q, w, h, sc, isDark) {
      const data = buildSceneOctaToIcosa(this.tau);
      const isGolden = Math.abs(this.tau - INV_PHI) < 0.015;
      const isMid = Math.abs(this.tau - 0.5) < 0.015;

      if (isGolden) {
        this.eulerEl.textContent = `GOLDEN SECTION • τ = ${INV_PHI.toFixed(4)} (1/φ)`;
        this.eulerEl.style.borderColor = '#f59e0b';
        this.statusEl.textContent = '12 Edge Points Form an Exact Regular Icosahedron (20 Congruent Equilateral Triangles)';
      } else if (isMid) {
        this.eulerEl.textContent = 'MIDPOINT DIVISION • τ = 0.500 (Cuboctahedron)';
        this.statusEl.textContent = '8 Triangles + 6 Squares form Archimedean Cuboctahedron';
      } else {
        this.eulerEl.textContent = `τ = ${this.tau.toFixed(3)} • Morphing Polyhedron`;
        this.statusEl.textContent = 'Continuous Morphism between Regular Octahedron and Regular Icosahedron';
      }

      data.octaEdges.forEach(([a, b]) => {
        const p1 = this.cam.project(data.ox[a], w, h, sc);
        const p2 = this.cam.project(data.ox[b], w, h, sc);
        q.push({
          z: (p1[2] + p2[2]) * 0.5 + 0.1,
          draw: ctx => {
            ctx.beginPath();
            ctx.setLineDash([4, 4]);
            ctx.moveTo(p1[0], p1[1]);
            ctx.lineTo(p2[0], p2[1]);
            ctx.strokeStyle = 'rgba(148, 163, 184, 0.45)';
            ctx.lineWidth = 1.3;
            ctx.stroke();
            ctx.setLineDash([]);
          }
        });
      });

      data.triangles.forEach(t => {
        const projPts = t.pts.map(v => this.cam.project(v, w, h, sc));
        const pCentroid = this.cam.project(t.centroid, w, h, sc);
        const shaded = shadeStudioFacet(this.cam, t.baseColor, t.norm, t.centroid, isGolden ? 0.88 : 0.72);

        q.push({
          z: pCentroid[2],
          draw: ctx => {
            ctx.beginPath();
            projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
            ctx.closePath();
            ctx.fillStyle = shaded.fill;
            ctx.fill();
            ctx.strokeStyle = isGolden ? 'rgba(254, 243, 199, 0.85)' : (isDark ? 'rgba(226, 232, 240, 0.65)' : 'rgba(15, 23, 42, 0.65)');
            ctx.lineWidth = isGolden ? 1.5 : 1.15;
            ctx.stroke();
          }
        });
      });

      data.pts.forEach(p => {
        const proj = this.cam.project(p, w, h, sc);
        q.push({
          z: proj[2] - 0.08,
          draw: ctx => drawVertexSphere(ctx, proj[0], proj[1], isGolden ? 4.8 : 3.8, true, isDark)
        });
      });
    }

    renderSceneDodecaFiveCubes(q, w, h, sc, isDark) {
      const data = buildSceneDodecaFiveCubes(this.activeCubes, this.showRoofWedge);
      const activeCount = this.activeCubes.filter(x => x).length;
      this.eulerEl.textContent = `Euclid XIII.17 • ${activeCount} Active Cubes • V = 20`;
      this.statusEl.textContent = 'Each Cube Edge of Length 2 is a Pentagonal Diagonal (φ × 2φ⁻¹) of the Dodecahedron';

      data.dodecaEdges.forEach(e => {
        const p1 = this.cam.project(data.vertices[e.a], w, h, sc);
        const p2 = this.cam.project(data.vertices[e.b], w, h, sc);
        q.push({
          z: (p1[2] + p2[2]) * 0.5 + 0.15,
          draw: ctx => {
            ctx.beginPath();
            ctx.moveTo(p1[0], p1[1]);
            ctx.lineTo(p2[0], p2[1]);
            ctx.strokeStyle = isDark ? 'rgba(148, 163, 184, 0.34)' : 'rgba(100, 116, 139, 0.36)';
            ctx.lineWidth = 1.25;
            ctx.stroke();
          }
        });
      });

      data.cubes.forEach(cube => {
        if (!cube.active) return;
        cube.edges.forEach(([a, b]) => {
          const p1 = this.cam.project(data.vertices[a], w, h, sc);
          const p2 = this.cam.project(data.vertices[b], w, h, sc);
          q.push({
            z: (p1[2] + p2[2]) * 0.5,
            draw: ctx => {
              ctx.beginPath();
              ctx.moveTo(p1[0], p1[1]);
              ctx.lineTo(p2[0], p2[1]);
              ctx.strokeStyle = cube.colorInfo.hex;
              ctx.lineWidth = 2.4;
              ctx.stroke();
            }
          });
        });
      });

      if (data.showRoofWedge) {
        data.roof.forEach(rf => {
          const projPts = rf.pts.map(v => this.cam.project(v, w, h, sc));
          const avgZ = projPts.reduce((acc, pt) => acc + pt[2], 0) / projPts.length;
          q.push({
            z: avgZ - 0.05,
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = rf.fill;
              ctx.fill();
              ctx.strokeStyle = rf.stroke;
              ctx.lineWidth = 2.0;
              ctx.stroke();
            }
          });
        });
      }
    }

    renderSceneRhombicTriacontahedron(q, w, h, sc, isDark) {
      const data = buildSceneRhombicTriacontahedron(this.rtShowDodeca, this.rtShowIcosa, this.rtShowDiagonals, this.rtSolid);
      this.eulerEl.textContent = 'V = 32 • E = 60 • F = 30 • χ = 2';
      this.statusEl.textContent = 'Kepler 1611 • 30 Golden Rhombi with Long:Short Diagonal Ratio = φ (1.618034)';

      const edgeCol = isDark ? 'rgba(248, 250, 252, 0.72)' : 'rgba(15, 23, 42, 0.72)';

      data.rhombi.forEach(r => {
        const projPts = r.pts.map(v => this.cam.project(v, w, h, sc));
        const pCentroid = this.cam.project(r.centroid, w, h, sc);
        const shaded = shadeStudioFacet(this.cam, [251, 191, 36], r.norm, r.centroid, r.opacity);

        q.push({
          z: pCentroid[2],
          draw: ctx => {
            ctx.beginPath();
            projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
            ctx.closePath();
            ctx.fillStyle = shaded.fill;
            ctx.fill();
            ctx.strokeStyle = shaded.isFront ? edgeCol : 'rgba(148, 163, 184, 0.25)';
            ctx.lineWidth = shaded.isFront ? 1.25 : 0.9;
            ctx.stroke();
          }
        });
      });

      if (this.rtShowDiagonals) {
        data.diagLines.forEach(l => {
          const p1 = this.cam.project(l.pts[0], w, h, sc);
          const p2 = this.cam.project(l.pts[1], w, h, sc);
          q.push({
            z: (p1[2] + p2[2]) * 0.5 - 0.05,
            draw: ctx => {
              ctx.beginPath();
              if (l.dashed) ctx.setLineDash([4, 4]);
              ctx.moveTo(p1[0], p1[1]);
              ctx.lineTo(p2[0], p2[1]);
              ctx.strokeStyle = l.color;
              ctx.lineWidth = l.width;
              ctx.stroke();
              if (l.dashed) ctx.setLineDash([]);
            }
          });
        });
      }

      if (this.rtShowDodeca) {
        data.obtuseVerts.forEach(v => {
          const p = this.cam.project(v, w, h, sc);
          q.push({
            z: p[2] - 0.08,
            draw: ctx => {
              ctx.beginPath();
              ctx.arc(p[0], p[1], 4.5, 0, Math.PI * 2);
              ctx.fillStyle = '#34d399';
              ctx.fill();
              ctx.strokeStyle = '#ffffff';
              ctx.lineWidth = 1.2;
              ctx.stroke();
            }
          });
        });
      }

      if (this.rtShowIcosa) {
        data.acuteVerts.forEach(v => {
          const p = this.cam.project(v, w, h, sc);
          q.push({
            z: p[2] - 0.08,
            draw: ctx => {
              ctx.beginPath();
              ctx.arc(p[0], p[1], 4.5, 0, Math.PI * 2);
              ctx.fillStyle = '#38bdf8';
              ctx.fill();
              ctx.strokeStyle = '#ffffff';
              ctx.lineWidth = 1.2;
              ctx.stroke();
            }
          });
        });
      }
    }

    renderSceneGreatPyramidKepler(q, w, h, sc, isDark) {
      const H = this.pyramidH;
      const a = 1.0;
      const s = Math.hypot(a, H);
      const isKepler = Math.abs(H - Math.sqrt(PHI)) < 0.01;
      const yOffset = this.showBipyramid ? 0 : -0.42;

      const pr = pt => this.cam.project([pt[0], pt[1] + yOffset, pt[2]], w, h, sc);

      const C0 = [ 1, 0,  1];
      const C1 = [-1, 0,  1];
      const C2 = [-1, 0, -1];
      const C3 = [ 1, 0, -1];
      const O  = [ 0, 0,  0];
      const A_top = [0,  H, 0];
      const A_bot = [0, -H, 0];

      function addLine3D(p1_3d, p2_3d, strokeStyle, lineWidth, isDashed, extraZ) {
        const p1 = pr(p1_3d);
        const p2 = pr(p2_3d);
        const avgZ = (p1[2] + p2[2]) * 0.5 + (extraZ || 0);
        q.push({
          z: avgZ,
          draw: ctx => {
            ctx.save();
            ctx.beginPath();
            if (isDashed) ctx.setLineDash([4, 4]);
            ctx.moveTo(p1[0], p1[1]);
            ctx.lineTo(p2[0], p2[1]);
            ctx.strokeStyle = strokeStyle;
            ctx.lineWidth = lineWidth || 1.5;
            ctx.stroke();
            ctx.restore();
          }
        });
      }

      function addCircle3D(center, normal, radius, strokeStyle, lineWidth, isDashed, fillStyle, extraZ) {
        const segs = 64;
        let u, v;
        if (Math.abs(normal[1]) > 0.9) {
          u = [1, 0, 0];
        } else {
          u = vNorm(vCross([0, 1, 0], normal));
        }
        v = vNorm(vCross(normal, u));

        const pts = [];
        for (let i = 0; i <= segs; i++) {
          const theta = (i / segs) * Math.PI * 2;
          const cos = Math.cos(theta);
          const sin = Math.sin(theta);
          const pt = [
            center[0] + radius * (u[0] * cos + v[0] * sin),
            center[1] + radius * (u[1] * cos + v[1] * sin),
            center[2] + radius * (u[2] * cos + v[2] * sin)
          ];
          pts.push(pr(pt));
        }

        const avgZ = pts.reduce((acc, p) => acc + p[2], 0) / pts.length + (extraZ || 0);

        q.push({
          z: avgZ,
          draw: ctx => {
            ctx.save();
            ctx.beginPath();
            pts.forEach((p, i) => i === 0 ? ctx.moveTo(p[0], p[1]) : ctx.lineTo(p[0], p[1]));
            ctx.closePath();
            if (fillStyle) {
              ctx.fillStyle = fillStyle;
              ctx.fill();
            }
            if (strokeStyle) {
              if (isDashed) ctx.setLineDash([4, 4]);
              ctx.strokeStyle = strokeStyle;
              ctx.lineWidth = lineWidth || 1.5;
              ctx.stroke();
            }
            ctx.restore();
          }
        });
      }

      function addPointMarker3D(pt3d, radius, fillStyle, strokeStyle, extraZ) {
        const p = pr(pt3d);
        q.push({
          z: p[2] - 0.08 + (extraZ || 0),
          draw: ctx => {
            ctx.save();
            ctx.beginPath();
            ctx.arc(p[0], p[1], radius || 3.5, 0, Math.PI * 2);
            ctx.fillStyle = fillStyle || '#f59e0b';
            ctx.fill();
            if (strokeStyle) {
              ctx.strokeStyle = strokeStyle;
              ctx.lineWidth = 1.2;
              ctx.stroke();
            }
            ctx.restore();
          }
        });
      }

      function addCallout3D(pt3d, text, color, isHighlight, extraZ) {
        const p = pr(pt3d);
        q.push({
          z: p[2] - 0.12 + (extraZ || 0),
          draw: ctx => {
            ctx.save();
            ctx.font = isHighlight ? '700 12px ui-monospace, sans-serif' : '600 11px ui-monospace, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.strokeStyle = 'rgba(13, 17, 23, 0.88)';
            ctx.lineWidth = 3.2;
            ctx.strokeText(text, p[0], p[1]);
            ctx.fillStyle = color;
            ctx.fillText(text, p[0], p[1]);
            ctx.restore();
          }
        });
      }

      addLine3D(C0, C1, 'rgba(180, 160, 130, 0.45)', 1.2, true, 0.05);
      addLine3D(C1, C2, 'rgba(180, 160, 130, 0.45)', 1.2, true, 0.05);
      addLine3D(C2, C3, 'rgba(180, 160, 130, 0.45)', 1.2, true, 0.05);
      addLine3D(C3, C0, 'rgba(180, 160, 130, 0.45)', 1.2, true, 0.05);
      addLine3D([-1.4, 0, 0], [1.4, 0, 0], 'rgba(148, 163, 184, 0.28)', 1.0, true, 0.06);
      addLine3D([0, 0, -1.4], [0, 0, 1.4], 'rgba(148, 163, 184, 0.28)', 1.0, true, 0.06);

      if (this.pyramidVacuum) {
        const vacPolys = buildPyramidVacuumMesh(H, this.showBipyramid, this.mu, 0.12);
        vacPolys.forEach(poly => {
          const projPts = poly.pts.map(pr);
          const pC = pr(poly.centroid);
          const shiftedC = [poly.centroid[0], poly.centroid[1] + yOffset, poly.centroid[2]];
          const shaded = shadeStudioFacet(this.cam, poly.baseColor, poly.norm, shiftedC, 0.94);

          q.push({
            z: pC[2],
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = shaded.fill;
              ctx.fill();
              ctx.strokeStyle = isDark ? 'rgba(15, 23, 42, 0.70)' : 'rgba(15, 23, 42, 0.55)';
              ctx.lineWidth = 0.95;
              ctx.stroke();
            }
          });
        });
      } else {
        const faces = [
          { name: 'south', pts: [C1, C0, A_top] },
          { name: 'east',  pts: [C0, C3, A_top] },
          { name: 'north', pts: [C3, C2, A_top] },
          { name: 'west',  pts: [C2, C1, A_top] }
        ];

        if (!this.showBipyramid) {
          faces.push({ name: 'base', pts: [C0, C1, C2, C3] });
        } else {
          faces.push(
            { name: 'south_bot', pts: [C0, C1, A_bot] },
            { name: 'east_bot',  pts: [C3, C0, A_bot] },
            { name: 'north_bot', pts: [C2, C3, A_bot] },
            { name: 'west_bot',  pts: [C1, C2, A_bot] }
          );
        }

        faces.forEach(f => {
          const k = f.pts.length;
          const cFace = f.pts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / k)), [0, 0, 0]);
          let faceNorm = vNorm(vCross(vSub(f.pts[1], f.pts[0]), vSub(f.pts[2], f.pts[0])));
          if (f.name === 'base' && faceNorm[1] > 0) faceNorm = vScale(faceNorm, -1);

          const projPts = f.pts.map(pr);
          const pCentroid = pr(cFace);
          const shiftedC = [cFace[0], cFace[1] + yOffset, cFace[2]];
          const shaded = shadeStudioFacet(this.cam, [244, 228, 196], faceNorm, shiftedC, 0.36);

          q.push({
            z: pCentroid[2],
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = shaded.fill;
              ctx.fill();
              ctx.strokeStyle = shaded.isFront ? 'rgba(248, 250, 252, 0.72)' : 'rgba(148, 163, 184, 0.32)';
              ctx.lineWidth = shaded.isFront ? 1.35 : 1.0;
              ctx.stroke();
            }
          });
        });
      }

      // --- 2. Kepler Meridian Triangle (1, √φ, φ) ---
      if (this.showKeplerTriangle) {
        const ME = [1, 0, 0];  // East edge midpoint
        const MW = [-1, 0, 0]; // West edge midpoint
        const pO = pr(O);
        const pME = pr(ME);
        const pA = pr(A_top);

        const cZ = (pO[2] + pME[2] + pA[2]) / 3 - 0.05;

        // Luminous Gold Triangle Polygon [O, ME, A]
        q.push({
          z: cZ,
          draw: ctx => {
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(pO[0], pO[1]);
            ctx.lineTo(pME[0], pME[1]);
            ctx.lineTo(pA[0], pA[1]);
            ctx.closePath();
            ctx.fillStyle = isKepler ? 'rgba(245, 158, 11, 0.44)' : 'rgba(245, 158, 11, 0.22)';
            ctx.fill();

            if (isKepler) {
              ctx.shadowColor = '#f59e0b';
              ctx.shadowBlur = 14;
            }
            ctx.strokeStyle = isKepler ? '#f59e0b' : 'rgba(245, 158, 11, 0.80)';
            ctx.lineWidth = isKepler ? 3.0 : 2.0;
            ctx.stroke();
            ctx.restore();
          }
        });

        // West half dashed cross-section outline [MW, A] and [MW, O]
        addLine3D(MW, A_top, 'rgba(245, 158, 11, 0.45)', 1.4, true, -0.04);
        addLine3D(MW, O, 'rgba(245, 158, 11, 0.45)', 1.4, true, -0.04);

        // Crisp Right-Angle Marker at Base Center O(0, 0, 0)
        const d = 0.12;
        const pR1 = pr([d, 0, 0]);
        const pR2 = pr([d, d, 0]);
        const pR3 = pr([0, d, 0]);
        q.push({
          z: pO[2] - 0.06,
          draw: ctx => {
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(pR1[0], pR1[1]);
            ctx.lineTo(pR2[0], pR2[1]);
            ctx.lineTo(pR3[0], pR3[1]);
            ctx.strokeStyle = isKepler ? '#f59e0b' : 'rgba(245, 158, 11, 0.85)';
            ctx.lineWidth = 1.8;
            ctx.stroke();
            ctx.restore();
          }
        });

        // Vertex Dots
        addPointMarker3D(O, 3.5, '#f59e0b', '#ffffff', -0.05);
        addPointMarker3D(ME, 4.0, '#f59e0b', '#ffffff', -0.05);
        addPointMarker3D(A_top, 4.8, isKepler ? '#fbbf24' : '#f59e0b', '#ffffff', -0.05);

        // Canvas Text Callouts for a=1, h, and apothem s
        addCallout3D([0.5, -0.10, 0], 'a = 1.000', '#f59e0b', false);
        addCallout3D([-0.16, H * 0.5, 0], `h = ${H.toFixed(4)}${isKepler ? ' (√φ)' : ''}`, '#f59e0b', isKepler);
        addCallout3D([0.58, H * 0.5 + 0.08, 0], `s = ${s.toFixed(4)}${isKepler ? ' (φ = 1.6180 ✨)' : ''}`, isKepler ? '#fbbf24' : '#f59e0b', isKepler);
      }

      // --- 3. Squaring the Circle (2πh = 8) ---
      if (this.showQuadrature) {
        // Horizontal Quadrature Circle of radius h in base plane (y = 0)
        addCircle3D([0, 0, 0], [0, 1, 0], H, '#06b6d4', 2.2, false, 'rgba(6, 182, 212, 0.07)', -0.02);
        const isQuadExact = Math.abs(2 * Math.PI * H - 8.0) < 0.02;
        addCallout3D([H + 0.18, 0, 0], `2πh = ${(2 * Math.PI * H).toFixed(3)}${isQuadExact ? ' ≈ 8 (Quadrature)' : ''}`, '#06b6d4', isQuadExact);

        // Vertical Meridian Circle of radius h in plane z = 0 passing right through Pyramid Apex
        addCircle3D([0, 0, 0], [0, 0, 1], H, '#38bdf8', 2.0, false, null, -0.02);
        addPointMarker3D(A_top, 6.0, 'transparent', '#38bdf8', -0.08);
        addCallout3D([0, H + 0.14, 0], `Apex on Circle (R = h = ${H.toFixed(4)})`, '#38bdf8', false);
      }

      // --- 4. Earth & Moon Cosmogram ---
      if (this.showCosmogram) {
        // Earth Sphere: Radius 1, inscribed tangent to the 4 sides of the 2x2 pyramid base, centered at (0, 0, 0)
        // Earth Equator (y = 0)
        addCircle3D([0, 0, 0], [0, 1, 0], 1.0, '#3b82f6', 2.0, false, 'rgba(59, 130, 246, 0.08)');
        // Earth Latitudes (+-30°, +-60°)
        [30, -30, 60, -60].forEach(deg => {
          const rad = (deg * Math.PI) / 180;
          addCircle3D([0, Math.sin(rad), 0], [0, 1, 0], Math.cos(rad), 'rgba(59, 130, 246, 0.45)', 1.2, true);
        });
        // Earth Longitude Great Circles (Meridians)
        [0, Math.PI / 4, Math.PI / 2, (3 * Math.PI) / 4].forEach(lambda => {
          addCircle3D([0, 0, 0], [Math.sin(lambda), 0, -Math.cos(lambda)], 1.0, 'rgba(59, 130, 246, 0.45)', 1.2, false);
        });
        // North Pole Marker (0, 1, 0)
        addPointMarker3D([0, 1, 0], 4.5, '#10b981', '#ffffff', -0.05);
        addCallout3D([0.35, 1.0, 0], 'Earth North Pole (0, 1, 0)', '#10b981', true);

        // Moon Sphere: Radius |h - 1|, centered at Pyramid Apex (0, h, 0), tangent to Earth's North Pole (0, 1, 0)
        const rM = Math.abs(H - 1.0);
        if (rM > 0.02) {
          addCircle3D([0, H, 0], [0, 1, 0], rM, '#e2e8f0', 1.8, false, 'rgba(241, 245, 249, 0.14)');
          [45, -45].forEach(deg => {
            const rad = (deg * Math.PI) / 180;
            addCircle3D([0, H + rM * Math.sin(rad), 0], [0, 1, 0], rM * Math.cos(rad), 'rgba(203, 213, 225, 0.45)', 1.1, true);
          });
          [0, Math.PI / 2].forEach(lambda => {
            addCircle3D([0, H, 0], [Math.sin(lambda), 0, -Math.cos(lambda)], rM, 'rgba(203, 213, 225, 0.55)', 1.2, false);
          });
          const isMoonMatch = Math.abs(rM - 0.2727) < 0.005;
          addCallout3D([0, H + rM + 0.10, 0], `Moon (r = ${rM.toFixed(4)}) • Ratio: ${(rM / 1.0).toFixed(4)} vs 0.2727`, '#e2e8f0', isMoonMatch);
        }
      }
    }
  }

  // --- Auto-Mounting Entrypoint ---
  function initPolyhedraMounts() {
    const mounts = document.querySelectorAll('.polyhedra-3d-mount:not(.polyhedra-mounted)');
    mounts.forEach(el => new PolyhedraWidget(el));
  }

  // Expose global registry for programmatic access & external widgets
  if (typeof window !== 'undefined') {
    window.GEOMETOR_POLYHEDRA = {
      getSolid,
      getSolidCategory,
      PolyhedraWidget,
      initPolyhedraMounts,
      buildSolidumMesh,
      buildVacuumMesh,
      buildAbscisumMesh,
      buildElevatumMesh,
      buildFaceCenterDual,
      buildGoldenOverlay
    };
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initPolyhedraMounts);
    } else {
      initPolyhedraMounts();
    }
  }

})();


