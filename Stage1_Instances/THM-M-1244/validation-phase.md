# THM-M-1244 validation-phase result

Item `S56-M-1244-VALIDATION` was run against base revision
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`. The exact frozen Gaussian
log-Sobolev target, package composition, vendored terminal theorem, proof root,
and a reconstruction without the `Proof` module replay at Lean trust level
zero. Lean recursively reports all seven checked declarations sorry-free and
observes no axioms outside `propext`, `Classical.choice`, and `Quot.sound`.

This is provisional nonrelease evidence, not theorem completion. The proof
predecessor remains `[_]`; the authoritative frozen graph still records `M4`,
`root_closed=false`, and cut set `M1244-L-UPSTREAM`/`M1244-L-INTEGRAL`.

## Validation method

`check_validation.sh` copies the owned Lean closure into a fresh `/tmp`
directory. Each Lean process runs with `--trust=0 -t0` inside Bubblewrap with
an unshared network namespace, read-only host root, fixed locale/timezone/thread
count, and only that temporary directory writable. It elaborates the statement,
all 24 vendored modules, and the proof into fresh temporary objects; it never
runs `lake update`, `lake build`, clone, fetch, or any dependency mutation.

`ProofAudit.lean` uses Lean's recursive `assert_no_sorry` and `#print sorries`
commands, then prints axiom closures. Before `Validation.lean` runs, the runner
removes both `Proof.lean` and `Proof.olean`. The latter reconstructs the
measure, entropy, regularity, coordinate-energy, package, and exact-root route.
That is differential same-worker evidence, not a distinct verifier.

## Gate decisions

| Gate | Decision | Evidence or boundary |
|---|---|---|
| Exact kernel replay | provisional pass | Frozen target, composition, vendored terminal, local packages, proof root, and reconstructed root elaborate at trust zero. |
| Placeholder/unsafe audit | pass | Seven recursive kernel sorry checks plus a comment-aware prohibited-construct scan pass. |
| Axiom observation | provisional pass | Checked declarations stay within `propext`, `Classical.choice`, and `Quot.sound`; foundation-policy acceptance and complete TCB review remain open. |
| Selected provenance | provisional pass | Local/vendored hashes, upstream revision, clean pinned mathlib revision/tree/remote/license, three pivotal source blobs/oleans, and tool hashes agree. |
| Proof dependency | fail closed | `S56-M-1244-PROOF` is provisional and lacks dependency-ordered master acceptance. |
| Structured state | fail closed | The frozen graph predates proof closure and remains `M4`/open; workers cannot reconcile it or accept the four remaining statement/foundation obligations. |
| Hermetic release replay | fail closed | Lean is network-isolated and host inputs are read-only, but dependencies are shared and warm rather than a clean empty-cache build from an offline-restorable archive. |
| Independent verification | fail closed | The reconstruction uses the same theorem route, worker identity, checkout, kernel, vendored modules, and cache; no second signed runner or minimal independent verifier exists. |
| Source/readability | fail closed | Primary-source `H0` and independently reviewed `R0` remain open. |

## Commands and results

Commands were run from the repository root on `2026-07-15`.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1244` | 0 | Rank 425, planned, theorem incomplete. |
| `bash Stage1_Instances/THM-M-1244/check_validation.sh` | 0 | Network-isolated trust-zero replay passed; its emitted audit/reconstruction output contains seven sorry-free and seven axiom reports. |
| `python3 -B Stage1_Instances/THM-M-1244/check_validation.py` | 0 | Hash, pin, graph, receipt, trust, provenance, scoped-status, and fail-closed boundary checks passed. |
| `python3 -m json.tool` on the validation spec, receipt, and worker packet | 0 | All three JSON artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1244 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The first node gate that remains closed is
`dependency.S56-M-1244-PROOF.master_acceptance`. The first release gate is
`S56-10.6-HERMETIC-COLD-BUILD`. Therefore `audit_complete=false` and
`theorem_complete=false`; no accepted debt-vector or theorem state changes.
