# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:498-503` supplies exactly:

- title: `马施克定理`;
- attribution: Heinrich Maschke;
- year: 1899;
- gloss: `有限群表示在特征不整除群阶时可完全约化`;
- importance: high;
- untrusted formalization status: `已验证`.

All six catalog lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:1947-1972`
repeats the gloss while explicitly leaving exact definitions, premises, proof route, equivalent
forms, axioms, machine status, and artifact links open. Neither repository record cites a primary
work or a modern proof source. They establish catalog identity, not `H0`.

## Human-source boundary

The catalog's Heinrich Maschke/1899 attribution is only a historical locator. The repository does
not identify a work title. Crossref REST metadata queried on 2026-07-13 offers two uninspected
candidates: Maschke, "Die Reduction linearer homogener Substitutionen von endlicher Periode auf ihre
kanonische Form," *Mathematische Annalen* 50 (1898), 220-224,
DOI `10.1007/BF01448063`; and "Ueber den arithmetischen Charakter der Coefficienten der
Substitutionen endlicher linearer Substitutionsgruppen," *Mathematische Annalen* 50 (1898),
492-498, DOI `10.1007/BF01444297`. Their 1898 dates also disagree with the catalog's 1899 date.
Neither candidate's primary text, exact theorem passage, incorporated definitions, proof boundary,
translation, errata, or assumption match was inspected and independently reviewed here. No primary
source statement is therefore reconstructed or accepted. The first human-source gate remains a
pinpoint primary or authoritative source audit with a complete assumption and errata crosswalk.

## Clause crosswalk

| Repository phrase | Required mathematical meaning | Pinned Lean candidate | Intake status |
|---|---|---|---|
| "finite group" | one group with finite cardinality | `[Group G] [Finite G]` | direct candidate scope; exact source/finiteness encoding open |
| "representation" | linear action of `G` on a vector space over one scalar field | `rho : Representation k G V` with field/module structures | direct candidate type; dimensionality and scalar conventions open |
| "characteristic does not divide the group order" | the group order remains nonzero/invertible in the scalar field | `[NeZero (Nat.card G : k)]`; module prose relates `IsUnit` to `not (ringChar k divides Fintype.card G)` | direct candidate assumption; exact source proposition and checked transports open |
| "completely reducible" | source-defined semisimplicity, commonly invariant complements or a sum of irreducibles | `Representation.IsSemisimpleRepresentation rho`, meaning `ComplementedLattice (Subrepresentation rho)` | direct complement-form candidate; identity with intended wording open |
| `已验证` | untrusted inventory label | no expression, source receipt, or proof evidence | explicitly rejected as credit |

## Pinned formal leads

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

1. `Mathlib/RepresentationTheory/Maschke.lean` constructs an averaged equivariant projection,
   proves `MonoidAlgebra.exists_leftInverse_of_injective` and
   `MonoidAlgebra.Submodule.exists_isCompl`, installs an `IsSemisimpleModule` instance, and finally
   synthesizes `Representation.IsSemisimpleRepresentation rho` under the finite-group, field, and
   nonzero-cardinality assumptions.
2. `Mathlib/RepresentationTheory/Semisimple.lean` defines the representation conclusion as a
   complemented lattice of subrepresentations and proves
   `Representation.isSemisimpleRepresentation_iff_isSemisimpleModule_asModule`.
3. The Maschke module's implementation notes say its invertibility condition is equivalent to the
   familiar characteristic nondivisibility condition. Its future-work note calls the
   finite-dimensional direct-sum-of-irreducibles statement the usual formulation and does not yet
   provide the bridge from the implemented complement convention to that formulation.

The intake probe checks these declaration types and instance synthesis in the pinned environment.
This is a bounded discovery result, not the exhaustive anchor audit. Exact normalized types,
terminal proof bodies, transitive declarations, axioms, placeholders, unsafe/oracle boundaries,
source identity, characteristic transports, and complete-reducibility transports remain downstream
gates.

## First failed statement/source gate

No accepted source fixes the scalar and dimensionality conventions or defines "completely
reducible." Therefore the direct complemented-subrepresentation candidate cannot yet be installed
as the canonical target, and the familiar finite-dimensional direct-sum formulation cannot be
substituted for it, without an approved source choice and checked transports.
