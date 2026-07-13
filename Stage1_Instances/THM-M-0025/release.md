# THM-M-0025 release decision

Item `S56-M-0025-RELEASE` has the exact verdict **blocked**. The lifecycle remains `planned`, the
accepted root vector remains `H1/M3/R3`, and both `AUDIT-Z` and `THEOREM-Z` are blocked.
`theorem_complete` remains false and there are no accepted receipt IDs. This is a self-tested
negative release reconciliation, not theorem completion, release, or master acceptance.

## Evidence reconciliation

The proof and validation receipts contain useful provisional kernel evidence. The exact frozen
Hilbert basis target closes through a local wrapper over pinned mathlib's
`Polynomial.isNoetherianRing`, and it also closes through the frozen child-to-parent composition.
A separately written validation wrapper reaches the same exact root without importing the local
proof module. The inspected declarations are sorry-free and report exactly `propext`,
`Classical.choice`, and `Quot.sound`. This supports a provisional `M0-W` proposal only.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the prerequisite validation receipt is
worker-self-tested, explicitly non-release-grade, and not master accepted. The planned instance has
no accepted proof state, while the frozen typed graph still records `root_closed=false`, `M3`, and
no accepted closed obligations. The historical local task DAG also keeps every task open. The
weaker structured state therefore wins and no lifecycle or debt transition occurs.

The validation receipt's recorded all-in-one recipe is not currently replayable: its checker binds
the historical base `c76fe0f1`, not the integrated release snapshot. Before the release packet was
written, it additionally failed on the validation worker's absent ephemeral self-test packet. The
release checker preserves this stale-recipe failure while running a smaller fresh
temporary-directory Lean replay of `Statement.lean` and `Validation.lean`.

`AUDIT-Z` is unavailable because the discovery, source-boundary, evidence-state, trust-boundary,
and debt inventory is not accepted and reconciled. The dossier also lacks accepted independent
`H0` primary-source and `R0` readability reviews. The first missing release-specific gate is
`S56-10.6-HERMETIC-COLD-BUILD`: evidence reused the shared warm `.lake` symlink rather than an
immutable empty-cache network-denied cold build with offline restoration. There is no complete
transitive provenance/TCB closure, SBOM/license archive, deterministic signed bundle, protected
adversarial CI evidence, two qualifying signed attestations, or independently implemented minimal
verifier.

## Validation

Commands were run from the repository root on 2026-07-13 (`Asia/Shanghai`) using the existing
pinned Lean artifacts read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0025
  exit 0: rank 1070 remains planned and theorem_complete=false

bash Stage1_Instances/THM-M-0025/check_proof.sh
  exit 0: the pinned terminal and three exact proof declarations are sorry-free and report
  exactly [propext, Classical.choice, Quot.sound]

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0025/Validation.lean
  exit 1: direct invocation cannot resolve the sibling Statement module because no local
  Statement.olean is on LEAN_PATH; the release checker uses the required temporary module layout

python3 -B Stage1_Instances/THM-M-0025/check_validation.py
  exit 1 as an expected reconciled blocker: the historical recipe binds base c76fe0f1 rather than
  the current snapshot; without the release packet it also required an absent validation packet

python3 -B Stage1_Instances/THM-M-0025/check_release.py
  exit 0: fresh narrow Lean replay and fail-closed release reconciliation passed
  verdict=blocked lifecycle=planned root_vector=H1/M3/R3
  AUDIT-Z=false THEOREM-Z=false theorem_complete=false accepted_receipts=0

python3 -m json.tool Stage1_Instances/THM-M-0025/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0025 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

Retry requires dependency-ordered master acceptance and authoritative instance/graph/audit
reconciliation, then independent H0/R0 review, complete transitive provenance and TCB closure, an
immutable cold offline-capable release build, supply-chain closure, independent verification, and
a deterministic bundle accepted by the master lane.
