# THM-M-1522 rev-5.6 intake

This is the `planned` dossier for the Birkhoff pointwise ergodic theorem. The Stage0 slogan
"time average equals space average" is frozen here as the standard ergodic probability-space
specialization, not as an unconditional identity.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Almost-everywhere convergence of orbit Cesaro averages to `integral f dmu` | Only for an integrable real-valued observable on an ergodic measure-preserving probability system |
| General theorem | Limit identified with conditional expectation on the invariant sigma-algebra | A required source/formal bridge, but not silently substituted for the root |
| Definitions | Iterates, finite sums, normalization, measure preservation, ergodicity, integrability, almost-everywhere convergence | Exact mathlib representations and ordered binders remain open |
| Boundary probes | Constant observables, identity map, non-ergodic invariant components, non-integrable observables | Used to test that no hypothesis or qualifier is accidentally erased |
| Machine surface | Lean 4 plus pinned mathlib measure theory, conditional expectation, and dynamics APIs | No module or declaration is credited before the anchor and statement phases |
| Human source | Birkhoff's 1931 pointwise theorem and a modern exact formulation | Pinpoint premise/notation/errata review is incomplete |

The initial architecture is: define the dynamical system and averages; obtain the general
pointwise limit; identify it as invariant conditional expectation; use ergodicity and probability
normalization to make that expectation the constant space integral. This is a scope map, not a
frozen obligation registry or proof tree.

## Intake verdict

Lifecycle is `planned`, with provisional root vector `[H1, M3, R3]`. The first failed theorem gate
is the exact Lean statement gate: there is no elaborated expression, environment fingerprint,
checked transport, or mutation record. The theorem is not complete.

## Validation

The exact commands and results establishing manifest membership, repository consistency, JSON
syntax, and dossier-local integrity are recorded in `validation.md`. These checks validate only
this intake deliverable.
