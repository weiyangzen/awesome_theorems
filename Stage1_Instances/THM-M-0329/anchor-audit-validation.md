# Anchor-audit validation

Item: `S56-M-0329-ANCHOR_AUDIT`  
Base revision: `106084d7f6343f3046dfb9e108503edbcdc86191`

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the Lax-Milgram
continuous equivalence and its application and uniqueness laws. `AnchorAudit.lean` constructs the
inverse image of the Riesz representative of an arbitrary continuous functional and proves that it
is the unique solution of the exact frozen target. This checks the argument order and does not add
symmetry, nontriviality, or a restricted datum. The kernel reports only `propext`,
`Classical.choice`, and `Quot.sound`.

The bounded external search found one other indexed Lean project,
`scottnarmstrong/DeGiorgi@4c1b3077d3782b24065184df4ba59501b2e56fc7`. Its existence-theory
module uses mathlib's same equivalence for a PDE application and is not a distinct proof of the
general root. GitHub code search required authentication, so that lane is recorded as blocked rather
than negative. Thus the audit proposes an `M0-W` mathlib candidate, but does not grant proof-phase or
theorem-completion credit.

## Commands and results

Commands ran on 2026-07-12 using only the existing pinned Lake artifacts. No update, build, clone,
fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard, assurance groups, and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0329` | 0 | rank 822, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0329/AnchorAudit.lean` | 0 | exact candidate adapter kernel-checked; axioms were `propext`, `Classical.choice`, `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0329/Statement.lean` | 0 | frozen canonical target and Riesz transport re-elaborated |
| `python3 Stage1_Instances/THM-M-0329/check_anchor_audit.py` | 0 | exact adapter, manifest pin, installed HEAD, source hash, inventory, and status boundary agreed |
| `git show` plus `rg` on pinned `LaxMilgram.lean` | 0 | no `sorry`, `admit`, axiom/unsafe declaration, or `proof_wanted` marker found |
| Sourcegraph alias query | 0 | exhaustive 14 matches in mathlib4 and DeGiorgi; response SHA-256 `7de38d9d...457e43b` |
| GitHub REST repository search | 0 | complete response, zero metadata matches; SHA-256 `08c082fd...2600b2` |
| GitHub REST code search | 0 | HTTP 401 authentication blocker; SHA-256 `9afb6c80...203c5bf` |
| GitHub immutable DeGiorgi tree and raw-file inspection | 0 | commit-bound 118-entry tree; downstream use confirmed; file SHA-256 `e6d48439...40936bf` |

## Status boundary

This completes only the bounded anchor-audit phase pending master acceptance. The obligation tree,
formal proof phase, transitive declaration-level trust closure, hermetic and independent validation,
readability and source gates, release receipt, full audit, and theorem completion remain open.
