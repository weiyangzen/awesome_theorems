# Scope map

## Root boundary

The provisional human root is:

> For every closed oriented integral homology 3-sphere, instanton Floer
> homology is well-defined, with the precise auxiliary choices and equivalence
> fixed in the formal statement, and is invariant under orientation-preserving
> diffeomorphism.

This is a conservative expansion of the repository's much shorter phrase,
"an invariant of three-dimensional manifolds." It follows the domain of the
historical construction rather than silently asserting a theory for every
3-manifold. Primary-source audit may narrow or restate it before the statement
gate; it may not broaden it without publishing a scope delta.

| Surface | In scope | Boundary at intake |
|---|---|---|
| `IFH-ROOT` | Well-definedness and orientation-preserving diffeomorphism invariance of the selected instanton Floer homology object | Human planning claim only; no Lean expression or equivalence strength is accepted |
| `IFH-DOM` | Closed oriented smooth integral homology 3-spheres | The Lean manifold, orientation, dimension, and homology-sphere predicates are unselected |
| `IFH-DATA` | SU(2) gauge-theoretic data, relative grading, and a fixed coefficient category | Bundle, connection, gauge quotient, reducible, grading, and coefficient conventions require source audit |
| `IFH-CPLX` | The instanton Floer chain complex and homology | Critical points, trajectories, transversality, compactness, orientations, and the proof that the differential squares to zero are proof architecture, not accepted facts |
| `IFH-CHOICE` | Independence from allowed metric, perturbation, and auxiliary choices | Whether the output is canonical, merely isomorphic, or chain-homotopy invariant is open |
| `IFH-DIFF` | Invariance under orientation-preserving diffeomorphism | Functoriality and orientation reversal are not silently included |
| `IFH-BOUND` | Domain, variant, and weaker-conclusion exclusions | Later framed, singular, equivariant, or admissible-bundle instanton theories require separate transports |

## Formal and trust boundary

Lean 4 with the repository's pinned mathlib is the selected backend. The
minimal imports, structures, universes, options, normalized expression, and
environment fingerprint remain open. The current mathlib surface may not
contain the gauge theory, elliptic/Fredholm analysis, moduli-space compactness,
orientation, and Floer-homology infrastructure needed for this root; that is a
later anchor-audit question, not a license to replace the theorem with an
abstract axiomatization.

No classical principle, quotient construction, analytic result, computation,
external formal artifact, or continuation-map theorem receives proof credit
at intake. Their foundation, TCB, and provenance boundaries must be audited
before use.

## Exclusions

- A theorem about all three-manifolds is not supported by the source phrase or
  the historical domain selected here.
- The chain groups, the Euler characteristic, or the Casson invariant relation
  alone do not establish invariance of the homology object.
- Heegaard Floer, monopole Floer, embedded contact, framed instanton, and
  instanton knot homologies are not interchangeable with this root.
- An abstract structure declaring an invariant without constructing and
  proving properties of instanton Floer homology would substitute a theorem.
- The untrusted `已验证` label is not evidence of a public formal proof.

No scope node is an accepted obligation, terminal proof body, or
`<=100`-step leaf. Those identities can be frozen only after the statement and
anchor-audit phases.
