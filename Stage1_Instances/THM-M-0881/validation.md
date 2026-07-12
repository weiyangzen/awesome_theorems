# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, planned-dossier structure, source provenance, JSON and
owned-file invariants, and a narrow pinned Lean API probe. Because the repository record supplies no
stable proposition, no canonical target, expression hash, statement mutation, source acceptance, or
proof is claimed. The automation-provided canonical `.lake` symlink and pinned artifacts were used
read-only. No dependency update, build, clone, fetch, or `.lake` mutation was performed. The
pre-existing untracked symlink makes this nonrelease worker evidence.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0881` | exit 0; rank 1035, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | exit 0; only pre-existing `Formalizations/Lean/.lake` was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base commit and tree shown above |
| `git blame -L 6453,6458 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over the manifest, blueprint, DAG, skill, guidelines, source corpus, Stage0, toolchain, lockfile, and relevant pinned graph modules | exit 0; hashes recorded in `instance.json` and `intake-receipt.json` |
| `lake env lean --version` (`cwd=Formalizations/Lean`) | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `lake --version` (`cwd=Formalizations/Lean`) | exit 0; Lake 5.0.0-src+98dc76e; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output, so the pinned package worktree was clean |
| `lake env lean ../../Stage1_Instances/THM-M-0881/IntakeProbe.lean` (`cwd=Formalizations/Lean`) | exit 0; eight adjacent finite-simple-graph, regularity, matrix, and Laplacian interfaces elaborated; no target theorem declared |
| bounded `rg` query for graph-expander terminology over repo-local Lean and pinned mathlib | exit 0; the only match was an unrelated recurrence-dossier sentence saying "spectral expansion remains unchecked"; no graph-expander candidate was found, and this intake query is not an exhaustive anchor audit |

Final JSON checks, Python syntax compilation with an external temporary bytecode cache, the scoped
checker with and without the worker packet, the prohibited-construct scan, and scoped whitespace
checks all passed; the no-match scan's expected exit was 1. Their replay commands and boundaries are
recorded in `intake-receipt.json` and the root worker packet. Because the new dossier is untracked,
`check_intake.py` independently verifies its exact inventory, final newlines, line endings, trailing
whitespace, and SHA-256 values; per-file `git diff --no-index --check` covers new-file whitespace.

## Result

The intake deliverable is self-tested and may be proposed as worker state `[_]`. Its provisional
vector is `[H5, M4, R4]`. The first unmet completion gate is independent integration-lane review and
master acceptance of a node-specific receipt. Exact source selection, canonical statement
elaboration, source/formal anchor audit, obligation freeze, proof, composition, trust closure,
readable reconstruction, hermetic replay, independent verification, and release remain downstream.
Consequently `audit_complete=false` and `theorem_complete=false`.
