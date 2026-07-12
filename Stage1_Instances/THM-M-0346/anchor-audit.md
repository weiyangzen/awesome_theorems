# Lean 4 anchor audit

## Audit identity

- Item: `S56-M-0346-ANCHOR_AUDIT`
- Frozen target: `Stage1.THM_M_0346.CarlesonTarget` in `Statement.lean`
- Repository base: `cc46a50150dae27c90dca0938294d8da17db9109`
- Local toolchain: `leanprover/lean4:v4.29.0`
- Pinned local mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- Audit date: 2026-07-12

This audit searched the repository, the complete local pinned mathlib source tree, the other
already-present Lake packages, and GitHub for public Lean repositories at immutable revisions. It
does not import, build, or award kernel closure to an external project.

## Pinned mathlib inventory

The only directly relevant declarations found in
`Mathlib.Analysis.Fourier.AddCircle` are:

| Declaration | What it proves | Relation to the target | Classification |
|---|---|---|---|
| `hasSum_fourier_series_L2` | Fourier series sums to an `Lp` element in the `L²` topology | Same coefficients and circle API, but not pointwise or a.e. convergence | infrastructure only |
| `hasSum_fourier_series_of_summable` | Uniform convergence for a continuous function whose Fourier coefficients are summable | Stronger regularity assumption not available for arbitrary `L²` input | ineligible theorem |
| `has_pointwise_sum_fourier_series_of_summable` | Everywhere pointwise convergence under the same summability hypothesis | Conclusion resembles the target, but its hypothesis and continuous-function domain broaden neither to all `L²` functions nor to the frozen `Lp` target | ineligible theorem |

A case-insensitive source search for `carleson`, pointwise Fourier convergence, and a.e. Fourier
convergence found no Carleson or Carleson-Hunt declaration in pinned mathlib. The similarly named
`PointwiseConvergenceCLM` hits concern tempered-distribution topology and are unrelated. Therefore
mathlib provides the encoding and approximation infrastructure but no exact closure of
`CarlesonTarget` at the pinned revision.

## External Lean 4 candidate

The credible public candidate is
[`fpvandoorn/carleson`](https://github.com/fpvandoorn/carleson/tree/80e151dff5ddce2426079ec6392616496a4ec927),
audited at commit `80e151dff5ddce2426079ec6392616496a4ec927` (commit date 2026-07-10). The
downloaded GitHub commit archive had SHA-256
`eefa873432b17516302b7352949797adc6c13497338e39578170184b9dcdf3c6`. Its license is
Apache-2.0, its toolchain is `leanprover/lean4:v4.30.0-rc2`, and its manifest pins mathlib
`1a4917a18b30ea1333c195e597067fe044ac9176`.

The closest candidate is `carleson_hunt` in
`Carleson/Classical/CarlesonHunt.lean`:

```lean
theorem carleson_hunt {T : ℝ} [Fact (0 < T)] {f : AddCircle T → ℂ}
    {p : ℝ≥0∞} (hp : 1 < p) (hf : MemLp f p AddCircle.haarAddCircle) :
    ∀ᵐ x, Tendsto (partialFourierSum' · f x) atTop (nhds (f x))
```

At `p = 2`, this is mathematically stronger than the frozen target. It is not an exact declaration:
the external theorem consumes a function plus `MemLp`, uses the project's
`partialFourierSum'`, and lives against a newer Lean release and a different mathlib revision. A
checked adapter must relate an `Lp` representative to `MemLp`, prove equality between
`partialFourierSum'` and this dossier's `symmetricPartialSum`, and transport the a.e. conclusion.
No such adapter is present or checked here.

The same commit also contains `classical_carleson`, but that declaration only treats continuous
periodic functions and is strictly too weak for the arbitrary `L²` target. Repository-wide textual
inspection of the commit archive found actual `sorry` terms in nine Lean files, including one in
`Carleson/Classical/CarlesonOnTheRealLine.lean` and several `ToMathlib` modules. No `sorry` occurs
textually in `Carleson/Classical/CarlesonHunt.lean`; however, textual absence is not a terminal-body
or transitive-axiom proof. The external project was not an existing pinned dependency, and its
incompatible dependency artifacts were not fetched or built. Consequently neither
`carleson_hunt` nor any of its transitive bodies receives machine-proof credit in this audit.

GitHub repository search also returned derivative or evaluation repositories, including
`banr1/tailored-carleson`, but no second independently established exact Lean closure was found.
Those results were not treated as candidates because their searched metadata did not identify a
canonical theorem matching the frozen target.

## Decision and debt

- Best candidate: external `carleson_hunt` at immutable commit
  `80e151dff5ddce2426079ec6392616496a4ec927`.
- Current machine classification: `external_upstream_anchor_only`, which is not repo-local closure.
- Debt: `repo_local_integration_debt`, plus unresolved trust/provenance until the exact dependency
  closure is built and `#print axioms`/placeholder checks are performed.
- Root remains open. This phase claims neither `M0`, audit completion, nor theorem completion.
- Required next action: pin a toolchain-compatible external revision or vendor an audited proof
  body, implement the two checked transports above, and validate the resulting exact wrapper.

## Validation record

All local dependency artifacts were used read-only. No `lake update`, dependency clone/fetch, or
build was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0346` | exit 0; rank 839, planned, theorem_complete false |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| scoped `rg` searches over local `.lean` sources | exit 0; only the three non-closing Fourier candidates above |
| GitHub API repository search and immutable raw-source inspection | exit 0; identified `fpvandoorn/carleson` and declarations above |
| immutable commit archive download, SHA-256, and scoped placeholder search | exit 0; archive digest above; actual `sorry` terms found in nine files |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0346/AnchorProbe.lean` | exit 0; all five pinned mathlib declarations elaborated |
| `git diff --check -- Stage1_Instances/THM-M-0346 .stage1-worker-selftest.json` | exit 0; no output |

This is self-tested anchor-audit evidence pending master acceptance. It is deliberately not an
external build receipt or a theorem receipt.

