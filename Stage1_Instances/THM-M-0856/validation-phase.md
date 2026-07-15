# THM-M-0856 validation-phase evidence

Item: `S56-M-0856-VALIDATION`. Base revision:
`9d50d838c8132b2aaf005a4863baeb5385e52a97`; base tree:
`ef268baf236c1fe55806a57847c7f78ed6587b9d`.

## Validation scope

The node recipe re-elaborates the exact frozen statement, root adapter and composition, proof
wrappers, and a separately written exact-target probe in temporary output space. Every Lean
subprocess runs at `--trust=0` in a Bubblewrap network namespace with the host filesystem read-only
except for the temporary directory. `Validation.lean` imports neither `Proof` nor `ObligationTree`;
it reconstructs `TutteOneFactorTarget` directly from pinned `SimpleGraph.tutte`. This is same-worker
differential corroboration, not an independent-runner attestation or a second proof body.

The pinned terminal, proof declarations, and differential target are sorry-free and report exactly
`propext`, `Classical.choice`, and `Quot.sound`. The validator binds the canonical expression,
registry denominator, predecessor receipt and graph hashes, mathlib revision/tree, clean dependency
checkout, terminal source/blob/body/olean, license, and tool identities. A comment-stripped scan
finds no placeholder, bodyless declaration, unsafe/native/oracle, or external implementation
mechanism in the four target Lean modules or terminal body region.

This is narrow, nonrelease validation. The proof prerequisite is only `[_]`; accepted authority
remains `[H1, M3, R4]` with no accepted receipt or closed obligation. Sixteen internal source-body
decomposition plans lack abstract-child composition certificates and receive no individual closure
credit.

## Commands and results

Commands ran from this worker clone on 2026-07-15 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch/checkout,
dependency mutation, or network operation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0856
  exit 0: rank 1410, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0856/check_validation.sh
  exit 0: the entire recipe ran inside a denied-network Bubblewrap namespace; trust-zero statement,
  root composition, exact proof roots, and Statement-only differential root elaborated; every
  covered axiom report was exactly [propext, Classical.choice, Quot.sound]; stdout was 985 bytes at
  SHA-256 9ee0e273e3a14a918a39712b361aa6b739194ec069be88d8e420aee1e0d2bb0f;
  stderr was empty at SHA-256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

bash Stage1_Instances/THM-M-0856/check_proof.sh
  exit 0: the recorded proof recipe replayed; stdout was 804 bytes at SHA-256
  d590c80efda1900056c6c889dba2db6be6df6ae6966ff9959106a8406ba53274

python3 -B Stage1_Instances/THM-M-0856/check_obligation_tree.py
  exit 1: recorded obligation-bundle recipe reached its stale integrated execution-DAG fingerprint
  assertion; combined output was 606 bytes at SHA-256
  b9cc3057c2c410a6a78ce32f9186438e9f34b5358e66e1302f76cb67a2948122

python3 -B Stage1_Instances/THM-M-0856/build_obligation_artifacts.py --check
  exit 1: recorded generator recipe reported `generated artifact drift: typed-graphs.json`; stdout
  was 44 bytes at SHA-256 a74785778a5be59739c07e1201664af54c66af4879d5eed4ec48f1aaeec88195

python3 -m json.tool Stage1_Instances/THM-M-0856/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0856/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0856-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0856/check_validation.py
  exit 0: validator compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-0856 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed direct hygiene checks
```

All recorded executable recipes relevant to the proof and frozen obligation packet were rerun.
The proof replay passed; both recorded obligation-tree recipes failed against their declared exit-0
expectations because their immutable phase snapshot predates the integrated execution-DAG hash.
The new fail-closed recipe binds those frozen artifacts and directly replays the Lean proof, but the
two stale recipe failures remain explicit blockers rather than being recast as passing evidence.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel and composition replay | provisional pass | Exact statement, adapter/composition, pinned terminal, proof roots, and differential exact target elaborate at `--trust=0`. |
| Placeholder and unsafe boundary | pass | Lean sorry reports and comment-stripped scans found no prohibited proof or implementation construct. |
| Trust observation | provisional pass | All covered proof-bearing declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; accepted foundation and complete transitive TCB closure remain open. |
| Selected provenance | provisional pass | Local hashes and pinned Tutte source/blob/body/olean, clean revision/tree, manifest, license, and tools agree; complete transitive provenance and SBOM remain open. |
| Internal source decomposition | fail closed | Sixteen source-body plans lack abstract-child composition certificates and receive no individual closure credit. |
| Structured authority | fail closed | `S56-M-0856-PROOF` is only `[_]`; the instance and graph accept no receipt or closure and remain H1/M3/R4. |
| Hermetic replay | fail closed | Shared warm `.lake`; no immutable clean checkout, empty-cache cold bootstrap, content-addressed offline restoration, complete TCB/SBOM, or deterministic release bundle. |
| Independent verification | fail closed | The differential route shares this worker, checkout, kernel, and cache; no distinct identity, runner, signature, or independently implemented minimal release verifier exists. |

The first failed node gate is `dependency.S56-M-0856-PROOF.master_acceptance`; the first failed
release gate is `S56-10.6-HERMETIC-COLD-BUILD`. The accepted vector remains `[H1, M3, R4]`.
Primary-source H0, independently reviewed R0, complete trust/provenance, `AUDIT-Z`, `THEOREM-Z`,
release, and theorem completion are false. This self-tested worker evidence claims no `E1`,
accepted `M0-W`, independent validation, release, or master acceptance.
