# THM-M-0079 obligation-tree validation

Item: `S56-M-0079-OBLIGATION_TREE`. Base revision
`1944ddb6f503b699293e82f18d19efe0f32b4380`, tree
`e5004bc50d7e6fae75e8332fb00748a57e3bf622`.

Validation ran in the isolated worker clone on 2026-07-13. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points to the canonical pinned environment and was used
read-only. No `lake update`, `lake build`, clone, fetch, dependency write, or network validation was
run. Exact per-command timestamps and a reproducible full untracked-input manifest were not
captured. This dirty worker packet is nonrelease evidence.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0079` | 0 | rank 1105; planned; theorem_complete false |
| `python3 -B Stage1_Instances/THM-M-0079/build_obligation_artifacts.py --write` | 0 | wrote 39 obligations and 147 typed edges; denominator `88cf0ea4...6b92` |
| `python3 -B Stage1_Instances/THM-M-0079/build_obligation_artifacts.py --check` | 0 | deterministic registry, graph, and two aggregate validation-spec bytes match |
| `python3 -B Stage1_Instances/THM-M-0079/check_obligation_tree.py` | 0 | 39 obligations; 147 legal typed edges; readable anchors; reciprocal proof/transport edges; workflow reciprocity; open M3 root; temporary Statement olean and ObligationTree replay; Lean output SHA-256 `a30d1009...f9e8` |
| `python3 -m json.tool Stage1_Instances/THM-M-0079/instance.json /dev/null` | 0 | instance manifest parses |
| `python3 -m json.tool Stage1_Instances/THM-M-0079/obligation-registry.json /dev/null` | 0 | obligation registry parses |
| `python3 -m json.tool Stage1_Instances/THM-M-0079/typed-graphs.json /dev/null` | 0 | typed graph bundle parses |
| `python3 -m json.tool Stage1_Instances/THM-M-0079/validation-specs.json /dev/null` | 0 | validation specifications parse |
| `python3 -m json.tool Stage1_Instances/THM-M-0079/obligation-tree-receipt.json /dev/null` | 0 | node receipt parses |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0079-obligation-pycache python3 -m py_compile ...` | 0 | generator and checker compile outside the repository |
| prohibited-token `rg` scan over `ObligationTree.lean` | 1 (expected no match) | no sorry, admit, sorryAx, axiom declaration, unsafe, oracle, or placeholder marker |
| `git diff --check -- Stage1_Instances/THM-M-0079 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Checked boundary

The structural checker recomputes the frozen denominator and exact statement/anchor hashes; checks
all node fields and frozen semantic architecture ledgers (not R0 logical-step reconstructions);
validates separate proof, refinement, provenance, evidence, trust, documentation, and workflow
graphs; checks reciprocal proof and statement-
transport edges, proof acyclicity, root reachability, frozen registry parent/child identity maps
(the non-root values are explicitly planned-signature hashes, not elaborated Lean fingerprints),
exact type ascriptions for five local composition interfaces, task-obligation reciprocity, stable
readable anchors, and both aggregate structured recipes; and enforces empty accepted closure.

The Lean check first compiles `Statement.lean` to a temporary olean and then elaborates
`ObligationTree.lean` with that directory first in `LEAN_PATH`. Five graph-parent composition
interfaces elaborate: quotient connectedness, end/subgroup equivalence, quotient-end
specialization, terminal assembly, and root identity. Nine
deeper imported source parents remain explicitly
`planned_source_composition_pending_exact_child_harness`; no composition certificate or proof
credit is claimed for them. The module imports the audited Nielsen-Schreier source so its interfaces
can be checked, but never applies `subgroupIsFreeOfIsFree` to close the root.

The mathematical architecture frontier contains 13 obligations. `M0079-S-FOUNDATION` is the
separate required machine-assurance frontier node. The one-step architecture records are not
section 6.6 substantive leaf-proof ledgers or verified step budgets. The root stays
`[H1, M3, R4]`, accepted obligations and receipt IDs stay empty, and both audit and theorem
completion stay false. The first gate is integration-lane
acceptance of the provisional anchor prerequisite and then this worker receipt. Proof integration,
the remaining composition harnesses, H0, R0, full provenance/trust, hermetic and independent
validation, `AUDIT-Z`, `THEOREM-Z`, release, and master acceptance remain open.

The prerequisite receipt is hash-bound as provisional input. Its historical worker checker is
base-revision-specific and is not replayed against this later integration commit; the obligation
checker instead verifies the integrated anchor JSON, statement, receipt hash, and authoritative
dependency edge. Master acceptance of that prerequisite remains the first gate.
