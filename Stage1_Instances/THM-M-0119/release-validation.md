# THM-M-0119 release decision

Item: `S56-M-0119-RELEASE`

Base revision: `50db6284742415b7da294d323c820bf4b224711d`

## Exact verdict

The release verdict is **blocked**. Lifecycle remains `planned`, the accepted
root vector remains `H4/M3/R4`, and both `AUDIT-Z` and `THEOREM-Z` are blocked.
`theorem_complete` is false and there are no accepted receipt IDs. The worker
state `[_]` records a self-tested negative reconciliation only; it is not
theorem completion, release-grade evidence, or master acceptance.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-0119-VALIDATION` is an integrated worker projection, but its receipt is
provisional, has `accepted=false` and `release_grade=false`, and the
target-local validation task remains open. Release is therefore not
dependency-legal.

## Theorem boundary

The first failed theorem gate is `S56-5.1-EXACT-TARGET-CONSISTENCY`. The frozen
Lean structure exposes the geometric predicates and
`cohomologyModelsDivisorialSheaf` as independent propositions, with no law
connecting them to the arbitrary `cohomology` family. `Proof.lean` instantiates
that family with `Int`; `Validation.lean`, without importing `Proof`, uses
`ZMod 2`. Both placeholder-free declarations kernel-check the negation of the
exact universe-`{0,0}` specialization. That specialization refutes the
universal universe-polymorphic backend target.

This is a defect in the disconnected Lean encoding, not a refutation of the
mathematical Kawamata--Viehweg vanishing theorem. It supplies no positive proof
credit. The accepted graph still has zero closed obligations and root `M3`;
`M5` is only the provisional diagnosis for the backend encoding.

## Release gates

| Gate | Result | Boundary |
|---|---|---|
| Current narrow Lean replay | provisional pass | The exact statement, conditional composition, and both countermodels elaborate with `--trust=0`; the countermodels report `propext`, `Classical.choice`, and `Quot.sound`. |
| Exact positive root | fail closed | The checked countermodels exclude a positive proof of the frozen target. |
| `AUDIT-Z` | fail closed | Inventory reconciliation, accepted source boundaries, H0, and R0 remain incomplete. |
| Trust and provenance | fail closed | No accepted foundation profile or complete declaration, compiled-artifact, TCB, and provenance closure exists. |
| Hermetic reproduction | fail closed | The replay uses the shared warm pinned `.lake`; there is no new clean checkout, empty-cache cold build, or offline restoration. |
| Supply chain | fail closed | Complete content-addressed dependency archives and SBOM/license closure are absent. |
| Independent verification | fail closed | There are no two signed independent clean runners, separately writable caches, or independently implemented minimal verifier. |
| Deterministic release | fail closed | Protected adversarial CI and a current deterministic signed bundle are absent. |

The historical validation receipt is correctly bound to its own earlier base.
Its snapshot-bound checker is expected to reject a different current `HEAD`;
the release checker therefore binds the receipt by SHA-256 and performs a
separate current-source narrow replay. That replay improves freshness of the
blocker diagnosis but remains warm-cache, same-worker, nonrelease evidence.

## Validation

Commands ran from the repository root on 2026-07-15 (Asia/Shanghai). The
existing pinned artifacts were read only. No `lake update`, `lake build`,
dependency clone/fetch, network access, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets at ranks 1..1546 passed

python3 scripts/stage1_target.py show THM-M-0119
  exit 0: rank 38 remains planned, L0/rework_required, theorem_complete=false

python3 Stage1_Instances/THM-M-0119/check_obligation_tree.py
  exit 0: 33 obligations and 42 typed edges passed; root remains M3/open

python3 Stage1_Instances/THM-M-0119/check_anchor_audit.py
  exit 0: pinned candidates and boundaries agree; no exact positive root is claimed

/usr/bin/python3 -I -B Stage1_Instances/THM-M-0119/check_release.py \
  --worker-packet .stage1-worker-selftest.json
  exit 0: current trust-zero replay and blocked release reconciliation passed
  AUDIT-Z=false; THEOREM-Z=false; accepted receipts=0

python3 -m json.tool Stage1_Instances/THM-M-0119/release-decision.json
  exit 0: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m0119-release-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0119/check_release.py
  exit 0: checker syntax passed without repository bytecode output

git diff --check -- Stage1_Instances/THM-M-0119 .stage1-worker-selftest.json
  exit 0: no tracked whitespace diagnostics; checker hygiene and per-file
  no-index checks cover the untracked release artifacts
```

Inside `check_release.py`, the current Lean replay copies the four unchanged
target modules to a fresh temporary directory, obtains the pinned `LEAN_PATH`
with `lake env printenv`, and invokes `lake env lean --trust=0 -t0` narrowly on
each module. Output hashes match the integrated validation evidence, and the
temporary object and directory are removed.

Retry begins at the statement boundary: replace the disconnected fields with
native or law-bearing definitions that connect the geometry, divisorial
sheaf, and cohomology without assuming vanishing, then refreeze and rerun every
dependent phase. Positive root closure must then be followed by accepted
AUDIT-Z, H0/R0 and trust/provenance closure, hermetic offline reproduction,
supply-chain closure, independent verification, and a deterministic bundle
accepted by the master lane.
