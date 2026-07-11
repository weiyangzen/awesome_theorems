# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Variational integral attains its infimum under Tonelli conditions | L. Tonelli, *Fondamenti di calcolo delle variazioni*, 2 vols., Bologna, 1921-1923 | `S1_M_162.StatementShape` | Primary treatise identified bibliographically, but volume/page/theorem, edition hash, assumptions, and errata are not yet pinned: no H0 |
| Nonempty admissible class and fixed endpoints | Part of the classical fixed-endpoint problem | `TonelliVariationalProblem.admissible`, `nonempty_admissible`, `boundary_conditions_closed` | Candidate fields locate the concepts; the boundary proposition is not connected to a topology or trace operation |
| Convexity in velocity | Classical lower-semicontinuity/direct-method hypothesis | `velocity_convex` | Predicate is explicit, but exact strict/ordinary/quasiconvex variant must follow the selected source |
| Coercive or superlinear growth | Supplies bounds/equicoercivity for minimizing sequences | `coercive_growth : Prop` | Merely an uninterpreted proposition in the legacy candidate; it cannot yield compactness |
| Compactness and boundary closure | Converts bounded minimizing sequences to admissible limits | `compactness_or_weakCompactness : Prop` | Merely an uninterpreted proposition; function space and convergence mode are absent |
| Lower semicontinuity and attainment | liminf inequality followed by minimization | `action_lowerSemicontinuous`; `LowerSemicontinuousOn.exists_isMinOn` | Compact-set minimization is a plausible checked subcase, not evidence for Tonelli's compactness theorem |
| Minimizing curve | action at the selected curve is no greater than at any admissible competitor | `TonelliMinimizerPackage.is_minimizer` | Expected conclusion shape; exact action codomain and integrability policy remain open |

The Stage0 metadata supplies only the Chinese title `Tonelli定理`, the gloss `变分问题的存在性`,
the date 1920, and Leonida Tonelli's name. It does not distinguish the multiple results commonly
called Tonelli's theorem, including the nonnegative-product-measure integration theorem. That
measure-theoretic theorem is expressly out of scope: this target's category, gloss, and legacy
artifact all select calculus-of-variations existence.

The historical candidate models classical derivatives on all functions `Real -> E` and a
real-valued Bochner integral, while a faithful existence theorem normally needs a specified
absolutely-continuous or Sobolev admissible space and an integrability/extended-value convention.
The statement phase must not silently promote that candidate. It must select and pin a primary
theorem, map every premise, elaborate the exact target, and mutation-test nonemptiness, convexity,
growth, boundary closure, domains, and endpoint cases.

No `H0` claim is made. The primary-source edition, theorem/page crosswalk, assumption genealogy,
translation differences, and errata search all require source-audit and independent review.
