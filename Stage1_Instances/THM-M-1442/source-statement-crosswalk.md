# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:10532-10537` records the title `二分法`, attributes it to "many
mathematicians," dates it only to antiquity, and gives the complete statement gloss
`方程求根的线性方法` ("a linear method for finding roots of equations"). It supplies no
bibliography, definition, function, domain, quantifier, hypothesis, recurrence, conclusion, proof,
or formal artifact. All six lines entered this repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; that is repository provenance, not a mathematical
source revision.

`Docs/Stage0_Blueprint.md:39217-39242` repeats the gloss while explicitly leaving exact definitions
and premises, proof process, dependency graph, equivalent formulations, axioms, machine status, and
artifact links open. The rev-5.6 manifest preserves `已验证` only in the untrusted source-status
field.

## Crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "equation root finding" | a function `f` and equation `f x = 0` | a function into an ordered topological additive type, often `Real -> Real` | function, domain, and equation absent |
| "bisection method" | initial bracket with ordered endpoints | `a <= b`, an interval such as `Set.Icc a b` | bracket and interval convention absent |
| "bisection method" | continuity and opposite-sign endpoint premises | `ContinuousOn f (Set.Icc a b)` plus oriented inequalities | premise location, orientation, and endpoint equality cases absent |
| "bisection method" | midpoint and branch recurrence | mutually defined endpoint sequences or interval recursion | recurrence, tie rule, and branch convention absent |
| possible invariant reading | each interval nests and still brackets a root | interval containment and endpoint-sign obligations | not stated by the source |
| possible existence reading | some root lies in the initial or every interval | `intermediate_value_Icc` or its reverse/unordered variants | adjacent IVT substrate only, not an algorithm theorem |
| "linear method" | a geometric interval-width or point-error inequality | powers of `(1 / 2)` and ordered/norm bounds | rate definition, constant, error measure, and approximant absent |
| possible convergence reading | endpoints or selected approximants converge to a root | `Tendsto`, nested-interval results, and continuity | sequence, limit, uniqueness, and convergence mode absent |
| possible complexity reading | an iteration count reaches a positive tolerance | Archimedean/logarithmic bounds over `Nat` | tolerance, rounding, and stopping contract absent |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | explicitly rejected as evidence |

## Candidate Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Mathlib.Topology.Order.IntermediateValue.intermediate_value_Icc` proves that values between
  `f a` and `f b` occur on a closed interval when `f` is continuous there.
- `intermediate_value_Icc'` handles the reverse orientation, and `intermediate_value_uIcc` handles
  an unordered interval.
- `Mathlib.Analysis.SpecificLimits.Basic.tendsto_pow_atTop_nhds_zero_of_lt_one` proves generic
  geometric decay once a nonnegative base below one is supplied.
- `Mathlib.Tactic.NormNum.Irrational.Tactic.NormNum.findNotPowerCertificateCore` is an internal
  natural-number metaprogram described as using bisection. It searches for a power certificate for
  `norm_num`; it is not equation-root bisection and is recorded to reject a lexical false match.

The first three intermediate-value declarations can support root existence after missing premises
are selected. None defines the algorithm, establishes the bracket invariant, selects approximants,
or proves an error, rate, complexity, or finite-precision result. The geometric-limit declaration
also needs a checked bridge from a yet-undefined bisection error. The bounded probe therefore
provides discovery input only, not a downstream anchor audit, proof-body audit, or absence claim
about external projects.

## Source and statement gate

No primary or approved authoritative theorem source is identified at intake. The statement phase
must first preserve an immutable source passage, record its edition, theorem or section and page,
definitions incorporated by reference, assumptions, exact conclusion, proof boundary, corrections
and errata, and independent review. Reviewers must justify why that proposition is the repository
target rather than a convenient theorem about interval roots.

Only then can the statement phase freeze domains and universes, ordered binders, every boundary
case, minimal imports, an elaborated expression and environment fingerprint, checked transports,
and the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations.
The provisional human-source status is `H5`: the supplied target is not a stable proposition. This
does not say that established bisection convergence theorems are false; it requires an approved
source correction before ordinary theorem-proof execution.
