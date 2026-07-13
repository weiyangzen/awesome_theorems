# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-0260`, the name `约科兹定理`, attribution to
Jean-Christophe Yoccoz, the year 1988, and the gloss `Siegel盘的线性化` ("linearization of Siegel
disks"). Importance "high" and status `已验证` are catalog metadata, not source or kernel evidence.
Intake preserves the subject boundary of one-dimensional complex dynamics and small-divisor
linearization without expanding the gloss into a theorem from memory.

## Proposition-changing decisions

An approved source correction must select one immutable primary-source proposition and freeze:

- whether the subject is a holomorphic germ near an indifferent fixed point, a normalized
  quadratic polynomial, a rational map, or a map on an explicitly chosen neighborhood;
- the complex domain, neighborhood/germ equivalence, fixed point, multiplier, and whether the
  rotation number is represented in `R/Z`, by a real lift, or by a unit complex number;
- the exact Brjuno/Bruno arithmetic predicate, continued-fraction conventions, irrationality and
  rational boundary, and the handling of roots of unity or resonant multipliers;
- whether linearizability means a local analytic conjugacy germ, a biholomorphism on a disk, or the
  existence of a maximal Siegel disk, including the normalization and direction of conjugacy;
- hypotheses such as nonzero derivative, univalence, injectivity, analyticity radius, and any
  normalization of the conjugating map;
- whether the conclusion is sufficiency for every germ, non-linearizability of a corresponding
  quadratic polynomial, an iff for the quadratic family, a Siegel-disk existence statement, or a
  boundary/geometric property; and
- every ordered binder, dependent definition, degenerate case, and local-to-global bridge.

These choices yield inequivalent propositions. They are a resolution ledger, not a statement.

## Candidate theorem families not credited

- Every one-variable holomorphic germ with irrational multiplier satisfying the Brjuno condition
  is analytically linearizable near the fixed point.
- If the Brjuno condition fails, the corresponding normalized quadratic polynomial is not locally
  analytically linearizable.
- A quadratic polynomial has a Siegel disk at its indifferent fixed point if and only if its
  rotation number satisfies an exact Brjuno condition.
- A geometric or boundary theorem about a quadratic Siegel disk, including critical-point or
  regularity claims under additional arithmetic assumptions.

No family in this list is selected, asserted, or credited at intake.

## Explicit exclusions

`THM-M-1432` is a separate catalog target with the same slogan and cannot be merged into this item.
The neighboring `THM-M-1433` Brjuno-condition target may supply a definition or prerequisite, but
it does not identify the root conclusion. Siegel's earlier Diophantine sufficiency theorem, a formal
power-series solution of a conjugacy equation, a generic analytic inverse theorem, or a bare
semiconjugacy identity is not a substitute for a source-selected Yoccoz proposition.

Also excluded are structures that assume linearizability or a Siegel disk as a field, tautologies
that assume the conclusion, finite-iteration examples, numerical orbit plots, and unchecked
small-divisor computations. The combinatorial large-Schroder-number power series in
`Mathlib.RingTheory.PowerSeries.Schroder` is unrelated despite the similar spelling.

## Boundary cases

The selected source must decide rational rotation numbers, roots of unity, multiplier zero or one,
the identity and already-linear maps, vanishing quadratic coefficient, local versus maximal disks,
germ equality versus chosen representatives, conjugacy direction and normalization, convergence
radius, boundary inclusion, and whether a claim covers all germs or only the quadratic family.
Silently resolving any of these can change the proposition.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies generic complex unit-disc,
`AnalyticAt`, analytic-composition, and `Function.Semiconj` APIs. A bounded intake search found no
Yoccoz, Brjuno/Bruno, Siegel-disk, Cremer, or holomorphic-dynamical linearization declaration in the
pinned Lean sources. The adjacent APIs and name search are discovery inputs only, not an exhaustive
anchor audit, statement elaboration, or proof evidence.
