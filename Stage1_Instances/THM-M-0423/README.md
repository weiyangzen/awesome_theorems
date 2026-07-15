# THM-M-0423 rev-5.6 dossier

This planned instance freezes the classical Hasse-Minkowski theorem for nondegenerate quadratic
forms over arbitrary number fields. The exact Lean target is
`Stage1.THM_M_0423.HasseMinkowskiStatement`; it quantifies both finite and infinite completions and
uses a nonzero isotropic witness. The historical label "Hasse principle" is not broadened to
general varieties or restricted to the rational field.

## Current surfaces

| Surface | Current boundary |
|---|---|
| Exact statement | Elaborated expression SHA-256 `4b5061f2c6f01173d7cb6c9b7005ca489aaa1da1f5740e980ea477d37ae04738`; statement evidence is provisional pending master acceptance |
| Anchor audit | Pinned mathlib supplies support only; both external candidates are Q-only and placeholder-contaminated |
| Obligation architecture | Registry v2 contains 105 canonical obligations at `32a5c78d7f9cf7b59541a9a35c52331cf5055159b93dbe758b3eb6134f7da866` |
| Lean work | Scalar-extension witness preservation and global-to-local elaborate; no accepted E0/E1 packet exists |
| Hard direction | Classification, reciprocity, realization, global Witt uniqueness, cancellation, and extraction are explicit open obligations |
| Source/readability | Hasse 1924 is H1 only; pinpoint node mapping, errata review, readable R0, and independent reviews remain open |

The typed proof graph is separate from source, provenance, evidence, trust, documentation, and
workflow overlays. All reverse proof edges are unverified `logical_decomposition` edges. The Lean
directional combinators are conditional harnesses and do not inhabit the open local-to-global
premise.

## Verdict

Lifecycle remains `planned`; root vector is `[H1, M3, R3]`. Accepted closure is empty,
`audit_complete=false`, and `theorem_complete=false`. Dependency-ordered master acceptance of the
prior phases and this worker proposal remains required.
