# Statement evidence

Item: `S56-M-1011-STATEMENT`  
Base revision: `6c2108d725fc300302148b2400ef718bbed05d76`

## Frozen target

`Statement.lean` freezes the target as follows:

- universe: `X : Type u`;
- structure on `X`: `MeasurableSpace`, `PseudoMetricSpace`, `BorelSpace`,
  `SecondCountableTopology`, and `CompleteSpace`;
- family: `S : Set (ProbabilityMeasure X)`;
- tightness: mathlib's `IsTightMeasureSet` applied to the image of `S` under the coercion from
  `ProbabilityMeasure X` to `Measure X`;
- relative compactness: `IsCompact (closure S)` in the topology already carried by
  `ProbabilityMeasure X`;
- conclusion: uniform tightness if and only if relative compactness, universally over `S`.

This includes empty and finite families without extra side conditions. `BorelSpace` deliberately
fixes the measurable space to the Borel sigma algebra, rather than the weaker
`OpensMeasurableSpace` boundary in the legacy discovery file. A pseudo-metric plus completeness
and second countability is the concrete mathlib presentation used here for the Polish hypothesis.

## Minimal import

The file has the single direct import `Mathlib.MeasureTheory.Measure.Tight`, the narrow mathlib
module that defines `IsTightMeasureSet` and imports the probability-measure topology needed by the
target. Neither the proof-oriented `Mathlib.MeasureTheory.Measure.Prokhorov` module nor the
Levy-Prokhorov metric API is needed to elaborate the canonical expression.

## Checked transport

`canonicalStatement_iff` is an `Iff.rfl` transport between the named target and its fully unfolded
expression. It checks the family coercion and binder scope without proving either direction of
Prokhorov's theorem. The legacy statement used a set comprehension with an existential equality;
the frozen target instead uses the definitional image of the injective coercion, avoiding an
unnecessary alternate encoding at the canonical boundary.

## Validation

The following commands were executed from `Formalizations/Lean` unless noted otherwise. Exact
results are recorded after the final self-test run.

| Command | Result |
|---|---|
| `lake env lean ../../Stage1_Instances/THM-M-1011/Statement.lean` | exit 0; `#print` emitted the fully explicit canonical expression with the expected universe, instances, family binder, and equivalence |
| `python3 Stage1_Instances/THM-M-1011/check_statement.py` (repository root) | exit 0; expression digest `5711575e...e812`; four structural mutations killed; pinned Lean 4.29.0 and mathlib `8a178386...a95` |
| `python3 Docs/tools/check_stage1_standard.py` (repository root) | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` (repository root) | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1011` (repository root) | exit 0; rank 260, planned, theorem completion false |
| `git diff --check -- Stage1_Instances/THM-M-1011` (repository root) | exit 0; no output |

## Status boundary

This receipt supports exact statement elaboration only. Primary-source theorem/page/errata review,
anchor and terminal-body audit, proof obligations, proof closure, hermetic replay, and independent
acceptance remain downstream gates. No `H0`, `M0`, `R0`, audit-complete, or theorem-complete claim
is made.
