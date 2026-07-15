# S56-M-0320-VALIDATION worker evidence

Item: `S56-M-0320-VALIDATION`

Base revision: `63a9ed9c4aae594da31423142b0658129d5452a7`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Scope and result

The structured recipe replayed fresh source outputs for the canonical statement, frozen
composition, graph bridge, three-module MIT Brouwer closure, proof core and exact root under pinned
Lean 4.29.0 with `--trust=0 -t0`. A separate `TrustAudit.lean` asked Lean for sorry and axiom
reports on eight selected local and vendored declarations. The exact root reported only `propext`,
`Classical.choice`, and `Quot.sound`; source hygiene and selected provenance checks also passed.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. It independently restates the graph
and core interfaces, re-proves the upper-hemicontinuity closed-graph bridge, and conditionally
recomposes the canonical target. The Kakutani core remains an explicit premise, so this is not a
second root proof or independent release verification.

This node is self-tested only as provisional, nonrelease evidence. Every predecessor is `[_]`, the
target-local task DAG and typed graph predate the proof candidate, and the accepted root remains
`H1/M4/R4`. No obligation closure or receipt is accepted here. The statement also lacks an accepted
independently recomputed normalized expression fingerprint.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0320` | 0 | Rank 686, planned, L0/rework-required, theorem incomplete. |
| `timeout 8 lake env lean --version` from `Formalizations/Lean` | 124 | Lake tried to resolve the incomplete manifest-pinned `flt-regular` checkout and timed out; the worker did not fetch, repair, build, remove, or mutate `.lake`. |
| `python3 Stage1_Instances/THM-M-0318/build_vendor_manifest.py` | 0 | Three modules and 182363 bytes passed reversible-port verification; patch SHA-256 `39fff43f...8790`. |
| `python3 Stage1_Instances/THM-M-0320/check_anchor_audit.py` | 0 | Anchor status boundary, seven probes, and pinned mathlib revision passed. |
| `python3 Stage1_Instances/THM-M-0320/check_obligation_tree.py` | 0 | Ten obligations and 22 typed edges passed; the frozen graph truthfully remained root-open. |
| Structured recipe with `STAGE1_SKIP_RECEIPT_CHECK=1` and `--probe` | 0 | Network-isolated fresh-output replay passed; output hashes are bound in `validation-receipt.json`. |
| Final structured recipe from `validation-spec.json` | 0 | Receipt, packet, kernel/trust/provenance observations, and every fail-closed decision passed. |
| `python3 -m json.tool` on spec, receipt, and worker packet | 0 | All JSON artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0320-validation-pycache python3 -m py_compile .../check_validation.py` | 0 | Validator syntax passed without writing the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0320 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |

Bubblewrap encloses the complete structured recipe, mounts the host read-only, provides a private
`/tmp`, and denies the network. The successful replay uses the digest-checked installed pinned Lean
binary with explicit existing compiled paths because the canonical Lake resolver is blocked. This
is stronger than a plain warm build but is still not the section 10.6 protocol: the checkout is
dirty, dependencies and oleans are shared and warm, caches are not empty, and there is no
offline-restorable SBOM/TCB archive.

## Gate decisions

| Gate | Decision | Boundary |
|---|---|---|
| Narrow kernel and placeholder replay | Provisional pass | Exact proof root elaborated at trust zero and selected declarations were sorry-free. |
| Selected provenance | Provisional pass | Local hashes, reversible vendor port, immutable upstream identities, MIT license, tools, and clean pinned mathlib agree. |
| Authority and expression identity | Fail closed | Predecessors are provisional, authority records are stale, and no accepted normalized expression fingerprint exists. |
| Complete foundation, provenance, and TCB | Fail closed | Accepted axiom policy, transitive declaration/artifact closure, TCB inventory, and SBOM are absent. |
| Hermetic release reproduction | Fail closed | Shared warm dependencies, blocked Lake resolution, dirty checkout, and no cold offline restoration. |
| Independent verification | Fail closed | Same worker/cache; conditional probe does not prove the core; no distinct signed runner or independent minimal verifier. |

The first node gate is `dependency.S56-M-0320-PROOF.master_acceptance`; the first release gate is
the section 10.6 cold empty-cache build. `audit_complete=false` and `theorem_complete=false`.
