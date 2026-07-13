# Scope map

## Received claim

`Docs/researches/math_theorems.md:2055-2060` fixes only `叶戈罗夫定理`, the attribution Dmitri
Egorov, the year 1911, and `几乎处处收敛与一致收敛的关系` ("the relationship between almost-
everywhere convergence and uniform convergence"). It supplies no primary citation, formula,
definitions, assumptions, theorem locator, proof boundary, or exact formal artifact.

The words name two convergence modes but do not say which implication, exceptional-set form, or
ambient measure-theoretic setting is intended. This intake does not choose among them.

## Candidate classical boundary

A familiar formulation says that an almost-everywhere convergent sequence of measurable functions
on a finite-measure space converges uniformly outside a measurable set of arbitrarily small
measure. This is a candidate boundary only, not the frozen source claim. The statement phase must
source and fix:

- the measurable space, measure, and whether finiteness is global or restricted to a measurable
  subset;
- the codomain, metric or extended metric, separation convention, and any completeness premise;
- natural-number sequence versus a more general directed countable index;
- measurability of each function, of the limit, or only of their pointwise distance;
- almost-everywhere convergence on which set and the exact implication convention outside it;
- the exceptional set's measurability, containment, measure bound, and strict versus non-strict
  inequality;
- uniform convergence on the complement or on a retained subset, and the exact quantifier order;
  and
- whether the source includes only the theorem statement or a larger equivalence or corollary.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.MeasureTheory.Function.Egorov` supplies four direct interfaces:

- `MeasureTheory.tendstoUniformlyOn_of_ae_tendsto_of_measurable_edist` assumes measurability of
  each extended-distance function, a measurable finite-measure set `s`, and almost-everywhere
  pointwise convergence on `s`; it returns a measurable `t` contained in `s` with
  `mu t <= ENNReal.ofReal epsilon` and uniform convergence on `s \ t`.
- `MeasureTheory.tendstoUniformlyOn_of_ae_tendsto` derives that interface from strong
  measurability of every function and the limit.
- The corresponding primed declarations replace the finite-measure subset by an
  `IsFiniteMeasure` instance and conclude uniform convergence on the complement of a measurable
  exceptional set.

All four use a `Countable`, `Nonempty`, `SemilatticeSup` index and a `PseudoEMetricSpace` codomain.
They are strong exact-topic interfaces, hence provisional `M3`, but none receives root identity,
source transport, proof-body, or completion credit at intake.

## Boundary cases to resolve

- Empty or null measurable subset, zero measure, and a zero exceptional-set budget limit.
- A nonmeasurable subset or functions for which only pointwise convergence is known.
- Infinite measure globally but finite measure on the selected subset.
- A non-Hausdorff pseudo extended metric codomain and points at zero distance.
- Empty index type, a countable directed order other than natural numbers, or failure of directed
  upper bounds.
- Whether the exceptional set must be a subset of the working set and whether it may equal it.
- Almost-everywhere convergence whose exceptional null set is separate from the small set produced
  by the theorem.

No boundary case is silently excluded before an exact proposition is selected.

## Explicit exclusions

- Convergence in measure, Vitali convergence, dominated convergence, Lusin's theorem, or Borel-
  Cantelli substituted for Egorov's theorem.
- A finite sequence, finite domain, constant-function case, or a hypothesis that already stores
  uniform convergence outside a small set.
- A globally finite-measure special case used as an unrestricted finite-subset theorem, or the
  reverse substitution without a checked transport.
- One pinned declaration selected solely because its file or docstring names Egorov.
- The catalog's untrusted `已验证` label, the mathlib Wikidata mapping, or this intake probe used as
  source, statement-identity, or proof credit.

## Statement retry condition

An independent source reviewer must admit an immutable primary edition and exact result locator,
map every incorporated definition, ordered binder, premise, conclusion, exceptional-set
convention, proof boundary, translation, correction, and attribution, and approve one source-to-
Lean root. The statement phase may then elaborate that root with minimal imports, fingerprint it,
compile checked transports, and run the required domain, hypothesis, binder-scope, and boundary
mutations.
