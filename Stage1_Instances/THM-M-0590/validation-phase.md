# THM-M-0590 validation-phase evidence

Item: `S56-M-0590-VALIDATION`

Base revision: `e73a459aa33f8b656019c9c36e3d5dfc84dffc30`

Base tree: `81105927f8e46d0076dd20433240ecf0fd185cea`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Verdict

`blocked`, with a self-tested negative validation packet proposed as `[_]`.
The node recipe freshly elaborates `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and `Validation.lean` under Lean `--trust=0`. Each Lean process
runs inside a disposable writable directory with a read-only host root, fixed
cleared environment, one thread, and an unshared network namespace. The nine
audited proof, composition, and differential declarations are sorry-free and
report exactly `propext`, `Classical.choice`, and `Quot.sound`.

This does not validate the Brown-Douglas-Fillmore theorem. The proof receipt is
provisional and closes no frozen obligation. The only root adapters consume
the forward and backward classification packages as explicit premises, and
neither package has a terminal proof body. The first failed gate is therefore
`dependency.S56-M-0590-PROOF.master_acceptance_and_exact_root_closure`. The
root remains `[H1, M4, R3]`; `audit_complete=false` and
`theorem_complete=false`.

## Gate Decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact statement and checked declarations | narrow nonrelease pass | The exact Prop target, conditional composition, five partial proof bodies, and three same-worker differential probes freshly elaborate under `--trust=0`. |
| Placeholder and unsafe hygiene | pass for audited sources and closure | Comment-aware source scanning, `assert_no_sorry`, Lean sorry reports, and closure inspection find no prohibited construct, bodyless nonaxiom, or unsafe declaration. |
| Trust observation | narrow nonrelease pass | Machine-derived axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no accepted foundation policy or complete TCB is inferred. |
| Selected provenance | narrow nonrelease pass | Frozen source hashes, tool identities, clean pinned mathlib revision/tree/origin/license, and compact-operator/adjoint source/blob/olean boundaries agree. |
| Proof dependency and exact root | fail closed | The proof phase is provisional, closes zero frozen obligations, and contains neither directional package nor a premise-free root. |
| Complete trust and provenance | fail closed | No accepted foundation profile, complete serialized transitive proof-body/import graph, compiler/bootstrap/plugin TCB, SBOM, or supply-chain archive exists. |
| Hermetic reproduction | fail closed | The network-isolated replay reuses the canonical shared warm `.lake`; it is not a new immutable checkout, empty-cache cold build, or offline archive restoration. |
| Independent verification | fail closed | The differential checks run in this worker with the same checkout, Lean binary, and warm cache; there is no second signed identity, independent runner, or independent minimal verifier. |

## Commands And Results

No command ran `lake update`, `lake build`, dependency clone/fetch, or modified
`.lake`. Generated Lean objects existed only under `/tmp` and were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Rank 630, planned hard-statement-first lane, legacy artifacts unaccepted, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | 17 obligations and 37 typed edges passed; denominator `2d5b17d...9a9e8`; the forward and backward packages and root remained open M4. |
| `Stage1_Instances/THM-M-0590/check_proof.sh` | 0 | The exact statement, conditional composer, and five partial proof bodies elaborated through pinned `lake env lean --trust=0 -t0`; final line `PASS THM-M-0590 partial proof bodies`. |
| `python3 -I -B Stage1_Instances/THM-M-0590/check_validation.py` | 0 | Network-isolated trust-zero replay, source hygiene, authority/closure checks, selected provenance, exact axiom reports, blocker, receipt, and worker-packet invariants passed; unavailable root/release gates failed closed. |
| `python3 -m json.tool` on the validation spec, receipt, blocker, and worker packet | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0590-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0590/check_validation.py` | 0 | Validator syntax compiled without writing in the dossier. |
| `git diff --check -- Stage1_Instances/THM-M-0590 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Retry Condition

Implement or pin exact placeholder-free proofs of `M0590-B-FORWARD` and
`M0590-T-BACKWARD` plus their missing Calkin/Atkinson, spectrum/index, Busby,
extension-classification, and index-completeness dependencies. After proof
master acceptance and accepted source/readability/foundation/provenance
records, replay an immutable clean snapshot from empty caches with an offline
archive, deterministic bundle, two signed independent runners, and an
independently implemented minimal verifier.

This packet supports only truthful negative validation implementation. It is
not an accepted validation result, exact root proof, `M0`/`E0`/`E1`, audit or
theorem completion, release, or master acceptance.
