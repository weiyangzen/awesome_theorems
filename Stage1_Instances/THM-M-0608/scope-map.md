# Scope map

## Metadata boundary

The repository supplies only the name "Seiberg-Witten invariants" and the gloss "invariants of
four-manifolds". These describe a subject rather than a proposition with a truth value. Intake may
identify the intended theory, but cannot invent a theorem by choosing one of its several standard
results. The statement phase must select and transcribe a pinpoint primary-source claim.

## Candidate mathematical boundary

A standard gauge-theoretic formulation may involve all of the following, with conventions fixed by
the selected source:

- a smooth, closed, connected, oriented four-manifold `X`, often with a hypothesis on `b2+(X)`;
- a `Spin^c` structure and its determinant line bundle, spinor bundles, and first Chern class;
- a Riemannian metric, a unitary connection, spinors, Clifford multiplication, and the perturbed
  Seiberg-Witten monopole equations modulo the gauge group;
- compactness, transversality or regularity, reducible solutions, expected dimension, and an
  orientation of the moduli space (including a homology orientation where required);
- a signed zero-dimensional count, or the higher-dimensional evaluation convention, and proof of
  independence from auxiliary choices; and
- chamber data and wall crossing in the `b2+ = 1` case, rather than an unconditional
  metric-independent integer.

The eventual claim must say whether the object is integer-valued, defined only up to sign, or
chamber-dependent; whether torsion and disconnected cases are allowed; and how conjugate
`Spin^c` structures and orientation reversal are treated.

## Variant decision required

The label could reasonably denote at least these inequivalent roots:

1. construction and well-definedness of `SW_X(s)` for an oriented closed smooth four-manifold with
   `b2+(X) > 1`;
2. the metric/perturbation invariance theorem for the signed monopole count in expected dimension
   zero;
3. the chamber-dependent invariant and wall-crossing behavior when `b2+(X) = 1`;
4. a vanishing or nonvanishing theorem, such as consequences for positive scalar curvature or
   symplectic four-manifolds; or
5. a comparison or application stated in Witten's original paper.

The statement phase must choose exactly one source-labelled theorem and retain its assumptions.
The likely default candidate is the well-definedness/invariance result, but intake does not freeze
that preference as the canonical statement.

## Explicit exclusions

- Replacing the gauge-theoretic invariant by an arbitrary function on four-manifolds and proving
  that it is invariant by assumption.
- Proving only gauge invariance of the equations and calling that metric/perturbation independence.
- Restricting to a trivial line bundle, an empty moduli space, or a single example merely to obtain
  a readily formalizable proposition.
- Treating Donaldson invariants, a finite-dimensional signed count, or an Euler characteristic as
  the named invariant without a checked equivalence theorem.
- Treating the metadata label `已验证`, mathematical consensus, or a source citation as Lean proof
  or accepted human-proof evidence.

Before proof-tree construction, the statement phase must freeze the exact domains, ordered
quantifiers, hypotheses, conclusion, degenerate cases, normalizations, profiles, imports,
declaration type, expression and environment fingerprints, checked alternate encodings, and all
required statement mutations.

