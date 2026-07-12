# Lean 4 anchor audit

Item: `S56-M-0373-ANCHOR_AUDIT`  
Target: `Stage1Instances.THM_M_0373.CoronaTheoremTarget`  
Audit date: 2026-07-12  
Worker base revision: `562c428c3d520ab42bba305174b7cad9409d7c0b`

## Audit boundary

The comparison target is the frozen finite-generator Bezout formulation on the open complex unit
disc. The audit searched repo-local Lean sources, the complete source tree of pinned mathlib, and
public Lean 4 discovery services. Queries included `corona`, `Carleson`, `CoronaTheorem`, `corona
theorem`, `corona problem`, `HInfinity`, `H-infinity`, and `H-infinity theorem prover`. A name or
unit-disc API alone was not treated as proof closure.

This is a completed bounded candidate inventory, not an exhaustive-discovery claim. GitHub's
repository metadata search was available, but grep.app's public code index returned HTTP 503 for
every attempted query. That access failure is retained and receives no negative-result credit.

## Pinned mathlib

The Lake manifest pins mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; the existing dependency checkout reports that exact
revision. Recursive, case-insensitive searches of all pinned `Mathlib/**/*.lean` sources found no
`corona` or `Carleson` hit. Searches for common bounded-analytic aliases found no `HInfinity`, `H∞`,
`BoundedAnalytic`, or equivalent named theorem family.

Mathlib supplies relevant infrastructure, but no terminal candidate:

| Pinned declaration family | Relevance | Exact-target status |
|---|---|---|
| `AnalyticOnNhd.add`, `AnalyticOnNhd.mul` | closure operations for analytic Bezout expressions | substrate only |
| `Bornology.IsBounded.mul`, `Bornology.IsBounded.union` | bounded-set operations used by finite algebraic combinations | substrate only |
| `Complex.UnitDisc.norm_lt_one` | canonical open-unit-disc boundary fact | encoding support only |

`AnchorAudit.lean` kernel-checks these declarations in the pinned environment. It contains no
`sorry`, axiom, placeholder, wrapper, or proof of the corona target.

## External Lean 4 search

GitHub repository searches for `Corona theorem Lean4`, `Carleson corona Lean`, `HInfinity Lean4`,
`H-infinity theorem prover`, and `corona problem formalization` each returned zero repositories on
2026-07-12. No external candidate was therefore available for statement normalization, immutable
revision inspection, dependency resolution, or repo-local integration. The result is deliberately
weaker than a claim that no formalization exists: repository metadata search is not source-code
search, and the attempted public code-index lane was unavailable.

No exact external machine closure was discovered, so there is no `repo_local_integration_debt` to
leave unresolved. The root remains `M4`, with `formalization_debt`: the local proposition is frozen
and elaborated, while a terminal proof candidate is not known from this bounded audit.

## Commands and results

Commands ran from the worker repository root unless a `cwd` is stated. Existing `.lake` artifacts
were used without update, build, clone, or fetch.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact pinned mathlib commit `8a178386...a95` |
| `rg -n -i --glob '*.lean' 'corona\|carleson' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match result |
| `rg -n --glob '*.lean' 'HInfinity\|H∞\|BoundedAnalytic\|bounded analytic\|Analytic.*IsBounded\|IsBounded.*Analytic' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | four unrelated `IsBoundedSMul` analytic-construction hits; no H-infinity theorem family |
| GitHub repository-search API queries listed above | 0 | zero repositories for all five queries |
| grep.app Lean code-index queries `CoronaTheorem`, `corona theorem`, `HInfinity`, and `H∞` | HTTP 503 | access failure recorded; no negative-result credit |
| `lake env lean ../../Stage1_Instances/THM-M-0373/AnchorAudit.lean` (cwd `Formalizations/Lean`) | 0 | five pinned substrate declarations elaborated |
| `lake env lean ../../Stage1_Instances/THM-M-0373/Statement.lean` (cwd `Formalizations/Lean`) | 0 | frozen exact comparison target still elaborated |
| `python3 ../../Stage1_Instances/THM-M-0373/check_statement.py` (cwd `Formalizations/Lean`) | 0 | exact statement hash unchanged and all four mutations distinguished |
| `python3 -m json.tool Stage1_Instances/THM-M-0373/anchor-audit.json` | 0 | structured inventory parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |

## Verdict and status boundary

The node-specific audit is self-tested and ready for master review. It does not establish `H0`,
prove the corona theorem, change the planned lifecycle, or authorize any obligation-tree, proof,
validation, release, `AUDIT-Z`, or theorem-completion claim. An exact external discovery must be
pinned or vendored and checked through an exact local wrapper before it can receive machine credit.
