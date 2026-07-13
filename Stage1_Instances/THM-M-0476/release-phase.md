# THM-M-0476 release reconciliation

Item: `S56-M-0476-RELEASE`. Base revision:
`309f58b7a54d36653b3483a543c6378eea53882c` (tree
`1051ab77fe56d6e32ba26761bbcfd3ad8a258743`).

## Exact verdict

The release verdict is **blocked**. The lifecycle remains `planned`, the accepted root vector
remains `[H1, M3, R4]`, `audit_complete=false`, and `theorem_complete=false`. This worker accepts
no receipt and claims neither `AUDIT-Z` nor `THEOREM-Z`.

There is substantive provisional machine evidence. The exact natural-prime Wilson statement, its
full frozen factorial-to-units composition, both proof roots, and the separately written
prime-characterization reconstruction elaborate with the pinned Lean toolchain. Twenty-five proof
and validation declarations are sorry-free, and every exact root reports precisely `propext`,
`Classical.choice`, and `Quot.sound`. This supports a candidate `M0-W` route for later master
reconciliation; it does not turn same-worker warm-cache evidence into accepted `M0-W/E1` or release
evidence.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-0476-VALIDATION` is only `[_]`: its receipt is provisional, `accepted=false`,
`release_grade=false`, and has no master acceptance. The authoritative instance and typed graph
also remain root-open with no accepted obligations. The first release-specific failure is immutable
clean input, followed by `S56-10.6-HERMETIC-COLD-BUILD`.

The remaining release cut includes H0 and R0 reviews; accepted source, provenance, foundation,
axiom, and TCB closure; an immutable clean snapshot; an empty-cache network-denied cold build plus
offline archive restoration; complete SBOM and license evidence; two distinct signed clean-runner
attestations; an independently implemented minimal verifier; protected adversarial CI; a
build-twice deterministic content-addressed bundle; and master reconciliation.

## Commands and exact results

Commands ran on 2026-07-14 in this worker clone. The scheduler-provided canonical `.lake` symlink
was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, manifest resolution,
or other dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0476` | 0 | rank 1357, planned, theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision and tree match the immutable identities above |
| `python3 -I -B Stage1_Instances/THM-M-0476/check_release.py --worker-packet .stage1-worker-selftest.json` | 0 | authority, evidence, pins, exact Lean replay, and both negative terminal decisions agreed |
| JSON parsing, Python compilation outside the repo, scoped prohibited-construct scan, and `git diff --check` | 0 | records parsed, checker compiled, scan passed, and whitespace checks passed |

The release checker does not invoke the historical validation Python checker as a fresh receipt:
that predecessor is correctly bound to its earlier base revision and worker packet. Instead, the
release checker authenticates the stored receipt by hash and reruns `check_validation.sh` directly.
That script copies only `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Validation.lean`
to a temporary directory, invokes the pinned `lake env lean` with an explicit `LEAN_PATH` inside
`bubblewrap --unshare-net`, mounts the host read-only, and writes only temporary outputs.

## Retry boundary

First obtain dependency-legal master acceptance and reconcile the exact root, graph, source H0,
readable R0, provenance, foundation, and TCB state. Then use a separately provisioned immutable
release lane for cold offline restoration, complete TCB/SBOM/license evidence, two agreeing signed
runners, an independently implemented minimal verifier, protected adversarial CI, a reproducible
deterministic bundle, and master reconciliation. Until then this is a self-tested negative release
decision, not theorem completion.
