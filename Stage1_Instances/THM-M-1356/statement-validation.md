# Statement validation

Item: `S56-M-1356-STATEMENT`

Base revision: `10064cd912bf0d94ab6c8d818dd3a30551a921cd` (tree
`f7483f57d60b00edad176cef2fa658a87622982d`). Validation date: 2026-07-13
(`Asia/Shanghai`).

## Selected target

The exact target is the finite Hurwitz-matrix form of Barkovsky's Theorem 40. For positive
`n`, it quantifies a real descending coefficient vector `a : Fin (n + 1) -> Real` with `a 0 > 0`.
The associated complex polynomial has Lean coefficient `j` equal to source coefficient `a_(n-j)`.
It is strictly stable when every complex root has negative real part. The target equates that
predicate with positivity of source minors `eta_1, ..., eta_n`.

`hurwitzMinor a k` uses `k : Fin n` to denote source `eta_(k+1)`: its determinant is taken on the
first `k+1` rows and columns. Matrix entry `(i,j)` is source coefficient `a_(2*j+1-i)` when the
subtraction is defined, and zero otherwise. The module kernel-checks that `a 0` lands at degree
`n` and that `a 0 > 0` prevents degree drop. Thus the coefficient reversal, exact-degree boundary,
matrix indexing, and zero extension are explicit rather than hidden in prose.

The selected source locations are Barkovsky arXiv:0802.1805v1 printed page 6 (strict stability),
page 18/equation (34) (finite matrix), and page 19/Theorem 40/equations (38)-(39). Hurwitz's 1895
pages 273-274 provide the intake's historical cross-check. This freezes a statement interface; it
does not promote the source axis to `H0`. Complete proof translation, correction or errata review,
independent source acceptance, and master acceptance remain open.

## Lean boundary

The target elaborates as `Stage1Instances.THM_M_1356.RouthHurwitzTarget`. Its explicit serialized
expression SHA-256 is `7901eb74686f457348ec06812b8584c69eb09649779637cbb28b2e7bd84b98bf`.
The checked source-shaped expansion is
`Stage1Instances.THM_M_1356.routhHurwitzTarget_iff_expandedTarget`.

The direct imports are:

- `Mathlib.Algebra.Polynomial.OfFn`
- `Mathlib.Data.Complex.Basic`
- `Mathlib.LinearAlgebra.Matrix.Determinant.Basic`

Deleting any one makes the exact module fail elaboration. The earlier intake import
`Mathlib.Algebra.Polynomial.Roots` was broader discovery substrate and is not imported here.
The checker also serializes four separately elaborated mutations and confirms that none equals the
canonical expression: removed leading-coefficient positivity, rational rather than real
coefficients, changed binder scope, and admitted degree zero.

The automation-provided `Formalizations/Lean/.lake` link to canonical pinned artifacts was used
read-only. No update, build, clone, fetch, or other dependency mutation was run. The worker tree is
dirty and therefore nonrelease evidence.

## Commands and results

Commands ran from the repository root unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1356` | 0 | rank 966, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'`; pre-edit `git status --short --untracked-files=all` | 0 | base identifiers above; only pre-existing `Formalizations/Lean/.lake` was untracked |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| pinned mathlib revision/tree and status checks | 0 | revision `8a178386...`, tree `bdc39a31...`; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1356/Statement.lean)` | 0 | target, coefficient adapter lemmas, checked expansion, four expected mutation rejections, and explicit target expression elaborated |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-1356/check_statement.py)` | 0 | expression hash emitted; four mutations distinguished; every direct-import deletion rejected; mathlib pin agreed |
| `python3 -m json.tool` over `statement.json`, `statement-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all finalized structured artifacts parsed |
| scoped JSON invariant checks | 0 | item, provisional state, target/hash/imports, debt boundary, false theorem completion, changed paths, and receipts agreed |
| prohibited-construct scan over owned Lean/Python statement artifacts | 1 | expected no match for `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, unsafe declaration, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-1356 .stage1-worker-selftest.json` plus per-new-file checks | 0 | no whitespace diagnostics |

An early draft failed narrowly because `Polynomial.ofFn` was not imported, `Fin.castLE` received an
index instead of a size proof, the direct matrix lambda lacked a type ascription, and the complex
mutation referenced a nonexistent `Complex.ofRat`. Those draft errors were corrected before the
recorded recipes passed. No dependency artifact changed.

## Status boundary

This proposal moves the machine axis from `M4` to `M3`: there is now a concrete exact interface,
but no proof of the Routh-Hurwitz criterion. The human and readability axes remain `H1` and `R4`.
No anchor audit, obligation freeze, proof, composition certificate, `H0`, `R0`, audit completion,
theorem completion, release receipt, or master acceptance belongs to this phase.
