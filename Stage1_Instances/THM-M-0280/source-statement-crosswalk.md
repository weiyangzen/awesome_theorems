# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2013-2018` supplies exactly the title `闵可夫斯基不等式`,
attribution to Hermann Minkowski, the year 1896, the gloss `L^p空间的三角不等式` ("the triangle
inequality in L^p space"), importance "high," and status `已验证`. Git history attributes all six
uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
bibliography, theorem locator, formula, definition of `L^p`, exponent range, measure assumptions,
function codomain, measurability or integrability premises, proof boundary, corrections, reviewer,
or formal artifact.

`Docs/Stage0_Blueprint.md:7738-7763` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets this target to `L0 / rework_required`.

## Human-source boundary

The historical attribution and date are retained as a bibliographic lead only. No primary or
authoritative edition, exact theorem/page/formula, incorporated definition chain, assumptions,
proof passage, translation, correction history, errata, immutable archive, or independent review
was inspected and admitted in this intake. Mathematical familiarity with the standard theorem
cannot manufacture those missing source fields. The provisional human state is therefore `H1`, not
`H0`.

## Clause crosswalk

| Catalogue component | Source information available | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `L^p` | notation only; no definition or exponent convention | `eLpNorm`, `lpNorm`, `MemLp`, or `MeasureTheory.Lp` | representation and endpoint regime open |
| "space" | no measure, quotient, scalar, or codomain specified | measurable functions modulo a.e. equality, or representative functions | domains, universes, and typeclasses open |
| "triangle inequality" | no formula or binders | addition closure and `norm_add_le`, or a direct seminorm inequality | exact conclusion and premises open |
| Hermann Minkowski, 1896 | uncited catalogue metadata | source provenance only | no edition, locator, passage, or review admitted |
| `已验证` | untrusted inventory label | source and kernel receipts would be required | no H or M credit |

## Pinned Lean discovery boundary

Pinned mathlib provides several nonidentical exact-topic candidates:

| Module / declaration | Candidate surface | Boundary at intake |
|---|---|---|
| `Mathlib.MeasureTheory.Function.LpSeminorm.TriangleInequality` / `MeasureTheory.eLpNorm_add_le` | extended `eLpNorm` inequality for AE-strongly-measurable functions, `p : ENNReal`, and `1 <= p`, including the infinity branch | strongest general direct candidate; source identity, exact transport, body/provenance, and trust audit open |
| `Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm` / `MeasureTheory.lpNorm_add_le` | real-valued `lpNorm` inequality with a `MemLp f p mu` premise and `1 <= p` | finite-real seminorm surface; its asymmetric explicit premise and behavior when `g` is not `MemLp` require source review |
| `Mathlib.MeasureTheory.Function.LpSpace.Basic` / `MeasureTheory.Lp.instNormedAddCommGroup` | normed additive group on the a.e.-quotient `Lp E p mu` under `Fact (1 <= p)` | quotient-space presentation; instance existence alone does not freeze the intended theorem or relocate its proof body |
| `Mathlib.MeasureTheory.Integral.MeanInequalities` / `ENNReal.lintegral_Lp_add_le` | explicit integral formula for `ENNReal`-valued measurable functions and real `p >= 1` | close to a textbook formula but has a specialized codomain and different exponent representation |
| `Mathlib.Analysis.MeanInequalities` / `Real.Lp_add_le` | finite-sum real-valued Minkowski inequality | special finite discrete case only |

`IntakeProbe.lean` elaborates these interfaces in the pinned environment and prints direct axiom
reports for the theorem declarations. Each printed theorem report is
`[propext, Classical.choice, Quot.sound]`. That authenticates only the named declarations and their
immediate reported axioms; it does not establish canonical statement identity, minimal imports,
terminal body provenance, transitive TCB closure, or any accepted proof state.

## Source gate

Before leaving `H1`, accountable reviewers must preserve an immutable accepted source edition,
pinpoint the statement and all incorporated definitions and assumptions, transcribe the exact
binder order and conclusion, settle exponent/endpoints, measure and codomain conventions, map every
boundary case, audit corrections and errata, and independently approve fidelity to `THM-M-0280`.
Only then may the statement phase choose the minimal pinned imports, serialize the elaborated target
and environment, compile any credited transports, and run the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations.
