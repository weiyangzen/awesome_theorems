# Anchor-audit validation record

Item: `S56-M-0510-ANCHOR_AUDIT`  
Base revision: `e9d545372b66f73be63271b2fb408ef134d1d6f7`

## Result

The exact repo-local artifact is only the proposition definition
`Stage1Instances.THM_M_0510.HardyRamanujanAsymptoticTarget`, so it remains an `M3` statement
candidate and earns no proof credit. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the ordinary partition type, a general
weighted generating function and its infinite-product theorem, `Asymptotics.IsEquivalent`, and
the real exponential and square root. All nine anchors elaborate in `AnchorAudit.lean`.

No pinned mathlib declaration proves the full constant-factor Hardy-Ramanujan asymptotic. Indeed,
`Mathlib.Combinatorics.Enumerative.Partition.GenFun` explicitly labels even the specialization of
its general generating function to the ordinary partition function as a TODO. That specialization
would itself still be only upstream infrastructure, not the required asymptotic theorem.

No exact external Lean 4 proof candidate was located. Four complete GitHub repository searches
returned zero repositories. Unauthenticated GitHub code search returned HTTP 401; Sourcegraph
returned `no route`; and grep.app returned a security checkpoint, so those three lanes are recorded
as blocked rather than falsely credited as negative. The complete 1204-entry tree of
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` contains only
unrelated Hardy-Littlewood, Ramanujan tau, and set-theory partition paths under the broad search.

The root therefore stays `[H2, M3, R4]`. This bounded formal-anchor inventory is complete for the
assigned node, but it is not proof closure, a global nonexistence claim, or full audit completion.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Lean used only existing pinned `.lake` artifacts;
no dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0510/AnchorAudit.lean` | 0 | Nine pinned mathlib infrastructure declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0510/Statement.lean` | 0 | Canonical target and checked statement transports re-elaborated |
| `python3 Stage1_Instances/THM-M-0510/check_anchor_audit.py` | 0 | Audit boundary, nine probes, GenFun TODO, manifest pin, and checked-out mathlib HEAD agreed |
| `rg -n -i 'Hardy.?Ramanujan\|partition function\|partition.*asympt\|asympt.*partition' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Archive --glob '*.lean'` | 0 | Only the GenFun module's partition-function documentation matched; no Hardy-Ramanujan/asymptotic declaration |
| `rg -n '\\bsorry\\b\|\\badmit\\b\|\\baxiom\\b\|unsafe\|implemented_by' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/Enumerative/Partition/GenFun.lean` | 1 | No placeholder, explicit axiom, unsafe, or oracle token; exit 1 is ripgrep's expected no-match status |
| GitHub REST repository searches for `"Hardy-Ramanujan" Lean`, `"partition function" Lean4`, `integer partitions Lean`, and `partition asymptotic Lean` | 0 | Each returned `total_count=0`, `incomplete_results=false`; each response SHA-256 `08c082...00b2` |
| GitHub REST code search for `"Hardy-Ramanujan" language:Lean` | 0 | Response captured; HTTP 401 authentication blocker; SHA-256 `b7dbd1...29e` |
| Sourcegraph and grep.app code searches for Lean aliases | 0 | `no route` and Vercel checkpoint respectively; recorded only as blocked lanes |
| GitHub commit-tree query for `google-deepmind/formal-conjectures@b2e608...` plus `jq`/`rg` | 0 | Complete, non-truncated 1204-entry tree; no target path; response SHA-256 `76fa3f...c61` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0510` | 0 | Rank 884; planned; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0510` | 0 | No whitespace errors |

## Open integration gate

Reopen integration only after finding a repository URL, immutable commit, Lean toolchain, module,
declaration, license, exact normalized type, and terminal proof body. It must then pass placeholder,
axiom, unsafe/oracle, provenance, and repo-local wrapper checks. Until then, there is no external
closure to integrate and no `M0-P`, `M1`, or theorem-completion credit.

