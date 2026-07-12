# Statement-phase blocker

Item: `S56-M-1025-STATEMENT`

## Verdict

The exact-statement gate is blocked. The only repository claim is `稳定分布的特征`
("characteristics of stable distributions"). It does not identify a proposition, quantified
variables, either implication direction, or a parameterization. The accepted intake explicitly
leaves the exact variant open. Elaborating a two-summand definition, an n-fold convolution
definition, a characteristic-function classification, or only the Gaussian/Cauchy cases would
therefore select or substitute mathematics that the source does not specify.

In particular, no truthful canonical Lean declaration can yet freeze all of the following:

- strict versus shifted stability and the quantification over positive coefficients;
- two-summand versus all-n convolution formulations;
- whether the claimed "characteristics" include one or both directions of a classification;
- Fourier sign, scale and location convention, especially at `alpha = 1`;
- inclusion of point masses and the `alpha = 2` endpoint.

Consequently this phase does not assign a declaration/expression hash, minimal canonical imports,
checked transports, or mutation receipts. The root remains `M4`; no proof or theorem-completion
credit is claimed. Unblocking requires a primary-source theorem/page (or an explicit master scope
decision) fixing the exact claim and conventions listed above.

## Narrow validation

Base revision: `97a7eb41befd3d09707663f246a3133706a9be08`.

Run on 2026-07-12 from `Formalizations/Lean`:

```text
lake env lean ../../Stage1_Instances/THM-M-1025/statement_probe.lean
```

The command exited 0 using the already pinned toolchain and printed types for
`MeasureTheory.Measure.conv`, `MeasureTheory.Measure.map`, and
`MeasureTheory.IsProbabilityMeasure`. The probe's
two explicit imports, `Mathlib.MeasureTheory.Group.Convolution` and
`Mathlib.MeasureTheory.Measure.Typeclasses.Probability`, establish only that the relevant pinned
measure/convolution API elaborates. They are not claimed minimal for a still-unknown canonical
target; the probe is not that target and receives no statement credit.
No dependency update, build, fetch, or `.lake` mutation was performed.

Additional checks and their results:

```text
python3 Docs/tools/check_stage1_standard.py
# exit 0: 15 assurance groups; 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
# exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1025
# exit 0: rank 501, planned, L0/rework_required, theorem_complete false

git diff --check -- Stage1_Instances/THM-M-1025
# exit 0
```

Because the assigned statement phase is not self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
