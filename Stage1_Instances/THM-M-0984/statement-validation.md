# Statement validation record

Item: `S56-M-0984-STATEMENT`  
Base revision: `ae3a77da9f973d2fb833b68ab90f37e9c6bc2ddd`

## Frozen target and boundary

`Stage1Instances.THM_M_0984.StrongLawTarget` is the exact modern target selected by intake: the
Banach-valued, integrable, identically distributed strong law under pairwise independence. Its sole
direct import is `Mathlib.Probability.StrongLaw`. `strongLawTarget_iff_bundled` checks that bundling
the measure, sequence, and three hypotheses does not change the claim.

This is not a source-fidelity decision about Borel's 1909 theorem. The terse repository source row
does not specify its variables or assumptions, and the modern target is materially more general
than the historical Bernoulli frequency setting. Human-source status therefore remains `H1`.

## Commands and results

Commands ran inside this worker clone. Lean commands used the existing pinned Lake environment from
`Formalizations/Lean`; no dependency update, fetch, build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0984/Statement.lean` | 0 | target, bundled iff, four mutation fixtures, zero-index boundary, zero-sequence boundary, and explicit target print elaborated |
| `python3 ../../Stage1_Instances/THM-M-0984/check_statement.py` | 0 | expression SHA-256 `d5e802fd68962ef2637033e80b2c948ef0ee7bbc64427ce24c2c86ab23435360`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0984/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `29fd61...8cfe`, `651c8a...1d2`, and `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0984` | 0 | rank 264, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation and boundary policy

The validator compares explicit elaborated expressions. It rejects deleting integrability,
specializing the codomain to `Real`, replacing pairwise independence by the stronger joint
independence predicate, and changing the limit from expectation to zero. Kernel checks establish
that the zero-index empirical average is zero and that the identically-zero sequence has the stated
limit for an arbitrary measure.

This is statement-only evidence pending master acceptance. It provides no upstream-anchor audit,
proof credit, theorem completion, or historical source equivalence.
