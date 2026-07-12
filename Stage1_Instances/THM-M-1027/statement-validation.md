# Statement validation record

Item: `S56-M-1027-STATEMENT`  
Base revision: `08764d477205bbae07c32197a9a83ac6c07866c9`

## Frozen target

`Stage1Instances.THM_M_1027.WienerExistenceTarget` is the intake-selected abstract-space
existence claim over `NNReal` time and real values. It requires a probability measure,
coordinate measurability, almost-sure zero start, independent centered Gaussian increments with
variance `t-s` for `s <= t`, and almost-sure continuous paths. The sole direct imports are the
mathlib real-Gaussian and independent-process-increment modules.

`PinnedIntakeSourceShape` directly expands the structured target, and
`wienerExistenceTarget_iff_pinnedIntakeSourceShape` checks both directions. Gaussian-process and
natural-filtration adaptation fields from the historical candidate are not silently added to this
root. A canonical path-space construction remains a possible witness, not statement evidence.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` using the
existing pinned toolchain and reused canonical Lake artifacts.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1027/Statement.lean` | 0 | exact target, checked intake expansion, four mutations, and equal-time variance boundary elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1027/check_statement.py` | 0 | expression SHA-256 `be0e748b7e1efd3bbe66636dedd6f5fcde9a5c73afb22b3b5ae7d50a2625cf5e`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1027/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `429c91...001b`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |

## Mutation boundary

The validator compares explicit elaborated expressions and kills a two-sided real-time domain,
removal of path continuity, removal of independent increments, and replacement of duration
variance by unit variance. The kernel-checked equal-time lemma confirms that the ordered-increment
variance convention includes the zero-duration boundary.

This is statement-only evidence pending master acceptance. It does not prove existence or advance
anchor-audit, obligation-tree, proof, validation, or release nodes.
