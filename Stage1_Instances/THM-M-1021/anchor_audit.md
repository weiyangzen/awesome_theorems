# Anchor audit

Audit date: 2026-07-12. The inspected dependency snapshot is mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, reused from the repository's
pinned `lake-manifest.json`. Its worktree was clean; no dependency was fetched
or modified.

## Search protocol

The audit searched repo-local Lean and Markdown, every Lean source file in the
pinned mathlib and `flt-regular` trees, and the GitHub repository-search API.
Case-insensitive terms covered `Bochner theorem`, identifier spellings
`bochner_theorem` and `bochnerTheorem`, positive-definite functions, probability
characteristic functions, and Fourier transforms of measures. GitHub code
search was unavailable without authentication, so this is a bounded candidate
audit, not a claim that no Lean 4 proof exists anywhere.

## Candidate ledger

| Candidate | Immutable location | Exact type role | Verdict |
|---|---|---|---|
| `MeasureTheory.charFun` | mathlib `8a178386...`, `Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic` | Defines `t |-> integral x, exp (inner x t * I) dmu`; on `Real`, `charFun_apply_real` gives `integral x, exp (t*x*I) dmu` | Usable encoding bridge; not the root equivalence |
| `MeasureTheory.charFun_zero` | same module and revision | Gives the transform at zero as total real mass | Forward normalization support only |
| `MeasureTheory.continuous_charFun` | mathlib `8a178386...`, `Mathlib.MeasureTheory.Measure.CharacteristicFunction.TaylorExpansion` | Continuity of a finite measure's characteristic function | Forward continuity support only |
| `MeasureTheory.Measure.ext_of_charFun` | `CharacteristicFunction.Basic`, same revision | Equality of finite measures from equality of characteristic functions | Uniqueness support; uniqueness is excluded from this root |

`AnchorAudit.lean` imports the strongest module above and kernel-elaborates all
five declaration names. Their types are compatible with the explicit integral
in `BochnerStatement.lean` up to elementary commutative reordering of the real
and complex factors, but none asserts existence of a measure from continuity,
normalization, and finite-family positive definiteness.

The `Mathlib.MeasureTheory.Integral.Bochner.*` name family is a false lexical
lead: it implements Bochner integration and contains no candidate for Bochner's
representation theorem. The only GitHub repository-search hit was
`mrdouglasny/hille-yosida`, whose description concerns a BCR semigroup-to-group
extension rather than this characteristic-function theorem. No external exact
Lean 4 candidate was identified, so there is nothing honest to pin or import.

## Verdict

The exact root remains `not_repo_local_closed`, with `formalization_debt` rather
than integration debt: the pinned library supplies substantial forward and
uniqueness infrastructure but no audited exact upstream proof body. The root
vector therefore stays `[H1, M3, R3]`. This completes only the bounded anchor
inventory for `S56-M-1021-ANCHOR_AUDIT`; it proves neither direction, makes no
H0 claim, and does not complete the theorem. Integration-lane master acceptance
is still required.
