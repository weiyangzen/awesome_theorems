# Exact-statement gate: blocked

Item: `S56-M-1094-STATEMENT`

## Decision

The exact Kolmogorov backward-equation target cannot be truthfully selected from the accepted
intake and repository source snapshot. The complete repository-level claim is only "evolution
equation for transition probabilities" (`Docs/Stage0_Blueprint.md`, entry `THM-M-1094`). It does
not identify a theorem, equation number, or assumptions that decide among materially different
targets:

- finite, countable, Euclidean, or general measurable state space;
- transition matrix, kernel, density relative to a reference measure, or operator semigroup;
- strong, weak, or pointwise differentiation and the relevant generator domain;
- conservative versus sub-Markov behavior, explosion policy, and boundary conditions;
- time-homogeneous versus two-time transition laws, including sign and composition conventions;
- an equation at time zero or only at positive times.

The intake names Kolmogorov's 1931 paper and Dynkin's *Markov Processes* only as discovery
candidates. It explicitly records that no stable edition, pinpoint theorem/page, assumptions, or
errata have been inspected. Those citations therefore cannot authorize choices for the alternatives
above. The nearby historical `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_216.lean` is also
ineligible as statement authority: it concerns the distinct `THM-M-1092`, supplies an arbitrary
`backwardGenerator`, and its proposed implication does not derive the backward equation from a
definition of the infinitesimal generator.

A finite-state matrix-exponential theorem could be encoded in the pinned environment, but that
would narrow the repository claim without source authorization. Conversely, taking the desired
derivative equation as package data would encode the conclusion as a premise. Both are substituted
targets and are rejected.

## Lean substrate checked

`StatementProbe.lean` uses only these pinned mathlib imports:

```lean
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.Probability.Kernel.Composition.Comp
```

It elaborates a deliberately noncanonical `SubstrateBoundary` containing time-zero identity,
continuous-time composition, density representation, and the familiar positive-time backward
derivative shape. It checks the concrete `Kernel.id`, `Kernel.comp`, `Measure.withDensity`, and
`HasDerivAt` APIs. This isolates the immediate blocker as statement identity and source fidelity,
not absence of these basic Lean types. The probe is not an alternate encoding and receives no
statement or theorem credit.

## Gate result and retry condition

First failed gate: rev-5.6 exact canonical mathematical claim and Lean expression. Machine status
remains `M4`; there is no canonical expression hash, credited transport, or meaningful mutation
suite to freeze. Retry after an accountable source audit selects an immutable edition and pinpoint
theorem/equation and maps every state-space, regularity, domain, generator, explosion, boundary,
time, sign, and representation convention to the repository claim.

## Validation record

Base revision: `5189c0229c937834719a387baffeba3e07335a4c`.

The worker used the existing canonical `.lake` symlink and did not update, fetch, clone, or modify
dependencies.

| Command and working directory | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1094/StatementProbe.lean` from `Formalizations/Lean` | 0 | the substrate declaration and five `#check` commands elaborated |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` from the repository root | 0 | standard validator passed for 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` from the repository root | 0 | ordered manifest passed for 1546 unique targets |
| `python3 scripts/stage1_target.py show THM-M-1094` from the repository root | 0 | rank 534, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1094` from the repository root | 0 | no whitespace errors |

An initial combined invocation incorrectly ran the three root-relative Python commands from
`Formalizations/Lean`; each exited 2 because the relative script path did not exist. They were
rerun separately from the repository root with the successful results above. Lean elaboration and
the whitespace check in that invocation succeeded.

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is blocked rather
than self-tested complete. No downstream node or theorem-completion state is advanced.
