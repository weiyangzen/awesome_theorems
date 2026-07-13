# THM-M-0912 release reconciliation

Item: `S56-M-0912-RELEASE`

Base revision: `be4282f0548d68633fface1489942950fd0b9c4d`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H1, M3, R4]`, and both `audit_complete` and `theorem_complete` remain false. This worker accepts no
receipt and makes no `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion claim.

The structured worker recipe is `release-spec.json`; its provisional node receipt is
`release-receipt.json`. That receipt is explicitly `release_grade=false`, records a dirty
warm-cache worker run, and remains subject to integration-lane acceptance.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-0912-VALIDATION` is only a provisional worker projection (`[_]`); its receipt is
non-release-grade, unaccepted, and itself records the proof prerequisite as unaccepted. The first
additional release-assurance failure is `S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The current narrow replay elaborates the exact DLMF-constrained Pascal target through the pinned
mathlib predecessor recurrence and through every frozen proof child. A separately written
`Validation.lean` route imports neither `Proof` nor `ObligationTree` and closes the same target.
Ten proof declarations and two differential declarations are sorry-free, and every observed axiom
report is exactly `[propext]`. This is useful provisional proof evidence, but both routes terminate
at the same pinned mathlib body and ran in this worker against the shared warm `.lake` cache.

Structured authority remains fail-closed. The instance and frozen graph are still `planned` and
`[H1, M3, R4]`, with `root_closed=false` and zero accepted closed obligations. The graph predates
proof closure, so its exact-root proposal has not been reconciled into accepted state. A worker
cannot turn a successful wrapper replay into accepted `M0-W` or update that authority.

`AUDIT-Z` is open because the dossier lacks accepted H0 proof-source fidelity and independently
reviewed R0 reconstruction. Release also lacks an accepted foundation profile, complete transitive
provenance and TCB closure, immutable clean input, empty-cache network-denied cold build, offline
archive replay, complete SBOM/licenses, two qualifying signed runner attestations, an independently
implemented minimal verifier, protected release CI evidence, and a deterministic content-addressed
bundle.

## Commands and results

Commands ran from this isolated worker root on 2026-07-14 (`Asia/Shanghai`). No `lake update`,
`lake build`, dependency clone/fetch, network operation, source edit, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required. |
| `python3 scripts/stage1_target.py show THM-M-0912` | 0 | Rank 1454 remains planned and theorem-incomplete. |
| `bash Stage1_Instances/THM-M-0912/check_proof.sh` | 0 | Ten declarations were sorry-free and all axiom reports were exactly `[propext]`. |
| `python3 -B Stage1_Instances/THM-M-0912/check_release.py` | 0 | Bound current evidence and authority, replayed all four Lean modules in a fresh temporary directory, and derived the blocked verdict. |
| `python3 -m json.tool` on `release-spec.json`, `release-decision.json`, `release-receipt.json`, and `.stage1-worker-selftest.json` | 0 | Every structured release artifact parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0912-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0912/check_release.py` | 0 | The checker compiled without writing generated files into the owned path. |
| `git diff --check -- Stage1_Instances/THM-M-0912 .stage1-worker-selftest.json` | 0 | No whitespace errors; the checker also inspected every untracked handoff file. |

The historical command `python3 -B Stage1_Instances/THM-M-0912/check_validation.py` currently exits
before Lean replay because it requires the validation phase's now-absent worker packet and hardcodes
that phase's base revision. Its immutable receipt remains reconciled provisional evidence, not a
current release recipe. The release checker therefore binds the receipt by SHA-256 and performs a
fresh scoped Lean replay rather than manufacturing the old packet.

Retry requires dependency-legal master acceptance, truthful graph reconciliation, independently
reviewed H0/R0 evidence, complete accepted trust and supply-chain closure, and a separately
provisioned hermetic and independent release run that closes every remaining gate.

Status boundary: this artifact self-tests only the negative release decision. It supplies no
accepted `M0-W`, `E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master acceptance.
