# THM-M-0444 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the target labelled "Kolyvagin Euler
system". The repository source supplies only the phrase "construction of an Euler system"; it does
not identify a unique theorem, coefficient representation, elliptic curve, field tower, or norm
relation. The intake therefore preserves that ambiguity rather than silently replacing it with a
more familiar Kolyvagin theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source claim | Kolyvagin's construction of an Euler system | The exact published theorem and conventions are not yet pinned |
| Arithmetic data | the number field/Galois representation, coefficient ring and prime intended by the source | All remain unresolved; no values are invented |
| Indexing data | admissible squarefree indices and the corresponding field extensions | Candidate architecture only |
| Euler-system object | cohomology classes indexed by those data | The cohomology theory, twists and local conditions remain unresolved |
| Compatibility | corestriction/norm relations with the appropriate Euler factors | Exact polynomial, Frobenius convention and exceptional cases remain unresolved |
| Lean boundary | Lean 4 plus pinned mathlib and, if required, a pinned external Lean 4 dependency | No canonical declaration or elaboration is credited at intake |

This scope intentionally excludes nearby consequences such as Selmer-group bounds, finiteness of
the Tate-Shafarevich group, and BSD rank statements. Those consequences are not interchangeable
with construction of the Euler-system classes.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R4]`. The first failed gate is exact
source identification: the metadata label is not a theorem-sized statement. Consequently the
statement phase may not choose a Lean proposition until a primary source theorem and its complete
data are pinned. No proof, machine closure, or theorem completion is claimed.

The structured intake is in `intake.json`, the source boundary is in
`source_statement_crosswalk.md`, and the dependent work is frozen in `task-dag.json`.

