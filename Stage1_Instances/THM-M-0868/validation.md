# Intake validation

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb` (tree
`e46d642646f80980838b6f016f5d69b817bd464d`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and probable-duplicate
boundaries, the six-node open downstream DAG, scoped intake invariants, a bounded pinned-source
search, and a narrow Lean API probe. It does not validate a canonical Graph Minor Theorem statement
or proof because the exact primary proposition and graph/minor conventions are not frozen.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

## Source discovery boundary

Crossref, OpenAlex, and CORE confirmed Neil Robertson and P. D. Seymour, *Graph Minors. XX.
Wagner's conjecture*, *Journal of Combinatorial Theory, Series B* 92(2) (2004), 325-357, DOI
`10.1016/j.jctb.2004.08.001`, PII `S0095-8956(04)00078-4`. CORE's secondary record carries the
abstract-level infinite-collection/minor wording recorded in the crosswalk.

The primary article body was not accessible for proposition-level inspection: publisher PDF paths
returned access errors and a full Elsevier API view required credentials. Therefore no exact
theorem/page locator, incorporated definitions, proof passage, or correction/errata state is
claimed. External metadata responses were inspected in `/tmp` and were not added to the repository.
They are discovery evidence only, not an accepted primary-source archive or H0 receipt.

## Environment

- Platform: Linux x86_64, kernel `7.0.0-27-generic`, timezone Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package worktree was clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran from the repository root unless a relative working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0868` | 0 | rank 1422, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6362,6367 -- Docs/researches/math_theorems.md` | 0 | all six uncited target fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 6355,6360 -- Docs/researches/math_theorems.md` | 0 | all six probable-duplicate fields originate at the same commit |
| Crossref query for DOI `10.1016/j.jctb.2004.08.001` | 0 | authors, title, journal, volume/issue, November 2004, pages 325-357, DOI, and PII confirmed; response SHA-256 `ca748048c60371506a6189b73555d68cfe88c6f7def29a14674e4b71bc6927fa` |
| OpenAlex lookup for the DOI | 0 | publication identity confirmed, no repository full-text location reported; response SHA-256 `eff521bd8d4ee19842d7f531bb35f683bf24c1f52178597a13fd619a1e36762b` |
| CORE lookup for the DOI | 0 | bibliographic identity and secondary abstract wording confirmed; response SHA-256 `c14e7bda6f32840c3551d150d8a899e84e65af4794eb6621665df7406db8884e` |
| publisher PDF/full-text retrieval attempts | nonzero/access-limited | primary theorem passage unavailable; exact source gate left open rather than inferred |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1` | 0 | empty output; package source worktree clean |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 1 | expected no-match result for graph-minor theorem, SimpleGraph minor/contraction, Wagner-conjecture, and Robertson-Seymour terms; bounded intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0868/IntakeProbe.lean)` | 0 | six adjacent graph-deletion, isomorphism, induced-graph, and WQO APIs elaborated; output SHA-256 `df9641e4f2a8f4eb12f09993327e1251f3b571dda24c5111a888faa3d45b2a8d`; no target or proof body declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and the worker packet | 0 | all four structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0868-pycache python3 -m py_compile Stage1_Instances/THM-M-0868/check_intake.py` | 0 | checker compiled without writing generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0868/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and duplicate hashes, planned H1/M4/R4 boundary, null target, exact artifact inventory, receipt/packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0868/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file no-index whitespace checks plus `git diff --check` | 0 aggregate | no whitespace diagnostics |

## Known open gates

- The exact primary theorem, incorporated graph/minor definitions, assumptions, proof boundary,
  correction history, immutable preservation, and independent review are open.
- Probable duplicate `THM-M-0867` identity, canonical ownership, redirect, and evidence-sharing
  policy are unresolved.
- Graph category, finiteness, collection/sequence and isomorphism representation, deletion and
  contraction semantics, branch-set transport, relation direction, binders, and boundary cases are
  not frozen.
- No canonical Lean target, graph-minor relation, minimal imports, expression/environment
  fingerprints, checked transports, or statement mutation results exist. The bounded API probe
  supplies no root proof.
- Exhaustive anchor and terminal-body audit, discovery protocol, obligation registry, typed graphs,
  proof and composition, trust closure, readable reconstruction, hermetic replay, deterministic
  evidence bundle, independent verification, master acceptance, audit completion, and theorem
  completion remain open.

These failures block statement and theorem execution but do not invalidate a truthful, self-tested
`planned` intake whose purpose is to freeze scope, source debt, duplicate ownership, and the open
task DAG. Only the integration lane may accept the provisional worker receipt.
