# Statement-phase blocker

Item: `S56-M-1321-STATEMENT`  
Base revision: `86b5fbdd7aeb66bbca3069f46c207c1d5f20790e`

## Failed gate

The exact-statement gate is blocked before Lean elaboration. The repository's only source wording
is "lower bound for the first eigenvalue of a convex domain". The intake's identified Zhong-Yang
paper instead concerns the first nonzero Laplace-Beltrami eigenvalue of a compact Riemannian
manifold under nonnegative Ricci curvature. The repository wording does not specify the operator,
boundary condition, eigenvalue ordering, geometric hypotheses, dimension, or normalization needed
to turn a convex-domain reading into one proposition. Choosing the classical manifold theorem
would silently correct the repository statement; choosing a Neumann convex-domain theorem would
substitute a differently attributed result. Neither choice is permitted without accepted source
resolution.

The pinned mathlib tree also has no source match for `Ricci`, a Laplace-Beltrami operator, or the
Zhong-Yang/Payne-Weinberger eigenvalue-diameter theorem. Consequently, an honest concrete
Riemannian target cannot be expressed using the pinned APIs found in this checkout. Introducing an
abstract spectral-gap parameter or a structure field containing the desired inequality would no
longer be the source theorem.

No `Statement.lean` is created: there is no exact proposition to elaborate, and parser success for
an invented surrogate would not satisfy this phase. No proof or theorem-completion claim is made.
The root remains `[H3, M4, R4]`, with `audit_complete=false` and `theorem_complete=false`.

## Validation evidence

Commands were run from the repository root unless a command shows another directory.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1321` | 0 | rank 483; `L0`; `rework_required`; planned; theorem completion false |
| `rg -n -C 12 'Zhong-Yang估计\|Zhong.Yang' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | only the underspecified convex-domain wording and metadata were found |
| `rg -n -i 'ricci\|laplace.?beltrami\|first (positive\|nonzero).*eigen\|eigenvalue.*diameter\|diameter.*eigenvalue\|payne.?weinberger\|zhong.?yang' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no match in the pinned mathlib source tree |

The existing `.lake` link/artifact was read only. No dependency update, build, clone, or fetch was
run. A `lake env lean` elaboration command is inapplicable because exact source identity is the
first failed gate and no valid Lean target exists.

## Retry condition

An integration owner must provide and accept a stable primary-source theorem/page (and errata
status), explicitly reconcile the convex-domain wording with the Zhong-Yang attribution, and freeze
all operator, boundary, spectrum, curvature, diameter, and degenerate-case conventions. If the
accepted claim is the classical manifold theorem, the retry also needs pinned concrete Lean APIs
for its Riemannian Laplacian, first positive eigenvalue, and Ricci hypothesis. Only then can this
phase create and elaborate the exact target with minimal imports and mutation checks.
