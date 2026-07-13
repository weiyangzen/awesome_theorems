# Intake validation

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d`; base tree:
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`.

This validation covers target membership, source provenance, planned-dossier structure, exact owned
file invariants, the open downstream DAG, and a narrow pinned Lean API probe. Because the repository
record is a topic/gloss rather than a stable proposition, it covers no canonical statement,
expression fingerprint, statement mutation, accepted source, formal proof body, or root closure.

The automation-provided canonical `.lake` symlink and pinned packages were used read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
pre-existing untracked symlink and new worker artifacts make this nonrelease evidence.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0884` | 0 | rank 1436, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; it was preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base commit and tree shown above |
| `git blame -L 6474,6479 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| immutable retrieval of `arXiv:1711.06558v1` PDF and source | 0 | PDF 81,953 bytes SHA-256 `cfcdc1d...`; source gzip 5,864 bytes SHA-256 `a6c798d...`; decompressed TeX 15,357 bytes SHA-256 `1a213fc...`; no dependency was created |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; the pinned package worktree remained clean |
| bounded `rg` for Ramanujan, Alon-Boppana, and spectral-expander declarations | 0 | only unrelated analytic-number-theory uses of the Ramanujan name matched; no graph-theoretic candidate was located; this is not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0884/IntakeProbe.lean)` | 0 | eight adjacent APIs elaborated; stdout 1,011 bytes, SHA-256 `338dc5b58bca6fa8b32a5e7bca7bc571b5f33033b8486a444857c78a05af24cd`; stderr empty; no target theorem declared |
| `python3 -m json.tool` on the three structured owned files and worker packet | 0 each | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0884-pycache python3 -m py_compile Stage1_Instances/THM-M-0884/check_intake.py` | 0 | scoped validator compiled with bytecode outside the owned path |
| `python3 -B Stage1_Instances/THM-M-0884/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | membership, authority, H5/M4/R4 boundary, source and dependency hashes, exact file inventory, packet agreement, and six open tasks passed |
| `python3 -B Stage1_Instances/THM-M-0884/check_intake.py` | 0 | public replay mode passed without requiring the scheduler-only root packet |
| prohibited-declaration `rg` over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check`, then scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; new-file difference exit 1 was accepted only when stderr/stdout contained no whitespace error |

## Result

The intake deliverable is self-tested and may be proposed as worker state `[_]`. The provisional
vector is `[H5, M4, R4]`. The first unmet item gate is independent integration-lane replay and
master acceptance of a node-specific intake receipt. The statement/root selection, source and
formal anchor audits, obligation freeze, proof, composition, trust, readable reconstruction,
hermetic replay, independent verification, and release phases remain open. Accordingly
`audit_complete=false` and `theorem_complete=false`.
