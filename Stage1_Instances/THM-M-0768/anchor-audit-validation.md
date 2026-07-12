# Anchor-audit validation record

Item: `S56-M-0768-ANCHOR_AUDIT`  
Base revision: `c72bad9e8827ffb1ba1a585dbe346c88393b4a3f`  
Audit date: 2026-07-12 (`Asia/Shanghai`)

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact candidate
`Function.Embedding.schroeder_bernstein`. Its raw-function binders, two injectivity hypotheses,
universe polymorphism, and existential bijection conclusion match the frozen target. The checked
local wrapper `pinnedSchroederBernstein` elaborates, and machine axiom reports for both the wrapper
and terminal library declaration list only `propext`, `Classical.choice`, and `Quot.sound`; neither
report contains `sorryAx`.

The terminal source route is also identified: `schroeder_bernstein` specializes
`schroeder_bernstein_of_rel` to the always-true relation. The latter constructs a piecewise map
from the least fixed point of a monotone set operator. The module is bound to its immutable commit,
tree, blob, source hash, three direct imports, and Apache-2.0 license hash.

Two public repositories were inspected at full commits. Both are Lean 3 projects rather than Lean
4 dependencies. `brunorochapaiva/schroeder_bernstein@ef34c92...a77` states the exact theorem but its
terminal body is `sorry`. `ccobb1/lean-cantor-bernstein@3d18117...8e9` has a substantive exact Lean
3 proof without an obvious placeholder, but it has no declared license or Lean 4 compatibility.
Neither improves on the exact pinned mathlib candidate, and neither receives integration credit.

This completes the bounded anchor-audit phase pending master acceptance. The exact mathlib route is
classified as an `M0-W candidate`, not as accepted root closure: the authoritative planned instance
remains `M3` until later obligation, proof, provenance, and master gates consume this evidence.
Full audit completion and theorem completion remain false.

## Commands and exact outcomes

All Lean commands used the existing pinned Lake environment. No Lake update/build, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0768` | 0 | rank 778, planned, legacy artifacts unaccepted, theorem incomplete |
| scoped `rg` over repo-local and pinned mathlib sources | 0 | exact mathlib module/declarations found; no separate repo-local proof body found |
| GitHub REST repository searches for four aliases | 0 | two Lean 3 repositories located; two narrower metadata queries returned zero |
| GitHub REST code search for `schroeder_bernstein language:Lean` | 0 | response recorded as HTTP 401 access failure; no negative result claimed |
| immutable GitHub API/raw reads for both external repositories | 0 | full commits, trees, toolchains, mathlib pins, declarations, source hashes, and placeholder boundaries inspected |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0768/AnchorAudit.lean` | 0 | exact wrapper and three candidates elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0768/check_anchor_audit.py` | 0 | exact target fingerprint, clean mathlib pin/tree, module hash, five candidates, and fail-closed state boundary agreed |
| `python3 -m json.tool Stage1_Instances/THM-M-0768/anchor-audit.json` | 0 | structured audit ledger parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0768 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

`anchor_audit_phase_complete=true`, while `audit_complete=false`, `theorem_proved=false`, and
`theorem_complete=false`. No H0 source review, frozen obligation architecture, accepted proof node,
hermetic replay, independent review, `AUDIT-Z`, or `THEOREM-Z` is claimed.
