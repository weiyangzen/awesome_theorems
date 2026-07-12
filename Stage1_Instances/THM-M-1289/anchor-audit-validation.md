# Anchor-audit validation record

Item: `S56-M-1289-ANCHOR_AUDIT`  
Base revision: `d7953d0695a725ae8ce67787c822bae069258f8e`

## Result

The exact repo-local artifact is only the proposition
`Stage1Instances.THM_M_1289.AubinTalentiTarget`, so it is an `M3` statement candidate without a
proof body. Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies checked
Gagliardo-Nirenberg-Sobolev bounds and coordinate formulas for the Laplacian. The six probes in
`AnchorAudit.lean` elaborate. The Sobolev declarations use implementation constants and prove no
least-constant or equality result; the Laplacian declarations are derivative identities. None
mentions the explicit bubble or proves its positivity, smoothness, PDE, or norm finiteness.

No exact external Lean 4 candidate was found in the bounded public searches. Sourcegraph returned
zero indexed Lean matches for the principal names and aliases. Both GitHub repository searches
returned zero complete results, while unauthenticated GitHub code search returned HTTP 401 and is
recorded as blocked. The complete immutable tree of
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` had no matching path.
These negative results delimit the audit; they do not assert global absence.

The exact root therefore remains `M4`. This is a completed anchor audit, not proof completion.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone. Lean used only existing pinned `.lake`
artifacts; no update, fetch, clone, dependency build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1289/AnchorAudit.lean` | 0 | Six pinned mathlib support declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1289/Statement.lean` | 0 | Exact canonical proposition and four statement mutations re-elaborated |
| `python3 Stage1_Instances/THM-M-1289/check_anchor_audit.py` | 0 | Audit status boundary, six probes, manifest pin, and installed mathlib HEAD agreed |
| `rg -n -i 'Aubin.?Talenti\|Talenti.?bubble\|sharp Sobolev\|best constant in Sobolev' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match result in pinned source |
| Sourcegraph public Lean search for five names/aliases | 0 | `matchCount=0`; response SHA-256 `5f0615...09c` |
| GitHub REST repository searches for `Aubin-Talenti Lean` and `sharp Sobolev Lean` | 0 | Both returned `total_count=0`, `incomplete_results=false` |
| GitHub REST code search for `Aubin-Talenti language:Lean` | 0 | Captured HTTP 401 response; SHA-256 `b7dbd1...e29e`; search lane blocked |
| GitHub immutable tree inspection of `formal-conjectures@b2e608...` | 1 | Complete 1204-entry tree had no Aubin/Talenti/Sobolev/Laplacian path; response SHA-256 `76fa3f...fc61` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1289` | 0 | rank 460, planned, theorem incomplete |

## Open integration gate

Proof work must construct the analytic bridges listed in `anchor-audit.json`, or pin an exact
external declaration. Any future external result needs immutable dependency and license review,
transitive proof-body and trust inspection, exact-type comparison, and successful local elaboration
before receiving proof credit.
