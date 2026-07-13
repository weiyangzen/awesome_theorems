# THM-M-0995 validation-phase result

Item: `S56-M-0995-VALIDATION`. Validation date: 2026-07-14. Base revision:
`92246ea92c0c44282c05728798bc7c7e4a5a1464`.

## Gate result

The network-isolated `--trust=0` replay passes for the exact frozen statement, the corrected
registry-v2 composition, the direct proof-phase root, and the validation adapters. The checker
parsed 31 axiom reports; every report stayed within, and the exact roots and composition
certificates used exactly, `propext`, `Classical.choice`, and `Quot.sound`. The local Lean sources
passed the placeholder, axiom-declaration, unsafe, and generated-artifact scan. Frozen input hashes,
the registry denominator, proof-receipt inputs, the clean pinned mathlib revision/tree/remote, four
selected terminal source/body/olean identities, the mathlib license, and validation executables are
bound in `validation-receipt.json`.

This validation node remains blocked. Its first failed gate is
`dependency.S56-M-0995-PROOF.master_acceptance`: the proof and every earlier prerequisite have only
provisional `[_]` evidence. The later typed graph proposes exact-root `H2/M0-L/R4`, but the intake
authority remains `planned` at `H2/M3/R3`; a worker validation cannot reconcile or accept that state.

The release-grade hermetic and independent gates also fail closed. The replay mounted the canonical
pinned warm `.lake` artifacts read-only rather than bootstrapping an immutable clean checkout from
empty caches and an offline-restorable archive. `Validation.lean` checks both already distinct
proof-phase roots and the statement transport, but it imports `Proof.lean` and ran with this worker,
kernel, checkout, and cache. It is not a distinct signed runner or an independently implemented
minimal verifier. Complete transitive TCB/provenance, SBOM/license closure, H0, independent R0,
deterministic release bundling, `AUDIT-Z`, and `THEOREM-Z` remain open.

## Commands and results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0995
  exit 0: rank 275, lifecycle planned, theorem_complete=false

bash Stage1_Instances/THM-M-0995/check_validation.sh
  exit 0: Statement, ObligationTree, Proof, and Validation replayed at --trust=0 inside
  a read-only bubblewrap sandbox with an unshared network namespace; 31 axiom reports,
  three sorry-free validation adapters, and local proof hygiene passed

python3 Stage1_Instances/THM-M-0995/check_obligation_tree.py
  exit 0: registry v2 has 21 obligations and 39 typed edges; denominator, graph,
  composition, append-only amendment, budgets, and fail-closed completion boundary passed

python3 Stage1_Instances/THM-M-0995/check_proof_hygiene.py
  exit 0: no placeholder, axiom declaration, unsafe declaration, or generated Lean artifact

python3 -m json.tool Stage1_Instances/THM-M-0995/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0995/validation-receipt.json
  exit 0: both structured artifacts are valid JSON
```

Earlier independent read-only attempts to run `check_proof.sh` and `check_statement.py` were
terminated with exit 143 under concurrent load and emitted no Lean diagnostic. The successful
network-isolated replay above supersedes their kernel scope; the failed attempts remain recorded for
provenance. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.
This packet self-tests a truthful blocked validation result only. It does not claim accepted M0-L,
hermetic or independent validation, theorem completion, release, or master acceptance.
