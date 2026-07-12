# THM-M-0984 anchor-audit validation

Item: `S56-M-0984-ANCHOR_AUDIT`  
Base revision: `578632bf0c98d5485dbd13f1946157f593e5087a`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The frozen modern target has an exact terminal candidate in pinned mathlib:
`Mathlib.Probability.StrongLaw.ProbabilityTheory.strong_law_ae` at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The direct local wrapper
`Stage1Instances.THM_M_0984.AnchorAudit.strongLawAnchor` elaborates with the
same universes, domains, three hypotheses, almost-everywhere quantifier,
empirical average, and Bochner-integral limit. Lean reports only `propext`,
`Classical.choice`, and `Quot.sound` for both the terminal theorem and wrapper.

The source file contains an explicit proof body at lines 788-819. Its module
documentation identifies Etemadi's pairwise-independent proof route. The
real-valued `strong_law_ae_real` is a specialization, while `strong_law_Lp`
has a different conclusion and stronger moment premise. The legacy
`S1_M_264` wrapper is a duplicate discovery surface, not independent proof
provenance.

Thus the exact modern machine candidate is `M0-W` at this audit node. This
does not resolve the `H1` mismatch between the repository's terse "Borel,
1909" row and the modern Banach-valued Etemadi theorem. It also does not pass
the later obligation-tree, validation, readability, release, or master gates,
so the theorem is not complete.

## Commands and exact outcomes

All commands ran in this worker clone. No Lake update, build, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1..1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0984` | 0 | rank 264, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `rg` over all installed dependency `*.lean` files for the six recorded aliases | 0 | terminal strong-law declarations occur in `Mathlib/Probability/StrongLaw.lean`; no separate external dependency candidate located |
| GitHub repository API query for `"strong law of large numbers" Lean` | 0 | `total_count: 0`, `incomplete_results: false` |
| GitHub code API and grep.app searches | limited | unauthenticated API and service rate limits; recorded as bounded-search limitations, not negative evidence |
| `lake env lean ../../Stage1_Instances/THM-M-0984/AnchorAudit.lean` from `Formalizations/Lean` | 0 | exact wrapper and three candidate types elaborated; terminal and wrapper axiom reports agree |
| `python3 -m json.tool Stage1_Instances/THM-M-0984/anchor-audit.json >/dev/null` | 0 | structured candidate/provenance ledger parses |
| forbidden-token scan of the new Lean and JSON artifacts | 1 | expected ripgrep no-match: no proof placeholder, bodyless declaration, or unsafe escape found |
| `git diff --check -- Stage1_Instances/THM-M-0984 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

## Status boundary

This phase is self-tested pending master acceptance. The machine component of
the frozen modern root is classified `M0-W`; the dossier root remains
`[H1, M0-W, R3]`, with source identity and every later rev-5.6 gate open.
