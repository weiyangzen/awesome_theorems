# THM-M-0914 validation-phase handoff

Item `S56-M-0914-VALIDATION` was self-tested from base revision
`c45f3c7090cb4adf616d45e5414985f956e807b2` (tree
`da6f991c07f11e8608ddc090af9356558d64d360`) on 2026-07-14.

## Validated boundary

The exact proof-phase root and every frozen child-to-parent composition re-elaborate with pinned
Lean 4.29.0. `Validation.lean` is a same-worker differential reconstruction that imports the frozen
statement and pinned mathlib pigeonhole module, but neither `Proof.lean` nor `ObligationTree.lean`.
It derives the unchanged `PigeonholeTarget` through `Fintype.not_injective_of_card_lt` and
`Function.not_injective_iff`, rather than invoking either proof-phase root or the finite-set
collision wrapper.

The validation recipe built fresh temporary local oleans with `--trust=0`. Bubblewrap mounted the
host root read-only, allowed writes only in the temporary module directory, fixed locale and
timezone, and denied outbound network with a separate network namespace. The 12 proof declarations
and three differential declarations were sorry-free. Each reported only a subset of `propext`,
`Classical.choice`, and `Quot.sound`; the differential transitive closure reported no unsafe
declaration and no unexpected bodyless nonaxiom.

The validator also checked the exact statement, registry denominator, proof receipt and composition
IDs, clean pinned mathlib revision/tree/official remote, selected direct and differential source,
body and `.olean` hashes, the mathlib license, and tool identities. These are real narrow kernel,
hygiene, provenance, and trust observations. Provenance and trust obligation IDs receive no closure
credit because their full transitive and release assurance remains open.

## Gate decisions

| Gate | Decision | Evidence or boundary |
|---|---|---|
| Exact target and kernel replay | provisional pass | Statement, frozen composition, both proof roots, and the separate noninjectivity root elaborated with `--trust=0`. |
| Placeholder and unsafe paths | pass for inspected closure | Fifteen declarations were sorry-free; local scans found no prohibited mechanism; the differential closure reported no unsafe or unexpected bodyless declaration. |
| Axiom observation | provisional pass | Every covered declaration stayed within `propext`, `Classical.choice`, and `Quot.sound`. |
| Selected provenance | pass | Local inputs, mathlib pin/tree/remote, four source and olean pairs, five body regions, and license agree. |
| Complete trust/provenance | fail closed | No complete transitive declaration/body/olean, compiler/bootstrap, SBOM, supply-chain, or accepted foundation/TCB closure. |
| Structured state and dependency | fail closed | `S56-M-0914-PROOF` lacks master acceptance; structured authority remains open `H1/M3/R4` with no accepted obligation. |
| Hermetic reproduction | fail closed | The network-isolated process reused shared warm `.lake`; no clean checkout, empty-cache cold build, or offline archive restoration. |
| Independent verification | fail closed | The differential implementation used this worker, kernel, checkout, and cache; there is no distinct signed runner or independently implemented minimal verifier. |

## Commands and results

Commands ran from the repository root unless noted. No `lake update`, `lake build`, dependency
clone/fetch, network request, or `.lake` mutation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1..1546, passed

python3 scripts/stage1_target.py show THM-M-0914
  exit 0: rank 1456, planned, L0/rework_required, theorem_complete=false

bash Stage1_Instances/THM-M-0914/check_proof.sh
  exit 0: isolated Statement, ObligationTree, and Proof replay; 12 declarations
  were sorry-free with axioms exactly propext, Classical.choice, Quot.sound

bash Stage1_Instances/THM-M-0914/check_validation.sh
  exit 0: network-isolated --trust=0 replay of Statement, ObligationTree, Proof,
  and differential Validation; 15 declarations were sorry-free, every axiom set
  stayed within the allowed surface, and the differential closure had no unsafe
  or unexpected bodyless declarations

python3 -B Stage1_Instances/THM-M-0914/check_validation.py
  exit 0: final exact identity, structured-state, pin, provenance, trust,
  network-isolated differential replay, receipt/packet, and fail-closed checks passed

python3 -m json.tool Stage1_Instances/THM-M-0914/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0914/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: all three structured artifacts parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-m0914-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0914/check_validation.py
  exit 0: validator bytecode compiled outside the repository

git diff --check -- Stage1_Instances/THM-M-0914 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; the validator also checked final newlines and bytes
```

## Fail-closed result

This is not section 10.6 release-grade hermetic evidence. The process denied network and isolated
new target outputs, but reused the automation-provided shared warm `.lake` source and compiled
cache. It did not bootstrap an immutable clean checkout with empty caches, restore the dependency
closure from offline archives, or produce a deterministic signed TCB/SBOM evidence bundle.

The differential proof is also not section 10.7 independent verification. It ran in this worker
with the same checkout, Lean kernel, and dependency cache. There is no second independently
provisioned clean runner, pair of signed attestations, or independently implemented minimal
receipt/graph verifier.

The first node failure is `dependency.S56-M-0914-PROOF.master_acceptance`; the first release failure
is `hermetic.cold_empty_cache_offline_replay`. The receipt verdict is therefore `blocked`. Accepted
state remains `H1/M3/R4`, with no accepted obligations or receipts, `audit_complete=false`, and
`theorem_complete=false`. Only the integration lane may accept the provisional `[_]` packet.
