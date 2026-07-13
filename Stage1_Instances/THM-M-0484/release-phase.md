# THM-M-0484 release reconciliation

Item: `S56-M-0484-RELEASE`. Base revision:
`e0a9d2c084c4d594e507b71814771c796d0a07a9` (tree
`bec710b64b57f2e7b6363ddc0d32722b57728dc5`).

## Exact verdict

The release verdict is **blocked**. The lifecycle remains `planned`, the accepted root vector
remains `[H1, M3, R4]`, `audit_complete=false`, and `theorem_complete=false`. No receipt is
accepted and neither `AUDIT-Z` nor `THEOREM-Z` is claimed.

There is substantive provisional machine evidence: the exact frozen Lucas-Lehmer criterion, the
two pinned correctness directions, their checked composition, and a separately written residue
route all elaborate at trust zero. They are sorry-free and report exactly `propext`,
`Classical.choice`, and `Quot.sound`. This proves that the blocker is not being disguised as a
missing local theorem body. It does not turn same-worker warm-cache evidence into accepted `M0-W`
or release evidence.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE` because
`S56-M-0484-VALIDATION` is only `[_]`: its receipt is provisional, unaccepted,
non-content-addressed, and `release_grade=false`. The authoritative instance and typed graph also
remain root-open with no accepted obligations. The remaining theorem gates include 17 unverified
internal composition plans, H0 and R0 review, accepted provenance/foundation/TCB closure, a cold
empty-cache network-denied offline replay, complete SBOM/license restoration, independent signed
runners and a minimal independent verifier, protected adversarial CI, a deterministic release
bundle, and master reconciliation.

## Commands and exact results

All commands ran on 2026-07-13 in this worker clone. The scheduler-provided canonical `.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0484` | 0 | rank 1365, planned, theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `e0a9d2c0...a07a9`, tree `bec710b6...dc5` |
| `python3 -I -B Stage1_Instances/THM-M-0484/check_release.py --worker-packet .stage1-worker-selftest.json` | 0 | exact-root/residue replay, input pins, receipts, graph cuts, negative gates, and worker packet agreed; verdict blocked |
| JSON parsing, Python compilation outside the repo, scoped prohibited-construct scan, and `git diff --check` | 0 | records parsed, checker compiled, scan passed, and whitespace checks passed |

## Retry boundary

First obtain dependency-legal master acceptance and reconcile the exact root, graph, source H0,
readable R0, composition, provenance, foundation, and TCB state. Then use a separately provisioned
immutable release lane for cold offline restoration, complete TCB/SBOM/license evidence, two
agreeing signed runners, an independently implemented minimal verifier, protected adversarial CI,
a reproducible deterministic bundle, and master reconciliation. Until then this is a self-tested
negative release decision, not theorem completion.
