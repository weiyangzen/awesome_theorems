# THM-M-0819 validation-phase evidence

Item: `S56-M-0819-VALIDATION`. Base revision:
`9d50d838c8132b2aaf005a4863baeb5385e52a97`; base tree:
`ef268baf236c1fe55806a57847c7f78ed6587b9d`.

## Validation scope

The executable recipe copies the exact `Statement.lean`, `FiniteDilworth.lean`, `Proof.lean`, and a
proof-only `Validation.lean` trust probe into fresh temporary output space. Every Lean process runs
with `--trust=0` in a Bubblewrap network namespace with a read-only host root, fixed locale and
timezone, one Lean thread, and a 240-second process bound. Only the disposable module directory is
writable. The automation-provided pinned `.lake` symlink is reused read-only and remains a shared
warm cache.

The replay reaches the unchanged arbitrary-poset target and
`Stage1Instances.THM_M_0819_Proof.dilworthPrimary : DilworthPrimaryTarget`. Lean's transitive sorry
collector finds no sorry in the exact root or the two finite partition terminals. Each checked
declaration reports exactly `propext`, `Classical.choice`, and `Quot.sound`. `Validation.lean` adds no
proof declaration. Reimplementing the substantial finite and compactness arguments during a
validation intent would add mathematical proof content and would still not create the distinct
runner evidence required by section 10.7.

Selected provenance checks bind the repo-local root body, current-pin finite port, upstream source
identity recorded by the proof receipt, byte-identical Apache-2.0 license, clean pinned mathlib
revision/tree/remote/license, the directly imported Compactness source and compiled artifact, and
the Lean/Lake/Elan/Python/Git/Bash/Bubblewrap/timeout identities. The original upstream source bytes
are not retained in this dossier, so the recorded port delta is not independently replayed here.
This is selected provenance only, not complete transitive declaration, source, compiled-artifact,
TCB, or SBOM closure.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (`Asia/Shanghai`). No `lake update`, `lake build`,
dependency clone/fetch, checkout, `.lake` mutation, or network request was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0819
  exit 0: rank 1377, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0819/check_proof.sh
  exit 0: fresh isolated exact root passed with --trust=0; sorry-free with exactly propext,
  Classical.choice, and Quot.sound

python3 -B Stage1_Instances/THM-M-0819/check_proof.py
  exit 0 during preflight before the validation self-test packet was written: exact target, frozen
  denominator, proof/provenance hashes, pinned mathlib identity, placeholder policy, and provisional
  proof receipt passed

python3 -B Stage1_Instances/THM-M-0819/check_obligation_tree.py
  exit 1 before content validation: the predecessor checker hardcodes its original worker base
  dc600635160cace0916df5234bf8808c39dc656d; this known replay limitation remains fail-closed

bash Stage1_Instances/THM-M-0819/check_validation.sh
  exit 0: network-isolated trust-zero fresh-output replay elaborated Statement, FiniteDilworth,
  Proof, and Validation; three sorry/axiom probes passed; stdout was 943 bytes with SHA-256
  5ce0375f67c0df938040d573b58b9f705dd90f1524a74c67ccc2570787d4ddb3

python3 -I -B Stage1_Instances/THM-M-0819/check_validation.py
  exit 0: exact target, kernel replay, selected trust/provenance, frozen authority boundaries,
  receipt, recipe, ownership, and fail-closed decisions passed

python3 -m json.tool Stage1_Instances/THM-M-0819/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0819/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m0819-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0819/check_validation.py
  exit 0: validator syntax checked without writing bytecode into the target

rg -n -i --glob '*.lean' '\\b(sorry|admit|sorryAx)\\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-0819/{Statement,FiniteDilworth,Proof,Validation}.lean
  exit 1 (expected no match): no prohibited construct was found after the validator's
  nested-comment-aware scan

git diff --check -- Stage1_Instances/THM-M-0819 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The predecessor `check_proof.py` is not a current validation recipe: when any worker self-test file
exists, it requires that file to describe the proof item. After this validation packet is written it
therefore rejects the validation item before inspecting proof content. Its receipt and sources are
hash-bound here, and `check_validation.sh` freshly replays the proof rather than weakening that
checker.

## Fail-closed decisions

The first node gate is `dependency.S56-M-0819-PROOF.master_acceptance`. The proof predecessor is
only `[_]`, so accepted state remains `[H1, M3, R3]` with no accepted closed obligation. Its receipt
proposes all 23 required-machine IDs, but the frozen registry and typed graph retain their pre-proof
state. Most rows have planned fingerprints, no terminal proof-body ID, and no evidence. Master must
reconcile the new local proof route, exact node bodies, composition, Rado provenance, and evidence
links before validation can ratify `M0-L`.

The per-theorem `instance.json` and `task-dag.json` are also unreconciled intake-era authorities:
the instance still has a null canonical target and registry hash, and the local task DAG still marks
all downstream tasks open. This validation worker observes that conflict but does not rewrite
master-owned scope or execution state.

The source crosswalk is not `H0`, no required readable obligation has an independently accepted
`R0` record, and the observed axioms have no accepted theorem-specific foundation profile. Complete
transitive declaration, source-origin, compiled-object, bootstrap, plugin, checker, TCB, license,
and SBOM closure is absent.

Network isolation and fresh local `.olean` outputs strengthen the narrow replay but do not satisfy
the release hermetic gate. There is no separate immutable clean checkout, empty-cache cold
bootstrap, content-addressed offline restoration, deterministic release bundle, distinct signed
runner, independently provisioned cache, second attestation, or independently implemented minimal
verifier. `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, and master acceptance remain false.

## Status boundary

This is self-tested `blocked` worker evidence for a network-isolated narrow kernel replay, exact
observed axioms, placeholder closure, and selected local provenance. It truthfully records failed
authority, node-specific composition/provenance, source/readability, foundation/TCB, empty-cache cold
bootstrap, and independent-verification gates. It is not accepted `M0-L`, `E0/E1`, audit completion,
theorem completion, release, or master acceptance.
