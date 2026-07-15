# THM-M-0509 release-phase reconciliation

Item: `S56-M-0509-RELEASE`
Base revision: `350285c48208616b6e3ad74154d9183d16523cfa`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains `[H1, M4, R4]`, and
both `audit_complete` and `theorem_complete` are false. This worker accepts no receipt and makes no
`AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion claim.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`:
`S56-M-0509-VALIDATION` is provisional `[_]` evidence with `accepted=false` and
`release_grade=false`, not a master-accepted prerequisite. Its nested predecessor failure is proof
master acceptance. Even if both dependencies were accepted, the exact theorem gate fails at
`M0509-T-P2-EXTRACTION`: no body inhabits `EventualPositiveRepresentationCount`, so the checked
equivalence and conditional root handoffs do not inhabit `ChenTheoremTarget`.

## Evidence reconciliation

The release checker freshly replays `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
`Validation.lean` at trust level zero. Each Lean process runs through pinned mathlib's `lake env
lean` inside Bubblewrap with networking unshared, the host root read-only, and output confined to a
fresh temporary directory. The three proof interfaces, conditional handoff, and differential
conditional composition elaborate without placeholders. The five-root observation reports 5203
declarations, 200 modules, only `propext`, `Classical.choice`, and `Quot.sound`, no unexpected
bodyless declarations, and no unsafe declarations. This is current warm-cache, nonrelease evidence.

The weaker accepted state controls several conflicts. `typed-graphs.json` calls definitions,
boundaries, and conditional assembly closed at `M0-L`, but their nodes have no evidence IDs;
`obligation-tree-receipt.json`, the proof receipt, and the validation receipt grant zero closed or
accepted obligations. The target-local task DAG still says every phase is open, and intake prose
still describes statement conventions as unresolved after `Statement.lean` froze them. These
surfaces are not reconciled, so `AUDIT-Z` is false independently of the open root.

The human-source status remains `H1`: no inspected primary edition, theorem/page, exact `P2`
convention, assumptions, errata map, or independent source review exists. No independently accepted
`R0` reconstruction exists. Complete transitive provenance, accepted foundation and TCB profiles,
an immutable clean source snapshot, empty-cache cold build, offline restoration, SBOM/licenses, two
independent signed runners, an independently implemented minimal verifier, protected adversarial CI,
and a deterministic build-twice bundle are also absent.

## Commands and results

Commands ran from the repository root on 2026-07-15 (Asia/Shanghai). Existing pinned `.lake`
artifacts were read only. No update, build, fetch, clone, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0509` | 0 | Rank 883 remains planned, L0/rework_required, and theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0509/check_anchor_audit.py` | 0 | Bounded candidate inventory and pinned support anchors agree. |
| `python3 Stage1_Instances/THM-M-0509/check_obligation_tree.py` | 0 | 15 obligations, 40 typed edges, denominator `74b4c30d...703bd`, and root open at M4. |
| `bash Stage1_Instances/THM-M-0509/check_proof.sh` | 1 | Direct pinned Lean and `lake env lean` replays passed first; historical `check_proof.py` then rejected current HEAD. Recorded as stale predecessor evidence, not current release validation. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0509/check_validation.py` | 1 | Historical checker requires validation base `229ca98e...` and its pre-integration DAG/packet. It is not reused as a current release recipe. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0509/check_release.py` | 0 | Current trust-zero replay and fail-closed release reconciliation passed; verdict blocked, both terminal decisions false, zero accepted receipts. |
| JSON parsing of the release spec, decision, receipt, and worker packet | 0 | All structured artifacts are valid JSON. |
| external-cache `py_compile` of `check_release.py` | 0 | Checker syntax compiled without repository bytecode output. |
| `git diff --check -- Stage1_Instances/THM-M-0509 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The release node can be proposed as `[_]` only because this negative reconciliation is self-tested.
Both `[_]` and `[ ]` remain unfinished. Retry requires an unconditional exact root and dependency-
ordered acceptance, reconciled audit state and H0/R0 reviews, then a separately provisioned hermetic
and independent release run accepted by the master lane.
