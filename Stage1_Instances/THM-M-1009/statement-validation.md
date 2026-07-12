# Statement validation record

Item: `S56-M-1009-STATEMENT`  
Base revision: `bd7798793e8cb0e4120b2ac26910a457207b30d4`

## Frozen target

`Stage1Instances.THM_M_1009.ErdosRenyiLowerBoundTarget` freezes the intake-selected lower-bound
form of the Erdos-Renyi second lemma. It uses real-valued finite sums over `Finset.range n`, an
ordered double sum over the same range, ordinary real division, and the filter limsup. The target
quantifies over a probability measure and measurable events and assumes divergence of the single
probability partial sums.

The sole direct import is `Mathlib.Probability.BorelCantelli`. The local definitions directly
normalize the legacy candidate without importing the legacy module. `lowerBoundTarget_iff_pointwise`
checks binder regrouping in Lean. The full-probability consequence and an ENNReal encoding are not
silently substituted or credited as equivalent.

## Commands and results

All commands ran inside this worker clone. Lean ran from `Formalizations/Lean` against the existing
pinned Lake closure. No update, build, clone, fetch, or mutation of `.lake` was performed. The
pre-existing untracked `.lake` path makes this worker evidence nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1009/Statement.lean` | 0 | exact target, checked regrouping, four mutations, and three zero-index boundary lemmas elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1009/check_statement.py` | 0 | expression SHA-256 `5933a50ff097d2de1336a67d4671b3caf7add728d2be6f8be22f95a0385dec1f`; all four structural mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum ../../Stage1_Instances/THM-M-1009/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `9906d8...d831`, `651c8a...b1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1009` | 0 | rank 289, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation and boundary policy

The validator compares fully explicit elaborated expressions. It distinguishes removal of event
measurability, weakening a probability measure to a finite measure, relocation of the sequence
binder across the measurability premise, and changing initial segments from `range n` to
`range (n + 1)`. The kernel-checked boundary lemmas show that at `n = 0` the numerator sum,
denominator sum, and ratio are all zero under Lean's real-division convention.

These are statement-identity checks, not claims that every mutation is mathematically false. This
is statement-only evidence pending master acceptance and does not prove the theorem or advance any
dependent phase.
