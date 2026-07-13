# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6033-6038` contains the full catalog record: `Sperner定理`,
Emanuel Sperner, 1928, `幂集反链的最大大小`, high importance, and `已验证`. It has no
bibliography, definitions, quantifiers, hypotheses, conclusion formula, proof boundary, errata, or
formal declaration. Stage0 repeats the gloss while explicitly leaving exact definitions,
assumptions, equivalences, axioms, proof path, and machine artifacts unresolved. The manifest
preserves `已验证` only as `source_status_untrusted`.

## Primary source inspected

Emanuel Sperner, "Ein Satz uber Untermengen einer endlichen Menge," *Mathematische Zeitschrift*
27 (1928), 544-548, DOI `10.1007/BF01171114`. The inspected Goettingen Digitization Centre copy is
the five printed article pages plus a repository cover/terms page; PDF SHA-256
`236629931717954288c77d99e487a1ff98c40af2fb29908eb06738ee253bbbde`.
Its stable article PURL is `http://resolver.sub.uni-goettingen.de/purl?GDZPPN002369915`. The archive
terms restrict redistribution, so the PDF is not copied into this repository; only its locator,
inspection boundary, byte count, and digest are recorded.

Printed page 544:

- fixes a finite ground set `M` of `n` elements;
- defines one subset as contained in another when all its elements occur in the other;
- defines a distinguished system `Sigma` by requiring that no member is a subset of another;
- calls the number of members the degree of `Sigma`;
- states `degree(Sigma) <= choose(n, floor(n / 2))`;
- states equality occurs only at the rank-`n/2` layer for even `n`, and at exactly the
  rank-`(n-1)/2` or rank-`(n+1)/2` layer for odd `n`;
- observes that these named layers are antichains of the asserted cardinality.

Printed pages 545-548 prove the result by replacing outlying ranks with their lower or upper
neighbors until the family lies in a middle rank, while increasing cardinality outside the listed
equality cases. The intake inspection is sufficient to identify the theorem family and expose the
catalog ambiguity. It is not H0: a qualified independent reviewer, an accountable translation,
full premise-to-node/proof mapping, and a corrections/errata audit remain open.

Crossref independently confirms author, title, DOI, year, volume, issue, and pages, but its returned
title contains a replacement character for `u`-umlaut. The scan, not that damaged payload, is the
title transcription authority.

## Pinned Lean candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Combinatorics.SetFamily.LYM` documents and defines:

```text
IsAntichain.sperner
  (hA : IsAntichain (fun x y => x \u2286 y) (SetLike.coe A)) :
  A.card \u2264 Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)
```

The module documentation calls this Sperner's theorem and derives it from the LYM inequality. The
same documentation says equality cases are TODO. Thus the declaration is a credible pinned exact
candidate for the upper-bound component, but it does not by itself match a root requiring
attainability or equality classification. Intake records M3 interface/discovery credit only; the
later statement and anchor-audit phases must establish exact source transport, terminal proof-body
provenance, trust closure, and the appropriate M state.

## Crosswalk

| Catalog/source component | Candidate Lean component | Intake status |
|---|---|---|
| finite `n`-element ground set | `[Fintype alpha]`, `Fintype.card alpha` | candidate encoding; not frozen |
| family of subsets | `A : Finset (Finset alpha)` | candidate encoding; source transport open |
| no member included in another | `IsAntichain (fun x y => x \u2286 y) (A : Set (Finset alpha))` | direct candidate |
| number of family members | `A.card` | direct candidate |
| middle binomial coefficient | `Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)` | direct lower-middle convention |
| universal upper bound | `IsAntichain.sperner` | pinned declaration elaborates; identity/audit open |
| middle layer realizes the bound | `Finset.powersetCard`, `Finset.card_powersetCard`, sized-layer APIs | ingredients only; no root witness credited |
| even/odd equality classification | no declaration located in the candidate file; documented TODO | missing from candidate |
| catalog `已验证` | no source or proof evidence | rejected as evidence |

## Open source gate

Before H0 or statement freeze, an independent reviewer must verify the page-544 transcription and
translation, inclusion convention, binomial/floor notation, all boundary cases, equality wording,
proof boundary on pages 545-548, and known corrections or errata. The reviewer must then decide
which of the upper-bound, maximum-value, attainability, and equality-classification claims is the
source-faithful root rather than allowing the available Lean theorem to choose the mathematics.
