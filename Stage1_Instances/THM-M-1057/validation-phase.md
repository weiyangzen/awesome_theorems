# THM-M-1057 validation-phase evidence

Item: `S56-M-1057-VALIDATION`. Base revision:
`e8499ef6898f9562fb480587db7eb9220c04b6fc`; base tree:
`d88a39b243dd6a835f2e7463b9805d1cb175fb80`.

## Validation scope

The executable recipe copies the exact statement, frozen composition, eight complete vendored
modules, proof, and a proof-only trust probe into fresh temporary output space. Every Lean process
runs with `--trust=0` in a Bubblewrap network namespace with a read-only host root, fixed locale and
timezone, and one Lean thread. The only writable path is the disposable module directory. The
automation-provided pinned `.lake` symlink is reused read-only and remains a shared warm cache.

The replay reaches the exact unchanged `KingmanTarget`, `pointwiseLimitPackage`, and `kingmanTarget`.
Lean's transitive sorry collector finds no sorry in the frozen composer, selected analytic
terminals, limit package, or root. Each checked declaration reports exactly `propext`,
`Classical.choice`, and `Quot.sound`. `Validation.lean` adds no proof declaration: it imports the
existing proof and runs trust commands. A proof-independent short exact-root probe is unavailable
because the target assumes subadditivity almost everywhere, while the upstream Kingman theorem
requires a pointwise cocycle. Reproducing the strictification would add substantial proof content,
which the validation phase may not do.

All eight local ports mechanically reconstruct to the recorded upstream source hashes. The
Apache-2.0 license, the locally available upstream archive digest, the clean pinned mathlib
revision/tree/remote, five selected mathlib source blobs, and the Lean/Lake/Python/Git/Bash/
Bubblewrap/Elan executable identities were checked. The archive was an optional local observation,
not a required replay input; the reversible port reconstruction and recorded immutable source
hashes remain checked when that transient archive is absent. This selected provenance is not a complete
transitive declaration/source graph, compiled-artifact inventory, TCB closure, or SBOM.

## Commands and results

Commands ran in this worker clone on 2026-07-14 (Asia/Shanghai). No `lake update`, `lake build`,
dependency clone/fetch, checkout, `.lake` mutation, or network request was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1057
  exit 0: rank 249, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-1057/check_obligation_tree.py
  exit 0: the frozen 15-obligation registry and 46 typed edges passed; the pre-proof graph remains M3

bash Stage1_Instances/THM-M-1057/check_validation.sh
  exit 0: network-isolated trust-zero replay elaborated the complete stack; all requested sorry and
  axiom checks passed; captured stdout was 4236 bytes with SHA-256
  4b5c2e9fe47c8baf55d029cb2462feb10c1309a17f4a9c72f7a3183a105b4826

python3 -B Stage1_Instances/THM-M-1057/check_validation.py
  exit 0: exact target, kernel replay, selected trust/provenance, stale authority boundaries,
  receipt, recipe, ownership, and fail-closed decisions passed

python3 -m json.tool Stage1_Instances/THM-M-1057/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1057/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m1057-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1057/check_validation.py
  exit 0: validator syntax checked without writing bytecode into the target

rg prohibited Lean constructs over Stage1_Instances/THM-M-1057/*.lean
  exit 1 (expected no match): no prohibited construct was found after the validator's nested-comment scan

git diff --check -- Stage1_Instances/THM-M-1057 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The predecessor `check_proof.py` is intentionally not a current validation recipe: its fail-closed
proof-worker guard expects base `c45f3c...`, the old DAG item, and that worker's root packet. Its
receipt and sources are hash-bound here, and the Lean proof is independently replayed rather than
weakening the predecessor checker or falsely claiming that it still passes.

## Fail-closed decisions

The first node gate is `dependency.S56-M-1057-PROOF.master_acceptance`. The proof predecessor is
only `[_]`, so accepted state remains `[H1, M3, R3]` with no accepted closed obligation. The frozen
anchor audit says no external Lean candidate was found, while the later proof imports an upstream
project; the provenance graph was not reconciled. The proof receipt provisionally closes ten IDs
using only three exact declarations, while every analytic registry node lacks a terminal proof-body
ID and typed-graph evidence/provenance ID. Validation therefore does not ratify node-specific
coverage or an `M0-*` class.

The primary-source crosswalk remains `H1`; it lacks an immutable pinpoint theorem/premise/errata
map and independent review. Readability remains `R3`. The observed axioms have no accepted
theorem-specific foundation profile, and complete declaration, compiled-object, bootstrap, plugin,
checker, and TCB closure is absent.

Network isolation and fresh local `.olean` outputs strengthen the narrow replay but do not satisfy
the release hermetic gate. There is no separate clean checkout, empty-cache cold bootstrap,
content-addressed offline restoration, deterministic release bundle, distinct signed runner,
independently provisioned cache, second attestation, or independently implemented minimal verifier.
`AUDIT-Z`, `THEOREM-Z`, release, theorem completion, and master acceptance all remain false.

## Status boundary

This is self-tested validation-node evidence for a network-isolated narrow kernel replay, exact
observed axioms, placeholder closure, and selected local provenance. It truthfully records failed
authority, node-specific provenance, source/readability, foundation/TCB, cold-hermetic, and
independent-verification gates. It is not accepted `M0`, `E0/E1`, audit completion, theorem
completion, release, or master acceptance.
