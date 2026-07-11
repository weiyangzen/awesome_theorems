# THM-M-0548 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Alexander duality. It does not inherit proof
credit from the historical Stage1 Lean file or the untrusted source label `已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Alexander duality for a compact, locally contractible subspace `A` of `S^n` | Exact coefficient category, (co)homology API, and Lean expression belong to the statement phase |
| Homology side | reduced homology of `S^n \ A` in degree `n - i - 1` | Negative-degree and truncation conventions must not be hidden by `Nat` subtraction |
| Cohomology side | reduced singular cohomology of `A` in degree `i` | The unrestricted compact-set version instead requires a suitable Cech theory and is excluded from this root |
| Naturality | maps induced by admissible inclusions/homeomorphisms | Candidate proof architecture only; no naturality evidence is credited |
| Boundary cases | empty/full subspace, `n = 0`, and degrees `i >= n` | Must be resolved by the eventual grading convention or explicit hypotheses |
| Foundations | Lean 4 kernel and pinned mathlib, with classical/choice policy audited | Exact toolchain, imports, dependency closure, and TCB remain open |

The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_120.lean` is discovery input only. Its
`StatementShape` existentially packages an arbitrary cohomology object and an isomorphism; it is not
the theorem frozen here and receives no closure credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: no canonical elaborated expression, coefficient choice, grading
transport, environment fingerprint, or mutation results exist yet. The theorem is not complete.

## Validation

The exact commands and results establishing manifest consistency, JSON syntax, and dossier-local
reference integrity are recorded in `validation.md`. These checks validate this intake only.
