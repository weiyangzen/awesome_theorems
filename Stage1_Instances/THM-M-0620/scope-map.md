# Scope map

## Preserved theorem family

The intake preserves the catalog claim that an arbitrary, including infinite, product of compact
spaces is compact. It does not narrow the result to finite or countable products, add metrizability
or Hausdorff assumptions, or replace the product topology by the box topology.

The most literal prospective space-level encoding is parameterized by an arbitrary index type `I`,
a dependent family `X : I -> Type`, one `TopologicalSpace (X i)` and one `CompactSpace (X i)`
instance for every coordinate, and concludes `CompactSpace (forall i, X i)`. Pinned mathlib also
has a stronger set-level presentation for a family `s : forall i, Set (X i)`. These are candidate
surfaces only until source review and checked transports select a canonical root.

## Decisions required at statement freeze

1. Admit and independently review an immutable exact source theorem, its incorporated definitions,
   assumptions, proof boundary, corrections, and errata.
2. Fix whether the source root is the space-level product or the product-of-compact-subsets form.
3. Fix the arbitrary index and factor universes, ordered binders, and dependent-family convention.
4. State explicitly that the function space carries the Pi product topology. In pinned mathlib it
   is the infimum of the coordinate-induced topologies and has finite-coordinate basic opens.
5. Decide the compactness convention. Mathlib's `CompactSpace` does not include `T2Space`; adding a
   Hausdorff premise would change the received claim unless source review requires it.
6. Freeze all empty and degenerate cases rather than silently adding `Nonempty` assumptions.
7. Select the foundation and axiom policy. All three pinned candidates report `Classical.choice`,
   as well as `propext` and `Quot.sound`, in their current transitive axiom reports.
8. Elaborate one exact target with minimal pinned imports, preserve its expression and environment
   fingerprints, compile every claimed transport, and run the required statement mutations.

## Boundary cases

- empty index type, whose dependent product is unit-like and compact;
- a family containing an empty factor, whose product is empty and compact;
- an empty compact subset in the set-level form;
- singleton factors and the trivial product;
- finite, countably infinite, and arbitrary index types;
- non-Hausdorff compact factors under mathlib's compactness convention;
- universe-polymorphic dependent families rather than only a constant family;
- product topology versus the strictly finer box topology for infinite products.

`IntakeProbe.lean` checks representative empty-index and empty-factor instances. No boundary case is
excluded at intake.

## Candidate encodings, not credited statements

| Candidate | Relationship to the catalog | Intake boundary |
|---|---|---|
| `Pi.compactSpace` | direct space-level arbitrary product | typeclass instance, not yet a frozen theorem wrapper or source-approved root |
| `isCompact_pi_infinite` | product of arbitrary compact subsets as a set-builder | stronger set-level form; transport to the space wording remains open |
| `isCompact_univ_pi` | product of compact subsets using `Set.pi univ s` | equivalent set representation only after checked normalization |
| finite binary-product compactness | consequence/special case | cannot replace the arbitrary product root |

## Explicit exclusions

- Tychonoff's fixed-point theorem, separately cataloged as `THM-M-0317` and `THM-M-0638`;
- only finite-product, countable-product, sequential-compactness, or metric-space specializations;
- products of merely locally compact spaces;
- compactness under the box topology;
- compactness of arbitrary unions or sums of compact spaces;
- adding Hausdorff, nonempty, metric, first-countable, or second-countable assumptions without an
  accepted source-fidelity reason;
- Alexander's subbasis theorem, the ultrafilter characterization, or the axiom of choice used as a
  substituted root rather than explicit dependencies or foundation boundaries;
- an inferred `Pi.compactSpace` instance, theorem name, catalog label, or API probe treated as
  accepted proof evidence without exact wrapper, provenance, trust, and master gates.

## First downstream gate

The statement phase must approve one exact source formulation and resolve the space/set encoding,
topology, compactness convention, universes, binders, choice policy, and every boundary case. Until
then the canonical Lean expression, obligation registry, and proof credit remain empty.
