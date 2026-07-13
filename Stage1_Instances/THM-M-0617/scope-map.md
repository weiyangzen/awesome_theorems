# Scope map

## Received claim

`Docs/researches/math_theorems.md:4580-4585` fixes a point-set-topology target with two clauses:

1. every closed subset of a compact set is compact; and
2. every continuous image of a compact set is compact.

The word `连续像` (continuous image) is read together with the preceding compact-set subject; it
does not assert that every image of an arbitrary set is compact. Both clauses must survive in the
eventual root. Neither may be treated as merely explanatory context for the other.

## Candidate mathematical boundary

A source-faithful general-topological-space formulation should quantify over a topological space
`X` and a compact set `s : Set X`. The first branch then independently quantifies a closed set
`t : Set X` with `t ⊆ s`. The second independently quantifies a target topological space `Y`, a map
`f : X -> Y`, and continuity of `f`, and concludes compactness of `f '' s`.

The statement phase should prefer independently quantified branches rather than one flat theorem
that unnecessarily requires a closed subset and a continuous map at the same time. One candidate
scope shape is:

```text
(forall closed t subset s, IsCompact t) and
(forall topological Y and continuous f : X -> Y, IsCompact (f '' s)).
```

This is a planning signature, not the canonical Lean expression. A source review may instead
authorize two canonical child declarations plus a checked composition root.

## Decisions required at statement freeze

1. Admit an immutable primary or authoritative source edition and pinpoint the exact statements,
   incorporated compactness and continuity definitions, assumptions, proof boundary, corrections,
   errata, translation, and historical attribution.
2. Fix universes and the ordered implicit and explicit binders for `X`, `Y`, `s`, `t`, and `f`.
3. Confirm that compactness is the general open-cover/filter notion without a Hausdorff condition.
4. Fix whether the closed-subset clause uses ambient `IsClosed t` plus `t ⊆ s`, closedness in the
   subspace `s`, or a checked transport between those formulations.
5. Fix whether the image branch assumes global `Continuous f`, `ContinuousOn f s`, a bundled
   continuous map, or one canonical form with checked directional transports.
6. Decide whether the catalog root is one conjunction, a structure of two results, or two child
   propositions with a checked root composition; no packaging may couple independent assumptions.
7. Mutation-test a removed closedness, subset, compactness, or continuity premise, changed source
   or target domain, changed binder scope, and all material boundary cases.

## Boundary cases

No case is silently excluded at intake. Source and statement review must cover empty and singleton
spaces, the empty and universal compact sets, `t = empty`, `t = s`, an empty closed set not contained
in `s`, empty target spaces and existence of maps into them, constant maps, noninjective and
nonsurjective maps, non-Hausdorff spaces, and compact sets that are not closed. The first clause
must not acquire a `T2Space` assumption merely because compact subsets are closed in Hausdorff
spaces; that is the converse direction and a different theorem.

## Explicit exclusions

- Model-theoretic compactness (`THM-M-0644`) is unrelated despite the identical Chinese title.
- Heine-Borel (`THM-M-0618`), Bolzano-Weierstrass, sequential compactness, countable compactness,
  local compactness, Tychonoff's theorem, and Alexander's subbasis theorem do not replace this root.
- Compact subsets being closed in a Hausdorff space is the converse-shaped separation theorem, not
  the closed-subset preservation clause.
- A version only for compact ambient spaces, metric spaces, finite sets, embeddings, proper maps,
  homeomorphisms, or identity/constant maps is not the general catalog claim.
- `ContinuousOn` may become an alternate or stronger-local interface only through an explicit
  checked relationship; it is not silently substituted for the catalog's continuity wording.
- A structure or premise that stores compactness of `t` or `f '' s`, a theorem name, `#check`, axiom
  report, or the untrusted `已验证` label supplies no source or proof credit.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.Compactness.Compact` contains `IsCompact.of_isClosed_subset`,
`IsCompact.image_of_continuousOn`, and `IsCompact.image`. The first and last are direct candidates
for the two catalog clauses. This bounded intake observation supports provisional `M3`; exact root
identity, minimal environment, transports, mutations, source and body provenance, trust closure,
and acceptance belong to downstream phases.
