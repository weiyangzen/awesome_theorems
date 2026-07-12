# Source-statement crosswalk

## Repository source record

`Docs/Stage0_Blueprint.md` names `G-指标定理`, glosses it as `等变椭圆算子的指标`
("the index of equivariant elliptic operators"), gives 1968, and attributes it to Michael Atiyah
and Isadore Singer. That metadata establishes the topic only. It supplies no theorem number,
quantifiers, hypotheses, formula, source edition, or formal artifact, and its `已验证` label is
explicitly untrusted under rev-5.6.

## Candidate primary sources

- M. F. Atiyah and G. B. Segal, "The Index of Elliptic Operators: II", *Annals of Mathematics*
  **87**(3) (May 1968), beginning at page 531, DOI `10.2307/1970716`.
- M. F. Atiyah and I. M. Singer, "The Index of Elliptic Operators: III", *Annals of Mathematics*
  **87**(3) (May 1968), beginning at page 546, DOI `10.2307/1970717`.

The bibliographic metadata above was checked against Crossref on 2026-07-12. It is discovery
evidence, not a direct inspection of the papers and not `H0`. The statement phase must inspect
stable copies, identify the exact theorem and incorporated definitions, record complete page
ranges and errata, and determine whether Part II, Part III, or another primary paper is the actual
source of the repository's intended claim. The current two-person attribution must not erase
Segal's role if the selected theorem is from Part II.

## Crosswalk

| Repository component | Candidate mathematical meaning | Required Lean component | Intake assessment |
|---|---|---|---|
| `G` | compact group, likely a compact Lie group in a smooth setting | concrete group topology/Lie structure and smooth action | group category unresolved |
| equivariant elliptic operator | operator commuting with the induced `G`-actions on section spaces | bundles, sections, operator, equivariance, symbol, ellipticity | concrete APIs unselected |
| analytic `G`-index | virtual kernel-minus-cokernel representation | finite-dimensional `G`-modules and representation/Grothendieck ring | intended component, foundations open |
| topological `G`-index | equivariant K-theory symbol pushforward | equivariant K-theory, Thom class, and pushforward | likely equality target, source confirmation required |
| character at `g` | trace on kernel minus trace on cokernel | character evaluation for virtual representations | alternate form, not yet selected |
| fixed-point contribution | formula supported on `M^g` with normal-bundle data | fixed locus, normal bundle, characteristic classes, denominator/localization | possible stronger branch, not silently in root |
| `已验证` | untrusted generated status | accepted receipts and kernel closure | rejected as evidence |

## Existing Lean boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains generic group-action,
manifold, vector-bundle, and fixed-point substrates. A scoped text search for equivariant-index
terminal names found no candidate. The nearby legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_108.lean` concerns the distinct Atiyah-Bott target
`THM-M-0576`; its terminal operator, index-character, and local-contribution notions are abstract
fields, so it supplies neither a canonical statement nor proof credit here.

Before `H0`, an independent reviewer must approve a row-by-row premise and conclusion mapping from
the selected primary theorem to Lean. Before any machine credit, the exact Lean target, imports,
environment fingerprint, transports, mutations, and terminal proof provenance must pass their own
gates.
