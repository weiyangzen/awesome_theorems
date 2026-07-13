# Scope map

## Preserved catalog scope

The catalog fixes the eponymous Nagata-Smirnov metrization family and says only that it gives
necessary and sufficient conditions for a topological space to be metrizable. It does not enumerate
those conditions or supply a citation. Intake therefore preserves the theorem-family identity while
leaving the canonical proposition and formal target open.

A stable secondary discovery page gives the conventional candidate: a topological space is
metrizable if and only if it is regular, Hausdorff, and has a countably locally finite (also called
sigma-locally finite) topological base. This guides source review; it is not accepted as the root.

## Proposition-changing decisions

The statement phase must freeze all of the following from an approved immutable source:

1. Whether "regular" includes T1, T0, or Hausdorff separation, and whether a separate Hausdorff
   premise is redundant or material under that source's terminology.
2. Whether metrizable means a compatible metric, a compatible uniformity satisfying a countability
   condition, or another encoding, and the checked transport to mathlib's `MetrizableSpace`.
3. Whether the basis condition is a sequence `B : Nat -> Set (Set X)` whose union is a topological
   basis and each indexed family is locally finite, or a single basis equipped with a countable
   cover by locally finite subfamilies.
4. Whether the locally finite pieces may overlap, contain the empty set, or repeat basis members,
   and whether local finiteness is indexed-family or set-family finiteness.
5. The ambient type, topology, universes, implicit and explicit binders, and exact direction and
   packaging of the equivalence.
6. The exact source edition, theorem/page, incorporated definitions, proof and dependency boundary,
   translation, corrections, errata, and independent review.
7. The foundation, classical-choice, TCB, computation, freshness, and invalidation profiles.

These choices are a resolution ledger, not a canonical statement.

## Boundary cases and mutations

Source and statement review must explicitly cover the empty and singleton spaces, discrete and
indiscrete topologies, non-T0 and non-Hausdorff spaces, an empty basis family, empty locally finite
layers, and finite or countable bases. Removing the separation or basis condition, weakening a
topological basis to a cover, changing `Nat` to a finite index, changing `MetrizableSpace` to
`PseudoMetrizableSpace`, or placing the topology outside the universal binder are material
mutations. No case is silently included or excluded at intake.

## Neighbor and substitution exclusions

- `THM-M-0623` separately owns the Urysohn second-countable regular-space metrization theorem.
- `THM-M-0625` separately owns the Bing metrization theorem. Neither neighboring condition may be
  used as this target without a checked theorem-family relationship.
- A one-way implication that metrizable spaces are regular, Hausdorff, or admit some convenient
  basis does not establish the necessary-and-sufficient root.
- A second-countable, separable, Lindelof, paracompact, Moore-space, uniformizable, or
  pseudometrizable special case is not a substitute.
- An opaque predicate named "sigma locally finite basis," a premise assuming metrizability, or the
  untrusted `已验证` label supplies no statement or proof credit.

## Lean boundary and retry condition

Pinned mathlib exposes `TopologicalSpace.MetrizableSpace`, `RegularSpace`, `T3Space`, `T2Space`,
`TopologicalSpace.IsTopologicalBasis`, and `LocallyFinite`. These interfaces make a future encoding
plausible but do not choose the source convention or prove the theorem. Minimal imports, the exact
expression and environment fingerprint, checked transports, and statement mutations remain owned
by `S56-M-0624-STATEMENT`.

Retry requires an accountable source reviewer to approve one immutable proposition and map every
definition, premise, conclusion, proof boundary, translation, correction, erratum, and boundary
case. Only then may the statement phase select the Lean encoding and elaborate it.
