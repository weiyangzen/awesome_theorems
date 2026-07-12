# Intake validation record

Base revision: `73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1269` | 0 | rank 445, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1269/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\bsorry\b|\baxiom\b|\bplaceholder\b' Stage1_Instances/THM-M-1269` (inside a fail-on-match shell check) | 1 | Overbroad hygiene check found the truthful prose phrase `axiom audit`; this was a check-design failure, not a proof marker |
| `find Stage1_Instances/THM-M-1269 -name '*.lean' -print -quit` | 0 | empty output: the intake introduces no Lean proof file, so proof-marker scanning is not applicable |
| `git diff --check -- Stage1_Instances/THM-M-1269 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean theorem is
introduced, so no kernel result is claimed. Primary-source identification,
exact statement elaboration, master acceptance, and every dependent phase
remain outstanding.

## Statement validation record

Statement-phase base revision: `8da22023e24f307fb21f41ed93f69f2b8fa82879`.
The existing `.lake` path is a worker-clone symlink to the canonical pinned
artifacts; no dependency update, fetch, build, or mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1269` | 0 | rank 445, planned, hard-mathlib-anchor lane, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1269/Statement.lean)` | 0 | Lean printed the four proposition types and the canonical normalized body; no elaboration errors |
| `python3 -m json.tool Stage1_Instances/THM-M-1269/statement.json >/dev/null && python3 -m json.tool Stage1_Instances/THM-M-1269/intake.json >/dev/null` | 0 | statement record and reconciled intake are valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1269 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The normalized body printed by Lean is
`fun X F => Nonempty X -> BddBelow (range F) -> exists sequence, Tendsto
(fun n => F (sequence n)) atTop (nhds (sInf (range F)))` (with Lean's Unicode
syntax in the actual output). Its whitespace-normalized UTF-8 serialization has SHA-256
`2400402b5b59e3d5e0f3dfebf1a67101fdac06364114b48f9ef5d5d0be6c4516`.
The mutations ensure the omitted hypotheses and the stronger attainment claim
remain visibly distinct proposition surfaces; they are not proofs or accepted
counterexamples. Statement elaboration is self-tested, while proof closure and
master acceptance remain open.

## Anchor-audit validation record

Anchor-audit base revision: `4197281122e0165098f43f0b967905d0378ee2db`.
The `.lake` path remained the existing symlink to canonical pinned artifacts;
no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n "exists_seq_tendsto_sInf\|minimizing sequence\|minimizingSequence\|sInf.*Tendsto\|Tendsto.*sInf" ...` over repo-local Lean/Markdown and then all pinned packages | 0 | mathlib definition plus one mathlib use; no independent exact repo-local or pinned-external theorem |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1269/AnchorAudit.lean)` | 0 | exact-shape wrapper elaborated; candidate type printed; axioms `[propext, Classical.choice, Quot.sound]` |
| `curl ... grep.app ...` | 22 | HTTP 429; public external search inconclusive, no proof credit |
| `curl ... api.github.com/search/code ...` | 22 | HTTP 403; unauthenticated external search inconclusive, no proof credit |
| `python3 -m json.tool Stage1_Instances/THM-M-1269/anchor_audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent: 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | ordered target manifest consistent |
| `git diff --check -- Stage1_Instances/THM-M-1269 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The smallest kernel-relevant audit check is the scoped Lean wrapper. The two
network failures are known limitations, not candidate evidence. The immutable
mathlib result is sufficient to finish the assigned candidate audit, while
proof installation and every later theorem gate remain open.

## Obligation-tree validation record

Obligation-tree base revision: `883205204cea57181965a9de9620f3c150aaf2e8`.
The existing `.lake` path remained the worker-clone link to canonical pinned
artifacts. No dependency update, build, clone, fetch, or mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1269/build_obligation_artifacts.py` | 0 | generated registry/graph/spec artifacts; denominator SHA-256 `12c3255b53f7432b3ca2e00b712901bb20da2f20429a047c1444ca1d79278efa` |
| `python3 Stage1_Instances/THM-M-1269/check_obligation_tree.py` | 0 | `PASS`: 14 obligations, all required node fields and ledgers, 23 legal typed reciprocal/indexed edges, acyclic root proof reachability, matching recipes, open root boundary |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1269/ObligationTree.lean)` | 0 | conditional exact-root composition elaborated; axioms `[propext, Classical.choice, Quot.sound]` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | ordered manifest consistent: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1269` | 0 | rank 445, planned, hard-mathlib-anchor lane, theorem incomplete |
| `python3 -m json.tool` on the registry, graph bundle, and validation specs | 0 | all three structured artifacts are valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1269 .stage1-worker-selftest.json` | 0 | no whitespace errors |

An initial Lean attempt imported the sibling as `Statement` and exited 1
because that out-of-project file is not a module on the pinned Lake search
path. The scoped check was corrected by repeating the already frozen canonical
definition locally; no dependency artifact or search path was changed.

The frozen minimal root cut is `M1269-L-SINF`. The pinned anchor and exact
wrapper are audited, but this architecture phase does not install accepted
proof evidence. Root debt remains `M1`, human debt `H2`, readability debt
`R3`, and both audit and theorem completion are false pending later phases and
master acceptance.
