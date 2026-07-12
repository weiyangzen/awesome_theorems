# THM-M-0322 release decision handoff

## Exact verdict

`S56-M-0322-RELEASE` is **blocked**. The lifecycle stays `planned`, the authoritative root vector
stays `[H2, M3, R4]`, and both `audit_complete` and `theorem_complete` stay false. There are no
accepted receipt IDs and no theorem-completion promotion.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The validation prerequisite is only a
`provisional_worker_selftest` receipt and has not been master-accepted. The worker therefore cannot
promote even the narrow exact-root kernel result to authoritative `M0-W` state.

## Evidence reconciliation

The validation receipt gives real same-workspace evidence that the exact statement, both
inclusions, their frozen composition, the exact root, and a separately implemented direct root all
elaborate against pinned mathlib. The observed axioms are `Classical.choice`, `Quot.sound`, and
`propext`; the placeholder and unsafe scan passed. This is useful provisional kernel evidence, not
release evidence.

The structured instance and graph remain deliberately unreconciled: the instance is still
`planned` at `[H2, M3, R4]`, while the pre-proof graph still lists reverse inclusion plus source,
foundation, and provenance nodes as open. Only the integration lane may accept and reconcile that
state. `AUDIT-Z` also fails because exact primary-source fidelity and an independently reviewed
readable reconstruction are absent.

`THEOREM-Z` additionally lacks complete transitive provenance/axiom/TCB closure, immutable clean
input, cold empty-cache network-denied replay, offline restoration, SBOM/licenses, protected CI and
mutation gates, two independently provisioned signed attestations, an independently implemented
minimal verifier, and a deterministic content-addressed release bundle. Reusing the shared warm
`.lake` symlink cannot satisfy those gates.

## Validation commands

Commands were run from base revision `bd0d227173ac95971603f633607751754850337e` on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets passed

python3 scripts/stage1_target.py show THM-M-0322
  exit 0: rank 819, planned, L0/rework-required, theorem_complete=false

python3 Stage1_Instances/THM-M-0322/check_validation.py
  exit 0: exact root replay, axiom observation, hashes, pin cleanliness, and same-worker
  differential reconstruction passed; release gates remained blocked

python3 Stage1_Instances/THM-M-0322/check_release.py
  exit 0: blocked dependency, preserved H2/M3/R4 vector, false terminal decisions, and complete
  release cut set agreed

python3 -m json.tool Stage1_Instances/THM-M-0322/release-decision.json
  exit 0: valid JSON

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0322/{Statement,ObligationTree,Proof,Validation}.lean
  exit 1 with empty output: pass, no prohibited placeholder or local declaration

git diff --check -- Stage1_Instances/THM-M-0322
  exit 0: no whitespace errors
```

No dependency update, build, clone, fetch, or `.lake` mutation was performed. The pre-existing
untracked `.lake` symlink is excluded from changed paths and is not release evidence.

## Retry boundary

The integration lane must first accept and reconcile the prerequisite evidence. Separate qualified
review and release lanes must then close H0/R0, full trust and supply-chain evidence, hermetic and
independent reproduction, and the deterministic bundle. Only master acceptance can advance the
authoritative state.
