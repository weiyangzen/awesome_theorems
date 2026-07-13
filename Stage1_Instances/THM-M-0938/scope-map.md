# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0938`, title `Kneser定理`, attribution to Martin Kneser, year
1953, and the gloss `阿贝尔群上子集和的结构`. Intake preserves the Kneser sumset-structure family
without manufacturing the missing proposition.

The label is distinct from the Lovasz-Kneser theorem about chromatic numbers. Within the local
additive-combinatorics cluster it is also distinct from the Cauchy-Davenport lower bound, Vosper's
inverse theorem, Kemperman's structural results, Freiman's theorem, and Ruzsa covering.

## Candidate roots, not credited

Three inspected Kneser source families require an explicit choice:

1. The 1953 paper studies lower finite and asymptotic density of sumsets of sets of rational
   integers and states a density/periodicity dichotomy.
2. The volume-61 paper states that for finite subsets `A`, `B` of an arbitrary abelian group there
   exists a subgroup `H` with `A + B + H = A + B` and
   `|A + B| >= |A| + |B| - |H|`.
3. The 1956 paper treats locally compact abelian groups with Haar measure and topological and
   measurability conditions.

The usual modern finite theorem often takes `H` to be the stabilizer of `A + B` and may state the
stronger bound `|A + B| >= |A + H| + |B + H| - |H|`. Those forms may be related, but source
selection and checked transports are required. None is canonical at intake.

## Proposition-changing decisions

The statement phase must freeze all of the following from one admitted source:

- integer sets with density, finite subsets of an abelian group, or measurable subsets of a
  locally compact abelian group;
- whether the ambient group is finite, arbitrary discrete, locally compact, compact, or another
  class, together with commutativity, topology, and universe data;
- `Set`, `Finset`, measurable-set, or quotient encoding and the exact sumset operation;
- lower finite density, lower asymptotic density, finite cardinality, `Set.ncard`, or Haar measure;
- nonempty, finite, measurable, integrable, compact, positive-measure, or other hypotheses;
- an existential period subgroup versus the greatest subgroup stabilizing `A + B`;
- the definition and action orientation of the stabilizer, and whether it acts on a set or finset;
- the exact conclusion: periodicity dichotomy, weak cardinal inequality, coset-count inequality,
  equality classification, measure inequality, or a conjunction of separately modeled claims;
- the ordered binders and whether `H` is an output witness or a defined term;
- source edition, theorem and page, incorporated definitions, proof boundary, translations,
  corrections and errata, complete premise/conclusion map, and independent review; and
- checked transports among existential/canonical-period, set/finset, cardinal/coset-count, and
  any quotient-group formulations.

These choices change the proposition. A familiar finite-stabilizer statement cannot be installed
merely because it is commonly called Kneser's theorem.

## Boundary cases

No case is excluded at intake. Source review must decide empty `A` or `B`, singleton inputs, the
trivial group, trivial or full stabilizer, aperiodic sumsets, finite subsets of infinite groups,
infinite or nonmeasurable sets, zero or infinite Haar measure, noncompact groups, and whether a
zero-cardinality convention makes an empty-input inequality intended or accidental. It must also
resolve coercions between finsets and sets and cardinal subtraction in every degenerate case.

## Explicit exclusions

- `THM-M-0936` Cauchy-Davenport, `THM-M-0937` Vosper, or `THM-M-0939` Kemperman as a substitute.
- The Lovasz-Kneser graph-coloring theorem or a theorem mentioning Kneser's name outside sumsets.
- Torsion-free, cyclic-prime, one-set doubling, small-doubling, finite-group-only, or numerical
  special cases substituted for the selected general root.
- An equality or inverse theorem substituted for a lower bound, or the reverse.
- A subgroup, periodicity witness, quotient, or structure supplied by a hypothesis that stores the
  desired conclusion.
- A cardinality theorem substituted for density or Haar measure without checked source transport.
- The catalog's `已验证` label, a citation, API probe, bounded search, or TODO as proof credit.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Algebra.Pointwise.Stabilizer` supplies pointwise sumsets and `AddAction.stabilizer` APIs,
including finite/coercion/periodicity lemmas. `Mathlib.Combinatorics.Additive.CauchyDavenport`
supplies a different lower-bound theorem. `Mathlib.Combinatorics.Additive.VerySmallDoubling`
contains one-set structural results and a Freiman-Kneser TODO/reference.

A bounded exact `Kneser` search over pinned mathlib found only that reference and no classical
terminal declaration. The probe checks adjacent substrate only. Exact candidate inventory,
external search, terminal-body provenance, and trust analysis remain the anchor-audit phase.
