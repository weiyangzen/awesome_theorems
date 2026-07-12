# Intake validation

Base revision: `b72c38f3df59ba12e643e0a20be2dd36c063eafc`; base tree:
`4b2126951b48faf4dd3d85dc1e81962ea29a7004`.

This validation covers target membership, the planned dossier and six-node open task DAG,
repository-source provenance, an authoritative modern source-family inspection, JSON and scoped
invariants, a narrow pinned Lean substrate probe, bounded local search, prohibited-construct
hygiene, and whitespace. It does not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 6.5, pages
198-199, and the author's official errata were retrieved outside the repository and inspected.
The text separately defines Lyapunov, asymptotic, and exponential stability and notes that local
attraction alone need not imply stability. The catalog does not cite the book or select one of
these notions, and the passage is primarily definitional. Its hashes are recorded for intake
provenance, but no canonical root, primary-source chain, H0 review, or source acceptance is claimed.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1342` | 0 | rank 953; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 9789,9794 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '9789,9794p' Docs/researches/math_theorems.md \| sha256sum` | 0 | target excerpt SHA-256 `112e3f51fa8d8b815cddbda141c557b39beeffc98a070ec5df4d105f24e3c763` |
| `curl -L --fail --max-time 90 -sS https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf -o /tmp/THM-M-1342-teschl-ode.pdf` | 0 | retrieved the 364-page author-hosted preliminary text outside the repository; SHA-256 `36243315...ffc36e` |
| `pdftotext -layout /tmp/THM-M-1342-teschl-ode.pdf /tmp/THM-M-1342-teschl-ode.txt` and bounded `rg` inspection | 0 | located Section 6.5's distinct Lyapunov, asymptotic, and exponential definitions and the attraction/stability warning |
| `curl -L --fail --max-time 60 -sS https://www.mat.univie.ac.at/~gerald/ftp/book-ode/errata.pdf -o /tmp/THM-M-1342-teschl-errata.pdf` plus `pdftotext`/bounded `rg` | 0 | official errata SHA-256 `3eacbac5...5996e`; no Section 6.5 or pages 198-199 correction found under the searched terms |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` plus package status | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1342/IntakeProbe.lean)` | 0 | seven pinned ODE, fixed-point, neighborhood, ball, and convergence API checks elaborated; no target theorem stated |
| `rg -n -i --glob '*.lean' 'lyapunov.*stability\|liapunov.*stability\|equilibrium.*stabl\|stable.*equilibrium\|asymptotic.*stabl\|exponential.*stabl' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/ODE Formalizations/Lean/.lake/packages/mathlib/Mathlib/Dynamics` | 1 (expected no match) | no obvious named target theorem under the bounded terms; intake discovery only, not an exhaustive anchor audit or external absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured files are valid JSON |
| `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-1342/check_intake.py').read_text())"` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1342/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and execution-DAG identity, current source hashes, planned H5/M4/R4 boundary, null target, exact inventory, receipt/packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1342/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1342` | 1 (expected no match) | no prohibited proof escape or declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1342 .stage1-worker-selftest.json` plus per-file `git diff --no-index --check /dev/null FILE` checks | 0 | no whitespace diagnostics in any new artifact; no-index exit 1 means a clean nonempty new-file diff and is accepted only when it emits no diagnostic |

## Known downstream failures

- The title and gloss are a theory-family label and noun phrase, not one proposition. No approved
  primary source, corrected target, proof boundary, errata audit, or independent source review
  exists.
- The dynamical model, time and state spaces, equilibrium object, solution and existence policy,
  stability notion, locality, ordered quantifiers, conclusion strength, and boundary cases remain
  open.
- No canonical Lean expression, expression/environment hash, minimal imports, checked alternate
  encoding, or statement mutation is frozen.
- The pinned declarations are only adjacent solution, fixed-point, topology, and convergence
  substrate; no exact source transport or exhaustive anchor audit exists.
- Discovery and obligation freezes, typed graphs, proof, composition, readable reconstruction,
  trust closure, hermetic replay, deterministic bundle, independent verification, release, and
  master acceptance remain open.

## Status boundary

This is provisional worker self-test evidence for `S56-M-1342-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. These downstream failures prevent statement,
audit-completion, and theorem-completion claims, but they do not invalidate the planned intake.
