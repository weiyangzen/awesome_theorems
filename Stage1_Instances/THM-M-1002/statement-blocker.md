# Exact-statement gate: blocked

Item: `S56-M-1002-STATEMENT`  
Base revision: `28bf820a9c304cb6e04fd040a0d3384d9ac0b15d`

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The authoritative repository source
record gives only the theorem name "Doob martingale convergence theorem" and describes convergence
of upper and lower martingales. It
does not state a proposition or give a primary-source theorem/page. In particular, it does not
settle the convergence-enabling hypothesis, the strength of the conclusion, or whether the two
order-dual branches form one theorem.

The accepted intake deliberately leaves these statement-defining choices open:

- a uniform bound on `E[X_n⁺]` versus a uniform `L¹` bound or uniform integrability;
- almost-sure convergence to a finite real limit versus an additional integrability or `L¹`
  convergence conclusion;
- the exact lower/submartingale and upper/supermartingale terminology and hypotheses;
- probability-space versus finite-measure formulation, completeness conventions, and source
  degenerate cases.

These alternatives are not definitionally interchangeable. Choosing the convenient existing
uniform-`L¹` wrapper would strengthen a classical one-sided hypothesis, while choosing uniform
integrability would select the separate `L¹` convergence variant. Either choice would substitute
mathematics not fixed by the source record. Consequently this phase fails at exact human-claim
identity, before a canonical declaration, expression fingerprint, minimal-import claim, checked
source transport, or meaningful statement mutations can be accepted.

## Lean discovery boundary

The pinned mathlib snapshot contains
`MeasureTheory.Submartingale.ae_tendsto_limitProcess`. It assumes a natural-number-indexed,
real-valued submartingale on a finite measure space and a single `R : NNReal` bounding
`eLpNorm (f n) 1 mu` for every `n`; its conclusion is almost-everywhere convergence to
`Filtration.limitProcess`. The historical file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_282.lean` elaborates a wrapper around that result
and derives the supermartingale branch by negation.

This check establishes that a stronger candidate statement is expressible in the pinned
environment. It does not establish that candidate as the exact THM-M-1002 statement. The same
mathlib module separately exposes the uniform-integrability theorem
`Submartingale.tendsto_eLpNorm_one_limitProcess`, confirming that the unresolved hypothesis and
conclusion choices select materially different formal targets. No legacy declaration or proof
credit is accepted here.

## Required unblock

An accountable source review must select an immutable edition or scan and record the exact
theorem/page, wording, assumptions, terminology, and relevant errata. It must decide the one-sided
boundedness convention, limit and integrability conclusion, dual-branch organization, measure-space
assumptions, and boundary cases. A later statement execution can then encode that proposition,
minimize its pinned imports, print and hash the elaborated expression, check any alternate encoding,
and mutation-test its hypotheses, domains, binder scope, and boundary policy.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. Lean commands ran from `Formalizations/Lean` using
the existing `.lake` symlink to the canonical pinned artifacts. No dependency update, build, clone,
or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1002` | exit 0; rank 282, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `lake env lean AwesomeTheorems/Stage1/S1_M_282.lean` | exit 0; historical uniform-`L¹` candidate and supermartingale negation wrapper elaborated; discovery evidence only |
| `lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n "theorem ae_tendsto_limitProcess\|ae_tendsto_limitProcess_of_uniformIntegrable" .lake/packages/mathlib/Mathlib/Probability/Martingale/Convergence.lean` | exit 0; located the pinned convergence declarations, including `ae_tendsto_limitProcess_of_uniformIntegrable` at line 322 |
| `sha256sum lean-toolchain lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked source transport, and mutation tests.
The assigned statement phase is therefore not self-tested or complete, and no
`.stage1-worker-selftest.json` is emitted. This artifact claims no theorem completion and no credit
for any downstream node.
