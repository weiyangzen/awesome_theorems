# THM-M-0931 validation-phase handoff

Item `S56-M-0931-VALIDATION` was self-tested from base revision
`4a10a7a4ddff88e302d5a303b16dd687d9468f63` (tree
`730de242597680b39a7087d3204dfd1e6c41c60e`) on 2026-07-13.

## Validated boundary

The exact proof-phase root and a separately written exact-root reconstruction
elaborate with Lean 4.29.0. `Validation.lean` imports the frozen statement and
the pinned mathlib EGZ module, but imports neither `Proof.lean` nor
`ObligationTree.lean`. It reconstructs the multiset witness from
`Int.erdos_ginzburg_ziv` through `s.toEnumFinset`, rather than invoking the
proof phase's direct multiset wrapper. This provides differential evidence for
the exact occurrence-preserving statement without duplicating proof-body credit.

The Lean replay ran in a fresh temporary output directory with a read-only host
root, fixed locale and timezone, and a bubblewrap network namespace. All nine
proof declarations and all three differential declarations were sorry-free and
reported exactly `propext`, `Classical.choice`, and `Quot.sound`. The verifier
also checked frozen statement/registry/graph/proof hashes, the clean pinned
mathlib revision and official remote, selected EGZ and Chevalley-Warning source,
body and `.olean` hashes, the mathlib license, and executable identities.

These are real narrow kernel, hygiene, selected-trust, and selected-provenance
checks. The provenance/trust obligation IDs in the recipe are covered only by a
fail-closed assessment; `closure_credit=false` and no accepted obligation is
claimed. Six deeper source-body decompositions still lack exact abstract-child
composition certificates.

## Commands and results

Commands ran from the repository root unless noted. No `lake update`, `lake
build`, dependency clone/fetch, network access, or `.lake` mutation was used.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0931
  exit 0: rank 1470, planned, L0/rework_required,
  theorem_complete=false

bash Stage1_Instances/THM-M-0931/check_proof.sh
  exit 0: isolated Statement and ObligationTree outputs plus Proof elaborated;
  nine declarations were sorry-free and reported exactly the allowed axioms

bash Stage1_Instances/THM-M-0931/check_validation.sh
  exit 0: network-isolated temporary replay of Statement, ObligationTree,
  Proof, and the differential indexed-to-multiset Validation root; twelve
  declarations were sorry-free with exactly the allowed axioms

python3 -B Stage1_Instances/THM-M-0931/check_validation.py
  exit 0: exact identity, frozen state, proof freshness, network-isolated
  kernel replay, selected provenance, trust observations, tool identities,
  receipt/packet consistency, and fail-closed boundaries passed

python3 -B Stage1_Instances/THM-M-0931/build_obligation_artifacts.py --check
  exit 0: frozen 32-obligation registry, 46 typed edges, denominator, and
  obligation-tree validation specification match deterministic regeneration

python3 -m json.tool Stage1_Instances/THM-M-0931/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0931/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for all three structured artifacts

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0931-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0931/check_validation.py
  exit 0: validator syntax compiled outside the repository

rg -n --glob '*.lean' '<prohibited-pattern>' \
  Stage1_Instances/THM-M-0931
  exit 1 with empty output: no sorry, admit, bodyless, opaque, unsafe,
  native-oracle, external-implementation, or placeholder construct found

git diff --check -- Stage1_Instances/THM-M-0931 \
  .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

## Fail-closed result

This is not section 10.6 release-grade hermetic evidence. The network-isolated
process reused the automation-provided shared warm `.lake` source and compiled
cache; it did not bootstrap an immutable clean checkout with empty caches,
restore the source/dependency closure from offline archives, or produce a
deterministic signed TCB/SBOM evidence bundle.

The differential proof is also not section 10.7 independent verification. It
used this worker, checkout, Lean kernel, and dependency cache. There is no
second independently provisioned clean runner, pair of signed attestations, or
independently implemented minimal release verifier.

The proof predecessor is only provisionally `[_]`, and the target-local task
DAG still records proof and validation open. Complete transitive provenance and
TCB closure, master acceptance, H0, R0, audit, and release reconciliation remain
open. Accepted state therefore remains `H1/M3/R4`, with no accepted obligations
or receipts, `audit_complete=false`, and `theorem_complete=false`.
