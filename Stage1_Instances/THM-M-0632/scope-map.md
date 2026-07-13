# Scope map

## Received scope

The repository fixes only the title "Baire-Hausdorff theorem," the attribution Baire/Hausdorff,
the date 1909, and the phrase "properties of Baire spaces." Stage0 explicitly leaves precise
definitions and premises, proof route, equivalent formulations, axioms, machine status, and
artifact links open. This identifies a point-set topology and category topic, but supplies no
ordered binders, hypotheses, or conclusion.

## Proposition families not selected

An admitted source might select one of these related families, but intake credits none as the
canonical root:

- the definition that every countable intersection of open dense subsets is dense;
- the first Baire theorem, that a completely (pseudo)metrizable space is a Baire space;
- the second Baire theorem, that a locally compact space with an appropriate separation axiom is
  a Baire space;
- preservation of the Baire property by open subspaces, open embeddings, or dense `G_delta`
  subspaces;
- the characterization of residual sets by contained dense `G_delta` sets;
- the nonmeagreness of nonempty open sets or dense `G_delta` sets under a nonempty ambient-space
  hypothesis;
- one of the closed-cover or category consequences of the Baire property;
- a functional-analysis consequence such as uniform boundedness, open mapping, or closed graph.

These are not interchangeable. Some are definitions, some construct an instance from completeness
or local compactness, some require R1/regular/Hausdorff or nonempty assumptions, and some are
downstream applications with additional algebraic structure.

## Decisions required at statement freeze

1. Admit an immutable primary or authoritative source and one exact theorem/page/formula,
   including all incorporated definitions, proof boundary, translation, corrections, and errata.
2. Resolve what the compound name and 1909 attribution designate in the catalog, rather than
   inferring a theorem from a modern library declaration or chapter title.
3. Fix the ambient type, universe, topology, metric/uniform structure if any, and all separation,
   completeness, local-compactness, countability, and nonemptiness assumptions.
4. Fix whether the conclusion is a `BaireSpace` instance, a density statement, nonmeagreness, a
   residual-set statement, a closed-cover statement, or a functional-analysis result.
5. Fix ordered binders and quantifiers, the indexing type and countability witness, and the precise
   meanings of dense, open, `G_delta`, meagre, residual, and second category used by the source.
6. Decide empty and singleton spaces, indiscrete and non-Hausdorff spaces, empty index families,
   empty and universal sets, nonempty-open hypotheses, subspace topologies, and incomplete or
   non-locally-compact counterexamples.
7. Record a checked direction for every credited alternate encoding and mutation-test removed
   hypotheses, changed domains, binder scope, and boundary cases.

## Explicit exclusions

- Do not substitute `THM-M-0631`, which separately owns the catalog's statement that complete
  metric spaces are of second category.
- Do not choose `BaireSpace.of_completelyPseudoMetrizable` or
  `BaireSpace.of_t2Space_locallyCompactSpace` merely because each is a convenient pinned theorem.
- Do not treat the defining field `BaireSpace.baire_property` as proof of an unspecified
  characterization or consequence.
- Do not replace the target with a dense-`G_delta`, open-subspace, residual, meagreness,
  closed-cover, or functional-analysis theorem without source authority.
- Do not encode the absent result as an opaque predicate, axiom, assumed certificate, structure
  field, or hypothesis from which the desired conclusion is projected.
- Do not treat the catalog's `已验证` label, a publisher title/abstract, an API name, a successful
  probe, or an unrelated build as source or theorem evidence.

## Lean boundary

Pinned mathlib defines `BaireSpace` by density of countable intersections of open dense sets. It
provides category consequences in `Mathlib.Topology.Baire.Lemmas`, the first Baire instance for
completely pseudometrizable spaces, and the second Baire instance for locally compact R1 spaces.
It also proves that dense `G_delta` subsets of Baire spaces and `G_delta` subsets of locally compact
R1 spaces are Baire. Their distinct types confirm rather than resolve the catalog ambiguity.
Minimal imports, the canonical expression and environment fingerprints, checked transports,
statement mutations, exhaustive formal discovery, and proof-body provenance remain downstream.

## Retry condition

The integration lane must admit one stable proposition and immutable source and obtain independent
review of its exact definitions, binders, assumptions, conclusion, proof boundary, translation,
corrections, historical naming, and relation to the catalog phrase. Only then may the statement
phase elaborate and mutation-test an exact Lean target.
