# Intake validation

## Boundary

This validates only the `S56-M-0040-INTAKE` planned dossier, scope/source crosswalk, open downstream
DAG, primary-paper provenance, and discovery-only pinned API probe. It does not validate a canonical
Amitsur-Levitzki statement, H0 source closure, exact formal candidate, proof-body provenance,
obligation tree, proof, audit completion, or theorem completion. The authoritative execution item
remains `[ ]`; the root worker packet proposes only `[_]` pending integration-lane review.

Base repository revision: `d66b6e80968b53d5b99774584721ae8976f303a5`.
Base tree: `aaa82721074fccea81033a9a18d21652af89f8e4`.
Initial worktree status contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It points to the canonical pinned artifacts, was used read-only,
and is excluded from this worker's changed paths. No `lake update`, `lake build`, dependency clone,
fetch, or `.lake` mutation was run.

## Commands and results

All commands ran on 2026-07-13 in the isolated worker clone unless another cwd is shown.

| Cwd | Command | Exit | Result |
|---|---|---:|---|
| `.` | `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `.` | `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `.` | `python3 scripts/stage1_target.py show THM-M-0040` | 0 | rank 1518; planned; L0; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `.` | `git status --short --untracked-files=all` | 0 | pre-edit output only `?? Formalizations/Lean/.lake` |
| `.` | `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `.` | `git blame -L 305,310 --porcelain Docs/researches/math_theorems.md` | 0 | all six uncited source-record lines originate at `bcf3f9fa...`; output SHA-256 `edb2494c...1add` |
| `.` | normalized Crossref API inspection for DOI `10.1090/S0002-9939-1950-0036751-9` | 0 | paper identity confirmed; normalized metadata SHA-256 `fdfb4957...cbca` |
| `.` | AMS version-of-record PDF download, SHA-256 capture, `pdfinfo`, `pdftotext`, and formula (2)/Theorem 1/Theorems 2-7 inspection | 0 | 1232089-byte, 15-page PDF; SHA-256 `0e823328...6a0b`; printed pages 449 and 455 define and prove the standard identity; wider package and attribution boundary recorded |
| `.` | normalized Crossref query for Levitzki's earlier lower-bound paper | 0 | DOI `10.1090/S0002-9939-1950-0035758-5` identified; query output SHA-256 `1cd72dd0...32f1`; paper text not credited |
| `Formalizations/Lean` | `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...`, x86_64 release |
| `Formalizations/Lean` | `lake --version` | 0 | Lake 5.0.0-src+98dc76e |
| `.` | `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib `8a178386...`; tree `bdc39a31...` |
| `.` | `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1` | 0 | empty; pinned package source clean |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-0040/IntakeProbe.lean` | 0 | nine finite-permutation, sign, list-product, sum, and matrix-ring interfaces elaborated; stdout SHA-256 `a1bf44b4...7db6`; no target or proof |
| `.` | exact-topic `rg` search of repository Lean and pinned mathlib | 1 (expected no match) | no obvious Amitsur or standard-polynomial/identity declaration; bounded intake discovery only |
| `.` | broader `Levitzki` search | 0 | only the unrelated `Mathlib.RingTheory.HopkinsLevitzki` family located |
| `.` | `python3 -B Stage1_Instances/THM-M-0040/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target, DAG, source, artifact, receipt, and worker-packet invariants pass |
| `.` | scoped prohibited-construct scan of owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `.` | scoped per-file no-index whitespace checks and `git diff --check` | 0/1 | expected new-file differences only; no whitespace diagnostics |

`check_intake.py` also passed without the scheduler packet, so the public dossier can replay its own
invariants. `intake-receipt.json` records exact output and artifact hashes for this provisional
nonrelease snapshot; the receipt excludes itself from its own digest to avoid self-reference.

## Known failures

1. The catalog does not select the paper's standard identity alone, its minimal-degree theorem,
   uniqueness/classification clauses, or a conjunction of these results.
2. Field versus later commutative-ring scope, positive size, matrix index, free-polynomial versus
   evaluation encoding, sign cast, noncommutative product order, and boundary cases remain open.
3. The catalog's `Alexander Levitzki` attribution conflicts with the primary paper and Crossref's
   `J. Levitzki`; no accountable correction, full errata audit, durable archive decision, complete
   premise/proof-node map, or independent source review exists.
4. No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
   alternate encoding, or statement mutation is frozen. The pinned APIs are vocabulary only, and
   the unrelated Hopkins-Levitzki theorem supplies no anchor.
5. Formal anchor/provenance audit, discovery protocol, obligation registry, typed graphs, proof,
   composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
   independent verification, release, and master acceptance remain open.

The first retry condition is independent approval of an exact source clause and complete
source-to-statement map, including the attribution and identity/minimality boundary. No proof-tree
construction is lawful before that statement gate passes.
