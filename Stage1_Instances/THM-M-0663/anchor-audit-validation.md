# Anchor-audit validation

Validation date: 2026-07-12 (Asia/Shanghai). Worker base revision:
`5db470f65548af5e1bcabfd26264a5b038ab1023`.

The existing untracked `Formalizations/Lean/.lake` link/artifact was used read-only. No `lake
update`, build, dependency clone, dependency fetch, or other `.lake` mutation was run. External
projects were inspected through `git ls-remote`, raw immutable files, and source archives fixed by
40-character Git revisions; archives were kept outside the repository and were not dependencies.

## Candidate result

Pinned mathlib provides the definability, ordered-structure, order-convexity, continuity, and strict
monotonicity vocabulary used by `Statement.lean`, but no o-minimal predicate or finite definable
monotonicity partition theorem. Three focused public GitHub candidates were found and audited at
immutable revisions. None closes the canonical statement: one is a placeholder-heavy partial
exercise collection, one exposes local real monotonicity through an assumed structure field, and
one concerns only o-minimality of the pure real order and has placeholder-bearing imports.

Exact candidate revisions, archive hashes, toolchains, declaration/body findings, and integration
decisions are recorded in `anchor-audit.json`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0663` | exit 0; rank 707, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'o.?minimal\|ominimal\|monotonicity theorem' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0 due incidental “minimal” matches; manual review found no o-minimal declaration or target theorem |
| focused GitHub repository API searches for the query families in `anchor-audit.json` | exit 0; union was exactly the three audited repositories |
| `git ls-remote https://github.com/theominimalist/monotonicity.git HEAD` | exit 0; `6e3ee129f0d9cc0d9d6a58cac4fc03bc7b121b30` |
| `git ls-remote https://github.com/tonysf/lean-OMIN.git HEAD` | exit 0; `fd8b4f3423265d9beb290a08992ad866eb5230e0` |
| `git ls-remote https://github.com/KittySaya/Lean-ominimal.git HEAD` | exit 0; `4429c2cc75e49a83043175f7a85c4c1bf284c2eb` |
| download each `https://github.com/OWNER/REPO/archive/REV.tar.gz`, then `sha256sum` | exit 0; hashes `9a7d3a...c603`, `38b2c5...c012`, `37a5cf...c9f` as fully recorded in JSON |
| complete-tree `rg` scans for declarations, `sorry`, `axiom`, `admit`, monotonicity, and o-minimality in the three extracted archives | exit 0; findings and exact counts recorded in JSON |
| `python3 Stage1_Instances/THM-M-0663/check_anchor_audit.py` | exit 0; `anchor audit invariant check: ok` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0663/AnchorAudit.lean` | exit 0; all pinned API probes elaborate |
| `python3 -m json.tool Stage1_Instances/THM-M-0663/anchor-audit.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0663 .stage1-worker-selftest.json` | exit 0; no output |

## Status boundary

This is self-tested anchor-audit evidence pending master acceptance. It establishes a bounded,
immutable candidate inventory and an honest `M3` formalization-debt classification. It supplies no
proof body, no external proof credit, no obligation-tree receipt, no complete theorem audit, and no
theorem-completion evidence.
