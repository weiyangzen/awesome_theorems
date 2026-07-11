# Anchor-audit validation

Item: `S56-M-0423-ANCHOR_AUDIT`. Base revision:
`d76396d014ed07f02b5e64944c3eafca7d453d40`. Audit date: 2026-07-12.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95`
provides the quadratic-form, scalar-extension, place/completion, real
classification, and number-field product-formula interfaces checked in
`AnchorAudit.lean`. A complete pinned-source name search found no
Hasse-Minkowski, Hilbert-symbol, or local-Hasse-invariant declaration.

The audit found two credible external Lean 4 candidates and inspected their
source at immutable commits through the GitHub contents API without cloning or
changing `.lake`. `facebookresearch/atlas-lean@34ffed3` has a theorem named
`hasse_minkowski`, but only for diagonal forms over `Q`, and its transitive
Hasse-Minkowski sources contain 13 `sorry` tokens. The project license is
noncommercial and adds a no-training rider. `mariainesdff/HassePrinciple@549601c`
also targets `Q`; its root `QuadraticForm.HasseMinkowski` has seven direct
`sorry` branches, with 33 `sorry` tokens across the nine audited quadratic-form
files, and it pins Lean 4.31.0-rc2 plus a different mathlib revision. Both are
`M5` candidates, not proof anchors and not integration work to perform.

Thus the exact root remains `M3`: the proposition and useful interfaces exist,
but no exact proof body does. This bounded audit is self-tested; it is not
theorem completion or a global claim that no other Lean proof exists.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0423/AnchorAudit.lean` | 0 | Eight pinned mathlib declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0423/Statement.lean` | 0 | Exact frozen target re-elaborated |
| `python3 Stage1_Instances/THM-M-0423/check_anchor_audit.py` | 0 | Statement identity, manifest pin, installed mathlib HEAD, classifications, and probes agreed |
| `rg -n -i 'Hasse.?Minkowski\|Hasse principle\|local.?global.*quadratic\|quadratic.*local.?global\|Hilbert.?symbol\|HasseInvariant' Formalizations/Lean/.lake/packages/{mathlib,flt-regular,checkdecls,plausible,LeanSearchClient,importGraph,proofwidgets,aesop,Qq,batteries,Cli} --glob '*.lean'` | 1 (expected) | No matching declaration in the complete installed pinned dependency source closure |
| GitHub repository API searches plus Sourcegraph public code search | 0 | Located the two external projects; Sourcegraph hit its result limit and GitHub code search returned HTTP 401, both recorded as bounded-search limitations |
| GitHub repository/commit/tree/contents API inspection at `34ffed3...` and `549601c...` | 0 | Immutable revisions, toolchains, mathlib pins, licenses, root types/bodies, and placeholder counts recorded |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets agree |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0423` | 0 | Rank 67, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0423/anchor-audit.json >/dev/null` | 0 | Audit record is valid JSON |
| `rg -n '\b(sorry\|axiom\|admit)\b' Stage1_Instances/THM-M-0423/AnchorAudit.lean Stage1_Instances/THM-M-0423/check_anchor_audit.py` | 1 (expected) | No prohibited declaration or placeholder in the executable audit artifacts |
| `git diff --check -- Stage1_Instances/THM-M-0423` | 0 | No whitespace errors |

No `lake update`, build, dependency clone/fetch, or `.lake` mutation was used.
Reopen integration only for an exact or checked-transport candidate with an
immutable placeholder-free trust closure, compatible reproducible toolchain,
acceptable license, and successful repo-local wrapper validation.
