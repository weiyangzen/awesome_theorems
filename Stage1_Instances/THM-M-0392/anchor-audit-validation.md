# THM-M-0392 anchor-audit validation

Item: `S56-M-0392-ANCHOR_AUDIT`  
Base revision: `cb5b64d8319cd77348c3bec3361760dd82e42d87`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the affine Weierstrass equation, short-normal-form/discriminant, and
abstract Northcott infrastructure needed to model or support a future proof.
A source-tree search found no Mordell or general integral-points finiteness
declaration. These are object-level or conditional anchors, not root closure.

The only directly relevant formal Mordell-equation project found is
`lean-forward/class-group-and-mordell-equation` at immutable revision
`baba2049f3bfe4d2cc184f8205997333e7c58638`. Its manifest pins Lean 3.49.1 and
Lean 3 mathlib `cf9386...f9`; `mordell.lean` proves results for five selected
negative parameters. It neither states the uniform nonzero-parameter finiteness
root nor supplies a Lean 4 dependency. A second immutable search hit concerns
Mordell-Weil, not the target.

The candidate inventory is complete for this bounded audit protocol. The root
remains `M2` and is not kernel-closed. Human source fidelity remains `H3`: no
primary-source theorem/page/errata crosswalk receives credit here. This is an
audit-only result and does not claim theorem completion.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1..1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0392` | 0 | rank 2, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Mordell\|IntegralPoints\|integral points\|Siegel' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | no terminal Mordell or integral-points finiteness theorem; the Siegel hits are unrelated Siegel lemma/analysis results |
| GitHub repository API searches for `Mordell Lean language:Lean`, `Mordell equation Lean4`, and the known class-group repository | 0 | one Mordell-Weil hit, no Lean 4 Mordell-equation hit, and the known Lean 3 project |
| `git ls-remote https://github.com/lean-forward/class-group-and-mordell-equation.git refs/heads/main` | 0 | resolved `baba2049f3bfe4d2cc184f8205997333e7c58638` |
| immutable raw inspection of that revision's `leanpkg.toml` and `src/number_theory/mordell.lean` | 0 | Lean 3.49.1/mathlib pin confirmed; five fixed negative-parameter theorem declarations confirmed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0392/AnchorAudit.lean` | 0 | audited root expression re-elaborated using only `Init` |
| `python3 Stage1_Instances/THM-M-0392/check_anchor_audit.py` | 0 | local pin/source declarations and immutable external source matched; root classification remained `M2` |
| `python3 -m json.tool Stage1_Instances/THM-M-0392/anchor-audit.json` | 0 | structured ledger is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0392 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The check reused the canonical pinned `.lake` tree without modifying it. No
`lake update`, build, clone, fetch, or dependency mutation was performed.
