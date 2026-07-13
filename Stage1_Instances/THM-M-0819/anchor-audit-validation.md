# THM-M-0819 anchor-audit validation

Item: `S56-M-0819-ANCHOR_AUDIT`

Base revision: `27400857bccc93638c97e9c65859ddf5d5b5f4da`; base tree:
`3762537e0e5ae46cd70b086da49a69e2fd7b275c`.

## Result

The exact frozen target remains
`Stage1Instances.THM_M_0819.DilworthPrimaryTarget`: arbitrary partial orders of attained finite
width, not merely finite carriers. A bounded inventory of nine repo-local, pinned, external,
other-prover, and human-source groups was frozen at `2026-07-13T23:02:43+08:00` and classified.
No exact Lean 4 proof candidate was located.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies `IsChain`,
`IsAntichain`, intersection bounds, `Set.chainHeight`, and cardinality APIs. It contains no
`Dilworth`, `minChainPartition`, `antichainWidth`, or `IsChainPartition` implementation. Its
curated `docs/1000.yaml` entry is only a URL to Vlad Tsyrklevich's external development.

At immutable commit `f82f920f05a381bb1ce5e8903bde33e27f4365b6`, that external file proves
`minChainPartition_eq_antichainWidth` for `[Finite alpha]`. It does not prove the frozen target:
there is no checked ENat-to-exact-Nat, set-of-sets-to-`Fin k`, or finite-to-arbitrary-poset
transport. The source has no textual proof escape, but it is pinned to Lean 4.28.0-rc1 and mathlib
`3234d21e...`. Its direct current-pin check fails at source lines 397, 404, and 597. Lean recovers
with holes, so both recovered terminal declarations report `sorryAx`. This is `M5` with no root
evidence tier, never proof credit. A clean native upstream kernel receipt and transitive
parser-aware trust audit were not captured.

The Coq finite-poset development at immutable commit `74c0cde...` is research evidence in the
wrong backend. The inspected primary preview identifies Theorem 1.1 but omits the complete finite
and transfinite proof, corrections, errata, and independent review. Neither boundary changes `H1`.

The public-search observations are not a replayable negative-evidence packet: a complete per-query
timestamp, status/count, and response-hash ledger was not preserved. They are classified only as
access-limited leads, and no discovery-saturation claim is made.

The truthful root vector remains `[H1, M3, R3]`. The nonexact finite candidate receives no root
evidence tier. This node is worker-self-tested only; it accepts no receipt and does not establish
`AUDIT-Z` or theorem completion.

## Validation

All repository commands ran from the worker clone root on 2026-07-13 Asia/Shanghai unless a
different working directory is shown. The automation-provided `.lake` symlink was used read-only;
no update, build, dependency clone/fetch/checkout, or dependency-cache mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0819` | 0 | rank 1377, planned, legacy artifacts unaccepted, theorem_complete false |
| preflight `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the pre-existing `.lake` symlink preceded the seven authorized changes; base identity recorded above |
| pinned mathlib revision/tree/status and source/blob/hash checks | 0 | revision/tree match the lock, package worktree is clean, and four audited files plus license match the ledger |
| bounded repo-local and all-materialized-package exact-topic searches | 0 | 2461 tracked Lean files and 9676 dependency Lean files covered; only the owned statement and mathlib's external locator are relevant hits |
| bounded mathlib history inspection | 0 | curated locator and adjacent helper commits found; no pinned implementation declaration |
| immutable `vlad902/misc-lean-proofs@f82f920...` archive/source/lock/license inspection | 0 | source, manifest, toolchain, license, terminal type/body, and hashes match the ledger; textual proof-escape scan is empty |
| `cd Formalizations/Lean && lake env lean /tmp/Dilworth-f82f-check.lean` | 1, expected blocker | failures at lines 397, 404, and 597; recovered declarations report `sorryAx`; output SHA-256 `01a36fd...` |
| bounded GitHub, grep.app, and Sourcegraph public queries | access-limited | no additional credible candidate established; inaccessible or timed-out surfaces are not negative evidence and saturation is not claimed |
| `cd Formalizations/Lean && LC_ALL=C LANG=C NO_COLOR=1 lake env lean ../../Stage1_Instances/THM-M-0819/AnchorAudit.lean` | 0 | exact audit copy and seven adjacent APIs elaborate; stdout SHA-256 `d2e476ab...`; no target proof or recovery hole |
| `LC_ALL=C LANG=C NO_COLOR=1 python3 -B Stage1_Instances/THM-M-0819/check_anchor_audit.py` | 0 | identity, ownership, pins, hashes, 9/9 classifications, M5 candidate, M3 root, receipt, and worker packet agree |
| `python3 -m json.tool` on the four new JSON files; `python3 -c "import ast,pathlib; ast.parse(...)"` on the checker | 0 | all structured artifacts parse and the validator has valid Python syntax |
| per-file `git diff --no-index --check /dev/null <file>` over all seven declared paths; `git diff --check -- Stage1_Instances/THM-M-0819 .stage1-worker-selftest.json` | 0 | every new file has no whitespace diagnostic; no-index status 1 was treated only as the expected new-file difference |

The external replay used source SHA-256 `4bc86897...` at the listed temporary path and was rerun
before finalization with the recorded exit and output hash. That temporary source and the raw public
query responses are not part of this handoff, so those rows are worker observations rather than
self-contained or content-addressed recipes. The integration lane must recapture them before any
stronger evidence claim.

## Boundary

The first node gate awaiting another authority is dependency-ordered master acceptance of the
provisional statement prerequisite and this receipt. The first theorem gate is an exact
placeholder-free kernel proof, or a checked composition and transport from a dependency-eligible
candidate to the arbitrary-poset target. Obligation freeze, proof, full provenance/TCB closure,
readable `R0`, source `H0`, hermetic and independent validation, deterministic release evidence,
`AUDIT-Z`, and theorem completion remain downstream.
