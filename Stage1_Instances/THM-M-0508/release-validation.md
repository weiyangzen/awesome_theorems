# THM-M-0508 release-phase reconciliation

Item: `S56-M-0508-RELEASE`
Base revision: `4d389eb47e043f6f44925a418baee0d034f764ba`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H1, M4, R3]`, and both `audit_complete` and `theorem_complete` are false.
This worker accepts no receipt and makes no `AUDIT-Z`, `THEOREM-Z`, release,
or theorem-completion claim.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`:
`S56-M-0508-VALIDATION` is provisional `[_]` evidence with `accepted=false`
and `release_grade=false`, not a master-accepted prerequisite. Its nested
predecessor failure is proof master acceptance. Even if both dependencies were
accepted, the exact theorem gate fails at `M0508-N-FOURIER` and the remaining
five-node analytic cut: no body inhabits `EventualPositiveRepresentationCount`,
so the checked equivalence and conditional root handoffs do not inhabit
`VinogradovThreePrimesTarget`.

## Evidence reconciliation

The release checker freshly replays `Statement.lean`, `AnchorAudit.lean`,
`ObligationTree.lean`, `Proof.lean`, and `Validation.lean` at trust level zero.
Every Lean process runs through the pinned `lake env lean` environment inside
Bubblewrap with networking unshared, the host root read-only, and output
confined to a fresh temporary directory. The finite-count equivalence,
conditional handoff, two proof interfaces, and differential conditional
composition elaborate without placeholders. The five-root observation reports
2567 declarations, 103 modules, only `propext`, `Classical.choice`, and
`Quot.sound`, no unexpected bodyless declarations, and no unsafe declarations.
This is current warm-cache, nonrelease evidence.

The weaker accepted state controls the recorded conflict. `typed-graphs.json`
calls `M0508-L-COUNT-POS` and `M0508-T-ASSEMBLE` closed at `M0-L`, but both
nodes have empty evidence-ID lists; the proof and validation receipts grant zero
accepted closed obligations. The target-local task DAG still says every phase
is open. The predecessor graph also names `VAL-M0508-*` recipes while
`validation-specs.json` is absent. These surfaces are not reconciled, so
`AUDIT-Z` is false independently of the open root.

The human-source status remains `H1`: no accepted pinpoint primary edition,
theorem/page, assumptions, errata map, node crosswalk, or independent source
review exists. No independently accepted `R0` reconstruction exists. Complete
transitive provenance, accepted foundation and TCB profiles, an immutable clean
source snapshot, empty-cache cold build, offline restoration, SBOM/licenses,
two independent signed runners, an independently implemented minimal verifier,
protected adversarial CI, and a deterministic build-twice bundle are also
absent.

## Commands and results

Commands ran from the repository root on 2026-07-15 (Asia/Shanghai). Existing
pinned `.lake` artifacts were read only. No update, build, fetch, clone, or
dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0508` | 0 | Rank 882 remains planned, L0/rework_required, and theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0508/check_anchor_audit.py` | 0 | Bounded candidate inventory, ten pinned probes, rejected placeholder candidate, and mathlib pin agree. |
| `python3 Stage1_Instances/THM-M-0508/check_obligation_tree.py` | 0 | 17 obligations, 86 typed edges, denominator `79ff122b...53bc2`, and root open at M4. |
| `bash Stage1_Instances/THM-M-0508/check_proof.sh` | 1 | Both direct pinned Lean and `lake env lean --trust=0 -t0` lanes passed before historical `check_proof.py` rejected this release-phase worker packet. The phase-bound checker result is not used as current release validation. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0508/check_validation.py --probe` | 1 | Historical validator rejects current HEAD before Lean because it is snapshot-bound to validation base `5b35bc15...`; not reused as current release validation. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0508/check_release.py` | 0 | Current network-isolated trust-zero replay and fail-closed release reconciliation passed; verdict blocked, both terminal decisions false, zero accepted receipts. |
| JSON parsing of the release spec, decision, receipt, and worker packet | 0 | All structured artifacts are valid JSON. |
| external-cache `py_compile` of `check_release.py` | 0 | Checker syntax compiled without repository bytecode output. |
| `git diff --check -- Stage1_Instances/THM-M-0508 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The release node can be proposed as `[_]` only because this negative
reconciliation is self-tested. Both `[_]` and `[ ]` remain unfinished. Retry
requires an unconditional exact root and dependency-ordered acceptance,
reconciled audit state and H0/R0 reviews, then a separately provisioned
hermetic and independent release run accepted by the master lane.
