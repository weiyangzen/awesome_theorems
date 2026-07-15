# THM-M-0957 validation-phase evidence

Item: `S56-M-0957-VALIDATION`. Base revision:
`d6616cc60ad980c635f22ef840e9c5db2ebcab50`; base tree:
`d6f3c3aedec26191f09878fd6eb1fec666adf318`.

## Validation scope

The structured recipe rechecks the already implemented proof without adding
mathematical content. It copies `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and the proof-only `Validation.lean` probe to disposable storage.
Every Lean process uses the absolute pinned toolchain with `--trust=0` inside a
Bubblewrap network namespace with `--clearenv`, a read-only host root,
disposable home, fixed `C.UTF-8` locale, UTC timezone, umask `022`, and one Lean
thread. The four-module replay uses absolute pinned Lake `env`, then sets the
temporary-module `LEAN_PATH` inside that adapter before invoking absolute pinned
Lean; this is the `lake env lean` environment without Lake reordering the fresh
module path. All four `.olean` outputs are fresh and temporary; their
run-specific hashes and each module's run-specific output hash are recorded. The
automation-provided pinned `.lake` symlink is reused read-only and remains a
shared warm cache.

The validation recipe freshly reproduces the dossier's established explicit
pretty-print expression serialization and its SHA-256 before replay. It reaches
the exact unchanged
`Stage1Instances.THM_M_0957.BehrendConstructionTarget`, both statement
transports, the imported `Behrend.bound_aux` construction body, the complete
sharp-parameter route, and the direct premise-free canonical declaration
`behrendConstructionTarget_proof`. The trust probe explicitly includes the
previously omitted root-reachable helper `radixBase_eventually_one`.

Lean reports all 31 selected declarations sorry-free. The exact root uses only
`propext`, `Classical.choice`, and `Quot.sound`. The elaborator-aware root and
transport closure contains 28,337 declarations from 1,086 modules, with no
unexpected bodyless or unsafe declaration. These are machine observations over
the selected closure, not an accepted foundation profile or complete release
TCB inventory.

Selected provenance checks bind the local proof bodies, the canonical source
and graph hashes, mathlib revision/tree/remote/license, and source/blob/olean/
ilean identities for the Behrend, 3AP, real-power, and trust utility modules.
The exact `Behrend.bound_aux` terminal body remains located in the pinned
Behrend source. A complete transitive source/import/compiled-object closure,
SBOM, license archive, compiler/bootstrap/plugin inventory, and offline archive
remain absent.

The exact dirty Git status, deterministic non-self-referential untracked-input
manifest, root commit/tree, and selected mathlib commit/tree/status/source/blob/
olean/ilean snapshot are captured before and after the replay and must agree.
The receipt and worker packet are outputs excluded from the manifest to avoid a
recursive hash; this is an integrity boundary for dirty nonrelease evidence,
not a deterministic release bundle.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai). No `lake
update`, `lake build`, dependency clone/fetch, checkout, `.lake` mutation, or
network request was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0957
  exit 0: rank 1491, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0957/check_validation.sh
  exit 0: absolute-tool, clear-environment, network-isolated trust-zero replay
  elaborated four fresh modules through the pinned Lake environment;
  31 sorry/axiom probes passed; closure was 28337 declarations in 1086 modules
  with empty bodyless-nonaxiom and unsafe sets; captured stdout was 5524 bytes
  with SHA-256 1cc961df3e886e7b21d47faec82d66e2d1e0bc878265944a5fdd2c4e55b2dbdb;
  wall time 365 seconds (19:58:31 through 20:04:36 +08:00); the inner
  canonical artifact record was 905 bytes and the merged replay stream was
  6429 bytes with SHA-256 1a82c79e7d2bb45ffd26dc1c5823fc9ad427700b10bdb7d02407f043f96ba667

python3 -I -B Stage1_Instances/THM-M-0957/check_validation.py
  exit 0: fresh established expression fingerprint, exact target, per-module
  output/olean hashes, current authority, kernel/trust observations, exact
  pre/post Git/input/mathlib snapshots, selected provenance, receipt, recipe,
  worker packet, and fail-closed gates passed

python3 -m json.tool Stage1_Instances/THM-M-0957/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0957/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m0957-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0957/check_validation.py
  exit 0: validator syntax checked without writing into the target

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-0957/{Statement,ObligationTree,Proof,Validation}.lean
  exit 1 (expected no match): no prohibited construct was found after the
  validator's nested-comment-and-string-aware scan

git diff --check -- Stage1_Instances/THM-M-0957 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The predecessor `check_proof.py` is intentionally not invoked. It is bound to
the proof worker's former HEAD, DAG state, dirty-path set, and ephemeral worker
packet. The proof source and receipt are hash-bound here, and the complete Lean
route is freshly replayed instead. The existing `validation-specs.json` remains
the obligation-tree recipe and is not silently relabeled as validation evidence.

## Fail-closed decisions

The first node gate is
`dependency.S56-M-0957-PROOF.master_acceptance`. The proof predecessor is only
`[_]`; therefore accepted state remains `[H1, M3, R3]`, and accepted obligations
and receipts remain empty. The frozen registry and typed graphs predate proof
execution: most node fingerprints remain planned identities, evidence links are
empty, and the graph still records the twelve implemented leaves as open.
Master reconciliation must bind actual Lean declarations and compositions to
the frozen denominator before accepting machine closure.

The source mapping is not accepted `H0`, no required readable record has an
independent `R0` review, and the observed axioms have no accepted theorem-
specific foundation profile. The selected source and compiled-object checks do
not constitute complete provenance, TCB, SBOM, or supply-chain closure.

Network isolation and fresh target-local outputs strengthen the narrow replay,
but do not satisfy release hermeticity. There is no immutable clean checkout,
empty-cache cold bootstrap, content-addressed offline restoration, deterministic
bundle, distinct verifier identity, independent cache, second signed
attestation, or independently implemented minimal verifier. A repeat in this
worker would not be independent evidence.

## Status boundary

This is self-tested validation-node evidence for an exact network-isolated
trust-zero kernel replay, machine-observed axiom and placeholder closure, and
selected local provenance. It truthfully records failed authority, per-node
fingerprint/provenance reconciliation, source/readability, complete TCB,
cold-hermetic, and independent-verification gates. It grants no accepted
`M0-L`, `E0/E1`, validation completion, audit completion, theorem completion,
release, independent verification, or master acceptance.
