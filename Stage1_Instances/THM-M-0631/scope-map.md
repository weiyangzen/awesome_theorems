# Scope map

## Preserved claim family

The intake preserves the catalog's classical claim that complete metric spaces satisfy a Baire
category conclusion. It does not silently identify the following formulations:

- every countable intersection of dense open subsets is dense (`BaireSpace`);
- every nonempty open subset is nonmeagre;
- the whole space is nonmeagre, i.e. is of second category in itself;
- a complete metric, a complete pseudometric, or a topology admitting some compatible complete
  metric or pseudometric has the selected category property;
- a category conclusion for locally compact regular spaces, which mathlib calls the second Baire
  theorem and which is not the catalog's complete-metric claim.

The first two are standard Baire-space formulations. The third is weaker and false for the empty
space unless nonemptiness is assumed. The remaining choices change domains, structures, and proof
boundaries. Intake therefore records them as candidates, not as the root.

## Decisions required at statement freeze

1. Admit an immutable primary or authoritative source edition and one exact theorem/page/section,
   including incorporated definitions, proof boundary, translation, corrections, and errata.
2. Decide whether "second category" denotes the whole space being nonmeagre or the stronger
   Baire-space property, and record checked implications or equivalences rather than prose aliases.
3. Decide whether the empty space is included. If the root is nonmeagreness of `univ`, an explicit
   `Nonempty X` premise or a source-sanctioned exclusion is required.
4. Fix whether the domain carries a `MetricSpace` plus `CompleteSpace`, a `PseudoMetricSpace` plus
   `CompleteSpace`, or only a topology with `IsCompletelyMetrizableSpace` or
   `IsCompletelyPseudoMetrizableSpace`.
5. Fix the ambient type and universe, topology/metric compatibility, all typeclass assumptions,
   ordered binders, quantifiers, hypotheses, and exact conclusion.
6. Fix whether countability is represented by a natural-number family, a countable index type, or
   a countable set; and whether the category side uses open dense sets, nowhere-dense coverings,
   residual sets, or nonmeagreness.
7. Decide boundary cases including empty, singleton, discrete, nonseparated pseudometric, and
   already-Baire spaces, plus empty or repeated families of open sets.
8. Elaborate the chosen target under minimal pinned imports, freeze expression and environment
   fingerprints, compile transports for credited alternatives, and mutation-test assumptions,
   domains, binder scope, and boundary cases before inspecting proof closure.

## Explicit exclusions

- Do not replace the catalog root with the locally compact R1 Baire theorem from
  `Mathlib.Topology.Baire.LocallyCompactRegular`.
- Do not use `THM-M-0632` (the separately cataloged Baire-Hausdorff theorem) or transfer any of its
  future source, statement, proof, or receipt credit.
- Do not assert `not IsMeagre univ` for every complete metric space without resolving the empty
  complete metric space.
- Do not treat the Baire-space property and whole-space nonmeagreness as definitions of one another
  without a source decision and checked relationship.
- Do not assume the conclusion as a typeclass or hypothesis and project it as a proof.
- Do not treat the catalog's `已验证` label, a theorem name, an API probe, or an unrelated build as
  source fidelity or theorem evidence.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a completely
pseudometrizable topology has a `BaireSpace` instance. A displayed complete pseudometric supplies
the former structure automatically; a complete metric is a separated special case. The imported
category API defines `IsMeagre`, explicitly proves that the empty set is meagre, and proves that
nonempty open subsets of Baire spaces are nonmeagre.

These facts make the missing scope decisions executable; they do not make them for the catalog.
Minimal imports for a canonical expression, checked transports, statement fingerprints, formal
candidate provenance, and proof-body credit remain downstream.

## Retry condition

The integration lane must admit one stable primary or authoritative proposition and obtain an
independent review of its definitions, domain, binders, assumptions, conclusion, proof boundary,
translation, corrections, empty-space treatment, and mapping to the catalog phrase. The statement
phase may then select and elaborate an exact Lean target rather than inheriting an intake candidate.
