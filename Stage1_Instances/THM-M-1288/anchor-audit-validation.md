# Anchor-audit validation record

Item: `S56-M-1288-ANCHOR_AUDIT`  
Base revision: `3bb2bb303df87d54d8d5dfafcee61ad3c329e278`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The exact frozen target exists locally only as a proposition definition. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains a substantial, kernel-checked
Gagliardo-Nirenberg-Sobolev development. Its closest theorem,
`MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq`, gives the correct conjugate-exponent pattern for
compactly supported `C^1` functions, but uses `ENNReal` `eLpNorm`, the Frechet derivative, and an
unspecified library constant. It does not identify the dossier's gamma-function constant or prove
that constant is least. The direct wrapper in `AnchorAudit.lean` elaborates and reports only
`propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`.

Sourcegraph's exact Talenti/Aubin-Talenti/sharp-Sobolev queries returned no Lean matches. The broader
mathlib-declaration query found only mathlib and
`scottnarmstrong/DeGiorgi@4c1b3077d3782b24065184df4ba59501b2e56fc7`. The latter's immutable
`DeGiorgi.sobolev_smooth` is a useful Euclidean exponent wrapper around the same non-sharp mathlib
theorem, on different Lean and mathlib revisions; it does not close optimality. Public search is
bounded and index-dependent, so this record does not claim global absence.

The root therefore remains `M3`. The formalization debt is specifically the real-integral/eLpNorm
and gradient/Frechet-derivative transports, derivation of the displayed coefficient, admissibility
at that coefficient, and the lower-bound argument proving least-constant sharpness.

## Commands and results

Commands ran from the repository root. Lean used only the existing pinned `.lake` artifacts. No
Lake update/build, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1288` | 0 | rank 459, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1288/AnchorAudit.lean` | 0 | Direct wrapper and five pinned mathlib declarations elaborated; axioms were `propext`, `Classical.choice`, `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1288/Statement.lean` | 0 | Exact canonical proposition re-elaborated |
| `python3 Stage1_Instances/THM-M-1288/check_anchor_audit.py` | 0 | Target fingerprint, exact mathlib pin/module hash, and three candidate classifications agree |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the manifest pin |
| `rg -n -i 'talenti\|aubin.?talenti\|sharp sobolev\|best constant in sobolev\|sobolev.*inequal' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | Located the non-sharp mathlib Sobolev family; no Talenti formula/optimality declaration |
| Sourcegraph queries for `Talenti`, `Aubin-Talenti`, and `sharp Sobolev` in Lean | 0 | Zero indexed matches; response hashes recorded in `anchor-audit.json` |
| Sourcegraph query for `eLpNorm_le_eLpNorm_fderiv_of_eq` in Lean | 0 | 10 matches in mathlib and DeGiorgi; response SHA-256 `063ab8...df2fd` |
| GitHub REST repository searches for Talenti/Sobolev Lean repositories | 0 | Both complete metadata responses had `total_count=0`; response SHA-256 `08c082...2600` |
| grep.app API searches for `Talenti` and the mathlib declaration | 22 | HTTP 503 access failures; no negative search conclusion |
| Immutable raw inspection of `scottnarmstrong/DeGiorgi@4c1b307.../DeGiorgi/WholeSpaceSobolev.lean` | 0 | `sobolev_smooth` wraps mathlib's theorem; source SHA-256 `0c0146...6729`; no `sorry`, `axiom`, or `unsafe` token |
| `python3 -m json.tool Stage1_Instances/THM-M-1288/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1288 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This bounded anchor audit is self-tested pending master acceptance. It supplies supporting checked
infrastructure but no exact proof, no external integration credit, no full audit completion, and no
theorem-completion claim.
