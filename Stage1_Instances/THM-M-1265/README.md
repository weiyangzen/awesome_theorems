# THM-M-1265 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the item named “直接法” (direct method). The
available repository sources say only “direct solution of variational problems.” That phrase names
a method, not one theorem with fixed domains and hypotheses. The intake therefore preserves the
ambiguity instead of silently substituting a compact-minimum theorem, a reflexive-Banach-space
existence theorem, or a PDE-specific minimizer theorem.

## Scope map

| Surface | Candidate scope exposed by the source phrase | Boundary at intake |
|---|---|---|
| Root claim | Existence of a minimizer for some variational problem | No functional, admissible class, ambient space, or exact conclusion is supplied |
| Compactness route | Compact admissible set; compact sublevels; weak/weak-star sequential compactness | The intended topology and compactness mechanism are unknown |
| Closure route | Lower semicontinuity or weak lower semicontinuity | The convergence notion and codomain of the functional are unknown |
| Boundedness route | Coercivity or an explicitly bounded minimizing sequence | No coercivity definition or hypotheses are supplied |
| Degenerate cases | Empty admissible set, identically infinite functional, unattained infimum, non-Hausdorff or nonreflexive settings | Inclusion and exclusion decisions cannot yet be made |
| Formal target | Lean 4 declaration using mathlib topology/analysis APIs | Selecting a declaration now would broaden or substitute the source statement |
| Foundations | Lean 4 kernel plus a versioned classical/choice/quotient policy | Exact profile remains open |

The next statement phase must first obtain an authoritative formulation identifying the ambient
space, admissible set, functional and codomain, convergence/topology, compactness or coercivity
assumptions, lower-semicontinuity assumptions, and exact existence conclusion. Only then can it
freeze ordered binders, boundary cases, a minimal import, and mutation tests.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H5, M4, R3]`. The first failed gate is source
statement identification, before Lean elaboration. The repository label `已验证` is explicitly
untrusted under rev-5.6 and supplies no proof credit. The theorem is not complete.

## Validation

On base revision `056367be3b1cb2e101200085ec5a5fdff670d16b`, the worker ran the exact commands in
`validation.md`. They validate manifest membership, repository-standard consistency, dossier JSON,
required local fields, crosswalk references, and whitespace only. No Lean theorem was fabricated
or checked because no exact proposition is available.
