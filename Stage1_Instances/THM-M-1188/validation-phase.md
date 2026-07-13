# THM-M-1188 validation-phase result

Item: `S56-M-1188-VALIDATION`. Validation date: 2026-07-14. Base revision:
`4d2c77230343716176b4192dc38e26f4c20c7547`.

## Gate result

The narrow kernel and trust gate passes provisionally. `check_validation.sh`
copies the statement, obligation tree, proof, and validation wrappers to a
fresh `/tmp` directory, mounts the host read-only, denies the network with
Bubblewrap, fixes locale/timezone/thread settings, and invokes the pinned
`lake env lean --trust=0`. The exact canonical root, the frozen composition,
and both same-worker exact-type wrappers elaborate. Nineteen axiom reports use
exactly `propext`, `Classical.choice`, and `Quot.sound`; both wrappers pass
`assert_no_sorry` and `#print sorries`. No mathematical defect or target
broadening was found in the proof route.

Selected direct provenance also passes. The receipt binds the local proof,
statement, registry, graph, proof receipt, six direct mathlib source/blob/olean
identities, the clean mathlib revision/tree/remote/license, and the validation
executables. This is not complete transitive provenance or TCB closure.

The validation node is truthfully blocked. Its first failed gate is
`dependency.S56-M-1188-PROOF.master_acceptance`. The proof receipt's base
commit predates `Proof.lean`, while the frozen typed graph remains at `M3/M4`
with empty evidence/provenance fields. Several semantic nodes are local proof
blocks rather than stable declarations, and the old per-node recipes still
compile the conditional pre-proof obligation tree. The integration lane must
reconcile these before accepting node closure.

The hermetic and independent gates fail closed. The successful replay used the
shared warm `.lake` source and oleans read-only; it was not an offline-restored
clean checkout with empty caches. `Validation.lean` imports `Proof.lean` and ran
under this worker, kernel, checkout, and cache, so it is neither a distinct
signed runner nor an independently implemented verifier. The canonical
`flt-regular` briefly had an invalid `HEAD` during an early check, but the
shared cache was externally restored to its pinned clean revision before the
final receipt. This worker did not mutate or fetch `.lake`.

## Commands and results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1188
  exit 0: rank 383, lifecycle planned, theorem_complete=false

cd Formalizations/Lean && lake env lean --version
  final exit 0: Lean 4.29.0; an earlier transient invalid-HEAD failure was
  superseded after the shared cache was externally restored

bash Stage1_Instances/THM-M-1188/check_validation.sh
  exit 0: fresh-output, network-isolated lake env lean --trust=0 replay passed;
  19 exact axiom reports and two sorry-free exact-type wrappers passed

python3 Stage1_Instances/THM-M-1188/check_obligation_tree.py
  exit 0: 17 obligations, typed graphs, denominator, and exact conditional
  composition passed; frozen root remains open at M3

python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1188
python3 Stage1_Instances/THM-M-1188/check_obligation_tree.py
python3 -m json.tool Stage1_Instances/THM-M-1188/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1188/validation-receipt.json
git diff --check -- Stage1_Instances/THM-M-1188 .stage1-worker-selftest.json
  exit 0 for each command in the final self-test run
```

The final structured recipe is:

```text
python3 -I -B Stage1_Instances/THM-M-1188/check_validation.py
```

It rechecks all hashes, DAG and authority boundaries, source hygiene, selected
provenance, dependency pins, exact gate decisions, worker packet, and
then reruns the isolated Lean recipe. This packet validates a truthful blocked
result only. Accepted state remains `H2/M3/R3`; `audit_complete=false` and
`theorem_complete=false`. It claims no accepted `M0-L`, complete provenance or
TCB, node-specific closure, cold hermetic evidence, independent verification,
`AUDIT-Z`, `THEOREM-Z`, release, or master acceptance.
