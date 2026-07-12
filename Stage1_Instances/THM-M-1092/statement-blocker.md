# Exact-statement gate: blocked

Item: `S56-M-1092-STATEMENT`

## Decision

The exact Kolmogorov forward/backward target cannot be truthfully selected from the accepted intake
and repository source snapshot. The complete repository-level source statement is only
"differential equations for transition densities" (`Docs/researches/math_theorems.md`, entry
`THM-M-1092`). It does not fix a theorem, equation number, or the assumptions needed to distinguish
the following materially different targets:

- finite, countable, or general measurable state space;
- a transition matrix, kernel, density relative to a reference measure, or operator semigroup;
- strong, weak, or pointwise differentiation and the relevant generator domain;
- a conservative or sub-Markov process, possible explosion, and boundary conditions;
- the forward generator on densities, an adjoint on measures, or the backward generator on test
  functions;
- time-homogeneous versus two-time transition laws, including sign and composition conventions.

The intake names Kolmogorov's 1931 paper and Dynkin's *Markov Processes* as discovery candidates,
but explicitly records that no stable edition, precise theorem/page, assumptions, or errata have
been inspected. Those citations therefore cannot decide the alternatives above. The legacy
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_216.lean` is also ineligible as authority: it
chooses arbitrary `backwardGenerator` and `forwardGenerator` fields, and its proposed implication
does not derive either differential equation from its hypotheses. Reusing it would freeze a false
or underspecified proposition rather than the exact source theorem.

A finite-state matrix-exponential theorem could be stated in the pinned environment, but doing so
would narrow the repository's transition-density claim without source authorization. Conversely,
introducing arbitrary operators or taking either desired equation as a structure field would encode
the conclusion as data. Both routes are rejected as substitution.

## Lean substrate checked

`StatementProbe.lean` uses only these pinned mathlib imports:

```lean
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.Probability.Kernel.Composition.Comp
```

It elaborates a deliberately noncanonical `SubstrateBoundary` containing the time-zero kernel,
continuous-time composition, density representation, and positive-time differentiability shapes.
It also checks the concrete `Kernel.id`, `Kernel.comp`, `Measure.withDensity`, and `HasDerivAt` APIs.
This establishes that the immediate blocker is statement identity and source fidelity, not the
absence of these basic Lean types. The probe is not an alternate encoding and receives no theorem
or statement-completion credit.

## Validation record

Base revision: `388f85443db876842b04fb42b0e5a952f22f66d9`.

The worker used the existing canonical `.lake` symlink and did not update, fetch, clone, or modify
dependencies.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1092/StatementProbe.lean` (from `Formalizations/Lean`) | 0 | substrate declaration and all five `#check` commands elaborated |
| `lake env lean --version` (from `Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard validator passed for 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | ordered manifest passed for 1546 unique targets |
| `python3 scripts/stage1_target.py show THM-M-1092` | 0 | rank 216, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1092` | 0 | no whitespace errors |

## Gate result and retry condition

First failed gate: rev-5.6 section 5 exact canonical mathematical claim and Lean expression. The
machine status remains `M4`; there is no canonical expression hash, credited transport, or valid
mutation suite to freeze. Retry after an accountable source audit selects a stable edition and
pinpoint theorem/equations and maps all state-space, regularity, domain, generator/adjoint,
explosion, boundary, time, sign, and density conventions to the repository claim.

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is blocked rather
than self-tested complete. No downstream node or theorem-completion state is advanced.
