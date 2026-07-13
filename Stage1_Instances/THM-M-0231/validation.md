# THM-M-0231 intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, exact catalog and source-statement boundaries, the
six-node open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does
not validate a canonical Mittag-Leffler statement or proof because source identity and exact
formulation are not frozen. The automation-provided canonical `.lake` symlink existed before
intake and was used read-only; no dependency update, build, clone, fetch, or other `.lake` mutation
was performed. This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status was clean before and after the
  probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0231` | 0 | rank 1243, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 1668,1673 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query for DOI `10.1007/BF02418410` | 0 | G. Mittag-Leffler, Acta Mathematica 4 (1884), pages 1-79 confirmed; response SHA-256 `aa7058a...981`; article retrieval attempts returned access-control HTML, so metadata only |
| Crossref query for DOI `10.1090/gsm/097/13` plus AMS product-page inspection | 0 | Ullrich, Chapter 12, pages 229-243 confirmed; response SHA-256 `cf957f88...cc5`; AMS table of contents confirms the chapter, but exact theorem text was not inspected |
| `sha256sum` over authority inputs, catalog/Stage0 excerpts, toolchain/lockfile, and four pinned mathlib modules | 0 | exact hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version and target recorded above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty before and after the probe |
| bounded case-insensitive search for analytic Mittag-Leffler, principal-parts, prescribed-poles, and meromorphic partial-fraction patterns in repo-local Lean and pinned mathlib | 0 | found the cotangent special case and unrelated inverse-system homonym but no arbitrary analytic prescribed-principal-parts theorem; scoped intake discovery only, not a global absence claim |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0231/IntakeProbe.lean)` | 0 | ten adjacent pinned APIs elaborated; stdout SHA-256 `26c136f8abf6d14c6bc02df15d6cdd8d728a3201257cb647cd137c00cbc5ca15`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured artifacts valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0231-pycache python3 -m py_compile Stage1_Instances/THM-M-0231/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0231/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority/DAG identity, source and dependency hashes, null target, H1/M4/R3 boundary, exact inventory, receipt/packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check`, plus `git diff --no-index --check /dev/null <file>` for every untracked changed file | 0 for whitespace diagnostics | every changed file passed |

## Known open gates

A preserved and approved source proposition; its complete definition, assumption, direction,
convergence, equality, uniqueness, correction and errata crosswalk; and independent source review
remain open. So do the canonical Lean target and minimal imports, expression and environment
fingerprints, checked transports, four statement mutation classes, exhaustive anchor audit,
discovery protocol, obligation registry, typed graphs, proof and composition, source/provenance/trust
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion. These open gates do not invalidate a
truthful self-tested `planned` intake.
