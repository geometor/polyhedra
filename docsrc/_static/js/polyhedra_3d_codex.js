/* =========================================================================
   GEOMETOR • polyhedra — Interactive 3D Codex Engine
   Exact symbolic geometry & Renaissance chiaroscuro rendering for Book Codices
   Auto-mounts onto every <div class="polyhedra-3d-mount" ...>
   ========================================================================= */

(function () {
  'use strict';

  // --- Mathematical Constants ---
  const PHI = (1 + Math.sqrt(5)) / 2;       // ~1.618033988749895
  const INV_PHI = PHI - 1;                 // ~0.618033988749895 (1 / PHI)
  const PHI_SQ = PHI + 1;                  // ~2.618033988749895 (PHI^2)

  // --- Chiaroscuro & Renaissance Woodcut Palettes ---
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

    // Renaissance Boxwood & Walnut tones for Vacuum frames
    boxwood: [224, 185, 130],     // Sunlit warm Italian boxwood (outer frame)
    walnut: [74, 52, 38],          // Deep shaded Italian walnut (inner frame)
    pearwood: [168, 128, 92],      // Mid-tone carved pearwood (window reveals)

    // Solidum Elemental Tones (Empedoclean / Platonic)
    fire: [239, 68, 68],           // Tetrahedron (Fire)
    earth: [202, 138, 4],          // Hexahedron (Earth)
    air: [56, 189, 248],           // Octahedron (Air)
    water: [59, 130, 246],         // Icosahedron (Water)
    aether: [168, 85, 247],        // Dodecahedron (Aether / Quintessence)

    // Golden Ratio accents
    gold: '#f59e0b',
    goldGlow: 'rgba(245, 158, 11, 0.35)',
    goldFill: 'rgba(245, 158, 11, 0.18)',

    // Five Cubes Jewel Palette (Euclid XIII.17)
    cubeColors: [
      { name: 'Cube 1', hex: '#f59e0b', rgb: [245, 158, 11] }, // Gold
      { name: 'Cube 2', hex: '#10b981', rgb: [16, 185, 129] }, // Emerald
      { name: 'Cube 3', hex: '#06b6d4', rgb: [6, 182, 212] },  // Cyan
      { name: 'Cube 4', hex: '#8b5cf6', rgb: [139, 92, 246] }, // Violet
      { name: 'Cube 5', hex: '#f43f5e', rgb: [244, 63, 94] }   // Crimson
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

    // Derive 20 equilateral triangular faces with CCW outward normals
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

    // Construct 12 pentagonal faces using dual icosahedron directions
    const faces = [];
    for (let ic = 0; ic < rawIco.length; ic++) {
      const dir = vNorm(rawIco[ic]);
      const scored = vertices.map((v, idx) => ({ idx, dot: vDot(v, dir) }));
      scored.sort((a, b) => b.dot - a.dot);
      const top5 = scored.slice(0, 5).map(x => x.idx);

      // Centroid of face
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

  function getPlatonicSolid(name) {
    switch (name.toLowerCase()) {
      case 'tetrahedron': return getTetrahedron();
      case 'hexahedron':
      case 'cube': return getHexahedron();
      case 'octahedron': return getOctahedron();
      case 'icosahedron': return getIcosahedron();
      case 'dodecahedron': return getDodecahedron();
      default: return getIcosahedron();
    }
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

  // --- Procedural Polyhedral Variants ---

  // 1. Solidum (Opaque planar faces)
  function buildSolidumMesh(base) {
    const { vertices, faces, color } = base;
    const polygons = faces.map(f => {
      const pts = f.map(idx => vertices[idx]);
      const c = pts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / pts.length)), [0, 0, 0]);
      const norm = vNorm(vCross(vSub(pts[1], pts[0]), vSub(pts[2], pts[0])));
      return {
        pts,
        centroid: c,
        norm,
        baseColor: color,
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
      label: 'Solidum (Opaque Faceted Faces)'
    };
  }

  // 2. Vacuum (Leonardo da Vinci Mitered Wooden Frame)
  // Generates 6 * E quads: outer_frame, inner_frame, window_reveal
  function buildVacuumMesh(base, mu, frameThickness) {
    const { vertices, faces } = base;
    const { edges } = getEdgesFromFaces(faces);
    const E = edges.length;
    const V = vertices.length;
    const F = faces.length;
    const R_in = 1.0 - (frameThickness || 0.14);

    const polygons = [];

    // For each face, generate outer and inner aperture vertices
    faces.forEach(f => {
      const k = f.length;
      const faceVerts = f.map(idx => vertices[idx]);
      const cFace = faceVerts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / k)), [0, 0, 0]);
      const faceNorm = vNorm(vCross(vSub(faceVerts[1], faceVerts[0]), vSub(faceVerts[2], faceVerts[0])));

      // Outer aperture vertices
      const wOut = faceVerts.map(v => vLerp(v, cFace, mu));
      // Inner shell vertices
      const vIn = faceVerts.map(v => vScale(v, R_in));
      const wIn = wOut.map(w => vScale(w, R_in));

      for (let i = 0; i < k; i++) {
        const next = (i + 1) % k;

        // 1. Outer frame quad (warm sunlit boxwood)
        const outerQuad = [faceVerts[i], faceVerts[next], wOut[next], wOut[i]];
        const cOuter = outerQuad.reduce((acc, p) => vAdd(acc, vScale(p, 0.25)), [0, 0, 0]);
        polygons.push({
          pts: outerQuad,
          centroid: cOuter,
          norm: faceNorm,
          baseColor: PAL.boxwood,
          type: 'vacuum_outer'
        });

        // 2. Inner frame quad (deep shaded walnut)
        const innerQuad = [vIn[next], vIn[i], wIn[i], wIn[next]];
        const cInner = innerQuad.reduce((acc, p) => vAdd(acc, vScale(p, 0.25)), [0, 0, 0]);
        polygons.push({
          pts: innerQuad,
          centroid: cInner,
          norm: vScale(faceNorm, -1),
          baseColor: PAL.walnut,
          type: 'vacuum_inner'
        });

        // 3. Window reveal / jamb quad (mid-tone carved pearwood)
        const revealQuad = [wOut[i], wOut[next], wIn[next], wIn[i]];
        const cReveal = revealQuad.reduce((acc, p) => vAdd(acc, vScale(p, 0.25)), [0, 0, 0]);
        const revealNorm = vNorm(vCross(vSub(wOut[next], wOut[i]), vSub(wIn[next], wOut[next])));
        polygons.push({
          pts: revealQuad,
          centroid: cReveal,
          norm: revealNorm,
          baseColor: PAL.pearwood,
          type: 'vacuum_reveal'
        });
      }
    });

    return {
      polygons,
      V_vac: 2 * V + 4 * E,
      E_vac: 12 * E,
      F_vac: 6 * E,
      genus: F - 1,
      label: `Vacuum (Leonardo Frame • μ = ${mu.toFixed(2)})`
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

  // --- Golden Structure Overlays & Duals ---
  function getGoldenOverlay(solidName, base) {
    const lines = [];
    const pols = [];
    const labels = [];

    if (solidName === 'icosahedron') {
      // 3 Mutually Orthogonal Golden Rectangles
      const s = 0.88;
      const rXY = [[ s,  s*PHI, 0], [-s,  s*PHI, 0], [-s, -s*PHI, 0], [ s, -s*PHI, 0]];
      const rYZ = [[0,  s,  s*PHI], [0, -s,  s*PHI], [0, -s, -s*PHI], [0,  s, -s*PHI]];
      const rZX = [[ s*PHI, 0,  s], [ s*PHI, 0, -s], [-s*PHI, 0, -s], [-s*PHI, 0,  s]];

      pols.push({ pts: rXY, color: 'rgba(245, 158, 11, 0.22)', stroke: '#f59e0b', width: 2.2 });
      pols.push({ pts: rYZ, color: 'rgba(251, 146, 60, 0.22)', stroke: '#fb923c', width: 2.2 });
      pols.push({ pts: rZX, color: 'rgba(56, 189, 248, 0.22)', stroke: '#38bdf8', width: 2.2 });

      labels.push({ pos: [0, s * PHI * 1.08, 0], text: 'XY (1:φ)' });
      labels.push({ pos: [0, 0, s * PHI * 1.08], text: 'YZ (1:φ)' });
      labels.push({ pos: [s * PHI * 1.08, 0, 0], text: 'ZX (1:φ)' });
    } else if (solidName === 'dodecahedron') {
      // Canonical Inscribed Cube (Euclid XIII.17)
      const s = 0.82;
      const cv = [
        [ s,  s,  s], [ s, -s,  s], [-s, -s,  s], [-s,  s,  s],
        [ s,  s, -s], [ s, -s, -s], [-s, -s, -s], [-s,  s, -s]
      ];
      const cubeEdges = [
        [0,1],[1,2],[2,3],[3,0],
        [4,5],[5,6],[6,7],[7,4],
        [0,4],[1,5],[2,6],[3,7]
      ];
      cubeEdges.forEach(([a, b]) => {
        lines.push({ pts: [cv[a], cv[b]], color: '#f59e0b', width: 2.5, dashed: false });
      });
      // 3 Axial Rectangles
      const rx = [[0, s*PHI, s*INV_PHI], [0, -s*PHI, s*INV_PHI], [0, -s*PHI, -s*INV_PHI], [0, s*PHI, -s*INV_PHI]];
      pols.push({ pts: rx, color: 'rgba(245, 158, 11, 0.15)', stroke: '#f59e0b', width: 1.5 });
    } else if (solidName === 'octahedron') {
      // 12 Golden Section Points on Edges
      const s = 1.45;
      const ox = [[ s,0,0],[-s,0,0],[0, s,0],[0,-s,0],[0,0, s],[0,0,-s]];
      const tau = INV_PHI;
      const pts = [
        vLerp(ox[2], ox[4], tau), vLerp(ox[3], ox[4], tau),
        vLerp(ox[2], ox[5], tau), vLerp(ox[3], ox[5], tau),
        vLerp(ox[4], ox[0], tau), vLerp(ox[4], ox[1], tau),
        vLerp(ox[5], ox[0], tau), vLerp(ox[5], ox[1], tau),
        vLerp(ox[0], ox[2], tau), vLerp(ox[1], ox[2], tau),
        vLerp(ox[0], ox[3], tau), vLerp(ox[1], ox[3], tau)
      ];
      pts.forEach(p => labels.push({ pos: p, text: '• φ⁻¹', color: '#f59e0b' }));
    } else if (solidName === 'hexahedron') {
      // Inscribed Stella Octangula / Two Tetrahedra
      const s = 1.0;
      const t1 = [[s,s,s], [s,-s,-s], [-s,s,-s], [-s,-s,s]];
      const tEdges = [[0,1],[0,2],[0,3],[1,2],[2,3],[3,1]];
      tEdges.forEach(([a, b]) => {
        lines.push({ pts: [t1[a], t1[b]], color: '#ef4444', width: 2.2 });
      });
    } else if (solidName === 'tetrahedron') {
      // Circumscribing Cube Wireframe
      const s = 1.25;
      const cv = [
        [ s,  s,  s], [ s, -s,  s], [-s, -s,  s], [-s,  s,  s],
        [ s,  s, -s], [ s, -s, -s], [-s, -s, -s], [-s,  s, -s]
      ];
      const cubeEdges = [
        [0,1],[1,2],[2,3],[3,0],
        [4,5],[5,6],[6,7],[7,4],
        [0,4],[1,5],[2,6],[3,7]
      ];
      cubeEdges.forEach(([a, b]) => {
        lines.push({ pts: [cv[a], cv[b]], color: '#64748b', width: 1.5, dashed: true });
      });
    }

    return { lines, pols, labels };
  }

  function getPolarDualWireframe(solidName, base) {
    const lines = [];
    const { vertices, faces } = base;

    // Face centers become dual vertices
    const dualVerts = faces.map(f => {
      const pts = f.map(idx => vertices[idx]);
      const c = pts.reduce((acc, p) => vAdd(acc, vScale(p, 1 / pts.length)), [0, 0, 0]);
      // Normalize to reciprocal radius
      const mag = vMag(c);
      return vScale(c, (1.25 * 1.25) / (mag * mag));
    });

    // Dual edges connect adjacent face centroids
    const { edges } = getEdgesFromFaces(faces);
    edges.forEach(e => {
      if (e.faces.length === 2) {
        lines.push({
          pts: [dualVerts[e.faces[0]], dualVerts[e.faces[1]]],
          color: '#38bdf8',
          width: 2.0,
          dashed: true
        });
      }
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

  // --- Projection & 3D Camera Engine ---
  class Camera3D {
    constructor(preset) {
      this.yaw = preset ? preset.yaw : 0.42;
      this.pitch = preset ? preset.pitch : 0.32;
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

    project(pt, w, h, baseScale) {
      const cy = Math.cos(this.yaw), sy = Math.sin(this.yaw);
      const cp = Math.cos(this.pitch), sp = Math.sin(this.pitch);

      // Rotate around Y (yaw)
      const x1 = pt[0] * cy - pt[2] * sy;
      const z1 = pt[0] * sy + pt[2] * cy;

      // Rotate around X (pitch)
      const y2 = pt[1] * cp - z1 * sp;
      const z2 = pt[1] * sp + z1 * cp;

      // Perspective transformation
      const fov = 1.0 / Math.max(0.25, 1.0 + this.persp * z2 * 0.28);
      const s = baseScale * this.zoom * fov;

      return [
        w * 0.5 + x1 * s,
        h * 0.52 - y2 * s,
        z2
      ];
    }
  }

  // --- Chiaroscuro Shading Helpers ---
  const LIGHT_DIR = vNorm([0.52, 0.78, 0.45]);

  function shadeColor(baseRgb, normal, isBackface, opacity) {
    const dot = vDot(normal, LIGHT_DIR);
    let intensity;
    if (!isBackface) {
      intensity = 0.35 + 0.65 * Math.max(0, dot);
    } else {
      intensity = 0.24 + 0.32 * Math.max(0, -dot);
    }
    const r = Math.min(255, Math.floor(baseRgb[0] * intensity));
    const g = Math.min(255, Math.floor(baseRgb[1] * intensity));
    const b = Math.min(255, Math.floor(baseRgb[2] * intensity));
    return opacity !== undefined ? `rgba(${r},${g},${b},${opacity})` : `rgb(${r},${g},${b})`;
  }

  // --- Main Polyhedra 3D Widget Controller ---
  class PolyhedraWidget {
    constructor(container) {
      this.container = container;
      this.solidName = container.getAttribute('data-solid') || '';
      this.sceneName = container.getAttribute('data-scene') || '';
      this.variant = container.getAttribute('data-initial-variant') || 'solidum';

      // State
      this.mu = 0.62;                  // Vacuum aperture ratio
      this.tau = INV_PHI;              // Octa to Icosa division ratio
      this.shellOpacity = 0.35;        // Icosa shell opacity
      this.showGoldenOverlay = false;
      this.showDual = false;
      this.autoOrbit = true;
      this.activeCubes = [true, true, true, true, true];
      this.showRoofWedge = false;
      this.rtShowDodeca = false;
      this.rtShowIcosa = false;
      this.rtShowDiagonals = true;
      this.rtSolid = false;

      // Camera presets
      this.presets = {
        leonardo: { yaw: 0.42, pitch: 0.32, zoom: 1.0, persp: 0.32 },
        isometric: { yaw: 0.615, pitch: 0.46, zoom: 1.0, persp: 0.0 },
        front: { yaw: 0.0, pitch: 0.0, zoom: 1.05, persp: 0.15 },
        top: { yaw: 0.0, pitch: 1.54, zoom: 1.05, persp: 0.0 }
      };

      this.cam = new Camera3D(this.presets.leonardo);

      this.initDOM();
      this.bindEvents();
      this.startLoop();
    }

    initDOM() {
      this.container.classList.add('polyhedra-mounted');

      let title = 'GEOMETOR • 3D Regular Polyhedra Codex';
      let subtitle = 'Drag to orbit • Scroll to zoom • Interactive Platonic & Golden Structure';

      if (this.solidName) {
        const solid = getPlatonicSolid(this.solidName);
        title = `REGULAR ${solid.title.toUpperCase()} • ELEMENT OF ${solid.element.toUpperCase()}`;
        subtitle = 'Leonardo da Vinci 1509 Codex • Exact Symbolic Geometry';
      } else if (this.sceneName === 'icosa_golden_rects') {
        title = 'INTERACTIVE 3D • THREE ORTHOGONAL GOLDEN RECTANGLES (1:φ)';
        subtitle = 'Euclid XIII.16 • 3 Intersecting Rectangles Generating the 12 Vertices of the Regular Icosahedron';
      } else if (this.sceneName === 'octa_to_icosa') {
        title = 'CONTINUOUS MORPHISM • REGULAR OCTAHEDRON TO REGULAR ICOSAHEDRON';
        subtitle = 'Edge Division τ: Midpoint (1/2 → Cuboctahedron) ↔ Golden Section (1/φ → Icosahedron!)';
      } else if (this.sceneName === 'dodeca_five_cubes') {
        title = 'EUCLID XIII.17 • ALL FIVE INSCRIBED CUBES IN REGULAR DODECAHEDRON';
        subtitle = '20 Vertices Partitioned into 5 Inscribed Cubes • Face Diagonals Form Cube Edges of Length 2';
      } else if (this.sceneName === 'rhombic_triacontahedron') {
        title = 'KEPLER • RHOMBIC TRIACONTAHEDRON (30 GOLDEN RHOMBI)';
        subtitle = '32 Vertices (20 Dodecahedron + 12 Icosahedron) • Diagonal Ratio Long:Short = φ : 1';
      }

      this.container.innerHTML = `
        <div class="polyhedra-header">
          <div>
            <div class="polyhedra-title">${title}</div>
            <div class="polyhedra-subtitle">${subtitle}</div>
          </div>
          <div class="polyhedra-presets">
            <button class="polyhedra-btn btn-preset" data-preset="leonardo">Leonardo 1509</button>
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
        // Variant Switchers
        const variants = [
          ['solidum', 'Solidum'],
          ['vacuum', 'Vacuum (Leonardo)'],
          ['abscisum', 'Abscisum'],
          ['elevatum', 'Elevatum']
        ];
        variants.forEach(([vKey, vLabel]) => {
          const btn = document.createElement('button');
          btn.className = `polyhedra-btn ${this.variant === vKey ? 'active' : ''}`;
          btn.textContent = vLabel;
          btn.addEventListener('click', () => {
            this.variant = vKey;
            varGroup.querySelectorAll('.polyhedra-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            this.updateSliderVisibility();
          });
          varGroup.appendChild(btn);
        });

        // Overlay Toggles
        const togGold = document.createElement('button');
        togGold.className = `polyhedra-btn ${this.showGoldenOverlay ? 'active' : ''}`;
        togGold.textContent = 'φ Golden Structure';
        togGold.addEventListener('click', () => {
          this.showGoldenOverlay = !this.showGoldenOverlay;
          togGold.classList.toggle('active', this.showGoldenOverlay);
        });
        togGroup.appendChild(togGold);

        const togDual = document.createElement('button');
        togDual.className = `polyhedra-btn ${this.showDual ? 'active' : ''}`;
        togDual.textContent = 'Polar Dual';
        togDual.addEventListener('click', () => {
          this.showDual = !this.showDual;
          togDual.classList.toggle('active', this.showDual);
        });
        togGroup.appendChild(togDual);

        const togSpin = document.createElement('button');
        togSpin.className = `polyhedra-btn ${this.autoOrbit ? 'active' : ''}`;
        togSpin.textContent = 'Auto-Spin';
        togSpin.addEventListener('click', () => {
          this.autoOrbit = !this.autoOrbit;
          togSpin.classList.toggle('active', this.autoOrbit);
        });
        togGroup.appendChild(togSpin);

        // Aperture Slider for Vacuum
        sliderWrap.innerHTML = `
          <div class="polyhedra-slider-row vacuum-slider-row" style="${this.variant === 'vacuum' ? 'display:flex;' : 'display:none;'}">
            <span class="polyhedra-label">Aperture (μ):</span>
            <input type="range" class="polyhedra-slider ap-slider" min="0.25" max="0.85" step="0.01" value="${this.mu}" />
            <span class="polyhedra-val ap-val">${this.mu.toFixed(2)}</span>
          </div>
        `;
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
            <span class="polyhedra-label">Icosahedron Shell Opacity:</span>
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
        btnGold.textContent = 'Golden Section (1/φ → Icosahedron!)';
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
        btnSolid.textContent = 'Solid / Translucent';
        btnSolid.addEventListener('click', () => {
          this.rtSolid = !this.rtSolid;
          btnSolid.classList.toggle('active', this.rtSolid);
        });
        togGroup.appendChild(btnSolid);
      }
    }

    updateSliderVisibility() {
      const vRow = this.container.querySelector('.vacuum-slider-row');
      if (vRow) {
        vRow.style.display = this.variant === 'vacuum' ? 'flex' : 'none';
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

    render() {
      const ctx = this.ctx;
      const dpr = this.scaleDpr || 1;
      const w = this.viewW || 600;
      const h = this.viewH || 460;

      ctx.save();
      ctx.scale(dpr, dpr);
      ctx.clearRect(0, 0, w, h);

      // Determine theme background
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark' ||
        (!document.documentElement.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);

      // Render items queue for depth sorting
      const renderQueue = [];
      const baseScale = Math.min(w, h) * 0.38;

      if (this.solidName) {
        this.renderPlatonicSolid(renderQueue, w, h, baseScale);
      } else if (this.sceneName === 'icosa_golden_rects') {
        this.renderSceneIcosaGoldenRects(renderQueue, w, h, baseScale);
      } else if (this.sceneName === 'octa_to_icosa') {
        this.renderSceneOctaToIcosa(renderQueue, w, h, baseScale);
      } else if (this.sceneName === 'dodeca_five_cubes') {
        this.renderSceneDodecaFiveCubes(renderQueue, w, h, baseScale);
      } else if (this.sceneName === 'rhombic_triacontahedron') {
        this.renderSceneRhombicTriacontahedron(renderQueue, w, h, baseScale);
      }

      // Sort by camera depth Z (Painter's algorithm: farthest first)
      renderQueue.sort((a, b) => b.z - a.z);

      // Draw all items
      renderQueue.forEach(item => item.draw(ctx));

      ctx.restore();
    }

    // --- Scene Renderers ---

    renderPlatonicSolid(q, w, h, sc) {
      const base = getPlatonicSolid(this.solidName);

      if (this.variant === 'solidum') {
        const mesh = buildSolidumMesh(base);
        this.eulerEl.textContent = `V = ${mesh.V} • E = ${mesh.E} • F = ${mesh.F} • χ = 2`;
        this.statusEl.textContent = `${base.title} in Solidum — Opaque Faceted Geometry`;

        mesh.polygons.forEach(p => {
          const projPts = p.pts.map(v => this.cam.project(v, w, h, sc));
          const pCentroid = this.cam.project(p.centroid, w, h, sc);

          // Normal in camera space
          const v1 = [projPts[1][0] - projPts[0][0], projPts[1][1] - projPts[0][1]];
          const v2 = [projPts[2][0] - projPts[0][0], projPts[2][1] - projPts[0][1]];
          const cross2D = v1[0] * v2[1] - v1[1] * v2[0];
          const isFacingCamera = cross2D > 0;

          const color = shadeColor(p.baseColor, p.norm, !isFacingCamera, 0.94);

          q.push({
            z: pCentroid[2],
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = color;
              ctx.fill();
              ctx.strokeStyle = isFacingCamera ? 'rgba(15, 23, 42, 0.75)' : 'rgba(15, 23, 42, 0.25)';
              ctx.lineWidth = 1.2;
              ctx.stroke();
            }
          });
        });
      } else if (this.variant === 'vacuum') {
        const mesh = buildVacuumMesh(base, this.mu);
        this.eulerEl.textContent = `V_vac = ${mesh.V_vac} • E_vac = ${mesh.E_vac} • F_vac = ${mesh.F_vac} • genus g = ${mesh.genus}`;
        this.statusEl.textContent = `Leonardo 1509 Vacuum Frame • μ = ${this.mu.toFixed(2)} • 6E = ${mesh.F_vac} Mitered Quads`;

        mesh.polygons.forEach(p => {
          const projPts = p.pts.map(v => this.cam.project(v, w, h, sc));
          const pCentroid = this.cam.project(p.centroid, w, h, sc);

          const v1 = [projPts[1][0] - projPts[0][0], projPts[1][1] - projPts[0][1]];
          const v2 = [projPts[2][0] - projPts[0][0], projPts[2][1] - projPts[0][1]];
          const isFacingCamera = (v1[0] * v2[1] - v1[1] * v2[0]) > 0;

          const color = shadeColor(p.baseColor, p.norm, !isFacingCamera, 0.96);

          q.push({
            z: pCentroid[2],
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = color;
              ctx.fill();
              ctx.strokeStyle = 'rgba(30, 20, 10, 0.70)';
              ctx.lineWidth = 1.1;
              ctx.stroke();
            }
          });
        });
      } else if (this.variant === 'abscisum') {
        const mesh = buildAbscisumMesh(base);
        this.eulerEl.textContent = `V = ${mesh.V} • E = ${mesh.E} • F = ${mesh.F} • χ = 2`;
        this.statusEl.textContent = `${base.title} Abscisum — Archimedean Rectification at Edge Midpoints`;

        mesh.polygons.forEach(p => {
          const projPts = p.pts.map(v => this.cam.project(v, w, h, sc));
          const pCentroid = this.cam.project(p.centroid, w, h, sc);
          const color = shadeColor(p.baseColor, p.norm, false, 0.90);

          q.push({
            z: pCentroid[2],
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = color;
              ctx.fill();
              ctx.strokeStyle = 'rgba(15, 23, 42, 0.85)';
              ctx.lineWidth = 1.2;
              ctx.stroke();
            }
          });
        });
      } else if (this.variant === 'elevatum') {
        const mesh = buildElevatumMesh(base);
        this.eulerEl.textContent = `V = ${mesh.V} • E = ${mesh.E} • F = ${mesh.F} • χ = 2`;
        this.statusEl.textContent = `${base.title} Elevatum — Outward Pyramidal Stellation on All Faces`;

        mesh.polygons.forEach(p => {
          const projPts = p.pts.map(v => this.cam.project(v, w, h, sc));
          const pCentroid = this.cam.project(p.centroid, w, h, sc);
          const color = shadeColor(p.baseColor, p.norm, false, 0.92);

          q.push({
            z: pCentroid[2],
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = color;
              ctx.fill();
              ctx.strokeStyle = 'rgba(15, 23, 42, 0.8)';
              ctx.lineWidth = 1.0;
              ctx.stroke();
            }
          });
        });
      }

      // Overlays
      if (this.showGoldenOverlay) {
        const overlay = getGoldenOverlay(this.solidName, base);
        overlay.pols.forEach(p => {
          const projPts = p.pts.map(v => this.cam.project(v, w, h, sc));
          const avgZ = projPts.reduce((acc, pt) => acc + pt[2], 0) / projPts.length;
          q.push({
            z: avgZ - 0.05,
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = p.color;
              ctx.fill();
              ctx.strokeStyle = p.stroke;
              ctx.lineWidth = p.width;
              ctx.stroke();
            }
          });
        });

        overlay.lines.forEach(l => {
          const p1 = this.cam.project(l.pts[0], w, h, sc);
          const p2 = this.cam.project(l.pts[1], w, h, sc);
          q.push({
            z: (p1[2] + p2[2]) * 0.5 - 0.08,
            draw: ctx => {
              ctx.beginPath();
              if (l.dashed) ctx.setLineDash([5, 4]);
              ctx.moveTo(p1[0], p1[1]);
              ctx.lineTo(p2[0], p2[1]);
              ctx.strokeStyle = l.color;
              ctx.lineWidth = l.width;
              ctx.stroke();
              if (l.dashed) ctx.setLineDash([]);
            }
          });
        });

        overlay.labels.forEach(lb => {
          const p = this.cam.project(lb.pos, w, h, sc);
          q.push({
            z: p[2] - 0.15,
            draw: ctx => {
              ctx.font = '700 12px sans-serif';
              ctx.textAlign = 'center';
              ctx.fillStyle = lb.color || '#f59e0b';
              ctx.fillText(lb.text, p[0], p[1]);
            }
          });
        });
      }

      if (this.showDual) {
        const dualLines = getPolarDualWireframe(this.solidName, base);
        dualLines.forEach(l => {
          const p1 = this.cam.project(l.pts[0], w, h, sc);
          const p2 = this.cam.project(l.pts[1], w, h, sc);
          q.push({
            z: (p1[2] + p2[2]) * 0.5 - 0.06,
            draw: ctx => {
              ctx.beginPath();
              ctx.setLineDash([5, 4]);
              ctx.moveTo(p1[0], p1[1]);
              ctx.lineTo(p2[0], p2[1]);
              ctx.strokeStyle = l.color;
              ctx.lineWidth = l.width;
              ctx.stroke();
              ctx.setLineDash([]);
            }
          });
        });
      }
    }

    renderSceneIcosaGoldenRects(q, w, h, sc) {
      const data = buildSceneIcosaGoldenRects(this.shellOpacity);
      this.eulerEl.textContent = 'V = 12 • 3 Golden Rectangles • Ratio = 1 : φ';
      this.statusEl.textContent = `Three Orthogonal Golden Rectangles (1:φ) inside Regular Icosahedron (Shell Opacity: ${Math.round(this.shellOpacity * 100)}%)`;

      // 3 Golden Rectangles
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

        // Rectangle side length labels
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

      // 20 Icosahedron Shell Faces
      if (this.shellOpacity > 0.01) {
        data.icoMesh.polygons.forEach(p => {
          const projPts = p.pts.map(v => this.cam.project(v, w, h, sc));
          const pCentroid = this.cam.project(p.centroid, w, h, sc);
          const color = shadeColor([59, 130, 246], p.norm, false, this.shellOpacity);

          q.push({
            z: pCentroid[2] + 0.05,
            draw: ctx => {
              ctx.beginPath();
              projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
              ctx.closePath();
              ctx.fillStyle = color;
              ctx.fill();
              ctx.strokeStyle = `rgba(56, 189, 248, ${Math.min(1.0, this.shellOpacity * 1.5)})`;
              ctx.lineWidth = 1.2;
              ctx.stroke();
            }
          });
        });
      }
    }

    renderSceneOctaToIcosa(q, w, h, sc) {
      const data = buildSceneOctaToIcosa(this.tau);
      const isGolden = Math.abs(this.tau - INV_PHI) < 0.015;
      const isMid = Math.abs(this.tau - 0.5) < 0.015;

      if (isGolden) {
        this.eulerEl.textContent = `✨ GOLDEN SECTION ACHIEVED • τ = ${INV_PHI.toFixed(4)} (1/φ)`;
        this.eulerEl.style.borderColor = '#f59e0b';
        this.statusEl.textContent = '✨ 12 Edge Points Form a 100% Exact Regular Icosahedron (20 Congruent Equilateral Triangles)!';
      } else if (isMid) {
        this.eulerEl.textContent = '⚖️ MIDPOINT DIVISION • τ = 0.500 (Archimedean Cuboctahedron)';
        this.statusEl.textContent = '8 Triangles + 6 Squares form Archimedean Cuboctahedron!';
      } else {
        this.eulerEl.textContent = `τ = ${this.tau.toFixed(3)} • Morphing Polyhedron`;
        this.statusEl.textContent = 'Continuous Morphism between Regular Octahedron and Regular Icosahedron';
      }

      // Octahedron Wireframe
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

      // 20 Inscribed Triangles
      data.triangles.forEach(t => {
        const projPts = t.pts.map(v => this.cam.project(v, w, h, sc));
        const pCentroid = this.cam.project(t.centroid, w, h, sc);
        const color = shadeColor(t.baseColor, t.norm, false, isGolden ? 0.88 : 0.65);

        q.push({
          z: pCentroid[2],
          draw: ctx => {
            ctx.beginPath();
            projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
            ctx.closePath();
            ctx.fillStyle = color;
            ctx.fill();
            ctx.strokeStyle = t.stroke;
            ctx.lineWidth = isGolden ? 1.6 : 1.1;
            ctx.stroke();
          }
        });
      });

      // 12 Sliding Edge Nodes
      data.pts.forEach(p => {
        const proj = this.cam.project(p, w, h, sc);
        q.push({
          z: proj[2] - 0.08,
          draw: ctx => {
            ctx.beginPath();
            ctx.arc(proj[0], proj[1], isGolden ? 4.5 : 3.5, 0, Math.PI * 2);
            ctx.fillStyle = isGolden ? '#f59e0b' : '#38bdf8';
            ctx.fill();
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1.0;
            ctx.stroke();
          }
        });
      });
    }

    renderSceneDodecaFiveCubes(q, w, h, sc) {
      const data = buildSceneDodecaFiveCubes(this.activeCubes, this.showRoofWedge);
      const activeCount = this.activeCubes.filter(x => x).length;
      this.eulerEl.textContent = `Euclid XIII.17 • ${activeCount} Active Cubes • V = 20`;
      this.statusEl.textContent = 'Each Cube Edge of Length 2 is a Pentagonal Diagonal (φ × 2φ⁻¹) of the Dodecahedron';

      // Subtle Dodecahedron Cage
      data.dodecaEdges.forEach(e => {
        const p1 = this.cam.project(data.vertices[e.a], w, h, sc);
        const p2 = this.cam.project(data.vertices[e.b], w, h, sc);
        q.push({
          z: (p1[2] + p2[2]) * 0.5 + 0.15,
          draw: ctx => {
            ctx.beginPath();
            ctx.moveTo(p1[0], p1[1]);
            ctx.lineTo(p2[0], p2[1]);
            ctx.strokeStyle = 'rgba(148, 163, 184, 0.28)';
            ctx.lineWidth = 1.2;
            ctx.stroke();
          }
        });
      });

      // Active Cubes Wireframes
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

      // Roof Wedge (Euclid XIII.17)
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

    renderSceneRhombicTriacontahedron(q, w, h, sc) {
      const data = buildSceneRhombicTriacontahedron(this.rtShowDodeca, this.rtShowIcosa, this.rtShowDiagonals, this.rtSolid);
      this.eulerEl.textContent = 'V = 32 • E = 60 • F = 30 • χ = 2';
      this.statusEl.textContent = 'Kepler 1619 • 30 Golden Rhombi with Long:Short Diagonal Ratio = φ (1.618034)';

      // 30 Golden Rhombi
      data.rhombi.forEach(r => {
        const projPts = r.pts.map(v => this.cam.project(v, w, h, sc));
        const pCentroid = this.cam.project(r.centroid, w, h, sc);
        const color = shadeColor(r.baseColor, r.norm, false, r.opacity);

        q.push({
          z: pCentroid[2],
          draw: ctx => {
            ctx.beginPath();
            projPts.forEach((pt, i) => i === 0 ? ctx.moveTo(pt[0], pt[1]) : ctx.lineTo(pt[0], pt[1]));
            ctx.closePath();
            ctx.fillStyle = color;
            ctx.fill();
            ctx.strokeStyle = 'rgba(15, 23, 42, 0.75)';
            ctx.lineWidth = 1.1;
            ctx.stroke();
          }
        });
      });

      // Diagonals (Long = phi, Short = 1)
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

      // 20 Obtuse Vertices (Dodecahedron)
      if (this.rtShowDodeca) {
        data.obtuseVerts.forEach(v => {
          const p = this.cam.project(v, w, h, sc);
          q.push({
            z: p[2] - 0.08,
            draw: ctx => {
              ctx.beginPath();
              ctx.arc(p[0], p[1], 4.5, 0, Math.PI * 2);
              ctx.fillStyle = '#10b981'; // Emerald
              ctx.fill();
              ctx.strokeStyle = '#ffffff';
              ctx.lineWidth = 1.2;
              ctx.stroke();
            }
          });
        });
      }

      // 12 Acute Vertices (Icosahedron)
      if (this.rtShowIcosa) {
        data.acuteVerts.forEach(v => {
          const p = this.cam.project(v, w, h, sc);
          q.push({
            z: p[2] - 0.08,
            draw: ctx => {
              ctx.beginPath();
              ctx.arc(p[0], p[1], 4.5, 0, Math.PI * 2);
              ctx.fillStyle = '#06b6d4'; // Cyan
              ctx.fill();
              ctx.strokeStyle = '#ffffff';
              ctx.lineWidth = 1.2;
              ctx.stroke();
            }
          });
        });
      }
    }
  }

  // --- Auto-Mounting Entrypoint ---
  function initPolyhedraMounts() {
    const mounts = document.querySelectorAll('.polyhedra-3d-mount:not(.polyhedra-mounted)');
    mounts.forEach(el => new PolyhedraWidget(el));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPolyhedraMounts);
  } else {
    initPolyhedraMounts();
  }

})();
