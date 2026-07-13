# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:4601-4606` supplies exactly the title `吉洪诺夫定理`, attribution
to Andrey Tychonoff, year 1930, gloss `任意多个紧空间的乘积紧`, importance high, and formalization
status `已验证`. All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:16963-16988` repeats the gloss while leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent statements,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted metadata and resets this target to `L0 / rework_required`. No repository record supplies a
bibliography, exact theorem/page, formula, definition chain, proof boundary, corrections, or review.

## Primary-source inspection

Crossref and the Springer bibliographic page were inspected on 2026-07-13. They identify:

> A. Tychonoff, *Uber die topologische Erweiterung von Raumen*, Mathematische Annalen 102
> (1930), 544-561, DOI 10.1007/BF01782364.

The observed Crossref response had SHA-256
`844ba3ad5ca835306d7cce7524079379ad5408186d9e6b3616cc2c794c2cd282`. Although the Springer PDF
endpoint returned a paywall page, the Goettingen Digitisation Centre exposes a stable IIIF volume
manifest with SHA-256 `66ba71aab6e4806322f3a08c59b3da17b84f17b9ba2df210d69954ff40b4ec10`.
Printed pages 544-561 map to canvases `00000548` through `00000565` and have per-page OCR.

The inspected OCR shows Section 2, `Beweis der Bikompaktheit`, beginning on printed page 548. It
proves compactness of an arbitrary-cardinality power of a closed interval by a concentration-point
and transfinite-coordinate argument. The article uses this result inside its main universal
embedding and complete-regularity results; its headline `Satz I`, `Satz II`, and `Satz III` do not
give a clean printed statement matching the catalog's general product of arbitrary compact spaces.
This establishes a primary historical proof boundary, but not an exact clause-by-clause source row
for the received general formulation. Translation of historical `bikompakt`, source genealogy for
the generalization, incorporated definitions, assumptions, corrections, errata, and independent
review remain open. The inspected article therefore supports `H1`, not `H0`.

As a modern secondary formulation lead, the permanent Encyclopedia of Mathematics revision
`Tikhonov theorem&oldid=38785` states: "The topological product of an arbitrary set of compact
spaces is compact." The observed HTML SHA-256 is
`a105610933a63c6491ba10888de9e3c94f4ea17cd33d870bf83ad68622240cbd`. It confirms the conventional
family and cites the 1930 article, but it cannot replace the unresolved primary-source crosswalk.

## Clause crosswalk

| Catalog clause | Source question | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "arbitrarily many" | arbitrary set/type of indices, including empty | `I : Type u` | arbitrary index is intended; exact universe/binder order open |
| "spaces" | family of topological spaces or family of compact subsets | `X : I -> Type v`, `TopologicalSpace (X i)` | space-level versus set-level source root open |
| "compact" factors | compact alone or compact Hausdorff | `CompactSpace (X i)` | mathlib compactness omits separation; source convention review open |
| "product" | categorical/product topology rather than box topology | Pi topology on `forall i, X i` | pinned topology is coordinate-induced with finite-coordinate basis |
| compact conclusion | compact product space or compact product subset | `CompactSpace (forall i, X i)` or `IsCompact (Set.pi Set.univ s)` | exact target and transport open |
| empty cases | whether nonempty factors/index are assumed | no `Nonempty` is needed by pinned candidates | retain cases pending source decision |
| `已验证` | requires source and kernel receipts | none | no H or M credit |

## Pinned formal leads

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.Compactness.Compact` contains:

- `isCompact_pi_infinite`: compactness of the set of dependent functions lying coordinatewise in
  compact sets;
- `isCompact_univ_pi`: the same product-of-sets theorem expressed with `Set.pi Set.univ`;
- `Pi.compactSpace`: compactness of a dependent product of compact spaces.

The pinned source labels the first two as Tychonoff's theorem. `Mathlib.Topology.Constructions`
defines the Pi topology as the infimum of coordinate-induced topologies, and
`Mathlib.Topology.Bases.isTopologicalBasis_pi` exhibits its finite-coordinate basis. Mathlib's
`CompactSpace` documentation explicitly says separation is not included.

The intake probe elaborates the three candidates and reports exactly `propext`,
`Classical.choice`, and `Quot.sound` for each. It also elaborates representative empty-index and
empty-factor compact-space instances. This supports provisional `M3`: direct pinned statement/proof
interfaces exist. It does not establish normalized identity with a source-selected root, terminal
proof-body provenance, full dependency and TCB closure, a checked local wrapper, or accepted M0.

## First source/statement gate

An independent source reviewer must preserve and approve one exact theorem, all incorporated
definitions and assumptions, the compactness/separation and product-topology conventions, proof
boundary, corrections, and errata. The statement phase must then freeze that same claim, resolve
the set/space and boundary encodings, elaborate it with minimal imports, compile transports, and
mutation-test removed hypotheses, changed topology/domain, binder scope, and empty cases.
