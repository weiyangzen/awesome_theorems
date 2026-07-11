# Source-statement crosswalk

| Claim component | Primary human source candidate | Lean candidate | Intake assessment |
|---|---|---|---|
| Concentration-compactness trichotomy | P.-L. Lions, *The concentration-compactness principle in the calculus of variations. The locally compact case, part 1*, Ann. Inst. H. Poincare Anal. Non Lineaire 1 (1984), no. 2, 109-145, especially the concentration-compactness lemma in Section I.1 | `TrichotomyShape P` | Primary paper and section located; exact theorem number/text, hypotheses, and errata are not yet pinned: `H2` |
| Continuation and applications of the locally compact case | P.-L. Lions, *... The locally compact case, part 2*, Ann. Inst. H. Poincare Anal. Non Lineaire 1 (1984), no. 4, 223-283 | future application/refinement nodes | Relevant primary continuation, not evidence that the generic Lean predicate matches any particular application |
| Compactness after excluding loss mechanisms | The two 1984 papers' use of the trichotomy in variational existence arguments | `CompactnessShape P` | Candidate architectural consequence; the current Lean target assumes `tightUpToSymmetry` and an abstract conclusion, so equivalence to a source result is unproved |
| Vanishing | Part 1 concentration function and vanishing alternative | `LocalCriticalMassVanishing` | Resembles uniform decay of modeled local mass, but balls, radii, normalization, and limiting quantifiers need exact crosswalk |
| Dichotomy | Part 1 splitting alternative | `DichotomyByEnergySplitting` | Legacy witness has an abstract `separation : Prop`; it is not yet a faithful source encoding |
| Compactness/concentration | Part 1 concentration alternative, modulo translations in the relevant setting | `P.tightUpToSymmetry u` and `P.compactnessConclusion u` | Both are unconstrained predicate fields at intake; no analytic content or proof credit |
| Public Lean alias | No separate human claim | `PublicStatementNormalization P` | Candidate definitional alias only; checked transport is deferred to the statement phase |

Bibliographic discovery identifiers are ISSN 0294-1449 and EuDML records for pages 109-145 and
223-283. They are not immutable evidence receipts. The later source audit must archive or hash the
exact editions, quote and pinpoint the selected lemma, map every assumption and quantifier, search
corrections/errata, and obtain independent review before `H0` is possible.

The catalog phrase "Lions concentration-compactness principle" does not itself decide between the
locally compact, limit, Sobolev, or application-specific formulations. Accordingly, this intake
freezes the intended branch but deliberately leaves exact source identity open rather than
inventing missing mathematics. The statement phase must reject or refine the generic model if its
degenerate instantiations, abstract separation, or assumed compactness conclusion broaden the
selected theorem.
