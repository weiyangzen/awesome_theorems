# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, duplicate and stronger-neighbor boundaries, JSON and scoped invariants, a narrow pinned
Lean vocabulary probe, bounded name search, prohibited-construct hygiene, and whitespace. It does
not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

The packet-aware validator mode requires the exact worker base and is worker-only evidence. The
packet-free structured recipe is the public replay: it authenticates the recorded base revision by
Git ancestry and immutable base blobs, validates current target/item semantics, and permits the
authoritative intake cursor to move from `[ ]` to `[_]`. The integration lane must still recapture
its own accepted receipt; the provisional worker receipt is not promoted by replay.

## Commands and results

All commands ran on 2026-07-13 in Asia/Shanghai. Commands without an explicit `cwd` ran at the
repository root.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0636` | 0 | rank 1053; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 4713,4718 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '4713,4718p' Docs/researches/math_theorems.md \| sha256sum` | 0 | excerpt SHA-256 `1911b377...fd1f6` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at `98dc76e3...`; Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...d81` as recorded in `instance.json` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0636/IntakeProbe.lean)` | 0 | nine adjacent compactness, convexity, continuity, self-map, finite-dimensional, and fixed-point APIs elaborated; no target theorem stated |
| bounded `rg` search for Brouwer and topological fixed-point theorem names in pinned mathlib | 0 | only unrelated Banach, Tarski, Kleene, Roger, Lawvere, Brouwer-algebra, and Brouwerian-logic occurrences; no named Brouwer topological or compact-convex terminal declaration found; intake discovery only, not a global absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured files are valid JSON |
| `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0636/check_intake.py').read_text())"` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0636/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and execution-DAG identity, current source pins, planned H1/M4/R4 boundary, null target, artifact hashes, receipt/packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0636/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0636` | 1 (expected no match) | no prohibited proof escape or declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0636 .stage1-worker-selftest.json` plus per-file untracked checks | 0 | no whitespace diagnostics in any new artifact |

## Known open gates

An approved immutable source proposition, complete definition/premise/conclusion/proof-boundary/
translation/errata crosswalk, duplicate-scope reconciliation, and independent source review remain
open. So do the canonical Lean expression and environment fingerprint, checked transports,
statement mutations, exhaustive formal anchor audit, discovery protocol, obligation registry,
typed graphs, proof and composition, trust and provenance closure, readable reconstruction,
hermetic replay, deterministic bundle, independent verification, master acceptance, audit
completion, and theorem completion. These failures do not invalidate a truthful self-tested
`planned` intake.
