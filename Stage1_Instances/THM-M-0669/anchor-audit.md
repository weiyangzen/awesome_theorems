# Immutable anchor audit

Item: `S56-M-0669-ANCHOR_AUDIT`. Cutoff: 2026-07-12. The frozen inventory and machine-readable
classification are in `anchor-audit.json`.

## Result

No exact Lean 4 candidate was found for
`Stage1.THM_M_0669.TarskiQuantifierEliminationTarget`. The audit classifies all three candidates in
inventory v1:

| Candidate | Immutable revision | Relationship | Decision |
|---|---|---|---|
| pinned mathlib real-closed-field API | `8a178386ffc0f5fef0b77738bb5449d50efeea95` | algebraic `IsRealClosed` ingredients, but no first-order QE theorem | support only |
| pinned mathlib model-theory API | `8a178386ffc0f5fef0b77738bb5449d50efeea95` | exact syntax/semantics interfaces, but no elimination proof | statement interface only |
| `avigad/qelim` | `b7d22864f1f0a2d21adad0f4fb3fc7ba665f8e60` | Lean 3 DLO/LIA development with custom syntax; no real-closed-field result | rejected as nonmatching |

The installed mathlib search covered aliases for quantifier elimination and real closed fields. Its
only theorem-relevant hit is the algebraic `IsRealClosed` API; `AnchorAuditProbe.lean` checks those
declarations and the model-theory interfaces against the pinned environment. The public GitHub
repository queries returned only `avigad/qelim`. grep.app returned HTTP 429, so that surface is an
explicit access failure, not negative evidence. Classification coverage is 3/3 for the frozen
inventory, while exhaustive public discovery is not claimed.

## Debt decision

The exact root remains `H1/M3/R3`. The elaborated statement and its supporting interfaces justify
`M3`, but neither an API ingredient nor a theorem for another theory can be transported to the
canonical formula-level claim. There is consequently no `M0-W`, `M0-P`, or
`M1` credit and no repo-local integration task for a known exact external closure. Reopen the
candidate inventory if an immutable Lean 4 RCF quantifier-elimination declaration is discovered;
otherwise the proof phase must implement the missing mathematics locally.

This completes only the bounded anchor-audit phase pending master acceptance. It does not complete
the wider dossier audit, primary-source review, proof, or theorem.
