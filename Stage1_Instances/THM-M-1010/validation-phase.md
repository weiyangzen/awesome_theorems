# THM-M-1010 validation-phase evidence

Item: `S56-M-1010-VALIDATION`

Base revision: `fd995645725ec3633e4da7e6d759deb14f530861`

Base tree: `5846121ab94ff0502b98217f643539881bc9c045`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Verdict

`blocked`, with a self-tested negative validation packet proposed as `[_]`.
The node recipe freshly elaborates `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and the validation audit under Lean `--trust=0`. Every Lean
process runs inside a fresh writable `/tmp` directory with a read-only host
root, fixed cleared environment, one thread, and an unshared network
namespace. All four audited proof/composition declarations are sorry-free and
report exactly `propext`, `Classical.choice`, and `Quot.sound`; their combined
closure contains no bodyless nonaxiom and no unsafe declaration.

This does not validate the Skorokhod theorem. The proof receipt is provisional,
closes zero frozen obligations, and explicitly reports
`root_kernel_closed=false`. `exists_common_space_exact_marginals` realizes the
prescribed laws using an independent product construction but supplies no
almost-sure convergence. The other two proof declarations cover only constant
law sequences. `target_of_couplingPackage` is a conditional composer whose
`CouplingPackage` premise remains uninhabited.

The first failed gate is
`dependency.S56-M-1010-PROOF.master_acceptance_and_exact_root_closure`. The
accepted vector remains `[H1, M3, R3]`, with `audit_complete=false` and
`theorem_complete=false`.

## Gate Decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact statement and checked declarations | narrow nonrelease pass | The frozen statement, conditional composer, and three partial declarations freshly elaborate under `--trust=0`; no unconditional root body exists. |
| Placeholder and unsafe hygiene | pass for audited closure | Parser-aware source scanning, `assert_no_sorry`, Lean sorry reports, bodyless-nonaxiom traversal, and unsafe traversal pass. |
| Trust observation | narrow nonrelease pass | Machine-derived axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no accepted foundation policy or complete TCB is inferred. |
| Selected provenance | narrow nonrelease pass | Frozen source hashes, tool identities, clean pinned mathlib revision/tree/origin/license, and `HasLaw`, `HasLawExists`, and `LevyProkhorovMetric` source/blob/olean boundaries agree. |
| Proof dependency and exact root | fail closed | The proof phase is provisional, closes zero frozen obligations, and contains neither `Target` nor `CouplingPackage`; the five-node root cut is open. |
| Complete trust and provenance | fail closed | No accepted foundation profile, serialized complete transitive proof-body/import graph, full compiler/bootstrap/plugin TCB, SBOM, or supply-chain archive exists. |
| Hermetic reproduction | fail closed | The network-isolated replay reuses the canonical shared warm `.lake`; it is not a new immutable checkout, empty-cache cold build, or offline archive restoration. |
| Independent verification | fail closed | The audit runs in this worker with the same checkout, Lean binary, and warm cache; there is no second signed identity, independently provisioned runner, or independent minimal verifier. |

## Commands And Results

No command ran `lake update`, `lake build`, dependency clone/fetch, or modified
`.lake`. Generated Lean objects existed only under `/tmp` and were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290, planned hard-mathlib anchor/wrapper lane, legacy artifacts unaccepted, theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `8cf08f66...16016`; the root remained open M3 on the five-node cut. |
| `python3 -I -B Stage1_Instances/THM-M-1010/check_validation.py --probe` | 0 | Network-isolated trust-zero replay passed; closure roots `4`, declarations `27818`, modules `1019`, no bodyless nonaxioms or unsafe declarations; observed axioms exactly the three listed above. |
| `python3 -I -B Stage1_Instances/THM-M-1010/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | Exact input, authority, root boundary, hygiene, tool, pin, selected provenance, kernel/trust, receipt, blocker, and worker-packet assertions passed. |
| `python3 -m json.tool` on the validation spec, receipt, blocker, and worker packet | 0 | All structured artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1010 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Retry Condition

Implement and master-accept the five missing Skorokhod leaves and their exact
composition into `Target`; close the foundation, complete provenance, source,
and readability records; then replay an immutable clean snapshot from empty
caches with offline-restorable dependencies and obtain a distinct signed
attestation from an independently provisioned verifier using an independently
implemented minimal checker.

This packet supports only truthful negative validation implementation. It is
not an accepted validation result, exact root proof, `M0`/`E0`/`E1`, audit or
theorem completion, release, or master acceptance.
