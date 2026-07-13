# Intake validation

Base revision: `940588d30669014430d5a1beb187f2bca118e816` (tree
`42d80725ccbabcdd826ed2bc8b3622ac31ac7695`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, exact catalog and duplicate-target boundary, six-node
open task DAG, structured intake invariants, and a narrow pinned Lean endpoint-API probe. It does
not validate a canonical Hausdorff-Young proposition or proof because neither has been frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0295` | 0 | rank 1299, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 2118,2123 -- Docs/researches/math_theorems.md` | 0 | all six uncited target fields originate at `bcf3f9fa...` |
| `git blame -L 754,759 -- Docs/researches/math_theorems.md` | 0 | separate `THM-M-0103` record has the same attribution/year but a distinct norm-inequality gloss |
| Crossref DOI metadata queries for Hausdorff and Young | 0 | confirmed both bibliographic leads; responses SHA-256 `83d49966...28d233` and `e7d8fd16...e554c`; no exact source result admitted |
| publisher Hausdorff PDF request | 0 | returned a 222431-byte HTML access page rather than article text; SHA-256 `161ec954...301af` |
| EuDML record request | 22 | HTTP 403; recorded as an access limitation, with no source evidence credited |
| `(cd Formalizations/Lean && lake --version && lake env lean --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above; package status clean |
| bounded `rg` for Hausdorff-Young and Riesz-Thorin in repo-local Lean and pinned mathlib | 1, expected | no named declaration; intake discovery only, not exhaustive audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0295/IntakeProbe.lean)` | 0 | six L1/L-infinity and L2 Fourier endpoint APIs elaborated; stdout SHA-256 `05866a11...1d09` |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | structured artifacts are valid JSON after finalization |
| `python3 -c` with `ast.parse` on `check_intake.py` | 0 | validator parsed without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0295/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source/dependency hashes, H1/M4/R4 null target, duplicate record, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0295/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean construct scan over the owned path | 1, expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics |

The external Crossref and publisher hashes are observational discovery data captured during this
worker run; their response bodies are not owned repository artifacts and the scoped checker does
not replay them. They receive no source-status, proof, or acceptance credit.

## Known open gates

The `THM-M-0295`/`THM-M-0103` duplicate boundary, exact primary-source admission and proposition,
Fourier-series versus Euclidean/LCA domain, measures and normalization, scalar field, p/q binders
and endpoints, function-space completion, exact norm constant and conclusion, source corrections,
translation, independent review, canonical Lean target and expression fingerprint, statement
mutations, exhaustive anchor audit, obligation registry, typed graphs, proof and composition, trust
and provenance closure, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion all remain open.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0295-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
