# THM-M-0318 validation-phase handoff

Item: `S56-M-0318-VALIDATION`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b` (tree
`c5771c47c12b80aba613e6d844570f83b39ded6d`).

Validation date: `2026-07-15` (`Asia/Shanghai`).

## Validation scope

The structured recipe copies the exact statement, frozen composition harness,
three-module vendored Brouwer closure, proof source, and differential module
into a disposable output tree. It invokes the pinned Lean 4.29.0 binary
directly with `--trust=0 -t0`, fixed `LEAN_PATH`, locale, timezone, and
thread count. Bubblewrap makes the host root and shared dependency cache
read-only and denies the network; only the disposable tree is writable.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. It repeats
the proof route directly against `Statement` and the vendored `Brouwer`
theorem. Its derivation deliberately parallels `Proof.lean`, so this is a
useful no-import differential replay, not an independently designed proof, a
distinct verifier identity, or a second-runner attestation.

The replay freshly checks the exact canonical root
`Stage1Instances.THM_M_0318.SchauderFixedPointTarget`, the frozen
`compose_schauder` route, both root declarations, and root-relevant vendored
terminals. Nine proof-phase and five differential declarations pass
`assert_no_sorry`; every one reports exactly `propext`,
`Classical.choice`, and `Quot.sound`. The nested-comment-aware scan rejects
executable placeholders, bodyless declarations, unsafe/oracle hooks, native
shortcuts, and externs while correctly ignoring abandoned text inside the
vendored nested comments.

The validator also re-runs `build_vendor_manifest.py`, which reverses all
nine compatibility edits plus the newline normalization and checks the three
reconstructed upstream hashes. It binds the vendored source hashes, immutable
upstream revision/tree/archive hash, MIT license, current repository inputs,
tool identities, clean pinned mathlib revision/tree/remote/license, and the
selected `AssertNoSorry` and `PrintSorries` source/blob/olean boundaries.

## Commands and exact results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546
  uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets at ranks 1..1546 passed

python3 scripts/stage1_target.py show THM-M-0318
  exit 0: rank 684, planned, L0/rework_required, theorem_complete=false

python3 Stage1_Instances/THM-M-0318/build_vendor_manifest.py
  exit 0: 3 modules and 182363 bytes passed reversible-port verification;
  compatibility stream SHA-256
  39fff43f92e646d6365f6279fd565d0d2d7b873f0922a1df9165f880a36b8790

python3 Stage1_Instances/THM-M-0318/check_obligation_tree.py
  exit 0: 12 obligations and 12 typed nodes passed; the frozen graph remains
  root-open with inventory digest 57d77a8f...376f87

python3 -I -B Stage1_Instances/THM-M-0318/check_validation.py --probe
  exit 0: trust-zero network-isolated fresh-output replay passed
  proof output SHA-256:
  fbf4a09c61a575094dd76b24a0e5e9ec777b049b24075d66a5bd12bc2a0fdccc
  differential output SHA-256:
  b814e52f874f2796b8ee098c49b3b8ce2113dc790702dc20897e654d093cb377
  vendor verifier output SHA-256:
  2bedb85de4e2e008ed02537b139ce36050d16d2497de120e75f1b3cccd3b961d

python3 Stage1_Instances/THM-M-0318/check_statement.py
  exit 1 before elaboration: Lake scans the canonical shared cache and finds
  .lake/packages/flt-regular with no resolvable HEAD

python3 Stage1_Instances/THM-M-0318/check_proof.py
  not credited or replayed: the predecessor checker is snapshot-bound to base
  557b928b..., proof DAG state [ ], and its former worker packet

python3 -I -B Stage1_Instances/THM-M-0318/check_validation.py
  exit 0: final receipt, packet, exact kernel/trust/provenance observations,
  dirty-input hashes, and fail-closed release decisions passed

python3 -m json.tool Stage1_Instances/THM-M-0318/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0318/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: all three JSON artifacts parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-m0318-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0318/check_validation.py
  exit 0

git diff --check -- Stage1_Instances/THM-M-0318 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

No `lake update`, `lake build`, dependency fetch/clone, network request, or
`.lake` write was performed by this validation phase. The normal
`lake env lean` surface is currently unusable because the canonical shared
`.lake/packages/flt-regular` directory is an incomplete Git repository with
no `HEAD`. The earlier proof receipt said that incomplete clone had been
removed, but it has reappeared in shared external state. This worker did not
remove, repair, inspect for proof credit, or otherwise mutate it. The validator
uses the already installed pinned Lean binary and explicit pre-existing
compiled paths, and the receipt records this discrepancy as a nonrelease
incident.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, frozen composition, vendored source closure, proof root, and no-import differential root compile at trust zero. |
| Placeholder and unsafe scan | pass | Fourteen Lean sorry reports and nested-comment-aware source scans pass. |
| Trust observation | provisional pass | Every checked declaration reports exactly the three disclosed classical/quotient axioms. No accepted foundation policy exists. |
| Selected provenance | pass | Current hashes, reversible port, upstream identities, license, tool digests, and clean mathlib pin agree. |
| Proof dependency and state | fail closed | Proof is provisional `[_]`; instance/task/typed-graph records predate it and still show the old Harfe/open route. |
| Complete trust/provenance | fail closed | Full declaration/import/compiled-artifact closure, compiler/bootstrap/plugin/checker TCB, accepted axiom profile, SBOM, and offline archive remain absent. |
| Hermetic reproduction | fail closed | A shared warm cache was reused; this is not a clean checkout, empty-cache cold build, or offline-restorable release replay. |
| Independent verification | fail closed | The parallel source replay shares this worker, checkout, kernel, cache, vendored terminal, and proof architecture. No distinct signed verifier exists. |

The node is genuinely self-tested as provisional validation work, but no
accepted state changes. The accepted root remains `H2/M3/R4`, with no
accepted closed obligation or receipt. The first node gate is proof master
acceptance; the first release-specific gate is the section 10.6 cold
empty-cache replay. Primary-source `H0`, independently reviewed `R0`,
authoritative graph/provenance reconciliation, accepted foundation and TCB
closure, deterministic bundle, independent verification, `AUDIT-Z`,
`THEOREM-Z`, release, and master acceptance remain open. Therefore audit and
theorem completion remain false.
