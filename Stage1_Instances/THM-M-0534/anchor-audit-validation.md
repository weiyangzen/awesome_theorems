# Anchor-audit validation record

Item: `S56-M-0534-ANCHOR_AUDIT`  
Base revision: `9a5088a76a8219c7df161c5dbaeb2de32d6ce742`

## Result

Pinned mathlib supplies the connecting morphism, both zero-composition lemmas, and the three
exactness declarations that match every family in the frozen target. Narrow adapters elaborate at
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; Lean reports the axiom set
`propext`, `Classical.choice`, and `Quot.sound` for each exactness theorem.

The candidate is `M1`, not `M0`: obligation-tree and proof phases must still create and compose a
THM-M-0534-owned root wrapper. Full transitive declaration/proof-body identity, accepted foundation
and TCB evidence, hermetic replay, and independent validation remain later gates. The exact wrapper
under `THM-M-0001` is useful repo-local precedent but cannot transfer proof credit between owned
targets. The older `S1_M_096` wrapper covers one adjacent window rather than the universally indexed
root.

Anonymous GitHub repository queries returned zero candidates. GitHub code search was rate-limited
with HTTP 403 and grep.app returned a security checkpoint with HTTP 429, so exhaustive discovery is
not claimed.

## Commands and results

All commands ran in this worker clone. Lean used the existing pinned Lake environment from
`Formalizations/Lean`. No update, build, fetch, clone, or other dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0534/AnchorAudit.lean` | 0 | six declarations typechecked; three exact-position adapters elaborated; all three exactness declarations reported `[propext, Classical.choice, Quot.sound]` |
| `lake env lean ../../Stage1_Instances/THM-M-0534/Statement.lean` | 0 | frozen target and checked regrouping transport still elaborate |
| `python3 ../../Stage1_Instances/THM-M-0534/check_statement.py` | 0 | canonical expression SHA-256 `6846afc...b7677`; all four structural mutations distinguished |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0534` | 0 | rank 591, planned, legacy artifacts unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a1783...a95`; tree `bdc39a...c2b` |
| `sha256sum` on mathlib source, license, and two repo-local candidates | 0 | values recorded in `anchor-audit.json` |
| scoped `rg` placeholder/trust-token scan | 0 | no matches in `HomologySequence.lean` or the exact repo-local wrapper |
| three GitHub repository API queries | 0 | HTTP 200 and zero results; response hash recorded |
| GitHub code search / grep.app search | 0 | curl completed; endpoints returned HTTP 403 / HTTP 429, recorded as access failures |
| `python3 -m json.tool Stage1_Instances/THM-M-0534/anchor-audit.json` | 0 | audit JSON parsed |
| `git diff --check -- Stage1_Instances/THM-M-0534 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This packet completes only the assigned formal-candidate anchor audit, pending master acceptance.
It proposes no accepted receipt and does not claim audit completion, theorem proof, `M0`, `H0`,
`R0`, hermetic validation, independent verification, or theorem completion. The next dependency is
`S56-M-0534-OBLIGATION_TREE`.
