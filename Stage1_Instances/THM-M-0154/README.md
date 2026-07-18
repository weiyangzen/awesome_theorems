# THM-M-0154 Historical Intake

This directory is the retained `planned` dossier for the generalized Stokes theorem. The source
record says only "integration of differential forms over the boundary of a manifold." This intake
freezes the standard smooth-manifold-with-boundary theorem family without pretending that the
repository already has the differential-form integration machinery or an exact Lean declaration.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Manifold | an oriented smooth `n`-manifold `M` with boundary | model space, chart regularity, second-countability, and universe parameters await the statement phase |
| Form | a smooth compactly supported differential `(n-1)`-form `omega` on `M` | support and smoothness must be represented by typed Lean predicates, not unconstrained propositions |
| Interior integral | integral of the exterior derivative `d omega` over `M` | no manifold-form integral in the pinned dependency closure is credited |
| Boundary integral | integral of the pullback of `omega` along `i : boundary M -> M` | boundary orientation uses the outward-normal-first convention and must be encoded explicitly |
| Equality | `integral_M (d omega) = integral_(boundary M) (i^* omega)` | signs and the boundary inclusion cannot be suppressed |
| Boundary cases | empty boundary gives a zero integral; `n = 0` and disconnected/noncompact manifolds require deliberate encoding | compact support permits noncompact `M`; the compact-manifold corollary is not the chosen root |
| Exclusions | Green's theorem, divergence theorem, complex contour theorems, singular chains, manifolds with corners | these are consequences or variants, not substitutes for this root |
| Foundations | Lean 4 kernel with pinned mathlib manifold, alternating-form, measure, and integration APIs | exact imports, axioms, dependency closure, and environment fingerprint remain open |

The pinned mathlib tree has exterior differentiation for differential forms on normed spaces and
manifold boundary infrastructure, but the intake search found no terminal generalized Stokes
declaration. That observation is discovery evidence only. It neither proves absence nor earns
machine credit.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The next phase must elaborate one source-faithful target and mutation-test dimension, orientation,
compact support, boundary pullback, sign convention, and empty-boundary behavior. Later phases must
separately audit sources and formal candidates, freeze typed integration obligations, and integrate
and replay an admitted exact machine proof. New root work requires an active reviewed frontier
exception; validation and release use the current v2 gates.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact statement gate: there is no accepted elaborated expression, environment fingerprint, or
checked transport. The historical "verified" label is untrusted. This intake is self-tested, but
the theorem is not complete and no downstream phase is claimed.

The commands and exact results in `validation.md` check only target membership, dossier structure,
JSON syntax, local hygiene, and the availability of the pinned Lean toolchain.
