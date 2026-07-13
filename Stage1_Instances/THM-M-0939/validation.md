# Intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7`; base tree:
`018557070da18ea1733a82de81a238750c59aa84`. Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-root discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, bounded local declaration search, prohibited-construct hygiene, and whitespace. It does not
validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Source discovery boundary

The Springer landing page and Crossref record corroborated the primary bibliographic candidate:
J. H. B. Kemperman, *On small sumsets in an abelian group*, *Acta Mathematica* 103 (1960),
63-88, DOI `10.1007/BF02546525`. The article body was subscription-gated, so no theorem-level
primary-source mapping is claimed.

Two complete modern source candidates were inspected temporarily outside the repository.
Boothby-DeVos-Montejano arXiv:`1301.0095v2` is 20 pages and 197,059 bytes, with PDF SHA-256
`641f3122...f38e8`; Definitions 4.1-4.4 and Theorem 4.5 give the recursive trio formulation.
Lev arXiv:`math/0508179v2`, PDF SHA-256 `e387d566...a60ff`, gives a pair formulation citing
Kemperman [K60, Theorem 5.1]. These establish a precise theorem family and published proof
candidates, not a canonical root, admitted H0 packet, original-to-modern equivalence, correction
audit, or independent review.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`; Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0939` | 0 | rank 1478, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6861,6866 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref and Springer metadata requests for DOI `10.1007/BF02546525` | 0 | title, author, journal, volume, 1960 date, pages 63-88, and DOI agree; mutable discovery metadata only |
| `curl` of arXiv:`1301.0095v2`, followed by `pdfinfo`, `pdftotext -layout`, and scoped inspection | 0 | 20-page complete modern proof candidate inspected; Theorem 4.5 and its definition chain located; observed PDF SHA-256 `641f3122...f38e8` |
| `curl` of arXiv:`math/0508179v2`, followed by `pdftotext -layout` and scoped inspection | 0 | pair-form candidate and original K60 locator inspected; observed PDF SHA-256 `e387d566...a60ff` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0939/IntakeProbe.lean)` | 0 | six adjacent sumset/stabilizer API signatures elaborated; complete stdout SHA-256 `896394b1...01e8ff`; no target theorem declared |
| bounded `rg` for Kemperman, Scherk, critical pairs/trios, and beat/chord structures in pinned mathlib and repo-local Lean | 1 (expected no exact match) | only a Kneser URL in a VerySmallDoubling comment was found under the broader first pass; no exact target declaration; not an exhaustive anchor audit |
| `python3 -m json.tool` on the three owned JSON files and the worker packet | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0939-pycache python3 -m py_compile Stage1_Instances/THM-M-0939/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0939/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H1/M4/R4 boundary, null target, artifact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0939/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0939 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0939-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact root selection and independent source review,
canonical Lean elaboration and statement mutations, complete anchor audit and discovery freeze,
obligation registry, typed graphs, proof, composition, trust closure, readable reconstruction,
hermetic replay, deterministic release bundle, and independent verification remain open. These
failures prevent statement, audit-completion, and theorem-completion claims, but they do not
invalidate the planned intake.
