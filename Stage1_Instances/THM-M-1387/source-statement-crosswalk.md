# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10104-10109` supplies exactly the title `振荡理论`, attribution
to "many mathematicians," the twentieth century, the gloss `解的振荡性` (`oscillatory behavior of
solutions`), importance `high`, and status `已验证`. Git history places all six uncited lines in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no equation, source,
definition, binder, hypothesis, conclusion, theorem locator, proof boundary, correction history,
or formal artifact.

`Docs/Stage0_Blueprint.md:37722-37747` repeats the metadata while explicitly leaving the formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Inspected authoritative discriminator, not credited

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society, 2012, Section 5.5, printed pages 166-174, was
inspected as a source-family discriminator. The author-hosted publisher-permitted preliminary
edition has observed SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`.

The section visibly separates multiple possible roots: Pruefer-variable definitions; a zero-count
lemma; eigenfunction nodal-count results; Sturm comparison and interlacing; spectral zero-count
identities; asymptotics; the half-line definition that an equation is oscillating when a solution
has infinitely many zeros; and Kneser's sufficient criteria for oscillation or nonoscillation. The
official errata, observed with SHA-256
`3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`, corrects material formulas
and proof details on printed pages 167-172. This multiplicity establishes ambiguity; it does not
select a root.

The catalog does not cite Teschl, and the external files are not admitted as immutable H0 evidence.
No full definition/assumption/conclusion/errata mapping or independent source review is accepted.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `振荡理论` | theory chapter, one oscillation criterion, comparison theorem, nodal theorem, or spectral equivalence | one exact `Prop`, not a family-name wrapper | root absent |
| "solutions" | scalar ODE solution, Sturm-Liouville eigenfunction, system trajectory, weak solution, or another class | derivative predicates or `IsIntegralCurveOn` plus source-defined equation | equation and solution class absent |
| "oscillatory" | infinitely many/arbitrarily large zeros, endpoint accumulation, sign changes, or phase growth | `Set.Infinite`, filters, zero sets, or a future Pruefer predicate | definition and domain absent |
| solution quantifier | every nontrivial solution, existence of one, or equation/operator-level classification | ordered universal/existential binders | polarity absent |
| conclusion | classification, sufficient/necessary criterion, comparison, zero count, or asymptotic result | source-mapped exact proposition | absent |
| `已验证` | untrusted inventory label | no declaration or proof object | no H/M/R credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
checks integral curves, derivative and iterated-derivative predicates, infinite sets, and filters.
These APIs can express pieces of possible encodings but do not define the catalog's intended
oscillation predicate or prove a theorem about it. `Mathlib.Analysis.Oscillation` instead defines
pointwise topological oscillation and relates zero oscillation to continuity; it is a false friend
for this ODE catalog item.

A bounded exact-topic search found no ODE oscillation, Sturm-Liouville, or Kneser declaration in
pinned mathlib or repo-local Lean. This is intake discovery only, not the later precommitted anchor
audit or an absence claim about external projects.

## Required source admission

The statement phase must preserve and hash one lawful complete source; select a precise theorem or
definition-backed proposition; transcribe its equation, domains, ordered binders, solution class,
coefficient and endpoint assumptions, oscillation definition, quantifier polarity, conclusion,
proof boundary, and errata; reconcile neighboring target ownership; and obtain independent review.
Only then may it freeze minimal imports, an elaborated expression and environment fingerprint,
checked transports, and the required statement mutations. Until then `H5` records that the catalog
phrase is not one stable proposition; it does not say that source-correct oscillation theorems are
false or mathematically open.
