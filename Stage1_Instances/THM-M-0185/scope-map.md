# Scope map

## Metadata boundary

The repository record says only "Seiberg-Witten invariants" and "new invariants of four-manifolds".
An invariant is an object or family of objects; it is not by itself a theorem. The record does not
choose between existence/well-definedness, independence from choices, chamber dependence, wall
crossing, vanishing, nonvanishing, or an application. Intake therefore freezes the theorem family
and its exclusions, not an invented proposition.

## Candidate mathematical scope

A source-faithful construction or invariance theorem is expected to involve, as fixed by the
eventually selected primary statement:

- a smooth, closed, connected, oriented four-manifold `X` and the applicable `b2+(X)` condition;
- a `Spin^c` structure, determinant line bundle, spinor bundles, and first Chern class;
- a Riemannian metric, unitary connection, spinor, Dirac operator, curvature and perturbation;
- the Seiberg-Witten monopole equations and quotient by the gauge group;
- compactness, transversality, reducibles, expected dimension, and orientation of the moduli space;
- a signed count or higher-dimensional evaluation with its exact coefficient/codomain convention;
- independence from auxiliary choices, or explicit chamber data when that independence fails; and
- the precise equivalence of four-manifolds under which the result is invariant.

The statement phase must also decide orientation reversal, conjugate `Spin^c` structures, torsion,
disconnected manifolds, zero-dimensional versus positive-dimensional moduli spaces, empty moduli
spaces, and the `b2+ = 1` wall-crossing boundary. Domains, universes, ordered binders, hypotheses,
conclusion, foundations, TCB, computation profile, imports, and expression fingerprint remain open.

## Competing root variants

The metadata is compatible with several inequivalent propositions:

1. construction and well-definedness of `SW_X(s)` under a `b2+(X) > 1` hypothesis;
2. metric and perturbation independence of a signed count in expected dimension zero;
3. chamber-dependent invariance and wall crossing when `b2+(X) = 1`;
4. a vanishing or nonvanishing theorem for a special geometric class; or
5. a comparison with Donaldson or Gromov invariants or a downstream smooth-structure application.

The statement phase must select a pinpoint source theorem and retain its exact assumptions. The
first two variants are plausible defaults, but neither is canonical at intake.

## Explicit exclusions

- An arbitrary function on four-manifolds whose invariance is assumed as a premise.
- The equations or gauge action alone, without construction and choice-independence of an invariant.
- A finite-dimensional signed-count abstraction that omits the analytic gauge-theory obligations.
- A trivial bundle, empty-moduli-space case, or single manifold used as a convenient replacement.
- Donaldson invariants, Taubes's `SW=Gr`, or another application without a checked equivalence.
- Reusing `THM-M-0585` or `THM-M-0608` as an alias or as proof credit; those are separate targets.
- Treating the metadata label `已验证`, a citation, or mathematical consensus as kernel evidence.

No exact Lean target is frozen in this phase, and no statement mutation or proof obligation receives
credit. That boundary is intentional: elaborating an abstract proxy would validate a substituted
theorem rather than this record.
