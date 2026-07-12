# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9768-9773` supplies exactly the title `解对初值的连续依赖性`,
attribution to "many mathematicians", a twentieth-century date, the broader gloss
`解对初值和参数的连续性`, importance "high", and status `已验证`. Git blame attributes all six
uncited lines to repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The entry contains
no equation, definitions, binders, hypotheses, conclusion, bibliography, proof boundary, or formal
artifact.

`Docs/Stage0_Blueprint.md:36426-36451` repeats the same mismatch and explicitly leaves the formal
system, foundation, background, exact definitions and premises, proof route, dependencies,
equivalent formulations, axioms, machine status, and artifact links open. The rev-5.6 manifest
retains `已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

The neighboring records are material boundaries. `THM-M-1340` is differentiability with respect to
parameters, and `THM-M-1341` is the variational equation. This intake neither absorbs those roots
nor borrows any eventual evidence from them.

## Inspected source lead

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society, 2012, Section 2.4, pages 42-48, is an authoritative
modern source lead. The author-hosted preliminary edition was inspected from the book's official
page at `https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf`; a stable complete copy had SHA-256
`166e267deab149704c811a72b44d640ebe0cb08fa31bd0b6a48ba317d88a54af` during this run.

- Theorem 2.8 (pages 43-44) compares solutions for possibly different vector fields and initial
  states, giving an exponential estimate from a spatial Lipschitz constant and a field-difference
  bound.
- Theorem 2.9 (pages 44-45) gives local continuity and a Lipschitz estimate for
  `phi(t,s,x)` in evaluation time, initial time, and initial state for a fixed vector field.
- Theorem 2.11 (pages 47-48) treats an explicit parameter `lambda` and concludes `C^k` dependence
  of `phi(t,s,x,lambda)` under `C^k`, `k >= 1`, hypotheses.

The official errata at `https://www.mat.univie.ac.at/~gerald/ftp/book-ode/errata.pdf`, SHA-256
`3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`, was dated 2026-06-23. It
corrects a displayed quantity in the proof on page 45; that correction must be incorporated if
Theorem 2.9 is selected. No listed correction to Theorems 2.8 or 2.11 was identified by the bounded
errata inspection. This source is not accepted as H0: the
catalog does not cite it or say which theorem it intends, and independent source selection,
complete definition/assumption mapping, edition preservation, and review remain open.

## Component crosswalk

| Repository element | Source-family component | Required Lean component | Intake assessment |
|---|---|---|---|
| title: initial-value dependence | Theorem 2.9 or the `f = g` case of Theorem 2.8 | a source-matched solution map and continuity/estimate proposition | recognizable family; root not selected |
| gloss: initial values and parameters | Theorem 2.11 already gives joint `C^k` dependence in `(t,s,x,lambda)`, or the catalog could refer to another source theorem | explicit parameter type, parameterized vector field, common solution domain, and joint-continuity predicate | materially broader than the title |
| "solutions" | unique local solutions of an IVP in the inspected source | exact solution predicate and existence/uniqueness bridge | equation and solution model absent |
| "continuous" | quantitative Lipschitz bounds in Theorem 2.9; `C^k` in Theorem 2.11 | `ContinuousOn`, `LipschitzOnWith`, or `ContDiffOn` according to the selected source | topology and strength absent |
| many mathematicians / twentieth century | broad historical metadata | provenance only | no pinpoint source identity |
| `已验证` | untrusted inventory label | reviewed source packet and kernel receipt would be required | no H or M credit |

## Pinned Lean candidate crosswalk

| Pinned declaration | Machine-checked content | Source mismatch or open bridge |
|---|---|---|
| `IsPicardLindelof` | time-dependent vector field on a normed real vector space; spatial Lipschitz, time continuity, uniform norm, and interval/radius conditions | one strong local hypothesis package, not selected by the catalog |
| `...exists_forall_mem_closedBall_eq_hasDerivWithinAt_lipschitzOnWith` | constructs solutions for initial states in a closed ball and a uniform `LipschitzOnWith` bound in the initial state at each time | fixed vector field; no external parameter and no source-identity closure |
| `...exists_forall_mem_closedBall_eq_hasDerivWithinAt_continuousOn` | constructs a jointly continuous local flow on initial-state ball times time interval | fixed vector field; still no external parameter |
| `ODE_solution_unique*` in `Mathlib.Analysis.ODE.Gronwall` | uniqueness under a Lipschitz bound for solutions already supplied | supporting boundary only; not continuous dependence by itself |

The two flow declarations elaborated under Lean 4.29.0 and pinned mathlib. Their observed axiom
reports are `[propext, Classical.choice, Quot.sound]`. That check authenticates candidate APIs, not
a canonical `THM-M-1339` expression, checked source transport, proof-body audit, or M0 state.

## Source gate

Before the target can leave `H5`, an accountable reviewer must select one stable source proposition
and edition, record exact theorem and page, incorporate the page-45 erratum when applicable,
transcribe every ordered binder, hypothesis, constant, conclusion, and definition, decide whether
the parameter clause is conjunctive or a separate target, and justify the boundary against
`THM-M-1340` and `THM-M-1341`. A second qualified reviewer must approve the mapping. Only then may
the statement phase choose a minimal Lean import, expression, transports, and mutation fixtures.
