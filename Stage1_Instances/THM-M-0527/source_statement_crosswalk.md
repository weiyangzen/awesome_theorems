# THM-M-0527 source-statement crosswalk

| Canonical component | Human source candidate | Pinned Lean discovery surface | Intake assessment |
|---|---|---|---|
| Base hypotheses | Allen Hatcher, *Algebraic Topology* (2002), Section 1.3, Proposition 1.36 and its standing hypotheses | `Mathlib.Topology.Homotopy.Lifting`; connectivity APIs imported transitively | Synopsis aligns, but printed page, immutable source digest, premise-level quotation, and errata review remain open |
| Pointed classification | Hatcher, Section 1.3, Proposition 1.36: basepoint-preserving isomorphism classes of path-connected covers versus subgroups | No exact classification declaration located during intake; later anchor audit is authoritative | This is the canonical source formulation; no H0 or M0 credit |
| Forward assignment | Hatcher Proposition 1.36 assigns a cover to the image of the induced map on fundamental groups | `FundamentalGroup`, `FundamentalGroupoid.map`, and covering-map lifting declarations are candidate ingredients | Exact induced-map expression and invariance proof are not frozen |
| Existence for each subgroup | Hatcher's construction preceding and used by Proposition 1.36 | `IsCoveringMap`, path/homotopy lifting, and `IsCoveringMap.monodromyFunctor` | Low-level APIs exist; the construction/classification theorem has not been integrated |
| Unpointed conjugacy form | Hatcher, discussion immediately following Proposition 1.36 | Quotients/conjugacy APIs not audited | Alternate encoding only, pending a checked pointed-to-unpointed transport |
| Monodromy/action formulation | Standard categorical refinement of covering theory | `IsCoveringMap.monodromyFunctor` in `Mathlib.Topology.Homotopy.Lifting` | Useful discovery anchor, but broader than the frozen root |

The repository discovery records, `Docs/Stage0_Blueprint.md` and
`Docs/researches/math_theorems.md`, provide only the Chinese name and the synopsis "covering spaces
and the fundamental group correspond," plus an untrusted verified label. They omit basedness,
connectivity, local hypotheses, and the isomorphism/conjugacy quotient. They therefore cannot
support `H0` or determine a Lean expression by themselves.

Hatcher is a precise primary textbook candidate for the modern theorem statement, not an accepted
source receipt. The source-audit phase must pin a stable edition or file digest, record exact pages
and standing assumptions, inspect corrections/errata, crosswalk the construction and both inverse
laws, and obtain independent review. Human status remains `H1`.

The Lean names above were inspected at pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The intake smoke test establishes only that the basic
covering and monodromy interfaces elaborate. It neither asserts that mathlib contains the full
classification nor assigns machine-proof credit.
