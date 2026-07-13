# Intake validation

Base revision: `940588d30669014430d5a1beb187f2bca118e816` (tree
`42d80725ccbabcdd826ed2bc8b3622ac31ac7695`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and duplicate-target
boundaries, the six-node open downstream DAG, scoped intake invariants, a bounded pinned-source
search, and a narrow Lean API probe. It does not validate a canonical atomic-decomposition
statement or proof because the catalog wording is not one stable proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It was used read-only. No dependency update, build, clone,
fetch, or other `.lake` mutation was performed. This dirty worker run is nonrelease evidence.

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

All commands ran from the repository root unless a relative working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0300` | 0 | rank 1304, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 2153,2158 -- Docs/researches/math_theorems.md` | 0 | all six uncited target fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 2633,2638 -- Docs/researches/math_theorems.md` | 0 | all six uncited probable-duplicate fields originate at the same commit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1` | 0 | empty output; package source worktree clean |
| `rg -n -i --glob '*.lean' 'HardySpace\|Hardy space\|real Hardy\|atomic decomposition\|RieszTransform\|Riesz transform\|H1Atom\|Atom.*Hardy\|Hardy.*Atom' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 | expected no-match result; no concrete Hardy-space, Riesz-transform, or atomic-decomposition root found; bounded intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0300/IntakeProbe.lean)` | 0 | seven generic pinned interfaces elaborated; output SHA-256 `bed2f49a4a8cb02785ce24e974bb32fe5e08d12b05bddccff30c30fadafecd8c`; no target or proof body declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and the worker packet | 0 | all four structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0300-pycache python3 -m py_compile Stage1_Instances/THM-M-0300/check_intake.py` | 0 | checker compiled without writing generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0300/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and duplicate hashes, planned H5/M4/R4 boundary, null target, exact artifact inventory, packet/receipt agreement, and six open tasks agree |
| `rg -n --glob '*.lean' '(\bsorry\b\|\badmit\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)\b)' Stage1_Instances/THM-M-0300` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0300 .stage1-worker-selftest.json` plus the scoped checker's byte-level file checks | 0 | Git reported no diagnostics (these paths are untracked); the checker separately verified final newlines and absence of CR, NUL, and trailing whitespace in every owned file |

## Known open gates

- The received wording is not one stable proposition. An immutable exact source theorem,
  definition/assumption/conclusion/proof-boundary/correction crosswalk, independent review, and
  integration-lane identity decision for `THM-M-0362` are open.
- The Hardy-space model, domain, dimension, measure, scalar and representative conventions, atom
  support/size/cancellation, coefficients, convergence/equality, both directions, norm comparison,
  constants, ordered binders, and boundary cases are unresolved.
- No canonical Lean target, minimal imports, expression/environment fingerprints, checked
  transports, or statement mutation results exist. The bounded API probe supplies no root proof.
- Exhaustive anchor and terminal-body audit, discovery protocol, obligation registry, typed graphs,
  proof and composition, trust closure, readable reconstruction, hermetic replay, deterministic
  evidence bundle, independent verification, master acceptance, audit completion, and theorem
  completion remain open.

These failures block ordinary statement and theorem execution but do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the ambiguity and ownership boundary. Only
the integration lane may accept the provisional worker receipt.
