# Statement-phase blocker record

Item: `S56-M-1528-STATEMENT`  
Base revision: `bdd6f284636bfb105a8c0dd8fea0603995b2682d`

## Gate decision

The exact-source statement gate is blocked. The repository phrase "the basic equations of general
relativity" and the intake's provisional formula `G + Lambda g = kappa T` do not determine one
theorem. In particular, the checked repository evidence does not freeze a source edition and exact
equation locator, sign conventions, dimension, regularity, constant normalization, matter
assumptions, or whether the target is an equation predicate, a derivation, an existence result, or
an equivalence.

The legacy module elaborates, but it cannot close this gate. Its `EinsteinFieldEquationAt` is only
pointwise algebra over already supplied bilinear forms. Its `StatementShape` places the intended
field equation in a `Prop` field of supplied data and asks for that field back in a conclusion
package. Crediting either declaration would replace the unresolved spacetime claim rather than
elaborate it exactly. No new Lean target was therefore created.

## Commands and results

All commands ran in this worker clone. The Lean command used only the existing pinned Lake
environment; no dependencies were fetched or updated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure passed: 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all rework-required |
| `python3 scripts/stage1_target.py show THM-M-1528` | 0 | rank 196, planned, legacy artifacts unaccepted, theorem incomplete |
| `lake env lean AwesomeTheorems/Stage1/S1_M_196.lean` from `Formalizations/Lean` | 0 | legacy algebraic and abstract declarations elaborated; this is candidate inspection only |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_196.lean` | 0 | hashes `651c8a...1d2`, `321626...2d81`, and `71691e...02d` |

## Retry condition

Preserve an immutable primary-source edition; transcribe and independently check the exact
page/equation and assumptions; freeze conventions and logical force; then elaborate the faithful
Lean expression with removed-hypothesis, changed-domain, binder-scope, and boundary mutations.

This is a truthful blocked statement-phase result. It grants no statement, proof, or theorem
completion credit. Because the assigned phase is not self-tested successfully,
`.stage1-worker-selftest.json` is intentionally absent.
