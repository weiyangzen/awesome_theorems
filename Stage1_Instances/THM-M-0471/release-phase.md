# THM-M-0471 release reconciliation

Item: `S56-M-0471-RELEASE`. Base revision:
`dc600635160cace0916df5234bf8808c39dc656d` (tree
`8ee34b31ec38be1ef067aaab38c9a4cb4935b75a`).

## Exact verdict

The release verdict is **blocked**. The lifecycle remains `planned`, the accepted root vector
remains `[H1, M3, R4]`, `audit_complete=false`, and `theorem_complete=false`. This worker
accepts no receipt and claims neither `AUDIT-Z` nor `THEOREM-Z`.

There is substantive provisional machine evidence. The exact natural-number statement, the two
frozen compositions, both proof roots, and a separately written prime-factor-list reconstruction
all elaborate with the pinned Lean toolchain. The 25 proof and validation declarations are
sorry-free, and the exact roots report precisely `propext`, `Classical.choice`, and
`Quot.sound`. This shows that a missing local proof body is not being disguised as a release
blocker. It does not turn same-worker warm-cache evidence into accepted `M0-W/E1` or release
evidence.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-0471-VALIDATION` is only `[_]`: its receipt is provisional, `accepted=false`,
`release_grade=false`, and has no master acceptance. The authoritative instance and typed graph
also remain root-open with no accepted obligations. The first release-specific failure is immutable
clean input, followed by `S56-10.6-HERMETIC-COLD-BUILD`.

The remaining release cut includes H0 and R0 reviews; accepted source, provenance, foundation, and
TCB closure; an immutable clean snapshot; an empty-cache network-denied cold build plus offline
archive restoration; complete SBOM and license evidence; two distinct signed clean-runner
attestations; an independently implemented minimal verifier; protected adversarial CI; a
build-twice deterministic content-addressed bundle; and master reconciliation.

## Commands and exact results

All commands ran on 2026-07-13 in this worker clone. The scheduler-provided canonical `.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, manifest
resolution, or other dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0471` | 0 | rank 1353, planned, theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision and tree match the immutable identities above |
| `python3 -I -B Stage1_Instances/THM-M-0471/check_release.py --worker-packet .stage1-worker-selftest.json` | 0 | authority, evidence, pins, exact Lean replay, and negative terminal decision agreed |
| JSON parsing, Python compilation outside the repo, scoped prohibited-construct scan, and `git diff --check` | 0 | records parsed, checker compiled, scan passed, and whitespace checks passed |

The nested Lean probe copies only `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
`Validation.lean` to a temporary directory. It invokes the pinned `lake env lean` with an
explicit `LEAN_PATH` inside `bubblewrap --unshare-net`, a read-only host root, and a fresh
writable output directory. It does not invoke the stale predecessor Python checkers as fresh
receipts. The outer Python reconciliation process was not placed in a network namespace; it made no
network request, and this limitation is recorded as a nonrelease boundary.

## Retry boundary

First obtain dependency-legal master acceptance and reconcile the exact root, graph, source H0,
readable R0, provenance, foundation, and TCB state. Then use a separately provisioned immutable
release lane for cold offline restoration, complete TCB/SBOM/license evidence, two agreeing signed
runners, an independently implemented minimal verifier, protected adversarial CI, a reproducible
deterministic bundle, and master reconciliation. Until then this is a self-tested negative release
decision, not theorem completion.
