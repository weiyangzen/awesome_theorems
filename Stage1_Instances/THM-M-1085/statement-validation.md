# Statement validation record

Item: `S56-M-1085-STATEMENT`  
Base revision: `7947d9e5d8986f9781776dbcebf381a3c9c000c5`

## Frozen target

`Stage1Instances.THM_M_1085.SlepianTarget` elaborates the intake-selected finite-dimensional
distributional comparison. `HasGaussianLaw` is applied to each full `I -> Real` vector, hence it is
joint rather than merely coordinatewise Gaussian. The vectors may inhabit different probability
spaces. Centering is expressed by coordinate integrals, variance by self-covariance, and the maximum
lower-tail event by `BelowAll`. The latter is definitionally the event that every coordinate is at
most the threshold and avoids an arbitrary maximum default.

The sole direct import is
`Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Basic`. The checked `rfl` transport to
`DirectSlepianShape` verifies the event expansion. No theorem proof is present or claimed.

## Commands and results

Commands ran in this worker clone; Lean commands ran from `Formalizations/Lean` against the existing
pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1085/Statement.lean` | 0 | target, direct-shape transport, four mutations, and singleton boundary elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1085/check_statement.py` | 0 | expression SHA-256 `2af285ae0bb208a80c325d1b8ba89cd273b83d01b2fef018b13e2feca9d43315`; four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1085/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `ac7160...6a9d`, `651c8a...1d2`, and `321626...2d81` |

## Boundary and status

The validator distinguishes removal of equal variance, replacement by deterministic vectors,
loss/re-scoping of substantive hypotheses, and admission of an empty index type. The singleton
boundary theorem checks that `BelowAll` reduces exactly to the sole coordinate event. Singular
covariance and zero-variance vectors remain admitted.

This is self-tested statement evidence pending master acceptance. Source fidelity remains at the
intake boundary until the downstream anchor/source audit; this node does not advance proof,
validation, release, audit-complete, or theorem-complete state.
