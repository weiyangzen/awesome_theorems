# Intake validation

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, scope and source crosswalks, the
all-open downstream DAG, structured invariants, and a narrow pinned Lean substrate probe. It does
not validate a canonical Cheeger proposition or proof because source identity and every formula-
changing convention remain open. The automation-provided canonical `.lake` symlink was present
before the work and used read-only. No dependency update, build, clone, fetch, or other `.lake`
mutation was performed. This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- Lean executable SHA-256:
  `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0888` | exit 0; rank 1438, planned, score 86, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before edits | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base commit and tree recorded above |
| `git blame -L 6502,6507 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| source, Stage0, manifest, DAG, skill, guideline, toolchain, lockfile, and relevant mathlib SHA-256 checks | exit 0; exact hashes are recorded in `instance.json` and `intake-receipt.json` |
| `lake env lean --version` and `lake --version` (`cwd=Formalizations/Lean`) | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0888/IntakeProbe.lean` (`cwd=Formalizations/Lean`) | exit 0; eleven adjacent finite-simple-graph, edge, degree, adjacency, Laplacian, positivity, kernel/component, and edge-connectivity interfaces elaborated; complete stdout+stderr SHA-256 `f59320fde116f63f9ee72bd9aa24cee7a6221b4e4461f52c280e8ce1c7ff4a2d`; no target theorem was declared |
| bounded `rg` query for Cheeger, conductance, isoperimetric-constant, edge-expansion, and spectral-gap terminology over repo-local Lean and pinned simple-graph mathlib | exit 0 because two unrelated prose strings matched outside simple-graph mathlib; no graph Cheeger candidate was found; this intake query is not an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after final serialization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0888-pycache python3 -m py_compile Stage1_Instances/THM-M-0888/check_intake.py` | exit 0; no bytecode was written into the owned path |
| `python3 -B Stage1_Instances/THM-M-0888/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after final serialization; authority identity, null target, H5/M4/R4 boundary, source/dependency hashes, artifact inventory, worker packet, and six open tasks agree |
| token-anchored prohibited declaration scan over `IntakeProbe.lean` | exit 1 as expected; no declaration-token match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped whitespace checks and `git diff --check` | no diagnostics; each new file also passed `git diff --no-index --check` against `/dev/null` apart from the expected new-file difference status |

## Known open gates

An approved canonical root, immutable primary source edition and pinpoint theorem, graph-versus-
geometric attribution decision, definition and premise map, proof boundary, corrections or errata,
neighbor ownership, and independent review remain open. So do finite versus locally finite or
infinite and directed versus undirected scope, weight and reversibility assumptions, the spectral
operator, eigenvalue or spectral infimum and attainment, isoperimetric invariant, normalization,
subset cutoff, regularity/connectivity premises, constants, directions, binders, conclusion, and
boundary cases; canonical Lean expression and
environment fingerprint; checked transports and statement mutations; exhaustive anchor and
provenance audit; discovery protocol; obligation registry; typed graphs; proof and composition;
trust closure; readable reconstruction; hermetic replay; deterministic bundle; independent release
verification; master acceptance; audit completion; and theorem completion.

These open downstream gates do not invalidate a truthful, self-tested `planned` intake. The first
unmet gate for this assigned node is integration-lane review and master acceptance of a fresh,
node-specific receipt. The proposed worker state is only `[_]`; authoritative state remains `[ ]`.
