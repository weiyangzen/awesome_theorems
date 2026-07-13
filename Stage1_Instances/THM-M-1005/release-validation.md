# THM-M-1005 release reconciliation

Item: `S56-M-1005-RELEASE`. Base revision:
`e8499ef6898f9562fb480587db7eb9220c04b6fc` (tree
`d88a39b243dd6a835f2e7463b9805d1cb175fb80`).

The narrow validation runner now resolves the already pinned Lean executable and compiled-library
paths directly. This avoids invoking Lake's package resolver after another concurrent lane left the
shared, unused `flt-regular` source checkout without a valid `HEAD`; no dependency content was
fetched, repaired, or mutated, and the same pinned mathlib artifacts remain the proof inputs.

## Exact verdict

The verdict is `blocked`. Lifecycle remains `planned`, and the conservative accepted root vector
remains `[H2, M4, R4]`. `AUDIT-Z` and `THEOREM-Z` are both blocked; `audit_complete=false` and
`theorem_complete=false`. This worker accepts no receipt and proposes no lifecycle, debt, root, or
obligation promotion.

The exact frozen Doob `L^p` root has useful provisional evidence. A fresh network-isolated replay
elaborates the locally vendored analytic terminal, exact exponent transport, frozen composition,
and a separately written same-workspace transport. The exact proof and differential roots are
transitively sorry-free and use exactly `propext`, `Classical.choice`, and `Quot.sound`. This is
warm-cache worker evidence, not accepted `M0-L/E0` or independent release verification.

Structured authority remains weaker. `instance.json` records `[H2, M4, R4]`; the frozen graph and
proof receipt record `[H2, M3, R4]`; the proof proposes `M0-L`; and the target-local DAG keeps every
phase open with no accepted state. The direct validation dependency is only `[_]`, has
`accepted=false` and `release_grade=false`, and lacks master acceptance. Under the weaker-status
rule, `[H2, M4, R4]` is unchanged.

The validation receipt is also stale under its own invalidation policy. It binds
`check_validation.sh` at `1750a9d5c733a5d4c20818b3bb8d0c88287c0c566f3bdc1a0b18ddb99f86872b`,
whereas the current runner is
`33846322b26f21742a1788e8adcec5299ab66d03c5f2b143b7f7823196bacea2`. The current runner's
separate replay is useful provisional evidence, but it cannot refresh or replace the historical
receipt and supplies no dependency acceptance.

## Separate terminal decisions

`AUDIT-Z` is blocked independently of proof closure. Four early phases have no target-local receipt
file, the source crosswalk still lacks a pinpoint immutable primary theorem/page and independent
review, all fourteen readable obligations remain `R4`, and the audit, source, foundation,
provenance, trust, and debt inventories are not completely reconciled and accepted.

`THEOREM-Z` is therefore also blocked. The current worker checkout and shared `.lake` link are not
an immutable clean release input. There is no empty-cache network-denied cold build, disconnected
offline restoration, complete TCB/SBOM/license archive, two signed independent-runner attestations,
independently implemented minimal verifier, protected adversarial CI record, or deterministic
content-addressed release bundle.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The first release-specific input
gate is `S56-RELEASE-IMMUTABLE-CLEAN-INPUT`, and the first failed release protocol gate is
`S56-10.6-HERMETIC-COLD-BUILD`. The exact remaining cut set and retry condition are recorded in
`release-decision.json` and mirrored by the release receipt.

## Commands and results

Commands ran on 2026-07-14 (`Asia/Shanghai`). No `lake update`, `lake build`, dependency clone or
fetch, checkout, or `.lake` mutation was run. The automation-provided canonical `.lake` symlink was
reused read-only. The historical `check_validation.py` is intentionally bound to its validation
base and validation worker packet. The release checker binds that stale committed receipt only as
inspected input and invokes the packet-independent current `check_validation.sh` for separate
provisional Lean evidence.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1005
  exit 0: rank 285 remains planned, L0/rework-required, and theorem-incomplete

bash Stage1_Instances/THM-M-1005/check_validation.sh
  exit 0: network-isolated exact proof/composition and same-workspace differential roots passed;
  observed axioms were exactly propext, Classical.choice, and Quot.sound; transitive sorry checks
  passed

python3 -B Stage1_Instances/THM-M-1005/check_release.py
  exit 0: release authority, hashes, stale-receipt detection, state conflict, fresh Lean replay,
  worker packet, and fail-closed AUDIT-Z/THEOREM-Z decisions passed

PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-1005/check_release.py
  exit 1 as expected: the checker rejects execution with Python assertions disabled

python3 -m json.tool on release-spec.json, release-decision.json, release-receipt.json, and the
worker packet
  exit 0 for each: structured release artifacts parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-m1005-release-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1005/check_release.py
  exit 0: checker syntax compiled outside the repository

git diff --check -- Stage1_Instances/THM-M-1005 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

Retry requires dependency-ordered master acceptance and reconciliation of every phase, the local
DAG, graph/vector conflict, and exact-root proposal. It then requires accepted audit inventory,
pinpoint H0, independently reviewed R0, complete foundation/provenance/TCB/SBOM closure, and a
separately provisioned cold/offline and independent release protocol through a deterministic bundle.

Status boundary: this artifact self-tests only the negative release decision. It is
`release_grade=false` and supplies no accepted `M0-L/E0`, `AUDIT-Z`, `THEOREM-Z`, release, theorem
completion, or master acceptance.
