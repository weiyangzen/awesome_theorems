# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` records J. H. C. Whitehead, 1949, and the phrase "weak homotopy
equivalence and homotopy equivalence." `Docs/Stage0_Blueprint.md` repeats that phrase. These records
establish the intended theorem family but do not specify connectedness, basepoints, CW hypotheses,
or a source theorem/page. Their `已验证` label is untrusted metadata under rev-5.6 and supplies no
human-source or machine-proof credit.

## Candidate mathematical sources

- J. H. C. Whitehead, "Combinatorial homotopy. I," *Bulletin of the American Mathematical
  Society* 55 (1949), 213-245. This is the historical primary-source candidate associated with
  the theorem. The exact theorem number, page, hypotheses, terminology, and errata have not yet
  been inspected and therefore are not `H0` evidence.
- Allen Hatcher, *Algebraic Topology*, Cambridge University Press (2002), the homotopy-theory
  chapter's statement of Whitehead's theorem. This is a modern exposition candidate for checking
  the connected based formulation and proof architecture, not a replacement for primary-source
  verification. Exact page/version wording remains to be recorded.

## Crosswalk

| Repository/source phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| weak homotopy equivalence | bijection on path components plus all positive based homotopy-group isomorphisms | component map; induced maps on `HomotopyGroup.Pi` | included; exact API open |
| CW complexes | CW structures on both domain and codomain | pinned `CWComplex` interface, with whole-space encoding checked | included; transport open |
| homotopy equivalence | the given `f` admits a homotopy inverse | `ContinuousMap.HomotopyEquiv` plus equality of its forward map with `f` | included; expression open |
| every homotopy group | every basepoint and every `n >= 1` | ordered binders and group isomorphisms | included |
| dimension zero | path-component bijection, not a group claim | concrete path-component quotient/map | included; API open |
| arbitrary components | apply the connected theorem componentwise if the source is connected | checked restriction, component correspondence, and assembly bridge | required if source scope differs |

## Lean discovery boundary

The pinned mathlib tree contains `Mathlib.Topology.CWComplex.Classical.Basic`,
`Mathlib.Topology.Homotopy.HomotopyGroup`, and `Mathlib.Topology.Homotopy.Equiv`. The intake smoke
module checks the public names `Topology.CWComplex`, `HomotopyGroup.Pi`, and
`ContinuousMap.HomotopyEquiv`. This establishes only that relevant substrate elaborates. No exact
Whitehead declaration, induced-map interface, terminal proof body, or source-to-Lean equivalence
has been audited.

Before `H0`, an independent reviewer must verify a stable primary edition, exact theorem/page,
definitions, assumptions, component and basepoint conventions, proof transitions, and errata, then
approve the row-by-row map to the eventual Lean target.
