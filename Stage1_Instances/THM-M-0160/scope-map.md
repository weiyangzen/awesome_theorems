# Scope map

## Included theorem family

- A two-dimensional coordinate domain carrying a positive-definite first fundamental form `I` and
  a symmetric second fundamental form `II`, at the differentiability required by the chosen source.
- The Gauss equation and both Codazzi-Mainardi equations as compatibility hypotheses, with the
  source's sign convention for the shape operator and unit normal.
- Local existence of a regular immersion into oriented Euclidean three-space realizing `I` and
  `II`.
- Local uniqueness of two realizations up to a Euclidean rigid motion, with orientation-preserving
  versus arbitrary isometry fixed explicitly by the selected theorem.
- A global simply-connected-domain formulation only if the selected source actually supplies it
  and its monodromy/globalization assumptions are mapped.

"Determined" must cover both realization and uniqueness. A uniqueness-only theorem presupposing an
immersion, or an existence-only integration result, cannot replace the combined theorem.

## Decisions required at statement freeze

The statement phase must select and inspect one exact theorem. It must freeze: local neighborhood
or global domain; open subset of `R^2` or abstract surface; connectedness and simple connectedness;
regularity of all six coefficients; `E > 0` and `EG - F^2 > 0` or coordinate-free metric
positivity; the precise Gauss curvature equation; the two Codazzi equations and sign conventions;
orientation and normal choice; ambient space `R^3`; immersion versus embedding; proper versus
arbitrary Euclidean motion; base-point/frame initial data; and the quantifier order for existence
and uniqueness.

Boundary cases include an empty or disconnected domain, degenerate first form, orientation reversal
changing `II` to `-II`, low regularity, and non-simply-connected domains with possible monodromy.
These must be stated or excluded from the source, never silently normalized away.

## Explicit exclusions

- The theorem that the first fundamental form alone determines intrinsic Gaussian curvature.
- Gauss's Theorema Egregium, the Gauss-Codazzi equations alone, or the fundamental theorem of curves.
- Rigidity theorems for convex closed surfaces, global embeddings, or hypersurfaces in arbitrary
  ambient manifolds unless an exact checked transport to the selected source statement is supplied.
- A structure containing an immersion, realization equality, or rigid-motion equivalence as an
  input field.
- Coordinate ODE/PDE solvability assumed wholesale as a hypothesis.
- The repository label `已验证` as source fidelity or kernel evidence.

No canonical Lean target is frozen at intake. A later target must expose concrete metrics/bilinear
forms, compatibility equations, immersion pullbacks, second fundamental form, and Euclidean motion.
