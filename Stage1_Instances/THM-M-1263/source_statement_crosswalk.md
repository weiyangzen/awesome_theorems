# Source-statement crosswalk

The Stage0 phrase `波前集与奇性传播` names a theorem family rather than a bibliographically exact
statement. This crosswalk therefore records candidates and the decisions still needed; it does not
award `H0` or exact-statement credit.

| Claim component | Human source anchor | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Singularities propagate along null bicharacteristics for real principal type operators | Lars Hörmander, *The Analysis of Linear Partial Differential Operators III*, Springer, chapter XXVI (“Operators of principal type”), especially the propagation results beginning in section 26.1 | a theorem relating a distributional wavefront predicate to integral curves of the Hamilton vector field of the principal symbol | Primary monograph family located; edition, exact theorem number/pages, hypotheses, and errata must be verified from the source before transcription |
| Local propagation away from forcing singularities | Same principal-type chapter; the intended relative form excludes `WF(Pu)` | predicates for `rho ∉ WF(Pu)` and orbitwise invariance of `rho ∈ WF(u)` | Likely canonical root, but the Stage0 label does not choose ordinary versus Sobolev wavefront sets or the precise neighborhood/maximality clause |
| Elliptic region | Hörmander's microlocal elliptic regularity preceding the propagation theorem | `p rho != 0 -> rho ∉ WF(u)` when `rho ∉ WF(Pu)` | Supporting branch, not a substitute for propagation on the characteristic set |
| Hamilton dynamics | Standard cotangent symplectic form and Hamilton vector field of the real principal symbol | cotangent bundle, characteristic set, vector field integral curve | Required definitional layer; availability and conventions in pinned mathlib remain unaudited |
| Smooth-forcing corollary | Standard formulation: when `Pu` is smooth, `WF(u)` is invariant/formed from null bicharacteristics | wrapper from the relative theorem plus `WF(Pu) = ∅` | Candidate corollary only; no transport is checked |
| Sobolev refinement | Hörmander's Sobolev/microlocal regularity formulation in the same theory | indexed `WF_s` predicates with operator-order shift | Alternate target; must not be conflated with the ordinary wavefront statement |

## Exactness questions for the statement phase

- Pin the edition/printing and verify the exact theorem number, page interval, assumptions, and any
  published corrections or errata.
- Decide whether `P` is differential or pseudodifferential, scalar or bundle-valued, and precisely
  what “real principal type” and proper support mean in the selected statement.
- Freeze ordinary versus Sobolev wavefront sets and all order shifts.
- Freeze whether the conclusion is local propagation, invariance on a bicharacteristic segment, or
  a global union-of-maximal-bicharacteristics corollary.
- Crosswalk every source premise to an ordered Lean binder or a named derived obligation.
- Mutation-test removal of real-principal-type, the `WF(Pu)` exclusion, characteristic-set
  membership, and nonstationarity; separately probe elliptic and radial points.

Discovery links, not immutable evidence receipts:

- Springer book DOI: <https://doi.org/10.1007/978-3-540-49938-1>
- Hörmander bibliographic record: *The Analysis of Linear Partial Differential Operators III:
  Pseudo-Differential Operators*, reprint of the 1994 edition, Springer (2007).

No claim is made that a matching Lean theorem exists. A later anchor audit must search pinned
sources and inspect exact declaration bodies, dependencies, axioms, licenses, and revisions.
