# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Catalogue claim | `Docs/researches/math_theorems.md`: "existence of solutions under a continuity condition" | none | Identifies the Peano family but omits all binders, domains, local interval data, and the solution predicate |
| Historical primary anchor | G. Peano, *Demonstration de l'integrabilite des equations differentielles ordinaires*, **Mathematische Annalen** 37 (1890), 182-228, DOI `10.1007/BF01206765` | none selected | Bibliographic discovery anchor only; an immutable copy, exact theorem/page, transcription, translation, and errata check remain open |
| Classical local theorem family | Continuous vector field near `(t0, x0)` implies at least one local integral curve through that point | no exact expression | Leading scope, but several inequivalent textbook formulations exist |
| Quantitative rectangle form | Continuity and a bound `M` on a time-state rectangle yield existence on a subinterval commonly sized using `min(a, b/M)` | no exact expression | Candidate formulation; conventions for `M = 0`, endpoint derivatives, vector norm, and two-sided versus forward time must be fixed |
| Integral-equation form | `x(t) = x0 + integral f(s, x(s)) ds` on the local interval | no checked wrapper | Candidate proof interface; equivalence to the ODE form needs kernel-checked calculus hypotheses |
| Pinned mathlib neighbor | `Mathlib.Analysis.ODE.PicardLindelof`, including `IsPicardLindelof` existence results | no Peano candidate located | Requires Lipschitz data and supports a different existence-and-uniqueness theorem; it is not a valid replacement |

The historical paper link is a discovery link, not an accepted evidence receipt:
<https://doi.org/10.1007/BF01206765>

The source phase must inspect an immutable primary artifact, pinpoint and transcribe one exact result,
audit translation and corrections, and crosswalk every assumption. The statement phase must then
choose the matching finite-dimensional Lean model, define a nontrivial interval and solution
predicate, elaborate the exact proposition, and mutation-test continuity, domain, binder scope, and
boundary cases.

No `H0`, exact-statement, or machine-closure claim is made. In particular, replacing continuity with
a Lipschitz assumption would broaden available conclusions while narrowing admissible vector fields;
that would formalize Picard-Lindelof rather than the assigned theorem.
