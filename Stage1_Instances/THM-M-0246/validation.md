# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978`; base tree:
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, the title/attribution/year/gloss conflict, duplicate-target boundaries, JSON and scoped
invariants, a narrow pinned Lean vocabulary probe, bounded name search, prohibited-construct
hygiene, and whitespace. It does not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

The packet-aware validator mode requires the exact worker base and is worker-only evidence. The
packet-free structured recipe is the public replay: it authenticates the recorded base by Git
ancestry and immutable blobs, validates current target/item semantics, and permits the authoritative
intake cursor to move from `[ ]` to `[_]`. The integration lane must still recapture an accepted
receipt; replay does not promote this provisional packet.

## Commands and results

All commands ran on 2026-07-13 in Asia/Shanghai. Commands without an explicit `cwd` ran at the
repository root.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0246` | 0 | rank 1256; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 1773,1778 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1773,1778p' Docs/researches/math_theorems.md \| sha256sum` | 0 | excerpt SHA-256 `c4dd040a...aac49` |
| bounded Encyclopedia of Mathematics, K10plus/GVK, GDZ, and Crossref inspection | 0 | immutable secondary/catalog evidence, a 1923 pinpoint citation, and the 1928 Marcel Riesz scan at Theorems I and II decisively distinguish the families; target correction, complete mapping, errata audit, independent review, and H0 remain open |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at `98dc76e3...`; Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...d81` as recorded in `instance.json` |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0246/IntakeProbe.lean)` | 0 | nine adjacent circle, Haar, Fourier, complex-measure, absolute-continuity, and `Lp` APIs elaborated; no target theorem stated |
| bounded `rg` search for Riesz-brothers, conjugate-function, Hilbert-transform, measure/Fourier, and Riesz theorem names in pinned mathlib | 0 | generic Riesz results and analytic substrate found, but no named exact candidate terminal theorem; intake discovery only, not an exhaustive anchor audit or global absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured files are valid JSON |
| `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0246/check_intake.py').read_text())"` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0246/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and execution-DAG identity, source pins, H5/M4/R4 boundary, null target, artifact hashes, receipt/packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0246/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0246` | 1 (expected no match) | no prohibited proof escape or declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0246 .stage1-worker-selftest.json` plus per-file untracked checks | 0 | no whitespace diagnostics in any new artifact |

## Known open gates

Target identity, an approved immutable primary proposition, complete definition/premise/conclusion/
proof-boundary/errata mapping, duplicate-scope reconciliation, and independent source review remain
open. So do the canonical Lean expression and environment fingerprint, checked transports,
statement mutations, exhaustive anchor audit, discovery protocol, obligation registry, typed
graphs, proof and composition, trust and provenance closure, readable reconstruction, hermetic
replay, deterministic bundle, independent verification, master acceptance, audit completion, and
theorem completion. These failures do not invalidate a truthful self-tested `planned` intake.
