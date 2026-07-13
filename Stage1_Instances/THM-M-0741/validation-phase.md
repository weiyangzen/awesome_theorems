# THM-M-0741 validation-phase evidence

Item: `S56-M-0741-VALIDATION`. Base revision:
`b243ebc0f9058ba5afafef8240b92c2dfb2edc6e`; base tree:
`b4b092069141ac54ea1ab5a6ea946192a30ec78c`.

## Validation scope

The node recipe re-elaborates the frozen statement, every conditional composition, both proof
roots, the pinned Rice and fixed-input terminals, and a new exact-root reconstruction in temporary
output space. Every Lean subprocess runs in a Bubblewrap network namespace. `Validation.lean`
imports neither `Proof` nor `ObligationTree`; it independently restricts an alleged pair decider to
input one and applies `ComputablePred.halting_problem 1`, whereas the proof phase uses input zero.
This is differential same-worker corroboration, not a distinct-runner attestation.

All ten proof and validation declarations are sorry-free. Every checked proof or differential route
reports exactly `propext`, `Classical.choice`, and `Quot.sound`. The validator also binds the exact
target expression, registry denominator, frozen graph and receipt hashes, mathlib revision/tree,
clean dependency source, Halting source/blob/body/compiled-object hashes, remote, license, and tool
identities. No prohibited proof or implementation mechanism was found.

## Commands and results

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused read-only. No `lake update`, `lake build`, clone, fetch, checkout,
dependency mutation, or network operation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0741
  exit 0: rank 1329, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0741/check_proof.sh
  exit 0: both exact proof roots and all required-machine bridges elaborated; eight declarations
  were sorry-free and reported exactly [propext, Classical.choice, Quot.sound]

bash Stage1_Instances/THM-M-0741/check_validation.sh
  exit 0: network-isolated exact proof and Statement-only differential roots elaborated; ten
  declarations were sorry-free and reported the exact allowed axiom set; stdout SHA-256
  ac39359651d6fede3ead227489adac19dff4a4700318abb9397733d69bf937c0

python3 -B Stage1_Instances/THM-M-0741/check_validation.py
  exit 0: exact target/composition replay, hygiene, selected trust/provenance, frozen hashes, pin,
  receipt, recipe, and worker packet passed; authority and release gates failed closed

python3 -m json.tool Stage1_Instances/THM-M-0741/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0741/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0741-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0741/check_validation.py
  exit 0: validator compiled outside the repository tree

rg -n --glob '*.lean' '<prohibited construct pattern>' \
  Stage1_Instances/THM-M-0741/{Statement,ObligationTree,Proof,Validation}.lean
  exit 1 with empty output: expected pass, no prohibited construct found

git diff --check -- Stage1_Instances/THM-M-0741 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed no-index checks
```

Snapshot-bound predecessor Python checkers are not current validation gates:
`check_proof.py` expects its proof-phase base and self-test packet, while
`check_obligation_tree.py` preserves its pre-integration workflow snapshot. This phase binds their
immutable artifacts by hash and directly replays the Lean proof instead of reporting stale checker
failures as proof failures.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel and composition replay | provisional pass | The exact statement, all frozen compositions, both proof roots, terminal declarations, and differential exact root elaborate under network isolation. |
| Placeholder and unsafe boundary | pass | Lean sorry reports and a comment-stripped scan found no placeholder, bodyless, unsafe/native/oracle, or external implementation construct. |
| Trust observation | provisional pass | Checked declarations report exactly the frozen `propext`, `Classical.choice`, and `Quot.sound` set; accepted foundation and complete transitive TCB closure remain open. |
| Selected provenance | provisional pass | Exact local hashes and the pinned Halting source/blob/body/olean, clean revision/tree, remote, manifest, license, and tool hashes agree; complete transitive provenance and SBOM do not exist. |
| Structured authority | fail closed | `S56-M-0741-PROOF` is only `[_]`; the instance and graph accept no receipt or closed obligation and remain H1/M3/R4. |
| Hermetic replay | fail closed | Shared warm `.lake`; no separate immutable clean checkout, empty-cache cold bootstrap, content-addressed offline restoration, complete TCB/SBOM, or deterministic release bundle. |
| Independent verification | fail closed | The different input-one reconstruction shares this worker, checkout, kernel, and cache; no distinct identity, runner, signature, or independently implemented minimal release verifier exists. |

The first failed node gate is `dependency.S56-M-0741-PROOF.master_acceptance`; the first failed
release gate is `S56-10.6-HERMETIC-COLD-BUILD`. The accepted vector remains `[H1, M3, R4]`.
Primary-source H0, independently reviewed R0, full trust/provenance, `AUDIT-Z`, `THEOREM-Z`,
release, and theorem completion are false. This self-tested worker evidence claims no `E0/E1`,
accepted `M0-W`, independent validation, release, or master acceptance.
