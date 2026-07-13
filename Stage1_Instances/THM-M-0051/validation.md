# Intake validation

Base revision: `d849f42c82f9da2e07c481c7beaeba6d92f86e19`; base tree:
`874c7795eb7b2cc49d6c8479c316b09b039e9786`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source and statement ambiguity, JSON and scoped invariants, a narrow pinned Lean probe
of materially different Grassmann/exterior-algebra candidate surfaces, prohibited-construct
hygiene, and whitespace. It does not validate a canonical theorem statement, source fidelity,
proof, audit completion, or terminal status.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref metadata for Hermann Grassmann's *Die Lineale Ausdehnungslehre ein neuer Zweig der
Mathematik*, DOI `10.1017/CBO9781139237352`, was inspected as a dated mutable discovery input. The
2,648-byte response had SHA-256 `119a63f...5149b`. It identifies a Cambridge University Press 2012
reprint record matching the historical author and work family. No source body was added or
inspected; no exact identity, original-edition passage, formula, definitions, premises, proof,
translation, corrections, or errata were reviewed. It is therefore an H1 bibliographic lead only.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0051` | 0 | rank 1520; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 384,389 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref metadata fetch for DOI `10.1017/CBO9781139237352`; `jq`; `wc -c`; `sha256sum` | 0 | matching monograph author/title and reprint metadata; 2,648-byte transient JSON, SHA-256 `119a63f...5149b`; discovery only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386...ea95`, tree `bdc39a31...e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned package worktree remained clean |
| `sha256sum` on toolchain, lock, and four inspected pinned mathlib modules | 0 | exact hashes recorded in `instance.json` and `intake-receipt.json` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0051/IntakeProbe.lean)` | 0 | exterior-algebra, subspace-dimension, and vector-triple-product candidate interfaces elaborated; five axiom reports printed; output SHA-256 `91a73943...9690` |
| bounded case-insensitive Grassmann, exterior-algebra, and Pluecker search over pinned mathlib and repo-local Lean | 0 | located distinct exterior APIs, subspace and cross-product meanings, and unrelated Grassmannian material; no catalog-identical declaration located; discovery only, not a complete anchor audit |
| `python3 -m json.tool` on owned JSON and the root worker packet | 0 | all finalized structured artifacts parse as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0051-pycache python3 -m py_compile Stage1_Instances/THM-M-0051/check_intake.py` | 0 | scoped validator compiles without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0051/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, source hashes, null target, artifact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0051/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over the owned Lean probe | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 per new file is only the expected content difference |
| `git diff --check -- Stage1_Instances/THM-M-0051 .stage1-worker-selftest.json` | 0 | no tracked-diff whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0051-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source admission and review, identity and
formula selection, canonical Lean elaboration, statement mutations, complete anchor and terminal-
body provenance audit, obligation registry, typed graphs, proof and composition, readable
reconstruction, hermetic replay, deterministic release bundle, and independent verification remain
open. These failures prevent statement, audit-completion, and theorem-completion claims, but they do
not invalidate the planned intake.
