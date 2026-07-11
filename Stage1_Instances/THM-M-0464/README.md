# THM-M-0464 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the metadata item named "Pila theorem". The
repository gloss, "rational-point counting in o-minimal structures", is treated as the
Pila-Wilkie counting theorem, not as a claim that every result bearing Pila's name has been
formalized. The year `2011` in the discovery metadata conflicts with the primary paper's 2006
publication date and provides no proof or machine credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Pila-Wilkie's sub-polynomial bound for rational points of bounded height in the transcendental part of a definable set | Exact quantifiers, height convention, definable-family parameters, and uniform/non-uniform form remain for the statement phase |
| Ambient geometry | subsets of real Cartesian powers definable in an o-minimal expansion of the real field | No particular Lean encoding of o-minimality or definability is selected yet |
| Exceptional locus | the algebraic part, the union of connected positive-dimensional semialgebraic subsets | Its exact source definition must be transported without replacing it by an arbitrary algebraic/Zariski locus |
| Counting | rational points of height at most `T`, bounded by `c * T^epsilon` | Source height and lower bound on `T` must be frozen before elaboration |
| Uniformity | constants may depend on the definable set and `epsilon`; family-uniform refinements are separate | Uniform variants and algebraic-point variants are excluded from the root unless source audit proves they are the intended item |
| Foundations | Lean 4 kernel plus a pinned mathlib environment | Toolchain, imports, axioms, TCB, and computation profiles remain open |

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. A primary source and theorem
pinpoint have been located, but the terse repository metadata does not determine the exact variant,
and no canonical Lean expression has been elaborated. The first failed theorem gate is therefore
the exact-statement gate. This intake makes no theorem-completion or machine-proof claim.

The structured claim and exclusions are in `intake.json`; the source relationship and precise
ambiguities are recorded in `source_statement_crosswalk.md`. Validation evidence is in
`validation.md`.
